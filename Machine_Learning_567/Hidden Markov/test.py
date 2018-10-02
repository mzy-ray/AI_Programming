import numpy as np

S = np.array([1,2,3,4,1,2,3,4,5]).reshape(3,3)
eig_value, eig_vector = np.linalg.eig(S)
eig_vector = eig_vector.transpose()
tmp = []
for i in range(len(eig_value)):
    tmp.append((i, eig_value[i]))
print(tmp)
sorted(tmp, key = lambda v: v[1], reverse=True)
print(tmp)