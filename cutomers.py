import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import zipfile
 #data Reading
with zipfile.ZipFile('archive.zip', 'r') as z:
    with z.open('Mall_Customers.csv') as f:
        df = pd.read_csv(f)
print(df.head())
print(df.info())
print(df.describe())


#data preprocessing
df = df.dropna()
df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})
X = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#no.of optimal clusters required
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10,5))
plt.plot(range(1, 11), wcss, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# applying the k means 
kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300, n_init=10, random_state=0)
y_kmeans = kmeans.fit_predict(X_scaled)
#visulizing the clusters
plt.figure(figsize=(10,5))
sns.scatterplot(x=X_scaled[:, 1], y=X_scaled[:, 2], hue=y_kmeans, palette='viridis')
plt.scatter(kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 2], s=300, c='red', label='Centroids')
plt.title('Customer Segments')
plt.xlabel('Annual Income (k$) (scaled)')
plt.ylabel('Spending Score (scaled)')
plt.legend()
plt.show()
