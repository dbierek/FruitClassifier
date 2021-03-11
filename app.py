import os
import FruitClassifier
from flask import Flask, render_template

app = Flask(__name__)


app.config['TEST_FOLDER'] = os.path.join(os.path.join('static/', 'fruit/'), 'test')

# @app.route('/')
def show_index():
    return render_template("index.html")

# @app.route('/next')
@app.route('/fruit-classifier')
def show_images():
    classification, path, features = FruitClassifier.get_images()
    full_filename = os.path.join('fruit/', path)
    return {
        "imageURL": full_filename,
        "classification": classification,
        "features": features,
        
    }
if __name__ == '__main__':
    app.run(host='0.0.0.0')