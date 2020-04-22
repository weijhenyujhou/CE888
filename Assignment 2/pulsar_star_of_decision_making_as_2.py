# -*- coding: utf-8 -*-
"""pulsar-star of Decision Making As 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Zp91LD3053aQ81GoG1UvwmT_pUgoYug_

## Import Library
"""

# Import library
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from sklearn.cluster import KMeans

"""## Load Data"""

from google.colab import files

#!pip install -q kaggle

# Load data from Kaggle to Google Colab virtual machine
os.environ['KAGGLE_USERNAME'] = "weiyuchen77" # username from the json file
os.environ['KAGGLE_KEY'] = "3d26b3cb2ae2ad68701ebe9a6baadcc4" # key from the json file
!kaggle datasets download -d pavanraj159/predicting-a-pulsar-star # api copied from kaggle

# read the datasets
p_pulsar = pd.read_csv("predicting-a-pulsar-star.zip")

p_pulsar.head(5)



"""# Data Visualization"""

plt.pie(p_pulsar["target_class"].value_counts().values,
        labels=["not pulsar stars","pulsar stars"],
        autopct="%1.0f%%",wedgeprops={"linewidth":2,"edgecolor":"white"})
my_circ = plt.Circle((0,0),.7,color = "white")
plt.gca().add_artist(my_circ)
plt.subplots_adjust(wspace = .1)
plt.title("Proportion of target variable in Pulsar dataset")
plt.show()

p_pulsar.info()

"""# Check missing value"""

# dealing with missing value

#p_pulsar
total = p_pulsar.isnull().sum().sort_values(ascending=False)
missing_data = pd.concat([total],axis=1,keys=['Total'])
missing_data.head()

"""# Normalization"""

from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler
for col in p_pulsar.select_dtypes(include='number').columns:
    mms = MinMaxScaler()
    p_pulsar[col] = mms.fit_transform(p_pulsar[[col]])
p_pulsar.describe()

"""#  Lable encoding"""

pulsar_X = p_pulsar.drop('target_class', axis = 1)
pulsar_Y = np.array(p_pulsar['target_class'])

from sklearn.preprocessing import LabelEncoder
for col in pulsar_X.select_dtypes(include='object').columns:
    le = LabelEncoder()
    pulsar_X[col] = le.fit_transform(pulsar_X[col].astype('str'))
pulsar_X=pulsar_X.values


print("Pulsar:",pulsar_X)
print(pulsar_X.shape)
print(pulsar_Y.shape)

import numpy as np
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=10)
skf.get_n_splits(pulsar_X, pulsar_Y)
print(skf)

"""# DecisionTree"""

from sklearn import tree
from sklearn.metrics import confusion_matrix, roc_auc_score ,roc_curve,auc
from sklearn.model_selection import StratifiedKFold

cv_score_DT =[]
Skf = StratifiedKFold(n_splits=10,shuffle=True,random_state=49)
i=1
for train_index,test_index in skf.split(pulsar_X,pulsar_Y):
    print('{} of KFold {}'.format(i,skf.n_splits))
    xtr,xvl = pulsar_X[train_index],pulsar_X[test_index]
    ytr,yvl = pulsar_Y[train_index],pulsar_Y[test_index]
    model_DT = tree.DecisionTreeClassifier(max_depth=10, criterion = "entropy")
    model_DT.fit(xtr,ytr)
    score_DT = roc_auc_score(yvl,model_DT.predict(xvl))
    print('ROC AUC score:',score_DT)
    cv_score_DT.append(score_DT)
    print('Confusion matrix \n',confusion_matrix(yvl,model_DT.predict(xvl)))
    i+=1

"""# RandomForest"""

from sklearn.metrics import confusion_matrix, roc_auc_score ,roc_curve,auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np
cv_score_RF =[]

