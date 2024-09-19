from flask import Flask, request, send_file, render_template
import os
import ffmpeg
from flask_cors import CORS


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'videoFile' not in request.files:
        return "No file part"
    
    file = request.files['videoFile']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, 'output.mp3')
        
        file.save(input_path)
        
        # Convert video to audio using ffmpeg and overwrite if file exists
        ffmpeg.input(input_path).output(output_path).run(overwrite_output=True)
        
        return send_file(output_path, as_attachment=True, download_name='output.mp3')

if __name__ == '__main__':
    app.run(debug=True)



