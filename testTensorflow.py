import tensorflow as tf
import mediapipe as mp
import cv2
import numpy as np
from PIL import Image
import tensorflow as tf

print("TensorFlow 版本:", tf.__version__)
print("可用 GPU:", tf.config.list_physical_devices('GPU'))
print("TensorFlow:", tf.__version__)
print("Mediapipe:", mp.__version__)
print("OpenCV:", cv2.__version__)