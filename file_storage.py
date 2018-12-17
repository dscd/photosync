"""Initial photo file scan class."""

from collections import defaultdict
import datetime
import os
import re

import constants as cn
from database import model
from PIL import Image, ExifTags


PHOTO_TYPE = ["jpg"]


def _from_exif_real(value):
	"""Gets value from EXIF REAL type = tuple(numerator, denominator)"""
	return value[0]/value[1]


def _from_GPS(tuple_tag, string_tag, pattern, default):
	"""Gets information from GPS tuples and formats it according to pattern given

	Args:
	  tuple_tag: tag in GPS_TAGS containing tuple of tuples to format, or None.
	  string_tag: tag in GPS_TAGS containing string information.
	  pattern: str, pattern in %-format to format incoming tuples.
	  default: returned if tuples is None,

	Return:
	  str: formatted string or default if tuple is None
	"""
	if tuple_tag:
		return (pattern % (tuple(_from_exif_real(l) for l in tuple_tag) +
			(string_tag,)))
	return default


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
		self._photos_index = 0

	def __getitem__(self, idx):
		"""Gets photo item."""
		return self._photos[idx]

	def __iter__(self):
		"""Iterating over photos list."""
		return self

	def __next__(self):
		try:
			result = self._photos[self._photos_index]
		except IndexError:
			raise StopIteration
		self._photos_index += 1
		return result

	def __len__(self):
		return len(self._photos)

	def scan(self):
		"""Scans file information to Photo instances."""
		filters = [re.compile(flt) for flt in cn.FILE_PATTERN]
		for (dirpath, dirnames, filenames) in os.walk(self.path):
			for f in filenames:
				if any([re.search(flt, f) for flt in filters]):
					self._photos.append(self._scan_file(os.path.join(dirpath, f)))

	def _scan_file(self, filename):
		"""Make a photo object from a file.

		Args:
		  filename: str, file name
		Returns:
		  Photo object
		"""
		img = Image.open(filename)
		exif_real = defaultdict(str)
		# Get EXIF tags
		for k, v in img._getexif().items():
			exif_real[ExifTags.TAGS.get(k, '')] = v
		exif_GPS = gps_lat = gps_long = gps_altitude = gps_datetime = ''
		# Get GPS tags if available
		if 'GPSInfo' in exif_real:
			exif_GPS = {ExifTags.GPSTAGS[k]: v
			            for k, v in exif_real['GPSInfo'].items()}
			gps_lat = _from_GPS(exif_GPS[cn.EXIF_GPS_LATITUDE],
				exif_GPS[cn.EXIF_GPS_LATITUDE_REF],	"%d %d' %5.2f''%s" , "0 0' 0.0'N")
			gps_long = _from_GPS(exif_GPS[cn.EXIF_GPS_LONGITUDE],
  			exif_GPS[cn.EXIF_GPS_LONGITUDE_REF], "%d %d' %5.2f''%s" , "0 0' 0.0'W")
			gps_altitude = _from_exif_real(exif_GPS[cn.EXIF_GPS_ALTITUDE])
			gps_datetime = datetime.datetime.strptime('%s %d:%d:%d' % ((
  			exif_GPS[cn.EXIF_GPS_DATE],) + tuple(
  			  _from_exif_real(l) for l in exif_GPS[cn.EXIF_GPS_TIME])),
			  cn.EXIF_DATE_FORMAT)
		# Creating a photo model
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
		  exposure_mode=cn.ExposureMode(exif_real[cn.EXIF_EXPOSURE_MODE]).name,
			white_balance=cn.WhiteBalance(exif_real[cn.EXIF_WHITE_BALANCE]).name,
			camera=' '.join([exif_real[cn.EXIF_CAMERA_MAKE],
				              exif_real[cn.EXIF_CAMERA_MODEL]]),
			camera_id=exif_real[cn.EXIF_CAMERA_ID],
  		lens_type=exif_real[cn.EXIF_LENS_MODEL],
			lens_serial=exif_real[cn.EXIF_LENS_SERIAL_NUMBER],
			gps_lat=gps_lat,
			gps_long=gps_long,
			gps_alt=gps_altitude,
			gps_datetime=gps_datetime,
			comments='',
			focal_length=_from_exif_real(exif_real[cn.EXIF_FOCAL_LENGTH]),
    )
