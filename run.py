import os
import datetime
import io
import base64

from flask import Flask, render_template, request, redirect
from sistemka.services import SearchEngine

from settings.paths import UPLOAD_DIR

app = Flask(__name__)


def getpictures(pictures_paths):
    pictures = []
    for fl in pictures_paths:
        output = io.BytesIO(open(fl, "rb").read())
        pictures.append(base64.b64encode(output.getvalue()).decode())
    return pictures


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
        file_paths = SearchEngine().predict(image_path=upload_file_path,
                                            image_name='upload_file')  # this has to be changed to neural method
        file_paths = [fl.get('url') for fl in file_paths]
        pictures = getpictures(file_paths)
        os.remove(os.path.join(UPLOAD_DIR, filename))
        return render_template("main.html", pictures=pictures)
    return render_template('main.html')


if __name__ == '__main__':
    app.run()