i=1
for train_index,test_index in skf.split(pulsar_X,pulsar_Y):
    print('{} of KFold {}'.format(i,skf.n_splits))
    xtr,xvl = pulsar_X[train_index],pulsar_X[test_index]
    ytr,yvl = pulsar_Y[train_index],pulsar_Y[test_index]
    model_RF = RandomForestClassifier(n_estimators=100)
    model_RF.fit(xtr,ytr)
    score_RF = roc_auc_score(yvl,model_RF.predict(xvl))
    print('ROC AUC score:',score_RF)
    cv_score_RF.append(score_RF)
    print('Confusion matrix \n',confusion_matrix(yvl,model_RF.predict(xvl)))
    i+=1

"""# Elbow Method"""

from sklearn.metrics import confusion_matrix, roc_auc_score ,roc_curve,auc
Skf = StratifiedKFold(n_splits=10,shuffle=True,random_state=49)

i=1
for train_index,test_index in skf.split(pulsar_X,pulsar_Y):
    print('{} of KFold {}'.format(i,skf.n_splits))
    xtr,xvl = pulsar_X[train_index],pulsar_X[test_index]
    ytr,yvl = pulsar_Y[train_index],pulsar_Y[test_index]

    score = []
    for cluster in range(2,9):
        kmeans = KMeans(n_clusters = cluster, init="k-means++", random_state=49)
        kmeans.fit(xtr)
        score.append(kmeans.inertia_)

    plt.plot(range(2,9), score, 'g-o')
    plt.title('The Elbow Method')
    plt.xlabel('no of clusters')
    plt.ylabel('Total within-cluster sum of square')
    plt.show()
    i+=1

"""# Silhouette score"""

#ref:https://www.kaggle.com/abhishekyadav5/kmeans-clustering-with-elbow-method-and-silhouette
#ref:https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm

silhouette_avg_list = []
n_clusters_list = []
for n_clusters in range(2,9):
    # Create a subplot with 1 row and 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18, 7)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(xtr) + (n_clusters + 1) * 10])

    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.
    clusterer = KMeans(n_clusters=n_clusters, random_state=49)
    cluster_labels = clusterer.fit_predict(xtr)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(xtr, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)
    silhouette_avg_list += [silhouette_avg]
    n_clusters_list += [n_clusters]
    
    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(xtr, cluster_labels)

    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # 2nd Plot showing the actual clusters formed
    colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(xtr[:, 0], xtr[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                c=colors, edgecolor='k')

    # Labeling the clusters
    centers = clusterer.cluster_centers_
    # Draw white circles at cluster centers
    ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
                c="white", alpha=1, s=200, edgecolor='k')

    for i, c in enumerate(centers):
        ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
                    s=50, edgecolor='k')

    ax2.set_title("The visualization of the clustered data.")
    ax2.set_xlabel("Feature space for the 3rd feature")
    ax2.set_ylabel("Feature space for the 9th feature")
    # ax2.set_xlabel("Feature space for the 1st feature")
    # ax2.set_ylabel("Feature space for the 2nd feature")

    plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                  "with n_clusters = %d" % n_clusters),
                 fontsize=14, fontweight='bold')

plt.show()

plt.plot(n_clusters_list, silhouette_avg_list, 'g-o')
plt.title('The Silhouette method')
plt.xlabel('no of clusters')
plt.ylabel('The Silhouette score')
plt.show()

"""# K-mean method and save the information"""

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2, random_state=49).fit(xtr)
kmLabels = kmeans.labels_
Label = [np.count_nonzero(kmLabels==0),np.count_nonzero(kmLabels==1)]
centroids = kmeans.cluster_centers_
print('Label:', Label)
print('Centroids',centroids)

plt.figure(figsize=(8,5))
plt.title("Pulsar of data points", fontsize=18)
plt.grid(True)
plt.scatter(xtr[kmeans.labels_ == 0, 2], xtr[kmeans.labels_ == 0, 5],
            c='red', label='cluster 0')
plt.scatter(xtr[kmeans.labels_ == 1, 2], xtr[kmeans.labels_ == 1, 5],
            c='blue', label='cluster 1')
