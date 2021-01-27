#source: https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.726.1250&rep=rep1&type=pdf
#source: https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
import nltk
import math
nltk.download('averaged_perceptron_tagger')
import numpy as np
from nltk.cluster.util import cosine_distance
import networkx as nx


def sentence_similarity(sent1,sent2):
	all_words = list(set(sent1 + sent2))
	vector1 = [0] * len(all_words)
	vector2 = [0] * len(all_words)
	for w in sent1:
		vector1[all_words.index(w)] += 1
	for w in sent2:
		vector2[all_words.index(w)] += 1
	return 1-cosine_distance(vector1,vector2)

def overlapTitle(title,sentence):
	titleNum = len(title)
	title_in_sent = 0
	for word in sentence:
		if word in title:
			title_in_sent += 1
	val = float(title_in_sent/titleNum)
	return val

def termfreq(sentence,content):
	content_tf = {}
	sentence_tf = {}
	s_sum = 0
	c_sum = 0
	val = 0
	for sent in range(len(content)):
		for word in range(len(content[sent])):
			if content[sent][word] not in content_tf:
				content_tf[content[sent][word]] = 1
			if content[sent][word] in content_tf:
				content_tf[content[sent][word]] += 1
	for word in sentence:
		if word not in sentence_tf:
			sentence_tf[word] = 1
		if word in sentence_tf:
			sentence_tf[word] += 1
	for word in sentence_tf:
		s_sum += sentence_tf[word]
		c_sum += content_tf[word]
		val += (1+s_sum)/(c_sum)
	return val

def early(j):
	if j < 10:
		val = 2
	else:
		val = 1
	return val

def build_matrix(title, content):
	matrix = np.zeros((len(content),len(content)))
	for i in range(len(content)):
		for j in range(len(content)):
			if i != j and len(content[i]) > 0 and len(content[j]) > 0:
				similarity = sentence_similarity(content[i],content[j])
				weight = (1+overlapTitle(title,content[j]))*(termfreq(content[j],content))*(early(j))*(math.sqrt(1+len(content)))
				if similarity > 0 and weight > 0:
					matrix[i][j] = ((i-j)**2)/(similarity * weight)
				else:
					matrix[i][j] = 0
	return matrix

def graph_summary(title,full_content,content,size):
	summary_list = []
	matrix = build_matrix(title,content)
	graph = nx.from_numpy_array(matrix)
	scores = nx.pagerank(graph)
	sorted_scores = sorted(scores.items(),key=lambda x: x[1],reverse=True)
	for s in range(len(full_content)):
		for i in sorted_scores[:size]:
			if s == i[0]:
				summary_list.append(full_content[s])
	summary = ''
	for s in range(len(summary_list)):
		summary += summary_list[s]
	return summary
