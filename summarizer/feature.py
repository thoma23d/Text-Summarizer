#source: https://core.ac.uk/download/pdf/11784914.pdf
#source: https://www.sciencedirect.com/science/article/pii/S1877050915000952
import math 
from collections import Counter
import nltk
nltk.download('averaged_perceptron_tagger') 
import numpy as np
from skfuzzy import control as ctrl


def get_tfidf(content): 
	N = len(content)
	num_words = 0
	tf_dict = {}
	idf_dict = {}
	tfidf_dict = {}
	for sent in range(N):
		num_words += len(content[sent])
		for word in range(len(content[sent])):
			if content[sent][word] not in tf_dict.keys():
				tf_dict[content[sent][word]] = 1
			if content[sent][word] in tf_dict.keys():
				tf_dict[content[sent][word]] += 1
			if content[sent][word] not in idf_dict.keys():
				idf_dict[content[sent][word]] = [sent]				
			if content[sent][word] in idf_dict.keys():
				if sent not in idf_dict[content[sent][word]]:
					idf_dict[content[sent][word]].append(sent)
	counter = Counter(tf_dict)
	thematic_dict = counter.most_common(5)
	for term in tf_dict.keys():
		tf_dict[term] /= num_words
		idf_dict[term] = float(math.log(N/(len(idf_dict[term])+1)))
		tfidf_dict[term] = float(tf_dict[term] * idf_dict[term])		
	sum_tfidf = sum(tfidf_dict.values())
	return thematic_dict, sum_tfidf

def title_feature(title,sentence):
	titleNum = len(title)
	title_in_sent = 0
	for word in sentence:
		if word in title:
			title_in_sent += 1
	score = float(title_in_sent/titleNum)
	return score

def sentence_length(sentence,content):
	longest = [0,'a']
	for sent in range(len(content)):
		if len(content[sent]) < 100:			
			if len(content[sent]) > len(longest[1]):
				longest.pop(0)
				longest.pop(0)
				longest.insert(0,sent)
				longest.insert(1,content[sent])
	sentence = len(sentence)
	longest_sentence = len(longest[1])
	score = float(sentence/longest_sentence)
	return score

def term_weight(sentence, content):
	sentence_tfisf = get_tfidf(sentence)[1]
	max_tfisf = get_tfidf(content)[1]
	score = float(sentence_tfisf/max_tfisf)
	return score

def sentence_position(sentence,content):
	if sentence == 0:
		score = 1
	if sentence == (len(content)-1):
		score = 1
	else:
		score = 0
	return score

def sentence_similarity(sentence,content):
	l1 =[];l2 =[]
	for sent in content:
		rvector = list(set(sentence) | set(sent)) 
		for w in rvector: 
			if w in sentence: 
				l1.append(1)
			else: 
				l1.append(0) 
			if w in sent: 
				l2.append(1) 
			else: 
				l2.append(0) 
		c = 0
	for i in range(len(rvector)): 
		c += l1[i]*l2[i]
	score = c / float((sum(l1)*sum(l2))**0.5)
	return score

def proper_noun(sentence):
	sentence = nltk.pos_tag(sentence)
	num_nouns = [w for w in sentence if w[1] == 'NN']
	score = float(len(num_nouns)/len(sentence))
	return score

def thematic_word(sentence, content):
	thematic_num = 0
	thematic_dict = get_tfidf(content)[0]	
	for word in sentence:
		for i in thematic_dict:
			if word == i[0]:
				thematic_num += 1	
	score = float(thematic_num/len(sentence))
	return score

def numerical_data(sentence):
	num_data = 0
	for word in sentence:
		if word.isnumeric():
			num_data += 1
		else:
			num_data += 0	
	score = float(num_data/len(sentence))
	return score

def feature_scores(title,content):
	feature_scores = []
	for sentence_index in range(len(content)):
		sentence = content[sentence_index]
		if len(sentence) > 0:
			one = title_feature(title,sentence)
			two = sentence_length(sentence, content)
			three = term_weight(sentence,content)
			four = sentence_position(sentence_index, content)
			five = sentence_similarity(sentence,content)
			six = proper_noun(sentence) 
			seven = thematic_word(sentence,content)
			eight = numerical_data(sentence)	
		else:
			one = 0
			two = 0
			three = 0
			four = 0
			five = 0
			six = 0 
			seven = 0
			eight = 0	
		feature_scores.append([one,two,three,four,five,six,seven,eight])
	return feature_scores

