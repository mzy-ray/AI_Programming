import numpy
# from hw1_lr import LinearRegression, LinearRegressionWithL2Loss
# from utils import mean_squared_error
# from utils import polynomial_features
# from data import generate_data_part_2
# features, values = generate_data_part_2()
# from data import generate_data_part_3
# features, values = generate_data_part_3()
#
# train_features, train_values = features[:100], values[:100]
# valid_features, valid_values = features[100:120], values[100:120]
# test_features, test_values = features[120:], values[120:]
#
# assert len(train_features) == len(train_values) == 100
# assert len(valid_features) == len(valid_values) == 20
# assert len(test_features) == len(test_values) == 30
#
# model = LinearRegression(nb_features=1)
# model.train(features, values)
#
# best_mse, best_k = 1e10, -1
# for k in [1, 3, 10]:
#     train_features_extended = polynomial_features(train_features, k)
#     model = LinearRegression(nb_features=k)
#     model.train(train_features_extended, train_values)
#     train_mse = mean_squared_error(train_values, model.predict(train_features_extended))
#
#     valid_features_extended = polynomial_features(valid_features, k)
#     print(valid_features_extended)
#     valid_mse = mean_squared_error(valid_values, model.predict(valid_features_extended))
#     print('[part 1.4.1]\tk: {k:d}\t'.format(k=k) +
#           'train mse: {train_mse:.5f}\tvalid mse: {valid_mse:.5f}'.format(
#               train_mse=train_mse, valid_mse=valid_mse))
#
#     if valid_mse < best_mse:
#         best_mse, best_k = valid_mse, k
#
# combined_features_extended = polynomial_features(train_features + test_features, best_k)
# model = LinearRegression(nb_features=best_k)
# model.train(combined_features_extended, train_values + test_values)
#
# test_features_extended = polynomial_features(test_features, best_k)
# test_mse = mean_squared_error(test_values, model.predict(test_features_extended))
# print('[part 1.4.1 Linear Regression]\tbest_k: {best_k:d}\ttest mse: {test_mse:.5f}'.format(
#     best_k=best_k, test_mse=test_mse))
print(numpy.power(2.5, 10))