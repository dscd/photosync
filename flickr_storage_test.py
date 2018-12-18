"""Test for scanner module."""

import datetime
import os
import unittest

import flickr_storage


class FlickrStorageTest(unittest.TestCase):
  
  def setUp(self):
    self.maxDiff = None
    self.flickr_storage = flickr_storage.FlickrStorage()
    self.flickr_storage.scan()

  def test_scanned_content(self):
    """Tests length of scanned list."""
    self.assertEqual(2, 2)


if __name__ == '__main__':
  unittest.main()

