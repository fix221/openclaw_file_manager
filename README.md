# Openclaw_File_Manager

[CN](https://github.com/fix221/openclaw_file_manager/blob/main/README-ZH.md)

## Project Description

This project is a Simple File Manager Tool customized for Openclaw to upload and download files conveniently

![Static Badge](https://img.shields.io/badge/Last_Updated-Apr_2026-blue)![Static Badge](https://img.shields.io/badge/Openclaw-Latest-green)

## Features

- Web-based file management interface
- Support for drag and drop file uploads
- File download functionality
- Real-time file list updates
- Copy download link to clipboard
- Delete files with confirmation
- Visual file type icons
- Responsive design with dark theme

## Quick Start

### Prerequisites

- Python 3.8+
- Flask

### Installation

```bash
pip install flask
```

### Running the Application

```bash
python app.py
```

The application will start at `http://0.0.0.0:8080`

### Configuration

Default directories:

- Downloads: `./downloads`
- Uploads: `./uploads`

You can modify the paths in `app.py` if needed.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/files/{folder}` | List files in folder |
| POST | `/api/upload` | Upload file |
| POST | `/api/delete` | Delete file |
| GET | `/api/download/{filename}` | Download file |

## Usage

1. Open the web interface
2. Upload files using the upload button
3. Download files from the download section
4. Copy shareable links for downloaded files

## Contribution Guidelines

Feel free to submit Issues or Forks to improve this project.

## License

MIT License

