from flask import Flask
import os
import glob
import shutil
import moviepy.editor as moviepy

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
	
@app.route('/')
def upload_form():
	shutil.rmtree(UPLOAD_FOLDER[:-1])
	os.mkdir(UPLOAD_FOLDER[:-1])
	shutil.rmtree("Video-Summarization-Pytorch/output/curr_out")
	os.mkdir("Video-Summarization-Pytorch/output/curr_out")

	return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_video():
	print(request.files)
	print(request.form.get("percent"))
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	else:
		filename = secure_filename(file.filename)
		print(filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_video filename: ' + filename)
		input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		print(input_path)
		percentage = request.form.get("percent")
		run_command = "python Video-Summarization-Pytorch/video_summary.py --input " + str(input_path) + " --percent " + str(percentage)
		print(run_command)
		os.system(run_command)
		curr_out  = "Video-Summarization-Pytorch/output/curr_out"
		output_path  = "Video-Summarization-Pytorch/output/curr_out/" + str(os.listdir("Video-Summarization-Pytorch/output/curr_out")[0])
		print(output_path)
		os.system("mv " +output_path+ " "+ curr_out+"/summary.mp4")
		os.system("cp -r  " + curr_out+"/summary.mp4" + "  " +UPLOAD_FOLDER )
		# os.system("ffmpeg -i "+input_path+" -vcodec h264 " +UPLOAD_FOLDER +"actual.mp4")
		# os.system("ffmpeg -i "+input_path+" -vcodec h264 " +UPLOAD_FOLDER +"summary.mp4")
		flash('Video successfully uploaded and displayed below')
		clip = moviepy.VideoFileClip(input_path)
		clip.write_videofile(UPLOAD_FOLDER+"input.mp4")
		clip = moviepy.VideoFileClip(UPLOAD_FOLDER+"summary.mp4")
		clip.write_videofile(UPLOAD_FOLDER+"output.mp4")
		file_names = []
		# file_names.append(filename)
		file_names.append("input.mp4")
		# ffmpeg -i input1.mp4 -vcodec h264 output.mp4
		#need to append the name of the summary file
		file_names.append("output.mp4")

		return render_template('index.html', filenames=file_names)

@app.route('/display/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()