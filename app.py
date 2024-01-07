import os
import FruitClassifier
import FruitClassifierTraining
from flask import Flask, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

app.config['TEST_FOLDER'] = os.path.join(os.path.join('static/', 'fruit/'), 'test')

@app.route('/train-model')
@cross_origin()
def train_model():
    model, history = FruitClassifierTraining.train_model(4)

    return {
        "model": model,
        "history": history
    }

@app.route('/fruit-classifier')
@cross_origin()
def show_images():
    classification, path, features = FruitClassifier.next_image()
    full_filename = os.path.join('fruit/', path)
    return {
        "imageURL": full_filename,
        "classification": classification,
        "features": features
    }


@app.route('/get-file-names)')
@cross_origin()
def get_file_names():
    file_names = FruitClassifier.get_file_names()
    return {
        "fileNames": file_names
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
