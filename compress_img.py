import PIL
from PIL import Image
import os

filename = 'img.jpg'

def compress_img(filename):
    img = Image.open(filename)
    w, h = img.size
    img = img.resize((w,h), PIL.Image.ANTIALIAS)
    new_filename = 'compressed_'+filename
    img.save(new_filename)
    before  = os.path.getsize(filename)
    after   = os.path.getsize(new_filename)
    savings = (before - after) / before
    return (f'reduced_by: {round(savings*100,2)}%')



print(compress_img(filename))
