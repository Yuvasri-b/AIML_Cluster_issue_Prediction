# AIML_Cluster_issue_Prediction

Team Name : RaKri

Problem Statement : 

Kubernetes clusters can encounter failures such as pod crashes, resource bottlenecks, and network issues. The
challenge in Phase 1 is to build an AI/ML model capable of predicting these issues before they occur by analysing
historical and real-time cluster metrics.

For a detailed **write up** explaining the approach, key metrics used, and model performance.
You can find here : https://drive.google.com/file/d/1vGMfGLKxrDbeqzUzqCbasxPyk5KqJApx/view?usp=drive_link

YouTube link for presentation : https://youtu.be/hzV_hq1OQJ0?feature=shared

Presentation File : https://docs.google.com/presentation/d/1DE9QcHgSQAwzh1UhFGjd9HX9R30Fu_uD/edit?usp=drivesdk&ouid=116248132805767967524&rtpof=true&sd=true

What I have done :

1️⃣ Collected real-time Kubernetes metrics (CPU, memory, disk, network usage, and logs) using Minikube and system monitoring tools.

2️⃣ Preprocessed and cleaned the dataset, converting categorical values, handling missing data, and applying SMOTE for class balancing.

3️⃣ Implemented multiple machine learning models:

->Pod/Node Failures → Random Forest & XGBoost

->Resource Exhaustion → Isolation Forest & Autoencoder

->Network Failures → ARIMA Time-Series Forecasting

->Service Disruptions → Isolation Forest & K-Means Clustering

4️⃣ Trained and evaluated the models, achieving high accuracy in failure prediction and anomaly detection.

5️⃣ Visualized predictions using confusion matrices, ROC curves, clustering analysis, and time-series plots.

6️⃣ Identified key challenges like data imbalance, real-time integration, false positives, and model retraining requirements.
