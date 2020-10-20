from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string

from base64 import b64decode


def get_image_from_str(image):	
	_, img_str = image.split('base64,')
	image_extension = _.split('/')[-1].split(';')[0]
	img_base64 = b64decode(img_str)
	image_b = ContentFile(img_base64)
	image_b.name = get_random_string(length=6) + '.' + image_extension
	return image_b