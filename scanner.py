"""Initial photo file scan class."""

import os

from database import model
from PIL import Image, ExifTags



PHOTO_TYPE = ["jpg"]

class Scanner(object):
	"""Scans initial information from photo files.

	Scans starting from root path recursively for all files defined as PHOTO_TYPE

	Args:
	  path: str, root path to scan photo files
	"""
	
	def __init__(self, path):
		if not os.path.isdir(path):
			raise ValueError("{path} is not directory".format(path=path))
		self.path = path
		self._photos = []

	def scan(self):
		"""Scans file information to Photo instances."""
		for (dirpath, dirnames, filenames) in os.walk(self.path):
			for f in filenames:
				self._photos.append(self._scan_file(
						os.path.join(self.path, dirpath, f)))

	def _scan_file(self, filename):
		"""Make a photo object from a file.

		Args:
		  filename: str, file name
		Returns:
		  Photo object
		"""
		exifData = {}
		img = Image.open(filename)
		exifDataRaw = img._getexif()
		for tag, value in exifDataRaw.items():
    	decodedTag = ExifTags.TAGS.get(tag, tag)
    	exifData[decodedTag] = value
    return model.Photo()



