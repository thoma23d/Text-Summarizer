# https://www.researchgate.net/publication/221102989_Text_Summarization_of_Turkish_Texts_using_Latent_Semantic_Analysis
import numpy as np
import nltk 
nltk.download('averaged_perceptron_tagger')
from numpy import array
from scipy.linalg import svd


def term_dict(content):
	term_dict = {}
	for sent in range(len(content)):
		for word in range(len(content[sent])):
			if content[sent][word] not in term_dict:
				term_dict[content[sent][word]] = [sent]
			if content[sent][word] in term_dict:	
				term_dict[content[sent][word]].append(sent)
	return term_dict

def root_matrix(content):
	terms = term_dict(content)
	term_list = list(terms)
	matrix = np.zeros((len(terms.keys()),len(content)))
	sentence = []
	for sent in range(len(content)):
		sentence.append(nltk.pos_tag(content[sent]))
	for sent in range(len(sentence)):
		for word in range(len(sentence[sent])):
			if sentence[sent][word][1] == 'NN' and sentence[sent][word][0] in terms:
				matrix[term_list.index(sentence[sent][word][0])][sent] += 1
	return matrix

def perform_svd(matrix):
	U, S, V = svd(matrix, full_matrices=False)
	S = np.flip(S)
	return U, S, V

def preprocess_concepts(matrix):
	adv_score = 0
	for concept in range(len(matrix)):
		for sent in range(len(matrix[concept])):
			adv_score += matrix[concept][sent]
		adv_score /= len(matrix)
		for sent in range(len(matrix[concept])):
			if matrix[concept][sent] < adv_score:
				matrix[concept][sent] = 0
		adv_score = 0
	return matrix

def cross_matrix(S,V):	
	for concept in range(len(V)):
		for sent in range(len(V[concept])):
			V[concept][sent] = V[concept][sent] * S[concept]
	transposed_matrix = [[V[concept][sent] for concept in range(len(V))] for sent in range(len(V[0]))]
	matrix = np.zeros((len(transposed_matrix),2))
	for sent in range(len(transposed_matrix)):
		matrix[sent][0] = sent
		matrix[sent][1] = sum(transposed_matrix[sent])
	matrix = sorted(matrix, key=lambda x: x[1], reverse=True)
	return matrix

def cross_summary(full_content,content,size):
	root = root_matrix(content)
	svd = perform_svd(root)
	U = svd[0]
	S = svd[1]
	V = svd[2]
	preprocessed_V = preprocess_concepts(V)
	matrix = cross_matrix(S,preprocessed_V)
	sentence_index = []
	summary_list = []
	summary = ''
	for sent in range(size): 
		sentence_index.append(matrix[sent][0])
	for s in range(len(full_content)):	
		for i in sentence_index:
			if s == i:	
				summary_list.append(full_content[s])
	for s in range(len(summary_list)):
		summary += summary_list[s]
	return summary
