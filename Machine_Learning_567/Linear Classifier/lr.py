from __future__ import division, print_function

from typing import List

import numpy
import scipy


############################################################################
# DO NOT MODIFY ABOVE CODES
############################################################################

class LinearRegression:
    def __init__(self, nb_features: int):
        self.nb_features = nb_features
        self.weights = [0.0] * (nb_features + 1)

    def train(self, features: List[List[float]], values: List[float]):
        """TODO : Complete this function"""
        # raise NotImplementedError
        x = numpy.array(features)
        y = numpy.array(values)
        A = numpy.column_stack([numpy.ones(len(x)), x])
        # prodA = numpy.dot(A.T, A)
        # invA = numpy.linalg.inv(prodA)
        # self.weights = numpy.dot(numpy.dot(invA, A.T), y)
        self.weights = numpy.linalg.lstsq(A, y)[0]


    def predict(self, features: List[List[float]]) -> List[float]:
        """TODO : Complete this function"""
        # raise NotImplementedError
        return numpy.dot(numpy.column_stack([numpy.ones(len(features)), features]), self.weights)

    def get_weights(self) -> List[float]:
        """TODO : Complete this function"""

        """
        for a model y = 1 + 3 * x_0 - 2 * x_1,
        the return value should be [1, 3, -2].
        """
        # raise NotImplementedError
        return self.weights


class LinearRegressionWithL2Loss:
    '''Use L2 loss for weight regularization'''
    def __init__(self, nb_features: int, alpha: float):
        self.alpha = alpha
        self.nb_features = nb_features
        self.weights = [0.0] * (nb_features + 1)

    def train(self, features: List[List[float]], values: List[float]):
        """TODO : Complete this function"""
        # raise NotImplementedError
        x = numpy.array(features)
        y = numpy.array(values)
        A = numpy.column_stack([numpy.ones(len(x)), x])
        prodA = numpy.dot(A.T, A)
        invA = numpy.linalg.inv(prodA + self.alpha * numpy.identity(len(prodA)))
        self.weights = numpy.dot(numpy.dot(invA, A.T), y)

    def predict(self, features: List[List[float]]) -> List[float]:
        """TODO : Complete this function"""
        return numpy.dot(numpy.column_stack([numpy.ones(len(features)), features]), self.weights)

    def get_weights(self) -> List[float]:
        """TODO : Complete this function"""
        """
        for a model y = 1 + 3 * x_0 - 2 * x_1,
        the return value should be [1, 3, -2].
        """
        # raise NotImplementedError
        return self.weights


if __name__ == '__main__':
    print(numpy.__version__)
    print(scipy.__version__)
