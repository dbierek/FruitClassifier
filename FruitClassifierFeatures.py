import io
import base64
from tensorflow.keras import Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow import expand_dims
from tensorflow.keras.applications.resnet import preprocess_input
import numpy as np
from PIL import Image
def show_features(img_path, model):
    img = load_img(img_path, target_size=(100, 100))
    img = img_to_array(img)
    img = expand_dims(img, axis=0)
    img = preprocess_input(img)
    features = []
    for layer_num in range(0, 6):
        layer_model = Model(inputs=model.inputs, outputs=model.layers[layer_num].output)
        feature_maps = layer_model.predict(img)
        for feature_map in feature_maps:
            feature_map_min = feature_map.min()
            feature_map_max = feature_map.max()
            for feature_num in range(3):                
                norm_feature_map = (feature_map - feature_map_min) / (feature_map_max - feature_map_min)
                features.append(norm_feature_map[:, :, feature_num].tolist())                
    return features



def show_features_pillow(img_path, model):
    img = load_img(img_path, target_size=(100, 100))
    img = img_to_array(img)
    img = expand_dims(img, axis=0)
    img = preprocess_input(img)
    images = []

    for layer_num in range(6):
        layer_model = Model(inputs=model.inputs, outputs=model.layers[layer_num].output)
        
        feature_maps = layer_model.predict(img)
        print("Drawing feature maps for layer", layer_num)
        for feature_map in feature_maps:
            r = feature_map[:, :, 0]
            c_min = r.min()
            c_max = r.max()
            r = (r - c_min) / (c_max - c_min)
            g = feature_map[:, :, 1]
            c_min = g.min()
            c_max = g.max()
            g = (g - c_min) / (c_max - c_min)
            b = feature_map[:, :, 2]
            c_min = b.min()
            c_max = b.max()
            b = (b - c_min) / (c_max - c_min)
            rgb = (np.dstack((r*255,g*255,b*255))).astype(np.uint8) 
            image = Image.fromarray(rgb)
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            data = base64.b64encode(img_byte_arr.getbuffer()).decode("ascii")
            images.append(f"data:image/png;base64,{data}")
    return images