#command line:
# >>> export FLASK_ENV=development
# >>> export FLASK_APP=app
# >>> flask run
#sources:
# https://viveksb007.github.io/2018/04/uploading-processing-downloading-files-in-flask
# https://stackoverflow.com/questions/39139009/reading-input-file-and-processing-it-in-flask
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

from flask import Flask, request, redirect, url_for, render_template, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
from summarizer.summarize import summarize

app = Flask(__name__)

@app.route('/')
def index():
	original = ''
	summary = ''
	data = {'original': original, 'summary': summary}
	return render_template('index.html', data=data)

ALLOWED_EXTENSIONS = {'pdf','txt'}
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/text/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/summarized')
def summarized():
	for root, dirs, files in os.walk(UPLOAD_FOLDER):
		for file in files:
			os.remove(os.path.join(root, file))
	try:
		title = request.args.get('title',0,type=str).title()
		file_type = request.args.get('file_type',0,type=str)
		algorithm = request.args.get('algorithm',0,type=str)
		summary_size = request.args.get('summary_size',0,type=str)
		if file_type == 'text':
			file = request.args.get('original',0,type=str)    
		elif file_type == 'wikipedia':
			file = request.args.get('title',0,type=str)
		elif file_type == 'txt' or file_type == 'pdf':
			if 'file' not in request.files:
				return jsonify(original='There is no file path for the selected file', summary = 'None')
			file = request.files['file']
			if file.filename == '':
				return jsonify(original='There is no file selected', summary = 'None')
			if file and allowed_file(file.filename):            
				filename = secure_filename(file.filename)
				filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
				file.save(filepath)
				file = filepath
		text = summarize(title,file,file_type,algorithm,summary_size)
	return jsonify(title=title, original=text[0], summary=text[1])
	except Exception as e:
		return str(e)

if __name__ == '__main__':
   app.run(debug = True)    
