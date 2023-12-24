import os
import io
import zipfile
from flask import Flask,render_template,request,send_file
from rembg import remove

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_images():
    temp_dir = 'temp_images'
    os.makedirs(temp_dir,exist_ok=True)

    files = request.files.getlist('images')

    for file in files:
        img_data = file.read()
        output_data = remove(img_data)

        filename = file.filename

        output_path = os.path.join(temp_dir,filename)
        with open(output_path,'wb') as f:
            f.write(output_data)

    ## zip file

    zip_path = "processed_images.zip"

    with zipfile.ZipFile(zip_path,"w") as zip_file:
        for root,_, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root,file)
                zip_file.write(file_path,file)

    for root,_, files in os.walk(temp_dir):
        for file in files:
            os.remove(os.path.join(root, file))
    os.rmdir(temp_dir)

    return send_file(zip_path, as_attachment= True)

if __name__ == "__main__":
    app.run(debug=True)