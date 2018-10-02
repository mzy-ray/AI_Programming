import numpy as np

p1 = np.array([0.1,0.1,0.8])
a = np.random.choice(np.arange(3), p=p1)
b = (1,'d')
print(b)


# covariance_matrix = np.zeros(2 * 2 * 2).reshape(2, 2, 2)
# a = np.array([2,2])
# b = np.array([1,1])
# c = np.matrix(a - b)
# d = np.matmul(c.transpose(), c)
# covariance_matrix[0] += d
# print(covariance_matrix[0])
