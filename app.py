import os
import FruitClassifier
from flask import Flask, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

app.config['TEST_FOLDER'] = os.path.join(os.path.join('static/', 'fruit/'), 'test')


@app.route('/fruit-classifier')
@cross_origin()
def show_images():
    classification, path, features = FruitClassifier.next_image()
    full_filename = os.path.join('fruit/', path)
    return {
        "imageURL": full_filename,
        "classification": classification,
        "features": features,

    }


if __name__ == '__main__':
    app.run(host='0.0.0.0')
