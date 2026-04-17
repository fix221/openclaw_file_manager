from flask import Flask, render_template, send_from_directory, request, jsonify
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/files/<folder>')
def list_files(folder):
    if folder == 'downloads':
        folder_path = DOWNLOAD_FOLDER
    elif folder == 'uploads':
        folder_path = UPLOAD_FOLDER
    else:
        return jsonify({'error': 'Invalid folder'}), 400
    
    files = []
    for f in os.listdir(folder_path):
        full_path = os.path.join(folder_path, f)
        if os.path.isfile(full_path):
            size = os.path.getsize(full_path)
            files.append({
                'name': f,
                'size': size,
                'is_folder': False
            })
    return jsonify(files)

@app.route('/api/download/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

@app.route('/api/delete', methods=['POST'])
def delete_file():
    data = request.get_json()
    filename = data.get('filename')
    folder = data.get('folder')
    
    if folder == 'downloads':
        folder_path = DOWNLOAD_FOLDER
    elif folder == 'uploads':
        folder_path = UPLOAD_FOLDER
    else:
        return jsonify({'error': 'Invalid folder'}), 400
    
    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'})
    return jsonify({'error': 'File not found'}), 404

# @app.route('/api/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#     file.save(os.path.join(UPLOAD_FOLDER, file.filename))
#     return jsonify({'message': 'File uploaded successfully'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename is None or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({'message': 'File uploaded successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