def feature_highest(feature_scores):
	highest_scores = []
	one = max(score[0] for score in feature_scores)
	two = max(score[1] for score in feature_scores)
	three = max(score[2] for score in feature_scores)
	four = max(score[3] for score in feature_scores)
	five = max(score[4] for score in feature_scores)
	six = max(score[5] for score in feature_scores)
	seven = max(score[6] for score in feature_scores)
	eight = max(score[7] for score in feature_scores)
	highest_scores.append([one,two,three,four,five,six,seven,eight])
	return highest_scores

def feature_summary(title,full_content,content,size):
	scores = feature_scores(title,content)
	highest = feature_highest(scores)
	one = ctrl.Antecedent(np.arange(0, highest[0][0]+1, 1), 'title feature') 
	one.automf(3)
	two = ctrl.Antecedent(np.arange(0, highest[0][1]+1, 1), 'sentence length') 
	two.automf(3)
	three = ctrl.Antecedent(np.arange(0, highest[0][2]+1, 1), 'term weight') 
	three.automf(3)
	four = ctrl.Antecedent(np.arange(0, highest[0][3]+1, 1), 'sentence position') 
	four.automf(3)
	five = ctrl.Antecedent(np.arange(0, highest[0][4]+1, 1), 'sentence similarity') 
	five.automf(3)
	six = ctrl.Antecedent(np.arange(0, highest[0][5]+1, 1), 'proper noun') 
	six.automf(3)
	seven = ctrl.Antecedent(np.arange(0, highest[0][6]+1, 1), 'thematic word') 
	seven.automf(3)
	eight = ctrl.Antecedent(np.arange(0, highest[0][7]+1, 1), 'numerical data') 
	eight.automf(3)	
	importance = ctrl.Consequent(np.arange(0, 11, 1), 'sentence importance')
	importance.automf(3)

	rule1 = ctrl.Rule(antecedent = (one['poor'] & two['poor'] & three['poor'] & four['poor'] & five['poor'] & six['poor'] & seven['poor'] & eight['poor']), consequent = importance['poor'])
	rule2 = ctrl.Rule(antecedent = (one['average'] & two['average'] & three['average'] & four['good'] & five['average'] & six['average'] & seven['average'] & eight['average']), consequent = importance['average'])
	rule3 = ctrl.Rule(antecedent = (one['good'] & two['good'] & three['good'] & four['good'] & five['good'] & six['good'] & seven['good'] & eight['good']), consequent = importance['good'])	
	rule4 = ctrl.Rule(antecedent = (three['poor'] & five['poor'] & six['poor']), consequent = importance['poor'])
	rule5 = ctrl.Rule(antecedent = (three['average'] & five['average'] & six['average']), consequent = importance['average'])
	rule6 = ctrl.Rule(antecedent = (three['good'] & five['good'] & six['good']), consequent = importance['good'])
	rule7 = ctrl.Rule(antecedent = (one['good']), consequent = importance['good'])
	rule8 = ctrl.Rule(antecedent = (three['poor']), consequent = importance['poor'])
	rule9 = ctrl.Rule(antecedent = (four['good']), consequent = importance['good'])
	rule10 = ctrl.Rule(antecedent = (five['good']), consequent = importance['good'])
	importance_ctrl = ctrl.ControlSystem(rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])
	sentence_importance = ctrl.ControlSystemSimulation(importance_ctrl)

	sentence_rank = {}
	for i in range(len(scores)):
		sentence_importance.input['title feature'] = scores[i][0]
		sentence_importance.input['sentence length'] = scores[i][1]
		sentence_importance.input['term weight'] = scores[i][2]
		sentence_importance.input['sentence position'] = scores[i][3]
		sentence_importance.input['sentence similarity'] = scores[i][4]
		sentence_importance.input['proper noun'] = scores[i][5]
		sentence_importance.input['thematic word'] = scores[i][6]
		sentence_importance.input['numerical data'] = scores[i][7]
		sentence_importance.compute()
		sentence_rank[i] = sentence_importance.output['sentence importance']
	sentence_rank = sorted(sentence_rank.items(), key=lambda x: x[1], reverse=True)
	
	summary_list = []
	for s in range(len(full_content)):
		for i in sentence_rank[:size]:
			if s == i[0]:		
				summary_list.append(full_content[s])
	summary = ''
	for s in range(len(summary_list)):
		summary += summary_list[s]
	return summary

