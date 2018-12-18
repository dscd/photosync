"""Test for scanner module."""

import datetime
import os
import unittest

import file_storage

PHOTOS = [{
    'id': None,
    'white_balance': 'AUTO',
    'metering_mode': 'CENTERWEIGHTEDAVERAGE',
    'lens_serial': '',
    'iso': '',
    'name': 'testdata/image_camera.jpg',
    'gps_datetime': datetime.datetime(2018, 12, 1, 18, 23, 53),
    'lens_type': '',
    'focal_length': 5.5,
    'height': 388,
    'aperture': 2.6,
    'camera': 'OnePlus ONEPLUS A5000',
    'camera_id': '',
    'date_original': datetime.datetime(2018, 12, 1, 10, 23, 53),
    'gps_long': "121 59'  1.89''W",
    'comments': '',
    'width': 518,
    'shutter': 0.0013477088948787063,
    'gps_lat': "37 13' 20.50''N",
    'exposure_mode': 'AUTO',
    'gps_alt': 80.485 },
    {
     'shutter': 0.0125,
     'exposure_mode': 'AUTO',
     'camera': 'Canon Canon EOS 80D',
     'width': 600,
     'camera_id': '',
     'height': 400,
     'gps_lat': '',
     'gps_alt': '',
     'comments': '',
     'date_original': datetime.datetime(2018, 11, 23, 14, 51, 2),
     'id': None,
     'metering_mode': 'PATTERN',
     'iso': '',
     'aperture': 8.0,
     'focal_length': 56.0,
     'name': 'testdata/dir1/image_phone.jpg',
     'gps_datetime': '',
     'lens_serial': '',
     'lens_type': '',
     'white_balance': 'AUTO',
     'gps_long': ''}
    ]


class FileStorageTest(unittest.TestCase):
  
  def setUp(self):
    self.maxDiff = None
    self.test_dir = os.path.join(os.path.dirname(__file__), 'testdata')
    self.file_storage = file_storage.FileStorage(self.test_dir)
    self.file_storage.scan()

  def test_scanned_len(self):
    """Tests length of scanned list."""
    self.assertEqual(2, len(self.file_storage))

  def test_scanned_content(self):
    """Tests length of scanned list."""
    model_dicts = [x.columns_to_dict() for x in self.file_storage]
    for m in model_dicts:
      m['name'] = os.path.relpath(m['name'])
    self.assertEqual(PHOTOS, model_dicts)


if __name__ == '__main__':
  unittest.main()

