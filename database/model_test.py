"""Testing model class."""

import datetime
import sqlite3
import unittest

import sqlalchemy

import model

PHOTOS = [
    {'id': 123,
     'name': 'photo1',
     'width': 640,
     'height': 480,
     'date_original': datetime.datetime(2018, 1, 1, 15,0,0),
     'aperture': 2.0,
     'shutter': 1/250.0,
     'iso': 100,
     'metering_mode': 'normal',
     'exposure_mode': 'center weight',
     'white_balance': 'daylight',
     'camera': 'Canon EOS 80D',
     'camera_id': '123ABC',
     'lens_type': 'EF-S 18-135',
     'lens_serial': '234ZXC',
     'gps_lat': '37.12345',
     'gps_long': '122.23456',
     'comments': 'comment1',
     'thumbnail': b'abcdef\x02\x03'},
    {'id': 234,
     'name': 'photo2',
     'width': 640,
     'height': 480,
     'date_original': datetime.datetime(2018, 1, 1, 15,0,2),
     'aperture': 2.8,
     'shutter': 1/100.0,
     'iso': 100,
     'metering_mode': 'normal',
     'exposure_mode': 'center weight',
     'white_balance': 'daylight',
     'camera': 'Canon EOS 70D',
     'camera_id': '123C',
     'lens_type': 'EF-S 18-135',
     'lens_serial': '234ABC',
     'gps_lat': '37.12345',
     'gps_long': '122.23456',
     'comments': 'comment1',
     'thumbnail': b'abcdef\x02\x03'},
    {'id': 345,
     'name': 'photo3',
     'width': 1024,
     'height': 768,
     'date_original': datetime.datetime(2018, 1, 2, 11,0,0),
     'aperture': 13.0,
     'shutter': 1/5.0,
     'iso': 1600,
     'metering_mode': 'normal',
     'exposure_mode': 'center weight',
     'white_balance': 'tungsten',
     'camera': 'Canon EOS 80D',
     'camera_id': '123ABC',
     'lens_type': 'EF-S 18-135',
     'lens_serial': '234ZXC',
     'gps_lat': '37.12345',
     'gps_long': '122.23456',
     'comments': 'comment2',
     'thumbnail': b'abcdefrf\x02\x03'},
]
BACKUPS = [
    {'id': 1,
     'name': 'local',
     'description': 'local storage'},
    {'id': 2,
     'name': 'flickr',
     'description': 'Flickr remote storage'},
    {'id': 3,
     'name': 'hdd',
     'description': 'hdd backup'},
]
LOCATIONS = [
    {'photo_id': 123,
     'backup_id': 1,
     'path': '/some/path/photo1'},
    {'photo_id': 123,
     'backup_id': 2,
     'path': 'http://some/path/photo1'},
    {'photo_id': 123,
     'backup_id': 3,
     'path': '/some/path/photo1'},
    {'photo_id': 234,
     'backup_id': 1,
     'path': '/some/path/photo2'},
    {'photo_id': 234,
     'backup_id': 3,
     'path': '/some/path/photo2'},
    {'photo_id': 345,
     'backup_id': 1,
     'path': 'http://some/path/photo3'},
]

engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)
session_factory = sqlalchemy.orm.sessionmaker(bind=engine)


class ModelTest(unittest.TestCase):
 
  def setUp(self):
    self.connection = engine.connect()
    self.trans = self.connection.begin()
    
    model.Base.metadata.create_all(engine)
    self.session = session_factory()
    # self.session.begin_nested()
    # import pdb
    # pdb.set_trace()
    self._create_db()

  def tearDown(self):
    self.session.close()
    model.Base.metadata.drop_all(engine)
    self.trans.rollback()
    self.connection.close()

  def _create_db(self):
    """Creates database."""    
    self.photos = {}
    self.backups = {}
    for backup in BACKUPS:
      self.backups[backup['id']] = model.Backup(**backup)
    for photo in PHOTOS:
      self.photos[photo['id']] = model.Photo(**photo)
    for location in LOCATIONS:
      l = model.Location(path=location['path'])
      l.backup = self.backups[location['backup_id']]
      self.photos[location['photo_id']].locations.append(l)
    for id_, photo in self.photos.items():
      self.session.add(photo)
    self.session.commit()
    
  def test_model_select_all(self):
    """Model select all testing."""
    self.assertListEqual(PHOTOS,
        [s.columns_to_dict() for s in self.session.query(model.Photo).all()])

  def test_model_insert(self):
    """Model insert testing."""
    new_photo = model.Photo(
        id=3,
        name='photo4',
        width=640,
        height=480,
        date_original=datetime.datetime(2018, 1, 1, 15,0,2),
        aperture=2.8,
        shutter=1/100.0,
        iso=200,
        metering_mode='normal',
        exposure_mode='center weight',
        white_balance='daylight',
        camera='Canon EOS 70D',
        camera_id='123ABCDEF',
        lens_type='EF-S 70-200',
        lens_serial='234FDC',
        gps_lat='37.12345',
        gps_long='122.23456',
        comments='comment1',
        thumbnail=b'abcdef\x00\x01')
    self.session.add(new_photo)
    self.session.commit()
    self.assertEqual(new_photo, self.session.query(model.Photo).filter(
        model.Photo.name == new_photo.name).one())

  def test_model_select_some(self):
    """Model select certain records testing."""
    self.assertEqual(PHOTOS[0], self.session.query(
        model.Photo).filter_by(aperture=2.0).one().columns_to_dict())

  def test_model_delete_successful(self):
    """Model successful delete records testing."""
    self.session.delete(self.backups[2])
    self.session.commit()
    self.assertEqual(2, self.session.query(model.Backup).count())

  def test_model_delete_constaint(self):
    """Model unsuccessful delete records testing."""
    # Deletion tries to black primary key in Location table
    with self.assertRaises(AssertionError):
        self.session.delete(self.photos[234])
        self.session.commit()
    


if __name__ == '__main__':
  unittest.main()
