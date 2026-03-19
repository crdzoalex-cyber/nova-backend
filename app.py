from flask import Flask, request, redirect, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "Servidor IPTV activo 🚀"

@app.route('/api/play')
def play_video():
    video_id = request.args.get('id')

    if not video_id:
        return jsonify({"error": "Falta el ID"}), 400

    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)

            formats = info.get('formats', [])
            m3u8_url = None

            for f in formats:
                url = f.get('url', '')
                if f.get('protocol') == 'm3u8' or 'm3u8' in url:
                    m3u8_url = url
                    break

            # fallback
            if not m3u8_url:
                m3u8_url = info.get('url')

            if m3u8_url:
                return redirect(m3u8_url, code=302)
            else:
                return jsonify({"error": "No se encontró stream"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
