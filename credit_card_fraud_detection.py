# -*- coding: utf-8 -*-
"""credit-card-fraud-detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MwsZ2VNNWSgRjd2luvsBvcE3tJXXl4WI
"""

from warnings import filterwarnings
filterwarnings('ignore')

import numpy as np
import pandas as pd
import sklearn
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report,accuracy_score
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from pylab import rcParams
rcParams['figure.figsize'] = 14, 8
RANDOM_SEED = 42
LABELS = ["Normal", "Fraud"]

"""# Dataset

[**Kaggle Dataset**](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) | [**Reference**](https://github.com/krishnaik06/Credit-Card-Fraudlent)

It is important that credit card companies are able to recognize fraudulent credit card transactions so that customers are not charged for items that they did not purchase.

The dataset contains transactions made by credit cards in September 2013 by European cardholders.

This dataset presents transactions that occurred in two days, where we have 492 frauds out of 284,807 transactions. The dataset is highly unbalanced, the positive class (frauds) accounts for 0.172% of all transactions.

It contains only numerical input variables which are the result of a PCA transformation. Unfortunately, due to confidentiality issues, we cannot provide the original features and more background information about the data. Features V1, V2, … V28 are the principal components obtained with PCA, the only features which have not been transformed with PCA are 'Time' and 'Amount'. Feature 'Time' contains the seconds elapsed between each transaction and the first transaction in the dataset. The feature 'Amount' is the transaction Amount, this feature can be used for example-dependent cost-sensitive learning. Feature 'Class' is the response variable and it takes value 1 in case of fraud and 0 otherwise.

"""

data = pd.read_csv('/content/creditcard.csv',sep=',')

data.head()

data.info()

"""# Exploratory Data Analysis

Analyzing the dataset to gain insights into the distribution of fraudulent and non-fraudulent transactions, identifying any class imbalance issues, and understanding the features' characteristics. Cleaning the dataset, handling missing values, scaling numerical features, and encoding categorical variables as necessary. Selecting relevant features and creating new informative features that can potentially improve the model's performance in detecting fraudulent transactions.
"""

data.isnull().values.any()

count_classes = pd.value_counts(data['Class'], sort = True)

count_classes.plot(kind = 'bar', rot=0)

plt.title("Transaction Class Distribution")

plt.xticks(range(2), LABELS)

plt.xlabel("Class")

plt.ylabel("Frequency")

## Get the Fraud and the normal dataset

fraud = data[data['Class']==1]

normal = data[data['Class']==0]

print(fraud.shape,normal.shape)

fraud.Amount.describe()

normal.Amount.describe()

f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
f.suptitle('Amount per transaction by class')
bins = 50
ax1.hist(fraud.Amount, bins = bins)
ax1.set_title('Fraud')
ax2.hist(normal.Amount, bins = bins)
ax2.set_title('Normal')
plt.xlabel('Amount ($)')
plt.ylabel('Number of Transactions')
plt.xlim((0, 20000))
plt.yscale('log')
plt.show();

# We Will check Do fraudulent transactions occur more often during certain time frame ? Let us find out with a visual representation.

f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
f.suptitle('Time of transaction vs Amount by class')
ax1.scatter(fraud.Time, fraud.Amount)
ax1.set_title('Fraud')
ax2.scatter(normal.Time, normal.Amount)
ax2.set_title('Normal')
plt.xlabel('Time (in Seconds)')
plt.ylabel('Amount')
plt.show()

## Take some sample of the data

data1= data.sample(frac = 0.1,random_state=1)

data1.shape

data.shape

#Determine the number of fraud and valid transactions in the dataset

Fraud = data1[data1['Class']==1]

Valid = data1[data1['Class']==0]

outlier_fraction = len(Fraud)/float(len(Valid))

print(outlier_fraction)

print("Fraud Cases : {}".format(len(Fraud)))

print("Valid Cases : {}".format(len(Valid)))

"""### Correlation"""

## Correlation
import seaborn as sns
#get correlations of each features in dataset
corrmat = data1.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(26,26))
#plot heat map
g=sns.heatmap(data[top_corr_features].corr(),annot=True,cmap="RdYlGn")

