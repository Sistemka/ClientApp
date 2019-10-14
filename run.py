from flask import Flask, render_template, request, url_for, redirect, flash
import os
import io, base64

app = Flask(__name__)

def getpictures(files):
    output = io.BytesIO()
    files.save(output)
    pictures = []
    input_pic = base64.b64encode(output.getvalue()).decode()
    pictures.append(input_pic)
    DIR = os.path.join(os.getcwd(), 'templates/media')
    for fl in os.listdir(DIR):
        output = io.BytesIO(open(os.path.join(DIR, fl), "rb").read())
        pictures.append(base64.b64encode(output.getvalue()).decode())
    return pictures

@app.route('/', methods=["GET",'POST'])
def hello_world():
    if request.method=="POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files["file"]
        pictures = getpictures(file)
        try:
            return render_template("result.html", pictures = pictures)
        except:
            return redirect(request.url)
    return render_template('main.html')

if __name__ == '__main__':
    app.run()