plt.scatter(centroids[0, 2], centroids[0, 5], marker='*', s=300, c='g', label='centroid 0')
plt.scatter(centroids[1, 2], centroids[1, 5], marker='*', s=300, c='y', label='centroid 1')
plt.legend()
plt.savefig('Pulsar Kmean_10th fold.png', dpi=300)
plt.show()

#ref:https://towardsdatascience.com/k-means-clustering-algorithm-applications-evaluation-methods-and-drawbacks-aa03e644b48a

pred_test_full =0
Label_all = []
centroids_all = []
cv_scoreRF_new =[]
ConfusionMatrix_all = []

i=0

fig, ax = plt.subplots(3, 3, figsize=(16, 16))
ax = np.ravel(ax)
centers = []

## Use different 9 bins in training dataset,
## and remain one to be the testing dataset
for train_index,test_index in skf.split(pulsar_X,pulsar_Y):
    print('{} of KFold {}'.format(i,skf.n_splits))
    xtr,xvl = pulsar_X[train_index],pulsar_X[test_index]
    ytr,yvl = pulsar_Y[train_index],pulsar_Y[test_index]

    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=2, random_state=49)
    kmeans.fit(xtr)
    kmeans.predict(xvl)
    kmLabels = kmeans.labels_
    centers.append(kmLabels)
    ## save the centroid and the number of samples in each cluster in each 9 bins
    Label = [np.count_nonzero(kmLabels==0),np.count_nonzero(kmLabels==1)]
    Label_all += [Label]
    centroids = kmeans.cluster_centers_
    centroids_all += [centroids]

    ## plot the distribution of samples and the centroids
    #plt.figure(figsize=(8,5))
    #plt.title("Titanic of data points" "(%d of KFold 10)" %i, fontsize=18)
    #plt.grid(True)
    ax[i].scatter(xtr[kmeans.labels_ == 0, 2], xtr[kmeans.labels_ == 0, 5],
                c='red', label='cluster 0')
    ax[i].scatter(xtr[kmeans.labels_ == 1, 2], xtr[kmeans.labels_ == 1, 5],
                c='blue', label='cluster 1')
    ax[i].scatter(centroids[0, 2], centroids[0, 5], marker='*', s=300, c='g', label='centroid 0')
    ax[i].scatter(centroids[1, 2], centroids[1, 5], marker='*', s=300, c='y', label='centroid 1')
    ax[i].legend()
    ax[i].legend(loc='lower right')
    ax[i].set_title( str(i) +'of K fold 10')
    ax[i].set_aspect('equal')
    #plt.savefig('Pulsar Kmean_' + str(i) + 'of K fold 10.png', dpi=300)
    #plt.show()

    ## train and test the dataset in random forest model
    modelRFnew = RandomForestClassifier(random_state=42)
    modelRFnew.fit(xtr,kmLabels)
    scoreRF_new = roc_auc_score(yvl,modelRFnew.predict(xvl))
    print('ROC AUC score:',scoreRF_new)
    cv_scoreRF_new.append(scoreRF_new)
    from sklearn.metrics import confusion_matrix
    ConfusionMatrix = confusion_matrix(yvl, modelRFnew.predict(xvl))
    print('Confusion matrix\n',ConfusionMatrix)
    ConfusionMatrix_all += [ConfusionMatrix]
    i+=1
plt.tight_layout();

ConfusionMatrix_all

#ref:https://medium.com/@kelfun5354/model-tuning-and-what-is-it-using-python-630e388e224a
from sklearn.model_selection import cross_val_score
Skf = StratifiedKFold(n_splits=10,shuffle=True,random_state=49)
scores = cross_val_score(model_DT, pulsar_X, pulsar_Y, cv=Skf)
scores
print("Mean : %.3f%%, Standard Deviation: (%.3f%%)" % (scores.mean()*100.0, scores.std()*100.0))