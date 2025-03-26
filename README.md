# Video Trimmer

A simple web-based tool for trimming multiple videos at once. Upload your videos, specify the duration, and get trimmed versions of all videos in a single ZIP file.

## Features

- Drag and drop video upload
- Support for multiple video formats (MP4, AVI, MOV, MKV)
- Bulk video processing
- Individual video downloads
- Download all processed videos as a ZIP file
- Modern, responsive UI

## Prerequisites

- Python 3.7 or higher
- FFmpeg installed on your system

### Installing FFmpeg on macOS

Using Homebrew:
```bash
brew install ffmpeg
```

## Setup

1. Clone this repository or download the files
2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Drag and drop your videos into the upload zone or click "Browse Files" to select videos
2. Enter the desired duration (in seconds) for the trimmed videos
3. Click "Process Videos" to start trimming
4. Once processing is complete, you can:
   - Download individual videos using the download links
   - Click "Download All" to get all processed videos in a ZIP file
5. Use the "Cleanup" button to remove all processed videos and start fresh

## Notes

- The maximum file size is set to 16GB
- Supported video formats: MP4, AVI, MOV, MKV
- Processed videos are stored in the `uploads` directory
- The application uses FFmpeg for video processing 