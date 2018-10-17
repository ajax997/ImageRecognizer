import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets.samples_generator import make_blobs

##############################################################################
# Generate sample data
np.random.seed(0)

batch_size = 45
centers = [[100, 1], [0, 100], [50, 10], [210, 100], [15, 15]]
n_clusters = len(centers)
import numpy as np
import cv2

img = cv2.imread('images/polistic.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.resize(img, (200, 200))
plt.imshow(img, cmap='gray')
plt.show()
W, H = img.shape[:2]
print(img.shape)
X = []
for i in range(0, W):
    for j in range(0, H):
        if img[i, j] < 130:
            X.append([j, i])

X = np.array(X)

from sklearn.cluster import AgglomerativeClustering

cluster = AgglomerativeClustering(n_clusters=8, affinity='euclidean', linkage='ward')
cluster.fit_predict(X)

plt.scatter(X[:, 0], X[:, 1], c=cluster.labels_, cmap='rainbow')
plt.show()

# X, labels_true = make_blobs(n_samples=3000, centers=centers, cluster_std=0.7)


##############################################################################
# Compute clustering with Means

# k_means = KMeans(init='k-means++', n_clusters=5, n_init=10)
# k_means.fit(X)
# k_means_labels = k_means.labels_
# k_means_cluster_centers = k_means.cluster_centers_
# k_means_labels_unique = np.unique(k_means_labels)
#
# ##############################################################################
# # Plot result
#
# colors = ['#4EACC5', '#FF9C34', '#4E9A06','#434321', '443842']
# plt.figure()
# plt.hold(True)
# for k, col in zip(range(n_clusters), colors):
#     my_members = k_means_labels == k
#     cluster_center = k_means_cluster_centers[k]
#     plt.plot(X[my_members, 0], X[my_members, 1], 'w',
#              markerfacecolor=col, marker='.')
#     plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
#              markeredgecolor='k', markersize=6)
# plt.title('KMeans')
# plt.grid(True)
# plt.show()
