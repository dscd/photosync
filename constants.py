"""Constants used in the whole project."""

from enum import Enum

# File search pattern, list of regexps
FILE_PATTERN = ['.*jpg$']

# Date format in photo files EXIF
EXIF_DATE_FORMAT = '%Y:%m:%d %H:%M:%S'

# EXIF tags names
EXIF_DATE_ORIGINAL = 'DateTimeOriginal'
EXIF_APERTURE = 'FNumber'
EXIF_SHUTTER = 'ExposureTime'
EXIF_ISO = 'IsoSpeedRatings'
EXIF_METERING_MODE = 'MeteringMode'
EXIF_EXPOSURE_MODE = 'ExposureMode'
EXIF_WHITE_BALANCE = 'WhiteBalance'
EXIF_CAMERA_MAKE = 'Make'
EXIF_CAMERA_MODEL = 'Model'
EXIF_CAMERA_ID = 'BodySerialNumber'
EXIF_LENS_MODEL = 'LensModel'
EXIF_LENS_SERIAL_NUMBER = 'LensSerialNumber'
EXIF_GPS_LATITUDE = 'GPSLatitude'
EXIF_GPS_LATITUDE_REF = 'GPSLatitudeRef'
EXIF_GPS_LONGITUDE = 'GPSLongitude'
EXIF_GPS_LONGITUDE_REF = 'GPSLongitude'
EXIF_GPS_ALTITUDE = 'GPSAltitude'
EXIF_GPS_DATE = 'GPSDateStamp'
EXIF_GPS_TIME = 'GPSTimeStamp'


#Enums
class MeteringMode(Enum):
  """Metering mode."""
  UNKNOWN = 0
  AVERAGE = 1
  CENTERWEIGHTEDAVERAGE = 2
  SPOT = 3
  MULTISPOT = 4
  PATTERN = 5
  PARTIAL = 6
  OTHER = 255


class ExposureMode(Enum):
  """Exposure mode"""
  AUTO = 0
  MANUAL = 1
  AUTOBRACKET = 2


class WhiteBalance(Enum):
  """White Balace"""
  AUTO = 0
  MANUAL = 1
