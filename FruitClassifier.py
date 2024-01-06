from FruitClassifierFeatures import show_features_pillow
from random import random
import os
import tensorflow as tf
from keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

def get_file_names():
    test_inorder_generator = ImageDataGenerator(rescale=1.0 / 255).flow_from_directory(
        os.path.join(os.path.join('static/', 'fruit/'), 'test'),
        target_size=(100, 100),
        batch_size=20,
        shuffle=False)
    return test_inorder_generator.filenames


file_names = get_file_names()
class_names = os.listdir(os.path.join('static/fruit/', 'test'))
class_names.sort()
model = load_model('savedModel')



def get_prediction(img_path, model):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = img.numpy()
    img = np.expand_dims(img, 0)
    pred = model.predict(img)
    return pred


def next_image():
    num_predictions = min(3000, len(file_names))
    image_num = int(random() * num_predictions)
    img_path = os.path.normpath(
        os.path.join(os.path.join(os.path.join('static/', 'fruit/'), 'test'), file_names[image_num]))
    label = class_names[np.argmax((get_prediction(img_path, model)))]
    # features = show_features(img_path, model)
    features = show_features_pillow(img_path, model)
    return label, file_names[image_num], features
