from typing import List

import numpy as np


def mean_squared_error(y_true: List[float], y_pred: List[float]) -> float:
    assert len(y_true) == len(y_pred)

    error = 0.0
    for i in range(0, len(y_true)):
        error += np.square(y_true[i] - y_pred[i])
    error /= len(y_true)
    return error
    # raise NotImplementedError


def f1_score(real_labels: List[int], predicted_labels: List[int]) -> float:
    """
    f1 score: https://en.wikipedia.org/wiki/F1_score
    """
    assert len(real_labels) == len(predicted_labels)
    # raise NotImplementedError
    correct_positive = 0.0
    predicted_positive = 0.0
    all_positive = 0.0
    for i in range(0, len(real_labels)):
        if real_labels[i] == 1:
            all_positive += 1.0
        if predicted_labels[i] == 1:
            predicted_positive += 1.0
        if real_labels[i] == 1 and predicted_labels[i] == 1:
            correct_positive += 1.0
    if predicted_positive != 0:
        precision = correct_positive / predicted_positive
    else:
        precision = 1
    if all_positive != 0:
        recall = correct_positive / all_positive
    else:
        recall = 1
    if precision + recall != 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0.0
    return f1


def polynomial_features(
        features: List[List[float]], k: int
) -> List[List[float]]:
    # raise NotImplementedError
    features_extended = []
    for i in range(0, len(features)):
        feature_extended = []
        base = []
        for j in range(0, len(features[i])):
            base.append(features[i][j])
            feature_extended.append(features[i][j])
        for j in range(2, k + 1):
            feature_extended.extend(np.power(base, j))
        features_extended.append(feature_extended)
    return features_extended

def euclidean_distance(point1: List[float], point2: List[float]) -> float:
    # raise NotImplementedError
    # ed = 0.0
    # for i in range(0, len(point1)):
    #     ed += np.square(point1[i] - point2[i])
    # ed = np.sqrt(ed)
    # return ed
    p1 = np.array(point1)
    p2 = np.array(point2)
    return np.linalg.norm(p1 - p2)

def inner_product_distance(point1: List[float], point2: List[float]) -> float:
    # raise NotImplementedError
    # ipd = 0.0
    # for i in range(0, len(point1)):
    #     ipd += point1[i] * point2[i]
    # return ipd
    return np.dot(point1, point2)

def gaussian_kernel_distance(
        point1: List[float], point2: List[float]
) -> float:
    # raise NotImplementedError
    gkd = 0.0
    for i in range(0, len(point1)):
        gkd += np.square(point1[i] - point2[i])
    gkd = -1 * np.exp(-1/2 * gkd)
    return gkd

class NormalizationScaler:
    def __init__(self):
        pass

    def __call__(self, features: List[List[float]]) -> List[List[float]]:
        """
        normalize the feature vector for each sample . For example,
        if the input features = [[3, 4], [1, -1], [0, 0]],
        the output should be [[0.6, 0.8], [0.707107, -0.707107], [0, 0]]
        """
        # raise NotImplementedError
        features_normalized = []
        for feature in features:
            norm = np.linalg.norm(feature)
            if norm != 0:
                feature_normalized = feature/norm
                features_normalized.append(feature_normalized.tolist())
            else:
                features_normalized.append([0] * len(feature))
        return features_normalized


class MinMaxScaler:
    """
    You should keep some states inside the object.
    You can assume that the parameter of the first __call__
        must be the training set.

    Note:
        1. you may assume the parameters are valid when __call__
            is being called the first time (you can find min and max).

    Example:
        train_features = [[0, 10], [2, 0]]
        test_features = [[20, 1]]

        scaler = MinMaxScale()
        train_features_scaled = scaler(train_features)
        # now train_features_scaled should be [[0, 1], [1, 0]]

        test_features_sacled = scaler(test_features)
        # now test_features_scaled should be [[10, 0.1]]

        new_scaler = MinMaxScale() # creating a new scaler
        _ = new_scaler([[1, 1], [0, 0]]) # new trainfeatures
        test_features_scaled = new_scaler(test_features)
        # now test_features_scaled should be [[20, 1]]

    """

    def __init__(self):
        self.col_min = []
        self.col_max = []
        pass

    def __call__(self, features: List[List[float]]) -> List[List[float]]:
        """
        normalize the feature vector for each sample . For example,
        if the input features = [[2, -1], [-1, 5], [0, 0]],
        the output should be [[1, 0], [0, 1], [0.333333, 0.16667]]
        """
        # raise NotImplementedError
        if len(self.col_min) == 0 or len(self.col_max) == 0:
            for j in range(0, len(features[0])):
                min = features[0][j]
                max = features[0][j]
                for feature in features:
                    if feature[j] < min:
                        min = feature[j]
                    if feature[j] > max:
                        max = feature[j]
                self.col_min.append(min)
                self.col_max.append(max)

        features_normalized = []
        for feature in features:
            feature_normalized = []
            for j in range(0, len(feature)):
                if self.col_max[j] - self.col_min[j] != 0:
                    feature_normalized.append((feature[j] - self.col_min[j]) / (self.col_max[j] - self.col_min[j]))
                else:
                    feature_normalized.append(feature)
            features_normalized.append(feature_normalized)

        return features_normalized
