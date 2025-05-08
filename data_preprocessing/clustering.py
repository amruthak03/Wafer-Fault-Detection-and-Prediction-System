import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from file_operations import file_methods

class KMeansClustering:
    """
    This class provides functionality to perform clustering using the K-Means algorithm. It includes methods for
    determining the optimal number of clusters using the Elbow method and for creating clusters by assigning data points
    to their respective clusters. The class incorporates logging and error handling for better debugging and monitoring.
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def elbow_plot(self,data):
        """
        This method determines the optimal number of clusters for K-Means clustering using the Elbow method and saves the
        plot for visualization.
        Steps:
            Iteratively computes the Within-Cluster Sum of Squares for a range of cluster counts (1 to 10).
            Creates a plot of WCSS against the number of clusters and saves it as K-Means_Elbow.PNG.
            Uses the KneeLocator library to find the "elbow point," where adding more clusters doesn't significantly
            reduce WCSS.
        Returns: The optimal number of clusters (self.kn.knee).
        """
        self.logger_object.log(self.file_object, 'Entered the elbow_plot method of the KMeansClustering class')
        # initializing an empty list
        wcss = []
        try:
            for i in range(1,11):
                # initializing the KMeans object
                kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
                kmeans.fit(data)
                wcss.append(kmeans.inertia_) # Compute WCSS for each cluster count
            plt.plot(range(1,11),wcss)
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            plt.show()
            plt.savefig('preprocessing_data/K-Means_Elbow.PNG')
            # finding the value of the optimum cluster programmatically
            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            self.logger_object.log(self.file_object, 'The optimum number of clusters is: ' + str(
            self.kn.knee) + ' . Exited the elbow_plot method of the KMeansClustering class')
            return self.kn.knee
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in elbow_plot method of the KMeansClustering class. Exception message:'
                                   + str(e))
            self.logger_object.log(self.file_object,
                                   'Failed to find the number of clusters. Exited the elbow_plot method of the KMeansClustering class')
            raise Exception()

    def create_clusters(self, data, number_of_clusters):
        """
        This method creates clusters by fitting the K-Means model to the data and assigning cluster labels to each data
        point.
        Steps:
            Initializes and fits a K-Means model with the specified number of clusters. Assigns cluster labels to data points.
            Saves the trained K-Means model using a file_methods utility.
            Adds a new column Cluster to the data containing the assigned cluster labels.
        Returns: A DataFrame with an additional Cluster column.
        """
        self.logger_object.log(self.file_object, 'Entered the create_clusters method of the KMeansClustering class')
        self.data = data
        try:
            self.kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)
            # self.data = self.data[~self.data.isin([np.nan, np.inf, -np.inf]).any(1)]
            # Assign cluster labels
            self.y_kmeans = self.kmeans.fit_predict(data)
            self.file_op = file_methods.File_Operation(self.file_object, self.logger_object)
            # saving the KMeans model to directory
            self.save_model = self.file_op.save_model(self.kmeans, 'KMeans')
            # Add cluster information to the DataFrame
            self.data['Cluster'] = self.y_kmeans
            self.logger_object.log(self.file_object, 'successfully created ' + str(self.kn.knee) +
                                   'clusters. Exited the create_clusters method of the KMeansClustering class')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in create_clusters method of the KMeansClustering class. Exception message:'
                                   + str(e))
            self.logger_object.log(self.file_object,
                                   'Fitting the data to clusters failed. Exited the create_clusters method of the KMeansClustering class')
            raise Exception()

