import numpy as np
from kmeans import KMeans


class GMM():
    '''
        Fits a Gausian Mixture model to the data.

        attrs:
            n_cluster : Number of mixtures
            e : error tolerance
            max_iter : maximum number of updates
            init : initialization of means and variance
                Can be 'random' or 'kmeans'
            means : means of gaussian mixtures
            variances : variance of gaussian mixtures
            pi_k : mixture probabilities of different component
    '''

    def __init__(self, n_cluster, init='k_means', max_iter=100, e=0.0001):
        self.n_cluster = n_cluster
        self.e = e
        self.max_iter = max_iter
        self.init = init
        self.means = None
        self.variances = None
        self.pi_k = None

    def fit(self, x):
        '''
            Fits a GMM to x.

            x: is a NXD size numpy array
            updates:
                self.means
                self.variances
                self.pi_k
        '''
        assert len(x.shape) == 2, 'x can only be 2 dimensional'

        np.random.seed(42)
        N, D = x.shape

        if (self.init == 'k_means'):
            # TODO
            # - comment/remove the exception
            # - initialize means using k-means clustering
            # - compute variance and pi_k

            # DONOT MODIFY CODE ABOVE THIS LINE

            k_means = KMeans(self.n_cluster, self.max_iter, self.e)
            self.means, membership, i = k_means.fit(x)

            Nk = np.zeros(self.n_cluster)
            self.pi_k = np.zeros(self.n_cluster)
            self.variances = np.zeros(self.n_cluster * D * D).reshape(self.n_cluster, D, D)
            for i in range(0, len(membership)):
                Nk[membership[i]] += 1
                diff = np.matrix(np.array(x[i]) - np.array(self.means[membership[i]]))
                self.variances[membership[i]] += np.outer(diff.transpose(), diff)
            for k in range(0, len(self.variances)):
                self.variances[k] /= Nk[k]
            self.pi_k = Nk / N

            # DONOT MODIFY CODE BELOW THIS LINE

        elif (self.init == 'random'):
            # TODO
            # - comment/remove the exception
            # - initialize means randomly
            # - compute variance and pi_k

            # DONOT MODIFY CODE ABOVE THIS LINE

            self.means = np.zeros(self.n_cluster * D).reshape(self.n_cluster, D)
            self.variances = np.zeros(self.n_cluster * D * D).reshape(self.n_cluster, D, D)
            for k in range(0, self.n_cluster):
                for d in range(0, D):
                    self.means[k][d] = np.random.rand()
                self.variances[k] = np.identity(D)
            self.pi_k = np.array(self.n_cluster * [1.0 / self.n_cluster])

            # DONOT MODIFY CODE BELOW THIS LINE

        else:
            raise Exception('Invalid initialization provided')

        # TODO
        # - comment/remove the exception
        # - find the optimal means, variances, and pi_k and assign it to self
        # - return number of updates done to reach the optimal values.
        # Hint: Try to seperate E & M step for clarity

        # DONOT MODIFY CODE ABOVE THIS LINE

        L = self.compute_log_likelihood(x)
        gamma = np.zeros(N * self.n_cluster).reshape(N, self.n_cluster)

        num_iteration = 0
        while num_iteration < self.max_iter:
            for i in range(0, len(x)):
                sum = 0.0
                for k in range(0, self.n_cluster):
                    gamma[i][k] = self.pi_k[k] * self.compute_distribution_probability(np.array(x[i]), k, D)
                    sum += gamma[i][k]
                gamma[i] = gamma[i] / sum


            Nk = np.zeros(self.n_cluster)
            self.means = np.zeros(self.n_cluster * D).reshape(self.n_cluster, D)
            for i in range(0, len(x)):
                for k in range(0, self.n_cluster):
                    Nk[k] += gamma[i][k]
                    self.means[k] += gamma[i][k] * np.array(x[i])
            for k in range(0, self.n_cluster):
                self.means[k] /= Nk[k]
            self.pi_k = Nk / N
            self.variances = np.zeros(self.n_cluster * D * D).reshape(self.n_cluster, D, D)
            for i in range(0, len(x)):
                for k in range(0, self.n_cluster):
                    diff = np.array(x[i]) - self.means[k]
                    self.variances[k] += gamma[i][k] * np.outer(diff.transpose(), diff)
            for k in range(0, self.n_cluster):
                self.variances[k] = self.variances[k] / Nk[k]

            num_iteration += 1
            L_new = self.compute_log_likelihood(x)
            if np.fabs(L - L_new) < self.e:
                break
            L = L_new

        return num_iteration
        # DONOT MODIFY CODE BELOW THIS LINE

    def sample(self, N):
        '''
        sample from the GMM model

        N is a positive integer
        return : NXD array of samples

        '''
        assert type(N) == int and N > 0, 'N should be a positive integer'
        np.random.seed(42)
        if (self.means is None):
            raise Exception('Train GMM before sampling')

        # TODO
        # - comment/remove the exception
        # - generate samples from the GMM
        # - return the samples

        # DONOT MODIFY CODE ABOVE THIS LINE

        samples = []
        Ks = np.arange(self.n_cluster)
        for i in range(0, N):
            k = np.random.choice(Ks, p=self.pi_k)
            x = np.random.multivariate_normal(self.means[k], self.variances[k])
            samples.append(x)

        return np.array(samples)

        # DONOT MODIFY CODE BELOW THIS LINE

    def compute_log_likelihood(self, x):
        '''
            Return log-likelihood for the data

            x is a NXD matrix
            return : a float number which is the log-likelihood of data
        '''
        assert len(x.shape) == 2,  'x can only be 2 dimensional'
        # TODO
        # - comment/remove the exception
        # - calculate log-likelihood using means, variances and pi_k attr in self
        # - return the log-likelihood
        # Note: you can call this function in fit function (if required)
        # DONOT MODIFY CODE ABOVE THIS LINE

        N, D = x.shape
        L = 0.0
        for i in range(0, len(x)):
            px = 0.0
            for k in range(0, self.n_cluster):
                px += self.pi_k[k] * self.compute_distribution_probability(np.array(x[i]), k, D)
            L += np.log(px)

        return float(L)

        # DONOT MODIFY CODE BELOW THIS LINE

    def compute_distribution_probability(self, x, k, D):
        while np.linalg.matrix_rank(self.variances[k]) != D:
            self.variances[k] += np.identity(D) / 1000

        diff = np.matrix(x - self.means[k])
        tmp = np.exp(-1/2 * np.matmul(np.matmul(diff, np.linalg.inv(self.variances[k])), diff.transpose()))
        tmp2 = np.sqrt(np.power(2 * np.pi, D) * np.linalg.det(self.variances[k]))
        pxk = np.exp(-1/2 * np.matmul(np.matmul(diff, np.linalg.inv(self.variances[k])), diff.transpose())) \
              / np.sqrt(np.power(2 * np.pi, D) * np.linalg.det(self.variances[k]))

        return pxk