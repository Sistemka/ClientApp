import os
import datetime
import io
import base64

from flask import Flask, render_template, request, redirect, abort
from sistemka.services import SearchEngine, ImageManager

from settings.paths import UPLOAD_DIR, FILES_DIR

app = Flask(__name__)


def getpictures(pictures_paths):
    pictures = []
    for fl in pictures_paths:
        output = io.BytesIO(open(fl, "rb").read())
        pictures.append(base64.b64encode(output.getvalue()).decode())
        os.remove(fl)
    return pictures


SE = SearchEngine()
image_manager = ImageManager()


@app.route('/', methods=["GET", 'POST'])
def hello_world():
    if request.method == "POST":
        if 'file' not in request.files or request.files['file'].filename == "":
            return redirect(request.url)
        file = request.files["file"]
        filename = str(hash(file.filename + str(datetime.datetime.now()))
                       ) + "." + file.filename.split(".")[-1]
        upload_file_path = os.path.join(UPLOAD_DIR, filename)
        file.save(upload_file_path)  # this thing saves file, so you can use it
        urls = SE.search(
            image_path=upload_file_path)
        for url in urls:
            image_manager.download_image(
                url=url,
                path_to_download=os.path.join(FILES_DIR, url)
            )
        uploaded_files = [os.path.join(FILES_DIR, url) for url in urls]
        pictures = getpictures(uploaded_files)
        os.remove(os.path.join(UPLOAD_DIR, filename))
        return render_template("main.html", pictures=pictures)
    return render_template('main.html')


@app.route('/set', methods=["POST"])
def set_pic():
    if request.method == "POST":
        if 'file' not in request.files or request.files['file'].filename == "":
            return abort(405)
        file = request.files["file"]
        output = io.BytesIO(file.read())
        picture = base64.b64encode(output.getvalue()).decode()
        return picture
    else:
        return abort(405)


if __name__ == '__main__':
    app.run()
