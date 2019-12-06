import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = Path(BASE_DIR, 'upload')
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

DIR = os.path.join(os.getcwd(), 'templates/media/')
FILES_DIR = os.path.join(os.getcwd(), 'files')
