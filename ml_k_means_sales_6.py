# -*- coding: utf-8 -*-
"""ML K-Means Sales 6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MnVLRmAmSg8iZ632_JjpXbudlVxFIXiL

# LP3 Group B Assignment 6
## Implement K-Means clustering/ hierarchical clustering on sales_data_sample.csv dataset. Determine the number of clusters using the elbow method.
Dataset link : https://www.kaggle.com/datasets/kyanyoga/sample-sales-data
"""

#Importing the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.read_csv('sales_data_sample.csv', encoding = 'unicode_escape') #Reading the csv file.
df.head()

#Removing the coloumns which dont add value for the analysis.
to_drop = ['PHONE','ADDRESSLINE1','ADDRESSLINE2','CITY','STATE','POSTALCODE','TERRITORY','CONTACTLASTNAME','CONTACTFIRSTNAME','CUSTOMERNAME','ORDERNUMBER','QTR_ID','ORDERDATE']
df = df.drop(to_drop, axis=1)
df.head()

df.nunique() #Checking unique values.

df.isnull().sum()

#Encodning Categorical Variables for easier processing.
status_dict = {'Shipped':1, 'Cancelled':2, 'On Hold':2, 'Disputed':2, 'In Process':0, 'Resolved':0}
df['STATUS'].replace(status_dict, inplace=True)
df['PRODUCTCODE'] = pd.Categorical(df['PRODUCTCODE']).codes
df = pd.get_dummies(data=df, columns=['PRODUCTLINE', 'DEALSIZE', 'COUNTRY'])
df.dtypes

#Using Heatmaps to find links between the data
plt.figure(figsize = (20, 20))
corr_matrix = df.iloc[:, :10].corr()
sns.heatmap(corr_matrix, annot=True);

#Finding correlation between variables using pairplots
fig = px.scatter_matrix(df, dimensions=df.columns[:8], color='MONTH_ID') #Fill color by months
fig.update_layout(title_text='Sales Data', width=1100, height=1100)
fig.show()

# Scale the data
std = StandardScaler()
sdf = std.fit_transform(df)
wcss = []
for i in range(1,15):
    km = KMeans(n_clusters=i)
    km.fit(sdf)
    wcss.append(km.inertia_) # intertia is the Sum of squared distances of samples to their closest cluster center (WCSS)

plt.plot(wcss, marker='o', linestyle='--')
plt.title('The Elbow Method (Finding right number of clusters)')
plt.xlabel('Number of CLusters')
plt.ylabel('WCSS')
plt.show()

#Applying k-means with 5 clusters as the elbow seems to form at 5 clusters
km = KMeans(n_clusters=5, random_state=1)
km.fit(sdf)
cluster_labels = km.labels_
df = df.assign(Cluster=cluster_labels)
df.head()

df = df.groupby(['Cluster']).mean() #Grouping by Cluster
df.head()

#Heatmap after Kmeans clustering
plt.figure(figsize = (20, 20))
corr_matrix = df.iloc[:, :8].corr()
sns.heatmap(corr_matrix, annot=True);

