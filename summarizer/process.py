#source: https://medium.com/datapy-ai/nlp-building-text-summarizer-part-1-902fec337b81
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import nltk.data
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from word2number import w2n
from collections import Counter


def processTitle(userInput):
	stop_words = set(stopwords.words('english'))
	ps = PorterStemmer()
	word_tokens = nltk.word_tokenize(userInput)
	filtered_title = [word for word in word_tokens if word not in stop_words]
	stemmed_title = [ps.stem(word) for word in filtered_title]
	return stemmed_title

def remove_ref(file):
	text = ''
	skip1c = 0
	skip2c = 0
	for i in file:
		if i == '[':
			skip1c += 1
		elif i == '(':
			skip2c += 1
		elif i == ']' and skip1c > 0:
			skip1c -= 1
		elif i == ')'and skip2c > 0:
			skip2c -= 1
		elif skip1c == 0 and skip2c == 0:
			text += i
	return text

def str_to_num(word):
	new_int = []
	try:
		new_int += str(w2n.word_to_num(word))
	except ValueError:
		new_int += word
	return new_int

def getTFdict(text):
	tf_dict = {}
	for sent in range(len(text)):
		for word in range(len(text[sent])):
			if text[sent][word] not in tf_dict:
				tf_dict[text[sent][word]] = 1
			if text[sent][word] in tf_dict:
				tf_dict[text[sent][word]] += 1
	return tf_dict

def combineCommonWords(text):
	adjacent_dict = {}
	for s in range(len(text)):
		for w in range(len(text[s])-1):
			if text[s][w] not in adjacent_dict:
				adjacent_dict[text[s][w]] = [text[s][w+1],1]
			elif text[s][w] in adjacent_dict:
				if adjacent_dict[text[s][w]][0] != text[s][w+1]:
					del adjacent_dict[text[s][w]]
				elif adjacent_dict[text[s][w]][0] == text[s][w+1]:
					adjacent_dict[text[s][w]][1] += 1
	freq_dict = {}
	for t in adjacent_dict:
		if adjacent_dict[t][1] > 1:
			freq_dict[t] = adjacent_dict[t]
		else:
			continue
	new_text = []
	for s in range(len(text)):
		new_text.append([])
		for w in range(len(text[s])-1):
			if text[s][w] not in freq_dict:
				new_text[s].append(text[s][w])
			if text[s][w] in freq_dict and text[s][w+1] == freq_dict[text[s][w]][0]:
				new_text[s].append(text[s][w]+" "+text[s][w+1])
				continue
	return new_text

def processText(userInput):
	tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
	stop_words = set(stopwords.words('english'))
	lemma = WordNetLemmatizer()
	filtered_sentence = []
	new_sents = []
	lemmatized_words = []
	processed = []
	tf_dict = {}
	#remove references, and strip empty space
	text = remove_ref(userInput)
	text = [text.strip('\n')]
	stripped = [i.strip() for i in text]
	#tokenize into sentences list then convert numeric words to int
	sent_tokens = [sent_tokenize(s) for s in stripped]
	word_tokens = [word_tokenize(w) for w in sent_tokens[0]]
	new_sents = [str_to_num(s) for s in word_tokens]
	#remove stop words from sentences and lower case
	for sent in range(len(new_sents)):
		filtered_sentence.append([])
		for word in range(len(new_sents[sent])):
			if new_sents[sent][word] not in stop_words:
				filtered_sentence[sent].append(new_sents[sent][word].lower())
	#remove punctuation and one letter words
	for sent in range(len(filtered_sentence)):
		for word in range(len(filtered_sentence[sent])):
			filtered_sentence[sent][word] = filtered_sentence[sent][word].translate(str.maketrans('','', string.punctuation))
			if len(filtered_sentence[sent][word]) <= 1:
				filtered_sentence[sent][word] = filtered_sentence[sent][word].replace(filtered_sentence[sent][word],"")
	#remove empty words
	for sent in range(len(filtered_sentence)):
		while("" in filtered_sentence[sent]) :
			filtered_sentence[sent].remove("")
	for sent in range(len(filtered_sentence)):
		lemmatized_words.append([])
		for word in range(len(filtered_sentence[sent])):
			lemmatized_words[sent].append(lemma.lemmatize(filtered_sentence[sent][word]))
	#count term frequency to get most common and rare words
	tf_dict = getTFdict(lemmatized_words)
	counter = Counter(tf_dict)
	common_words = counter.most_common(10)
	rare_words = counter.most_common()[:-5-1:-1]
	#remove 10 most common and 5 rare words from sentences
	for sent in range(len(lemmatized_words)):
		processed.append([])
		for word in range(len(lemmatized_words[sent])):
			if lemmatized_words[sent][word] not in common_words or lemmatized_words[sent][word] not in rare_commons:
				processed[sent].append(lemmatized_words[sent][word])
	#combine words that only appear together
	processed = combineCommonWords(processed)
	#return unprocess setences tokens and processed sentence tokens
	return sent_tokens[0], processed
