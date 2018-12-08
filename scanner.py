"""Initial photo file scan class."""

import os

import constants as cn
from database import model
from PIL import Image, ExifTags



PHOTO_TYPE = ["jpg"]


def _from_exif_real(value):
	"""Gets value from EXIF REAL type = tuple(numerator, denominator)"""
	return value[0]/value[1]*1.0  # To avoid returning integer


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
		exif_real = {ExifTags.TAGS.get(k, k): v for k, v in img._getexif().items()}
    return model.Photo(
    	  name=filename,
  		  width=img.width,
  	  	height=img.height,
  	  	date_original=datetime.datetime.strptime(
  	  		exif_real[cn.EXIF_DATE_ORIGINAL], cn.EXIF_DATE_FORMAT),
  			aperture=_from_exif_real(exif_real[cn.EXIF_APERTURE]),
  		  shutter=_from_exif_real(exif_real[cn.EXIF_SHUTTER]),
  	  	iso=exif_real[cn.EXIF_ISO],
  			metering_mode=cn.MeteringMode(exif_real[cn.EXIF_METERING_MODE]).name,
  		  exposure_mode=cn.ExposureMode(exif_real[cn.EXIF_EXPOSIRE_MODE]).name,
  # # White balance
  # white_balance = Column(String)
  # # Camera model
  # camera = Column(String)
  # # Camera id
  # camera_id = Column(String)
  # # Lens type
  # lens_type = Column(String)
  # # Lens serial no
  # lens_serial = Column(String)
  # # GPS Latitude
  # gps_lat = Column(String)
  # # GPS longitude
  # gps_long = Column(String)
  # # comments
  # comments = Column(String)
  # # thumbnail
  # thumbnail = Column(LargeBinary)
  )



