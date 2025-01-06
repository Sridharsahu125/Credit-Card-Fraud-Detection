Credit Card Fraud Detection
----------------------------

This project involves detecting fraudulent credit card transactions using machine learning techniques. We analyze a dataset of credit card transactions, apply outlier detection methods, and compare multiple algorithms to identify fraudulent transactions.

Dataset
Source: The dataset contains transactions made by European cardholders in September 2013.
Data: 284,807 transactions, including 492 frauds (0.172% of total transactions).

Features:
V1, V2, ..., V28: Principal components obtained using PCA.
Amount: The transaction amount.

Time: Time elapsed in seconds since the first transaction.
Class: Response variable (1 for fraud, 0 for normal).


Objective
The goal is to build a machine learning model to detect fraud and improve the accuracy of fraud detection using different outlier detection algorithms.

Outlier Detection Algorithms Used
Isolation Forest: A tree-based ensemble method for anomaly detection.
Local Outlier Factor (LOF): A density-based method for detecting anomalies in data.
Support Vector Machine (SVM): A supervised method used for classification tasks.

Approach

Data Preprocessing:

Load and clean the dataset.
Analyze the distribution of fraudulent vs. normal transactions.
Visualize the dataset to understand patterns in the data.
Feature Engineering:

Split the data into independent (X) and dependent (Y) variables.
Create outlier detection models.
Model Evaluation:

Compare the performance of Isolation Forest, LOF, and SVM.
Analyze precision, recall, and accuracy of each model.
Conclusion:

Isolation Forest performs best with 27% fraud detection and 99.74% accuracy.


LOF detects 2% of frauds and has an accuracy of 99.65%.

SVM detected no frauds and had lower accuracy.


Results

Best Model: Isolation Forest (30% fraud detection rate).

Performance Metrics:
Isolation Forest: 99.74% accuracy.

LOF: 99.65% accuracy.

SVM: 70.09% accuracy.


How to Run the Project

Clone the repository:

Copy code
[git clone https://github.com/Sridharsahu125/Credit-Card-Fraud-Detection.git](https://github.com/Sridharsahu125/Credit-Card-Fraud-Detection/blob/main/credit_card_fraud_detection.ipynb)

csv file :
copy code:https://drive.google.com/file/d/1DuaIXxBnARusx6CShthOyD23gLY7-kIG/view?usp=drive_link

Install dependencies:

Copy code

pip install -r requirements.txt

Run the Jupyter notebook:

Copy code

jupyter notebook Fraud_Detection.ipynb

Dependencies

pandas

numpy

matplotlib

seaborn

sklearn

xgboost

scipy

.