#Create independent and Dependent Features
columns = data1.columns.tolist()
# Filter the columns to remove data we do not want
columns = [c for c in columns if c not in ["Class"]]
# Store the variable we are predicting
target = "Class"
# Define a random state
state = np.random.RandomState(42)
X = data1[columns]
Y = data1[target]
X_outliers = state.uniform(low=0, high=1, size=(X.shape[0], X.shape[1]))
# Print the shapes of X & Y
print(X.shape)
print(Y.shape)

"""## Model & Analysis

# Isolation Forest

Isolation Forest is an unsupervised machine-learning algorithm used for outlier detection. It leverages the concept of isolating anomalies to detect outliers in a dataset. It builds an ensemble of isolation trees, which are binary trees that randomly partition the data points. Anomalies are expected to have shorter average path lengths in the trees, making them easier to isolate. By assigning anomaly scores based on the average path lengths, the algorithm identifies outliers as data points with low scores. Isolation Forest is particularly effective in high-dimensional datasets and does not rely on assumptions about the data distribution.

<img src="https://miro.medium.com/v2/resize:fit:1174/1*-TANPVnrnxPo-p2cnZpPHQ.png" height=80% width=80% style="text-align:center;">

# Local Outlier Factor

LOF (Local Outlier Factor) is an unsupervised anomaly detection algorithm that assesses the local density deviation of a data point compared to its neighbors. It quantifies the degree of abnormality of a data point based on its relative density.

<img src="https://www.googleapis.com/download/storage/v1/b/kaggle-forum-message-attachments/o/inbox%2F1341832%2F27b93ecfd56afa80040f9b1ebecccbed%2F1_217TN2_-cgZ1d7hZUWhYUA.png?generation=1600286513104059&alt=media" height=45% width=45% style="text-align:center;">

The LOF algorithm works by calculating a local reachability density for each data point, which represents how isolated or tightly grouped the point is compared to its neighbors. Anomaly scores are assigned based on the degree to which a point's density deviates from the density of its neighbors. Points with significantly lower density compared to their neighbors are considered outliers with higher LOF scores.

LOF is effective in identifying anomalies in datasets with varying densities or clusters of different sizes. It can handle data with complex structures and does not rely on strict assumptions about the data distribution. LOF provides a local perspective on anomalies, allowing for more fine-grained anomaly detection in the dataset.

# One Class Support Vector Machine

<img src="https://www.researchgate.net/publication/345644388/figure/fig1/AS:1024147857620994@1621187285679/Overview-of-one-class-Support-Vector-Machine-SVM.png" height=60% width=60% style="text-align:center;">

SVM (Support Vector Machine) is a supervised machine learning algorithm used for classification and regression tasks. It finds an optimal hyperplane that separates data points into different classes or predicts continuous values. SVM aims to maximize the margin between classes, making it robust to outliers. It can handle linearly separable data and can also utilize kernels to handle non-linearly separable data by mapping it to a higher-dimensional feature space. SVM is effective in high-dimensional spaces, but it can be computationally expensive for large datasets due to its quadratic time complexity.

"""

##Define the outlier detection methods

classifiers = {
    "Isolation Forest":IsolationForest(n_estimators=100, max_samples=len(X),
                                       contamination=outlier_fraction,random_state=state, verbose=0),
    "Local Outlier Factor":LocalOutlierFactor(n_neighbors=20, algorithm='auto',
                                              leaf_size=30, metric='minkowski',
                                              p=2, metric_params=None, contamination=outlier_fraction),
    "Support Vector Machine":OneClassSVM(kernel='rbf', degree=3, gamma=0.1,nu=0.05,
                                         max_iter=-1)
}

type(classifiers)

"""# Accuracy

# Conclusion

-	Isolation Forest detected 73 errors versus Local Outlier Factor detecting 97 errors vs. SVM detecting 8516 errors.

-	Isolation Forest has a 99.74% more accurate than LOF of 99.65% and SVM of 70.09%.

-	When comparing error precision & recall for 3 models, the Isolation Forest performed much better than the LOF as we can see that the detection of fraud cases is around 27 % versus the LOF detection rate of just 2 % and SVM of 0%.

-	So overall Isolation Forest Method performed much better in determining the fraud cases which is around 30%.

-	We can also improve on this accuracy by increasing the sample size or using deep learning algorithms however at the cost of computational expense. We can also use complex anomaly detection models to get better accuracy in determining more fraudulent cases.
"""