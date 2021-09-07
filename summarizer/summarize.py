
def summarize(title,file,file_type,algorithm,size):
	from summarizer.process import processTitle, processText
	import os

	if file_type == 'text':
		file = file
	elif file_type == 'txt':
		fileInput = file
		file = open(fileInput).read()
		print("FILE ONE: ",file)
	elif file_type == 'pdf':
		from tika import parser
		fileInput = file
		parsed_pdf = parser.from_file(fileInput)
		tika = parsed_pdf['content']
		file = open(os.path.join(os.path.dirname(__file__),"../text/content.txt"), 'w')
		file.write(tika)
		print("TIKA: ",tika)	
		file = open(os.path.join(os.path.dirname(__file__),"../text/content.txt")).read()
	elif file_type == 'wikipedia': 
		import wikipedia
		wikisearch = wikipedia.page(title)
		wikicontent = wikisearch.content
		file = open(os.path.join(os.path.dirname(__file__),"../text/content.txt"), 'w')
		file.write(wikicontent)
		file = open(os.path.join(os.path.dirname(__file__),"../text/content.txt")).read()
	title = processTitle(title)	
	processed = processText(file)
	unprocessed_content = processed[0]
	processed_content = processed[1]
	summary_size = int((int(size)/100) * len(unprocessed_content))
	orginal = file
	summary = ''
	if algorithm == 'feature':
		from summarizer.feature import feature_summary
		summary = feature_summary(title,unprocessed_content,processed_content,summary_size)
	if algorithm == 'graph':
		from summarizer.graph import graph_summary
		summary = graph_summary(unprocessed_content,processed_content,summary_size)
	if algorithm == 'topic':
		from summarizer.topic import topic_summary
		summary = topic_summary(unprocessed_content,processed_content,summary_size)
	if algorithm == 'cross':
		from summarizer.cross import cross_summary
		summary = cross_summary(unprocessed_content,processed_content,summary_size)
	return orginal,summary
