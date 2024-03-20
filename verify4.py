import tesserocr
from PIL import Image

choice = 2

if 1 == choice:
    image = Image.open('captcha2.png')
    result = tesserocr.image_to_text(image)
    print(result)
elif 2 == choice:
    print(tesserocr.file_to_text('captcha2.png'))
else:
    pass
