from flask import Flask, request
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

base_dir = "M:\\Archive\\yt all\\"

@app.route("/archive")
def do_archive():
	url = request.args.get("url")
	if not url:
		return "?url=..."

	ydl_opts = {
		'writethumbnail': True,
		'writesubtitles': True,
		'writeinfojson': True,
		'getcomments': True,
		'embedchapters': True,
		'format_sort': ['res', 'codec:av1'],
		'outtmpl': os.path.join(base_dir, '%(webpage_url_domain)s/%(uploader)s/[%(upload_date)s] %(title)s [%(id)s].%(ext)s')
	}

	with YoutubeDL(ydl_opts) as ydl:
		try:
			ydl.download([url])
		except Exception as e:
			return f"error: {str(e)}"

	return "ok"


@app.route("/test")
def do_test():
	return "test"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6082, debug=True)
