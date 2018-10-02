import numpy as np
from typing import List
from classifier import Classifier

class DecisionTree(Classifier):
	def __init__(self):
		self.clf_name = "DecisionTree"
		self.root_node = None

	def train(self, features: List[List[float]], labels: List[int]):
		# init.
		assert(len(features) > 0)
		self.feautre_dim = len(features[0])
		num_cls = np.max(labels)+1

		# build the tree
		self.root_node = TreeNode(features, labels, num_cls)
		if self.root_node.splittable:
			self.root_node.split()

		return
		
	def predict(self, features: List[List[float]]) -> List[int]:
		y_pred = []
		for feature in features:
			y_pred.append(self.root_node.predict(feature))
		return y_pred

	def print_tree(self, node=None, name='node 0', indent=''):
		if node is None:
			node = self.root_node
		print(name + '{')
		if node.splittable:
			print(indent + '  split by dim {:d}'.format(node.dim_split))
			for idx_child, child in enumerate(node.children):
				self.print_tree(node=child, name= '  '+name+'/'+str(idx_child), indent=indent+'  ')
		else:
			print(indent + '  cls', node.cls_max)
		print(indent+'}')


class TreeNode(object):
	def __init__(self, features: List[List[float]], labels: List[int], num_cls: int):
		self.features = features
		self.labels = labels
		self.children = []
		self.num_cls = num_cls

		count_max = 0
		for label in np.unique(labels):
			if self.labels.count(label) > count_max:
				count_max = labels.count(label)
				self.cls_max = label # majority of current node

		if len(np.unique(labels)) < 2:
			self.splittable = False
		else:
			self.splittable = True

		self.dim_split = None # the dim of feature to be splitted

		self.feature_uniq_split = None # the feature to be splitted


	def split(self):
		def conditional_entropy(branches: List[List[int]]) -> float:
			'''
			branches: C x B array, 
					  C is the number of classes,
					  B is the number of branches
					  it stores the number of 
			'''
			########################################################
			# TODO: compute the conditional entropy
			########################################################
			C = len(branches)
			B = len(branches[0])
			sum_n = 0
			cond_entropy = 0.0
			for j in range(0, B):
				sum_branch_n = 0
				for i in range(0, C):
					sum_branch_n += branches[i][j]
				entropy = 0.0
				for i in range(0, C):
					p = float(branches[i][j]) / sum_branch_n
					if p == 0:
						entropy = 0
					else:
						entropy += -p * np.log(p)

				cond_entropy += sum_branch_n * entropy
				sum_n += sum_branch_n

				cond_entropy /= sum_n

			return cond_entropy


		min_cond_entropy = None
		for idx_dim in range(len(self.features[0])):
		############################################################
		# TODO: compare each split using conditional entropy
		#       find the 
		############################################################
			branches_dict = {}
			for i in range(0, len(self.labels)):
				if self.features[i][idx_dim] not in branches_dict:
					branches_dict[self.features[i][idx_dim]] = [0] * self.num_cls
				branches_dict[self.features[i][idx_dim]][self.labels[i]] += 1

			branches = []
			for i in range(0, self.num_cls):
				branches.append([])
			for branch in branches_dict:
				for i in range(0, self.num_cls):
					branches[i].append(branches_dict[branch][i])

			cond_entropy = conditional_entropy(branches)
			if min_cond_entropy == None or cond_entropy < min_cond_entropy:
				min_cond_entropy = cond_entropy
				self.dim_split = idx_dim


		############################################################
		# TODO: split the node, add child nodes
		############################################################
		if self.dim_split == None:
			self.splittable = False
			return

		children_data = {}
		for i in range(0, len(self.labels)):
			if self.features[i][self.dim_split] not in children_data:
				children_data[self.features[i][self.dim_split]] = []
			children_data[self.features[i][self.dim_split]].append((self.features[i][:self.dim_split] + self.features[i][self.dim_split+1:], self.labels[i]))

		self.feature_uniq_split = []
		for child_idx in children_data:
			features = []
			labels = []
			for d in children_data[child_idx]:
				features.append(d[0])
				labels.append(d[1])
			self.children.append(TreeNode(features, labels, self.num_cls))
			self.feature_uniq_split.append(child_idx)

		# split the child nodes
		for child in self.children:
			if child.splittable:
				child.split()

		return

	def predict(self, feature: List[int]) -> int:
		if self.splittable:
			# print(feature)
			idx_child = self.feature_uniq_split.index(feature[self.dim_split])
			feature = feature[:self.dim_split] + feature[self.dim_split+1:]
			return self.children[idx_child].predict(feature)
		else:
			return self.cls_max



