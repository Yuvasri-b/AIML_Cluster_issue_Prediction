# -*- coding: utf-8 -*-
"""Resource exhaustion.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZSUuwVifWqkqMeFKAA4acFquQUQkBWFY

# **RESOURCE EXHAUSTION PREDICTION using Isolation Forest and Autoencoder**
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import IsolationForest
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

"""STEP 1 : Load dataset"""

# Load dataset
df = pd.read_csv("sys_failure.csv")

# Remove '%' and convert to numeric
df["CPU_Usage"] = df["CPU_Usage"].str.replace("%", "").astype(float)
df["Memory_Usage"] = df["Memory_Usage"].str.replace("%", "").astype(float)
df["Disk_Usage"] = df["Disk_Usage"].str.replace("%", "").astype(float)

# Display cleaned data
print(df.head())

encoder = LabelEncoder()

# Encode categorical features
df["Network_Usage"] = encoder.fit_transform(df["Network_Usage"])
df["Pod_Status"] = encoder.fit_transform(df["Pod_Status"])
df["K8s_Event_Log"] = encoder.fit_transform(df["K8s_Event_Log"])
df["System_Log"] = encoder.fit_transform(df["System_Log"])
df["Network_Error"] = encoder.fit_transform(df["Network_Error"])

print(df.head())

"""STEP : 2 Model Prediction

**Isolation Forest Model**
"""

from sklearn.ensemble import IsolationForest

# Increase contamination
iso_forest = IsolationForest(n_estimators=400, contamination=0.4, max_samples=0.9, random_state=42)
df["Anomaly_IF_Tuned"] = iso_forest.fit_predict(df[["CPU_Usage", "Memory_Usage", "Disk_Usage"]])

# Check new anomaly count
print("Tuned Isolation Forest Anomalies:\n", df["Anomaly_IF_Tuned"].value_counts())

# Define failures based on high CPU, Memory, or Disk usage
df["Known_Failures"] = 0  # Default to normal

df.loc[(df["CPU_Usage"] > 90) | (df["Memory_Usage"] > 90) | (df["Disk_Usage"] > 90), "Known_Failures"] = 1

# Define actual failure labels
y_true = df["Known_Failures"]

from sklearn.metrics import precision_score

# Convert Isolation Forest predictions (-1 = Anomaly) to (1 = Failure)
y_pred_if = (df["Anomaly_IF_Tuned"] == -1).astype(int)  # Convert -1 anomalies to 1 (failure)

# Calculate Precision
precision_if = precision_score(y_true, y_pred_if)


print(f"Isolation Forest - Precision: {precision_if:.2f}")

"""**Autoencoder**"""

# Select features for anomaly detection
X = df[["CPU_Usage", "Memory_Usage", "Disk_Usage"]]
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

# Define a deeper autoencoder
input_dim = X.shape[1]
encoding_dim = 4  # Increase encoded representation

input_layer = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation="relu")(input_layer)
encoded = Dense(encoding_dim//2, activation="relu")(encoded)  # Added extra compression
decoded = Dense(encoding_dim, activation="relu")(encoded)
decoded = Dense(input_dim, activation="linear")(decoded)

autoencoder = Model(input_layer, decoded)
autoencoder.compile(optimizer="adam", loss="mse")

# Increase epochs & batch size for better training
autoencoder.fit(X, X, epochs=100, batch_size=64, shuffle=True, validation_split=0.2)

# Predict reconstruction errors
reconstructions = autoencoder.predict(X)
losses = ((X - reconstructions) ** 2).mean(axis=1)

# Tune threshold dynamically
threshold = losses.mean() + 2.5 * losses.std()  # Adjusted sensitivity
df["Anomaly_AE_Tuned"] = (losses > threshold).astype(int)

print("Tuned Autoencoder Anomalies:", df["Anomaly_AE_Tuned"].value_counts())

# Convert Autoencoder predictions (1 = Anomaly, 0 = Normal)
y_pred_ae = df["Anomaly_AE_Tuned"]

# Calculate Precision
precision_ae = precision_score(y_true, y_pred_ae)


print(f" Autoencoder - Precision: {precision_ae:.2f}")

print("Isolation Forest Anomalies:", df["Anomaly_IF_Tuned"].value_counts())
print("Autoencoder Anomalies:", df["Anomaly_AE_Tuned"].value_counts())

"""STEP 3 : Plot Analysis"""

import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style
sns.set_style("whitegrid")

# Plot distributions
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

sns.histplot(df["CPU_Usage"], bins=20, kde=True, ax=axes[0], color="blue")
axes[0].set_title("CPU Usage Distribution")

sns.histplot(df["Memory_Usage"], bins=20, kde=True, ax=axes[1], color="green")
axes[1].set_title("Memory Usage Distribution")

sns.histplot(df["Disk_Usage"], bins=20, kde=True, ax=axes[2], color="red")
axes[2].set_title("Disk Usage Distribution")

plt.show()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot Isolation Forest Anomalies
sns.scatterplot(x=df.index, y=df["CPU_Usage"], hue=(df["Anomaly_IF_Tuned"] == -1), palette={True: "red", False: "blue"}, ax=axes[0])
axes[0].set_title("Isolation Forest Anomalies (CPU Usage)")

# Plot Autoencoder Anomalies
sns.scatterplot(x=df.index, y=df["CPU_Usage"], hue=(df["Anomaly_AE_Tuned"] == 1), palette={True: "red", False: "blue"}, ax=axes[1])
axes[1].set_title("Autoencoder Anomalies (CPU Usage)")

plt.show()