"""File storage support."""

from collections import defaultdict
import datetime
import os
import re

import flickrapi

import constants as cn
from database import model


class FlickrStorage(object):
  """Gets/Stores initial information from photo files in Flickr.

  Scans starting from root path recursively for all files defined as PHOTO_TYPE
  """
  
  def __init__(self):
    flickr_file = os.path.join(os.path.dirname(__file__), cn.FLICKR_FILE)
    with open(flickr_file, 'r') as f:
      api_key = f.readline().replace('\n', '')
      api_secret = f.readline().replace('\n', '')
    self.flickr = flickrapi.FlickrAPI(api_key, api_secret)
    self.user_id = self.flickr.people.findByUserName(
      username=cn.FLICKR_USERNAME, format='parsed-json')['user']['nsid']
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
    import pdb
    pdb.set_trace()
    json_result = []
    response = self.flickr.photos.search(user_id=self.user_id,
      min_taken_date='2018-11-16', format='parsed-json')
    json_result.extend(response['photos']['photo'])
    for page in range(2, response['photos']['pages'] + 1):
      response = self.flickr.photos.search(user_id=self.user_id,
      min_taken_date='2018-11-16', format='parsed-json', page=page)
      json_result.extend(response['photos']['photo'])


  def store(self, photo_file, new_path):
    """Stores photo file into path into storage.

    Args:
      photo_file: str, path to photo file
      new_path: str, path in storage to copy photo_file
    """
    raise NotImplementedError
