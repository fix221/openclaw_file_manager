import os

from flask import Flask, abort, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
MAX_UPLOAD_SIZE = 16 * 1024 * 1024

app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_folder_path(folder):
    if folder == 'downloads':
        return DOWNLOAD_FOLDER
    if folder == 'uploads':
        return UPLOAD_FOLDER
    return None


def sanitize_filename(filename):
    if not isinstance(filename, str):
        return None

    normalized = filename.strip()
    if not normalized or normalized in {'.', '..'}:
        return None
    if '/' in normalized or '\\' in normalized:
        return None

    safe_name = secure_filename(normalized)
    if not safe_name:
        return None

    return safe_name


def build_safe_path(folder_path, filename):
    safe_name = sanitize_filename(filename)
    if safe_name is None:
        return None, None

    candidate = os.path.abspath(os.path.join(folder_path, safe_name))
    base_path = os.path.abspath(folder_path)
    if os.path.commonpath([base_path, candidate]) != base_path:
        return None, None

    return candidate, safe_name


@app.errorhandler(413)
def handle_file_too_large(_error):
    return jsonify({'error': 'File too large'}), 413


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/files/<folder>')
def list_files(folder):
    folder_path = get_folder_path(folder)
    if folder_path is None:
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
    _file_path, safe_name = build_safe_path(DOWNLOAD_FOLDER, filename)
    if safe_name is None:
        abort(404)

    return send_from_directory(DOWNLOAD_FOLDER, safe_name, as_attachment=True)


@app.route('/api/delete', methods=['POST'])
def delete_file():
    data = request.get_json(silent=True) or {}
    filename = data.get('filename')
    folder = data.get('folder')

    folder_path = get_folder_path(folder)
    if folder_path is None:
        return jsonify({'error': 'Invalid folder'}), 400

    file_path, _safe_name = build_safe_path(folder_path, filename)
    if file_path is None:
        return jsonify({'error': 'Invalid filename'}), 400

    if os.path.isfile(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'})
    return jsonify({'error': 'File not found'}), 404


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename is None or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path, _safe_name = build_safe_path(UPLOAD_FOLDER, file.filename)
    if file_path is None:
        return jsonify({'error': 'Invalid filename'}), 400

    file.save(file_path)
    return jsonify({'message': 'File uploaded successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
