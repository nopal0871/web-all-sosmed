from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import re

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Fungsi biar nama file gak aneh-aneh 🗿
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    format_choice = request.form.get('format')
    
    if not url:
        return jsonify({'error': 'URL kosong? Bapak lagi lupa ingatan? 🤣'}), 400

    try:
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'format': format_choice if format_choice else 'best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if os.path.exists(filename):
                return send_file(filename, as_attachment=True, download_name=sanitize_filename(info['title']) + ".mp4")
            else:
                return jsonify({'error': 'File gagal tersimpan, server nangis nih 🥀'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Gagal download: {str(e)} 😹'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
      
