from flask import Flask, render_template, request, jsonify
import requests
import os

# Configuramos la ruta base para que Flask siempre encuentre la carpeta 'templates'
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

# --- CONFIGURACIÓN DE API ---
API_KEY = "6b33482b54mshae38d632818034fp1de0abjsn1c6d3e1183a1"
API_HOST = "tiktok-video-no-watermark2.p.rapidapi.com"
API_URL = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

@app.route('/', methods=['GET'])
def index():
    # Verifica que el archivo index.html exista antes de intentar cargarlo
    if not os.path.exists(os.path.join(template_dir, 'index.html')):
        return "Error: No se encuentra 'templates/index.html'. Verifica la carpeta."
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    
    if not video_url:
        return jsonify({"success": False, "message": "Por favor, introduce una URL de TikTok válida."})

    # Limpieza de URL
    if "?" in video_url:
        video_url = video_url.split("?")[0]
    
    payload = {"url": video_url, "hd": "1"}
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    try:
        response = requests.post(API_URL, data=payload, headers=headers, timeout=15)
        response.raise_for_status() 
        data = response.json()
        
        if data.get('code') == 0 and data.get('data'):
            video_info = data['data']
            return jsonify({
                "success": True, 
                "video": {
                    'title': video_info.get('title', 'Video de TikTok'),
                    'cover': video_info.get('cover'),
                    'download_url': video_info.get('play')
                }
            })
        else:
            return jsonify({"success": False, "message": data.get('msg', 'URL no válida.')})

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

if __name__ == '__main__':
    print(f"Buscando plantillas en: {template_dir}")
    app.run(debug=True, port=5000)