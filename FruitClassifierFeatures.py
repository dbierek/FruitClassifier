from tensorflow.keras import Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow import expand_dims
from tensorflow.keras.applications.resnet import preprocess_input
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

#         for feature_map in feature_maps:
#             feature_num = 1
#             for _ in range(features_to_show):
#                 # Create a subplot for this feature map
#                 subplot = plt.subplot(1, 4, feature_num)
#                 subplot.set_xticks([])
#                 subplot.set_yticks([])
#                 # Show this feature map
#                 image = subplot.imshow(feature_map[:, :, feature_num - 2])
