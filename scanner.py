"""Initial photo file scan class."""

import os
import re

import constants as cn
from database import model
from PIL import Image, ExifTags



PHOTO_TYPE = ["jpg"]


def _from_exif_real(value):
	"""Gets value from EXIF REAL type = tuple(numerator, denominator)"""
	return value[0]/value[1]


def _guard_GPS()


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
	if tuples:
		return (pattern % tuple(_from_exif_real(l) for l in tuple_tag) +
			(string_tag,))
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

	def scan(self):
		"""Scans file information to Photo instances."""
		filters = [re.compile(flt) for flt in cn.FILE_PATTERN]
		for (dirpath, dirnames, filenames) in os.walk(self.path):
			for f in filenames:
				if any([re.search(flt, f) for flt in filters]):
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
		exif_real = {ExifTags.TAGS.get(k, ''): v for k, v in img._getexif().items()}
		exif_GPS = gps_lat = gps_long = gpa_altitude = gps_datetime = ''
		if 'GPSInfo' in exif_real:
			exif_GPS = {ExifTags.GPSTAGS[k]: v
			            for k, v in exif_phone['GPSInfo'].items()}
			gps_lat=(exif_GPS[EXIF_GPS_LATITUDE], exif_GPS[EXIF_GPS_LATITUDE_REF],
				"%d %d' %5.2f'' %s" , "0 0' 0.0'N"),
  		gps_long=(exif_GPS[EXIF_GPS_LONGITUDE],
  			exif_GPS[EXIF_GPS_LONGITUDE_REF],	"%d %d' %5.2f'' %s" , "0 0' 0.0'N")
  		gps_altitude=_from_exif_real(exif_GPS[EXIF_GPS_ALTITUDE])
  		gps_datetime=datetime.datetime.strptime('%s %d:%d:%d' % (
  			exif_GPS[cn.EXIF_GPS_DATE],) + tuple(
  			  _from_exif_real(l) for l in exif_GPS[cn.EXIF_GPS_TIME])),
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
  			white_balance=cn.WhiteBalance(exif_real[cn.EXIF_WHITE_BALANCE]).name,
  			camera=' '.join(exif_real[cn.EXIF_CAMERA_MAKE],
  				              exif_real[cn.EXIF_CAMERA_MODEL]),
  			camera_id=exif_real[cn.EXIF_CAMERA_ID],
    		lens_type=exif_real[cn.EXIF_LENS_MODEL],
  			lens_serial=exif_real[cn.EXIF_LENS_SERIAL_NUMBER],
  			gps_lat=gps_lat,
  			gps_long=gps_long,
  			gps_altitude=gps_altitude,
  			gps_datetime=gps_datetime,
  			comments='',
  			focal_length=_from_exif_real(exif_real[cn.EXIF_FOCAL_LENGTH]),
  )



