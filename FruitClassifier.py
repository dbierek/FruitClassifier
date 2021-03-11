from FruitClassifierFeatures import show_features_pillow
from random import random
import os
import tensorflow as tf
from keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np


def get_class_names():
    class_names = os.listdir(os.path.join('static/fruit/', 'test'))
    class_names.sort()
    return class_names

def get_file_names():
    test_inorder_generator = ImageDataGenerator(rescale=1.0 / 255).flow_from_directory(
        os.path.join(os.path.join('static/', 'fruit/'), 'test'),
        target_size=(100, 100),
        batch_size=20,
        shuffle=False)
    return test_inorder_generator.filenames

def get_prediction(img_path, model):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = img.numpy()
    img = np.expand_dims(img, 0)
    pred = model.predict(img)
    return pred

def next_image(file_names, class_names, model):
    num_predictions = min(3000, len(file_names))
    image_num = int(random() * num_predictions)
    img_path = os.path.normpath(os.path.join(os.path.join(os.path.join('static/', 'fruit/'), 'test'), file_names[image_num]))
    label = class_names[np.argmax((get_prediction(img_path, model)))]
    # features = show_features(img_path, model)
    features = show_features_pillow(img_path, model)
    return label, file_names[image_num], features

model = load_model('savedModel')
def get_images():
    file_names = get_file_names()
    class_names = get_class_names()
    return next_image(file_names, class_names, model)


# def plot_filters():
#     retObject = {}
#     for layer in model.layers:
#         if "conv2d" not in layer.name:
#             continue
#         filters, _ = layer.get_weights()
#         filters_min = filters.min()
#         filters_max = filters.max()
#         filters = (filters - filters_min) / (filters_max - filters_min)
#         # print("Layer:", layer.name, " Filter Shape:", filters.shape)
#         retObject[layer.name] = filters
#     return retObject
        
#         # Graph 8 filters for each layer
#         num_filters = 8
#         row = 1
        
#         # Create a figure for this model layer
#         plt.figure()
        
#         # Graph each filter
#         for filter_num in range(num_filters):
#             # Initialize filter_data to be each filter's data
#             filter_data = filters[:, :, :, filter_num]
            
#             # Show Red, Green, and Blue color channels for each filter
#             for channel in range(3):
#                 # Create a new subplot that is 3 columns wide for each filter
#                 subplot = plt.subplot(num_filters, 3, row)
#                 subplot.set_xticks([])
#                 subplot.set_yticks([])
#                 # Graph the Red, Green, and Blue channels of the filter
#                 plt.imshow(filter_data[:, :, channel], cmap='gray')
#                 row += 1
#         # After graphing, plt.show() must be called to display the graphs
#         plt.show()
