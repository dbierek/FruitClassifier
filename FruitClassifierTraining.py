import os
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def get_class_names():
    class_names = os.listdir(os.path.join('static/fruit/', 'test'))
    class_names.sort()
    return class_names

def build_model(class_names):
    img_input = layers.Input(shape=(100, 100, 3))
    x = layers.Conv2D(16, 3, activation='relu')(img_input)
    x = layers.MaxPooling2D(2)(x)
    x = layers.Conv2D(32, 3, activation='relu')(x)
    x = layers.MaxPooling2D(2)(x)
    x = layers.Conv2D(64, 3, activation='relu')(x)
    x = layers.MaxPooling2D(2)(x)
    x = layers.Flatten()(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.7)(x)
    output = layers.Dense(len(class_names), activation='softmax')(x)
    model = Model(img_input, output)
    model.summary()
    model.compile(optimizer='adam',
                loss=tf.keras.losses.CategoricalCrossentropy(),
                metrics=['accuracy'])
    return model

def get_file_names():
    test_inorder_generator = ImageDataGenerator(rescale=1.0 / 255).flow_from_directory(
        os.path.join(os.path.join('static/', 'fruit/'), 'test'),
        target_size=(100, 100),
        batch_size=20,
        shuffle=False)
    return test_inorder_generator.filenames

def get_train_generator():
    return ImageDataGenerator(
        rescale=1.0 / 255,
        horizontal_flip=True).flow_from_directory(
        os.path.join(os.path.join('static/', 'fruit/'), 'train'),
        target_size=(100, 100), 
        batch_size=100)

def get_test_generator():
    return ImageDataGenerator(rescale=1.0 / 255).flow_from_directory(
        os.path.join(os.path.join('static/', 'fruit/'), 'test'),
    target_size=(100, 100),
    batch_size=60)

def train_model(epochs):
    print("Beginning fit of the model: This could take around 15 minutes to fully train.")
    model = build_model(get_class_names())
    history = model.fit(
        get_train_generator(),
        steps_per_epoch=100,
        epochs=epochs,
        validation_data=get_test_generator(),
        validation_steps=50,  
        verbose=2)
    model.save('savedModel')
    return model, history
if __name__ == "__main__":
    train_model(4)