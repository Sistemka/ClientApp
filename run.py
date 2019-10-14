from flask import Flask, render_template, request, url_for, redirect, flash
import os, datetime
import io, base64

from settings.paths import DIR, UPLOAD_DIR

app = Flask(__name__)



def getpictures(file_path):
    output = io.BytesIO(open(file_path, "rb").read())
    pictures = []
    pictures.append(base64.b64encode(output.getvalue()).decode())
    for fl in os.listdir(DIR):
        output = io.BytesIO(open(os.path.join(DIR, fl), "rb").read())
        pictures.append(base64.b64encode(output.getvalue()).decode())
    return pictures

@app.route('/', methods=["GET",'POST'])
def hello_world():
    if request.method=="POST":
        if 'file' not in request.files or request.files['file'].filename == "":
            return redirect(request.url)
        file = request.files["file"]
        filename = str(hash(file.filename + str(datetime.datetime.now()))) + "." + file.filename.split(".")[-1]
        file.save(os.path.join(UPLOAD_DIR, filename))
        pictures = getpictures(os.path.join(UPLOAD_DIR, filename))
        os.remove(os.path.join(UPLOAD_DIR, filename))
        return render_template("result.html", pictures = pictures)            
    return render_template('main.html')

if __name__ == '__main__':
    app.run()