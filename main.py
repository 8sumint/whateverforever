from flask import Flask, request, jsonify, render_template
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

base_dir = "M:\\Archive\\yt all\\"

jobs = {}

def job_hook(dl):
	status = dl['status']
	info_dict = dl['info_dict']
	url = info_dict['original_url']

	jobs[url]["dl"] = dl

class MyLogger:
	def __init__(self, url):
		self.url = url
		jobs[self.url]["logs"] = []
		self.logs = jobs[self.url]["logs"]
		
	def debug(self, msg):
		self.logs.append(msg)

	def warning(self, msg):
		self.logs.append(msg)

	def error(self, msg):
		self.logs.append(msg)
		print(msg)

@app.route("/archive")
def r_archive():
	url = request.args.get("url")
	if not url:
		return "?url=..."

	jobs[url] = {"dl": {"status": "extract_info"}}

	ydl_opts = {
		'writethumbnail': True,
		#'writesubtitles': True, # was causing it to fail??
		'writeinfojson': True,
		'getcomments': True,
		'embedchapters': True,
		'format_sort': ['res', 'codec:av1'],
		'progress_hooks': [job_hook],
		'logger': MyLogger(url),
		'color': 'never',
		'outtmpl': os.path.join(base_dir, '%(webpage_url_domain)s/%(uploader)s/[%(upload_date)s] %(title)s [%(id)s].%(ext)s')
	}

	with YoutubeDL(ydl_opts) as ydl:
		try:
			ydl.download([url])
		except Exception as e:
			return f"error: {str(e)}"

	if jobs[url]["dl"]["status"] == "extract_info":
		jobs[url]["dl"]["status"] = "no_download"

	return "ok"


@app.route("/test")
def r_test():
	return "test"

@app.route("/jobs")
def r_jobs():
	return jsonify(jobs)

@app.route("/")
def r_dashboard():
	return render_template("dashboard.html", jobs=jobs)

@app.route("/logs/")
def r_logs():
	url = request.args.get("url")
	if not url:
		return "?url=..."
	if not jobs.get(url):
		return "job not found"
	return "<pre>" + "<br>".join(jobs[url]["logs"])+ "</pre>"


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=6082, debug=True)
