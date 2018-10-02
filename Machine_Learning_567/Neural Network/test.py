import numpy as np

X = np.zeros((2,3))
Y = np.zeros((2,3))
X += np.array([1,2,3])
Y += np.array([2,2,2])
z = np.multiply(X, Y)
print(z)