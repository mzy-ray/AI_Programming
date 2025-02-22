from __future__ import division, print_function

from typing import List, Tuple, Callable

import numpy as np
import scipy
import matplotlib.pyplot as plt

class Perceptron:

    def __init__(self, nb_features=2, max_iteration=10, margin=1e-4):
        '''
            Args : 
            nb_features : Number of features
            max_iteration : maximum iterations. You algorithm should terminate after this
            many iterations even if it is not converged 
            margin is the min value, we use this instead of comparing with 0 in the algorithm
        '''
        
        self.nb_features = 2
        self.w = [0 for i in range(0,nb_features+1)]
        self.margin = margin
        self.max_iteration = max_iteration

    def train(self, features: List[List[float]], labels: List[int]) -> bool:
        '''
            Args  : 
            features : List of features. First element of each feature vector is 1 
            to account for bias
            labels : label of each feature [-1,1]
            
            Returns : 
                True/ False : return True if the algorithm converges else False. 
        '''
        ############################################################################
        # TODO : complete this function. 
        # This should take a list of features and labels [-1,1] and should update 
        # to correct weights w. Note that w[0] is the bias term. and first term is 
        # expected to be 1 --- accounting for the bias
        ############################################################################
        # raise NotImplementedError
        count_iteration = 0
        flag_converge = False

        while not flag_converge and count_iteration < self.max_iteration:
            flag_converge = True
            count_iteration += 1
            for i in range(0, len(features)):
                y_pred = np.dot(self.w, features[i])
                if y_pred >= 0:
                    y_pred = 1
                else:
                    y_pred = -1
                if y_pred != labels[i]:
                    flag_converge = False
                    if np.linalg.norm(features[i]) != 0:
                        for j in range(0, len(self.w)):
                            self.w[j] += labels[i] * features[i][j] / np.linalg.norm(features[i])

        return flag_converge


    def reset(self):
        self.w = [0 for i in range(0,self.nb_features+1)]
        
    def predict(self, features: List[List[float]]) -> List[int]:
        '''
            Args  : 
            features : List of features. First element of each feature vector is 1 
            to account for bias
            
            Returns : 
                labels : List of integers of [-1,1] 
        '''
        ############################################################################
        # TODO : complete this function. 
        # This should take a list of features and labels [-1,1] and use the learned 
        # weights to predict the label
        ############################################################################
        
        # raise NotImplementedError
        pred = []
        for i in range(0, len(features)):
            y_pred = np.dot(self.w, features[i])
            if y_pred >= 0:
                y_pred = 1
            else:
                y_pred = -1
            pred.append(y_pred)

        return pred

    def get_weights(self) -> Tuple[List[float], float]:
        return self.w
    