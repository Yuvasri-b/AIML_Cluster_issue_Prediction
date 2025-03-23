# AIML_Cluster_issue_Prediction

Team Name : RaKri

Problem Statement : 
Kubernetes clusters can encounter failures such as pod crashes, resource bottlenecks, and network issues. The
challenge in Phase 1 is to build an AI/ML model capable of predicting these issues before they occur by analysing
historical and real-time cluster metrics.

For a detailed **write up** explaining the approach, key metrics used, and model performance.
You can find here : https://drive.google.com/file/d/1vGMfGLKxrDbeqzUzqCbasxPyk5KqJApx/view?usp=drive_link

What I have done :
1️⃣ **Collected real-time Kubernetes metrics** (CPU, memory, disk usage, network traffic, and logs) using Minikube and system monitoring tools.  

2️⃣ **Developed multiple AI/ML models** to predict failures, including **Random Forest & XGBoost (Pod/Node Failures), Isolation Forest & Autoencoder (Resource Exhaustion), ARIMA (Network Failures), and K-Means & Isolation Forest (Service Disruptions).**

3️⃣ **Preprocessed and balanced the dataset** using encoding techniques and SMOTE to handle class imbalance, ensuring better model accuracy.  

4️⃣ **Evaluated model performance** using **accuracy scores, precision-recall analysis, ROC curves, and clustering techniques**, optimizing failure detection.  

5️⃣ **Proposed future enhancements** like **real-time deployment, deep learning integration, self-healing automation, and CI/CD pipelines** for continuous model improvement. 
