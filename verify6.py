import tesserocr
from PIL import Image
import numpy as np

# image = Image.open('captcha2.png')
image = Image.open('dl.png')
image = image.convert('L')
threshold = 150
array = np.array(image)
array = np.where(array > threshold, 255, 0)
image = Image.fromarray(array.astype('uint8'))
print(tesserocr.image_to_text(image))
