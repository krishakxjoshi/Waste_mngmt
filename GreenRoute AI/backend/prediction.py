import tensorflow as tf
import numpy as np
from PIL import Image

MODEL_PATH = "model.h5"

model = tf.keras.models.load_model(MODEL_PATH)

def preprocess_image(image_bytes):

    img = Image.open(image_bytes).convert("RGB")
    img = img.resize((64,64))

    img = np.array(img)/255.0
    img = np.expand_dims(img, axis=0)

    return img


def predict(image_bytes):

    img = preprocess_image(image_bytes)

    pred = model.predict(img)[0][0]

    label = "Non Biodegradable" if pred > 0.5 else "Biodegradable"

    confidence = float(pred if pred>0.5 else 1-pred)

    return label, confidence