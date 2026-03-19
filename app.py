from flask import Flask, request, redirect, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/ping')
def ping():
    return "ok"

@app.route('/api/play')
def play_video():
    video_id = request.args.get('id')

    if not video_id:
        return jsonify({"error": "Falta el ID"}), 400

    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'format': 'best',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)

            # 🔥 buscar m3u8 primero
            for f in info.get('formats', []):
                url = f.get('url')
                if url and "m3u8" in url:
                    return redirect(url, code=302)

            # 🔁 fallback
            if info.get('url'):
                return redirect(info['url'], code=302)

            return jsonify({"error": "No stream"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
