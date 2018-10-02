import numpy as np
from typing import List, Set

from classifier import Classifier
from decision_stump import DecisionStump
from abc import abstractmethod

class Boosting(Classifier):
  # Boosting from pre-defined classifiers
	def __init__(self, clfs: Set[Classifier], T=0):
		self.clfs = clfs
		self.num_clf = len(clfs)
		if T < 1:
			self.T = self.num_clf
		else:
			self.T = T

		self.clfs_picked = [] # list of classifiers h_t for t=0,...,T-1
		self.betas = []       # list of weights beta_t for t=0,...,T-1
		return

	@abstractmethod
	def train(self, features: List[List[float]], labels: List[int]):
		return

	def predict(self, features: List[List[float]]) -> List[int]:
		########################################################
		# TODO: implement "predict"
		########################################################
		N = len(features)
		preds_sum = np.array([0.0] * N)
		for t in range(0, self.T):
			preds_sum += self.betas[t] * np.array(self.clfs_picked[t].predict(features))

		preds = []
		for i in range(0, N):
			if preds_sum[i] > 0:
				preds.append(1)
			else:
				preds.append(-1)

		return preds

class AdaBoost(Boosting):
	def __init__(self, clfs: Set[Classifier], T=0):
		Boosting.__init__(self, clfs, T)
		self.clf_name = "AdaBoost"
		return

	def train(self, features: List[List[float]], labels: List[int]):
		############################################################
		# TODO: implement "train"
		############################################################
		N = len(labels)
		w = [1/N] * N
		for t in range(0, self.T):
			minEt = None
			bestC = None
			for c in self.clfs:
				preds = c.predict(features)
				et = np.dot(w, (np.array(preds) != np.array(labels)).astype(int))
				if minEt == None or et < minEt:
					minEt = et
					bestC = c
			#if not bestC == None
			self.clfs_picked.append(bestC)

			beta = 1 / 2 * np.log((1 - minEt) / minEt)
			self.betas.append(beta)

			sum_w = 0.0
			preds = bestC.predict(features)
			for i in range(0, N):
				if preds[i] == labels[i]:
					w[i] = w[i] * np.exp(-beta)
				else:
					w[i] = w[i] * np.exp(beta)
				sum_w += w[i]
			w /= sum_w

		return



	def predict(self, features: List[List[float]]) -> List[int]:
		return Boosting.predict(self, features)


class LogitBoost(Boosting):
	def __init__(self, clfs: Set[Classifier], T=0):
		Boosting.__init__(self, clfs, T)
		self.clf_name = "LogitBoost"
		return

	def train(self, features: List[List[float]], labels: List[int]):
		############################################################
		# TODO: implement "train"
		############################################################
		N = len(labels)
		pi = [1 / 2] * N
		for t in range(0, self.T):
			z = []
			w = []
			for i in range(0, N):
				zi = ((labels[i] + 1) / 2 - pi[i]) / pi[i] / (1 - pi[i])
				z.append(zi)
				w.append(pi[i] * (1 - pi[i]))

			minEt = None
			bestC = None
			for c in self.clfs:
				preds = c.predict(features)
				et = np.dot(w, np.square(np.array(z) - np.array(preds)))
				if minEt == None or et < minEt:
					minEt = et
					bestC = c
			#if not bestC == None
			self.clfs_picked.append(bestC)

			beta = 1 / 2
			self.betas.append(beta)

			f = np.array([0.0] * N)
			for i in range(0, t + 1):
				f += 1 / 2 * np.array(self.clfs_picked[i].predict(features))
			pi = 1 / (1 + np.exp(-2 * f))

		return

	def predict(self, features: List[List[float]]) -> List[int]:
		return Boosting.predict(self, features)
