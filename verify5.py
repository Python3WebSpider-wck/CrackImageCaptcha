import tesserocr
from PIL import Image
import numpy as np

image = Image.open('captcha2.png')
print(np.array(image).shape)
print(image.mode)
