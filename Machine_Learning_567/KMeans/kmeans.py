import numpy as np


class KMeans():

    '''
        Class KMeans:
        Attr:
            n_cluster - Number of cluster for kmeans clustering
            max_iter - maximum updates for kmeans clustering
            e - error tolerance
    '''

    def __init__(self, n_cluster, max_iter=100, e=0.0001):
        self.n_cluster = n_cluster
        self.max_iter = max_iter
        self.e = e

    def fit(self, x):
        '''
            Finds n_cluster in the data x
            params:
                x - N X D numpy array
            returns:
                A tuple
                (centroids or means, membership, number_of_updates )
            Note: Number of iterations is the number of time you update means other than initialization
        '''
        assert len(x.shape) == 2, "fit function takes 2-D numpy arrays as input"
        np.random.seed(42)
        N, D = x.shape

        # TODO:
        # - comment/remove the exception.
        # - Initialize means by picking self.n_cluster from N data points
        # - Update means and membership untill convergence or untill you have made self.max_iter updates.
        # - return (means, membership, number_of_updates)

        means = []
        cluster_members = []
        initial_idx = np.random.permutation(N)[:self.n_cluster]
        for idx in initial_idx:
            means.append(x[idx])
            cluster_members.append([])

        J = np.inf
        number_of_updates = 0
        for i in range(0, self.max_iter):
            new_J = 0.0
            for j in range(0, len(x)):
                min_dist = np.inf
                min_idx = -1
                for k in range(0, len(means)):
                    distance = np.sum(np.square(np.array(x[j]) - np.array(means[k])))
                    if distance < min_dist:
                        min_dist = distance
                        min_idx = k
                new_J += min_dist
                cluster_members[min_idx].append(j)

            new_J /= N
            if np.fabs(J - new_J) <= self.e:
                break
            J = new_J

            means = []
            for i in range(0, len(cluster_members)):
                sum = np.array(D * [0.0])
                for member in cluster_members[i]:
                    sum += np.array(x[member])
                mean = sum / len(cluster_members[i])
                means.append(mean)
                cluster_members[i] = []

            number_of_updates += 1

        membership = N * [-1]
        for i in range(0, len(cluster_members)):
            for member in cluster_members[i]:
                membership[member] = i

        return (np.array(means), np.array(membership), number_of_updates)

        # DONOT CHANGE CODE ABOVE THIS LINE
        # raise Exception(
        #     'Implement fit function in KMeans class (filename: kmeans.py')

        # DONOT CHANGE CODE BELOW THIS LINE


class KMeansClassifier():

    '''
        Class KMeansClassifier:
        Attr:
            n_cluster - Number of cluster for kmeans clustering
            max_iter - maximum updates for kmeans clustering
            e - error tolerance
    '''

    def __init__(self, n_cluster, max_iter=100, e=1e-6):
        self.n_cluster = n_cluster
        self.max_iter = max_iter
        self.e = e

    def fit(self, x, y):
        '''
            Train the classifier
            params:
                x - N X D size  numpy array
                y - N size numpy array of labels
            returns:
                None
            Stores following attributes:
                self.centroids : centroids obtained by kmeans clustering
                self.centroid_labels : labels of each centroid obtained by
                    majority voting
        '''

        assert len(x.shape) == 2, "x should be a 2-D numpy array"
        assert len(y.shape) == 1, "y should be a 1-D numpy array"
        assert y.shape[0] == x.shape[0], "y and x should have same rows"

        np.random.seed(42)
        N, D = x.shape
        # TODO:
        # - comment/remove the exception.
        # - Implement the classifier
        # - assign means to centroids
        # - assign labels to centroid_labels

        # DONOT CHANGE CODE ABOVE THIS LINE
        k_means = KMeans(self.n_cluster, self.max_iter, self.e)
        centroids, membership, i = k_means.fit(x)
        centroids_votes = []
        for centroid in centroids:
            centroids_votes.append({})
        for i in range(0, len(membership)):
            if y[i] in centroids_votes[membership[i]]:
                centroids_votes[membership[i]][y[i]] += 1
            else:
                centroids_votes[membership[i]][y[i]] = 1
        centroid_labels = []
        for centroid_vote in centroids_votes:
            max_vote = 0
            max_label = -1
            for c in centroid_vote:
                if centroid_vote[c] > max_vote:
                    max_vote = centroid_vote[c]
                    max_label = c
            centroid_labels.append(max_label)
        centroid_labels = np.array(centroid_labels)

        # DONOT CHANGE CODE BELOW THIS LINE

        self.centroid_labels = centroid_labels
        self.centroids = centroids

        assert self.centroid_labels.shape == (self.n_cluster,), 'centroid_labels should be a vector of shape {}'.format(
            self.n_cluster)

        assert self.centroids.shape == (self.n_cluster, D), 'centroid should be a numpy array of shape {} X {}'.format(
            self.n_cluster, D)

    def predict(self, x):
        '''
            Predict function

            params:
                x - N X D size  numpy array
            returns:
                predicted labels - numpy array of size (N,)
        '''

        assert len(x.shape) == 2, "x should be a 2-D numpy array"

        np.random.seed(42)
        N, D = x.shape
        # TODO:
        # - comment/remove the exception.
        # - Implement the prediction algorithm
        # - return labels

        # DONOT CHANGE CODE ABOVE THIS LINE

        pred_labels = []
        for point in x:
            min_dist = np.inf
            min_idx = -1
            for k in range(0, len(self.centroids)):
                distance = np.sum(np.square(np.array(point) - np.array(self.centroids[k])))
                if distance < min_dist:
                    min_dist = distance
                    min_idx = k
            pred_labels.append(self.centroid_labels[min_idx])

        return np.array(pred_labels)

        # DONOT CHANGE CODE BELOW THIS LINE
