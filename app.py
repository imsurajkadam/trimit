import os
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
import zipfile
import shutil
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024  # 16GB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        return jsonify({
            'filename': unique_filename,
            'message': 'File uploaded successfully'
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/trim', methods=['POST'])
def trim_video():
    data = request.json
    filename = data.get('filename')
    duration = float(data.get('duration', 0))
    
    if not filename or duration <= 0:
        return jsonify({'error': 'Invalid parameters'}), 400
    
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output_filename = f"trimmed_{filename}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    
    try:
        with VideoFileClip(input_path) as video:
            trimmed_video = video.subclip(0, duration)
            trimmed_video.write_videofile(output_path, codec='libx264')
        
        return jsonify({
            'filename': output_filename,
            'message': 'Video trimmed successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/download-all', methods=['GET', 'POST'])
def download_all():
    try:
        zip_filename = 'trimmed_videos.zip'
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
        
        # Create a new zip file
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            has_files = False
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                if filename.startswith('trimmed_') and not filename.endswith('.zip'):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    zipf.write(file_path, filename)
                    has_files = True
        
        if not has_files:
            return jsonify({'error': 'No processed videos found'}), 404
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name='trimmed_videos.zip',
            mimetype='application/zip'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.startswith('trimmed_') or filename.endswith('.zip'):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'Cleanup successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 