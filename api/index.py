from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/extract', methods=['POST'])
def extract():
    data = request.json
    url = data.get('url', '').strip()
    if not url: return jsonify({"status": "error", "message": "Link missing"}), 400
    
    try:
        ydl_opts = {'quiet': True, 'nocheckcertificate': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": "success",
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "video": info.get('url')
            })
    except:
        return jsonify({"status": "error", "message": "Not supported"}), 500

@app.route('/api/download')
def download_proxy():
    file_url = request.args.get('url')
    req = requests.get(file_url, stream=True)
    return Response(req.iter_content(chunk_size=1024*8), headers={
        "Content-Disposition": "attachment; filename=video.mp4",
        "Content-Type": "application/octet-stream"
    })

app = app
