# https://www.researchgate.net/publication/221102989_Text_Summarization_of_Turkish_Texts_using_Latent_Semantic_Analysis
import numpy as np
import nltk 
nltk.download('averaged_perceptron_tagger')
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
	return U, S, V

def preprocess_topics(matrix):
	adv_score = 0
	for topic in range(len(matrix)):
		for sent in range(len(matrix[topic])):
			adv_score += matrix[topic][sent]
		adv_score /= len(matrix)
		for sent in range(len(matrix[topic])):
			if matrix[topic][sent] < adv_score:
				matrix[topic][sent] = 0
		adv_score = 0
	return matrix

def topic_matrix(matrix):
	transposed_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
	similarity_matrix = np.zeros((len(matrix),len(matrix)+2))
	topic_a = 0
	while topic_a < len(matrix):
		for sent in range(len(transposed_matrix)):
			for topic_b in range(len(transposed_matrix[sent])):
				if transposed_matrix[sent][topic_a] == 0:
					continue
				elif transposed_matrix[sent][topic_a] != 0 and transposed_matrix[sent][topic_b] != 0:
					if topic_b != topic_a:
						value = transposed_matrix[sent][topic_a] + transposed_matrix[sent][topic_b]
					elif topic_b == topic_a:
						value = transposed_matrix[sent][topic_b]
					similarity_matrix[topic_a][topic_b] += value
		similarity_matrix[topic_a][len(matrix)] = topic_a
		similarity_matrix[topic_a][len(matrix)+1] = sum(similarity_matrix[topic_a])
		topic_a += 1
	similarity_matrix = sorted(similarity_matrix, key=lambda x: x[len(matrix)+1], reverse=True) 
	return similarity_matrix

def topic_summary(full_content,content,size):
	matrix = root_matrix(content)
	svd = perform_svd(matrix)
	U = svd[0]
	S = svd[1]
	V = svd[2]
	preprocessed = preprocess_topics(V)
	topic = topic_matrix(preprocessed)
	score = 0
	top_sent = 0
	sentence = []
	summary_list = []
	for row in range(size):
		top_topic = int(topic[row][len(topic[row])-2])
		for sent in range(len(preprocessed[top_topic])):
			if score < preprocessed[top_topic][sent] and sent not in sentence:
				score = preprocessed[top_topic][sent]
				top_sent = sent
		sentence.append(top_sent)
		score = 0
		top_sent = 0
	for s in range(len(full_content)):	
		for i in sentence:
			if s == i:		
				summary_list.append(full_content[s])
	summary = ''
	for s in range(len(summary_list)):
		summary += summary_list[s]
	return summary

