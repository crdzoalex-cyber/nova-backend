from flask import Flask, request, redirect, jsonify
import yt_dlp
import subprocess

app = Flask(__name__)

# 🔥 ACTUALIZAR yt-dlp correctamente (clave real)
try:
    subprocess.run(["pip", "install", "-U", "yt-dlp"], check=True)
except:
    pass


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
        'format': 'bestaudio/best',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        },
        'http_headers': {
            'User-Agent': 'com.google.android.youtube/19.09.37 (Linux; U; Android 11)'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)

            # 🔥 PRIORIDAD: formatos m3u8 (para VLC)
            for f in info.get('formats', []):
                url = f.get('url')
                if url and "m3u8" in url:
                    return redirect(url, code=302)

            # 🔁 fallback
            if info.get('url'):
                return redirect(info['url'], code=302)

            return jsonify({"error": "No stream disponible"}), 404

    except Exception as e:
        return jsonify({
            "error": "yt-dlp fallo",
            "detalle": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
