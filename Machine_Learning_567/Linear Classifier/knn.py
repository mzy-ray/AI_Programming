from __future__ import division, print_function

from typing import List, Callable

import numpy
import scipy


############################################################################
# DO NOT MODIFY ABOVE CODES
############################################################################

class KNN:

    def __init__(self, k: int, distance_function) -> float:
        self.k = k
        self.distance_function = distance_function
        self.x = []
        self.y = []


    def train(self, features: List[List[float]], labels: List[int]):
        # raise NotImplementedError
        self.x_train = features
        self.y_train = labels


    def predict(self, features: List[List[float]]) -> List[int]:
        # raise NotImplementedError
        label_predict = []
        if self.k < 1:
            return [0] * len(features)

        for i in range(0, len(features)):
            nearest_neighbors = []

            for j in range(0, len(self.x_train)):
                dis = self.distance_function(features[i], self.x_train[j])

                if len(nearest_neighbors) < self.k:
                    nearest_neighbors.append((j, dis))
                else:
                    max = nearest_neighbors[0][1]
                    max_index = 0
                    for k in range(1, len(nearest_neighbors)):
                        if nearest_neighbors[k][1] > max:
                            max = nearest_neighbors[k][1]
                            max_index = k
                    if dis < max:
                        nearest_neighbors[max_index] = (j, dis)

            pos = 0
            neg = 0
            for k in range(0, len(nearest_neighbors)):
                if self.y_train[nearest_neighbors[k][0]] == 1:
                    pos += 1
                else:
                    neg += 1
            if pos >= neg:
                label_predict.append(1)
            else:
                label_predict.append(0)

        return label_predict


if __name__ == '__main__':
    print(numpy.__version__)
    print(scipy.__version__)
