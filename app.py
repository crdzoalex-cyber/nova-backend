from flask import Flask, request, redirect
import yt_dlp

app = Flask(__name__)

@app.route('/api/play')
def play_video():
    # 1. Recibimos el ID del video que nos manda tu app Android
    video_id = request.args.get('id')
    if not video_id:
        return "Falta el ID del video", 400

    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    # 2. Configuramos el tanque para sacar el Vivo en mejor calidad
    ydl_opts = {
        'format': 'best[protocol^=m3u8]', 
        'quiet': True,
        'no_warnings': True,
    }

    # 3. ¡Fuego! Extraemos el link puro
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            m3u8_url = info_dict.get('url', None)

            if m3u8_url:
                # 🔥 LA MAGIA: Redirigimos al VLC directamente al video puro
                return redirect(m3u8_url, code=302)
            else:
                return "No se pudo encontrar el link m3u8", 404
    except Exception as e:
        return f"Error en el servidor: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
