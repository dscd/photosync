"""Constants used in the whole project."""

from enum import Enum

# Date format in photo files EXIF
EXIF_DATE_FORMAT = '%Y:%m:%d %H:%M:%S'

# EXIF tags names
EXIF_DATE_ORIGINAL = 'DateTimeOriginal'
EXIF_APERTURE = 'FNumber'
EXIF_SHUTTER = 'ExposureTime'
EXIF_ISO = 'IsoSpeedRatings'
EXIF_METERING_MODE = 'MeteringMode'
EXIF_EXPOSIRE_MODE = 'ExposureMode'


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
  """Exposire mode"""
  AUTO = 0
  MANUAL = 1
  AUTOBRACKET = 2

