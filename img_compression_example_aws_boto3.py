import os, io, sys, boto3

sys.path.append('..')
from config.config_read import config_read
from pathlib import Path
import PIL #pip install Pillow
from PIL import Image
from io import BytesIO


# Configuration
config       = {'endpoint_url'          : config_read('wasabi_endpoint'),
                'aws_access_key_id'     : config_read('wasabi_access_key'),
                'aws_secret_access_key' : config_read('wasabi_secret_key')}


bucket=config_read('wasabi_bucket')
prefix = f'imgs/43/'
compressed_prefix = f'imgs/compressed_43/'

s3 = boto3.client('s3', **config)
result = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

def convertToJpeg(im):
    with BytesIO() as f:
        im.save(f, format='JPEG')
        return f.getvalue()

for n, i in enumerate(result.get('Contents')):
    if i['Key'] == prefix: continue 
    data = s3.get_object(Bucket=bucket, Key=i.get('Key'))
    image_data = data['Body'].read()
    img = Image.open(io.BytesIO(image_data))

    print(sys.getsizeof(img))
    w, h = img.size
    compressed_img = img.resize((w,h), PIL.Image.ANTIALIAS)
    compressed_img = convertToJpeg(compressed_img)
    print(sys.getsizeof(compressed_img))
    upload_path = Path(compressed_prefix, i['Key'].replace(prefix, ''))

    print('from: ', i['Key'])
    print('to: ', upload_path)

    response    = s3.put_object(Body   = compressed_img,
                                       Bucket = config_read('wasabi_bucket'),
                                       Key    = str(upload_path),
                                       ACL    = 'public-read')



