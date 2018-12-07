# Database ORM descriptor for photo sync.

from sqlalchemy import Column, Integer, String, DateTime, Float, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class to_dict_mixin(object):

  def columns_to_dict(self):
    dict_ = {}
    for key in self.__mapper__.c.keys():
        dict_[key] = getattr(self, key)
    return dict_


class Photo(Base, to_dict_mixin):
  """photo table."""
  __tablename__ = 'photo'

  # Photo id 
  id = Column(Integer, primary_key=True)
  # Photo name
  name = Column(String)
  # Photo width, pixels
  width = Column(Integer)
  # Photo height, pixels
  height = Column(Integer)
  # Date when photo has been taken
  date_original = Column(DateTime)
  # Aperture, F number (2.0 means f/2.0)
  aperture = Column(Float) 
  # Shutter (s, 1/250 means 1/250s)
  shutter = Column(Float) 
  # ISO (ISO sensitivity)
  iso = Column(Integer)  
  # Metering mode
  metering_mode = Column(String)
  # Exposure mode
  exposure_mode = Column(String)
  # White balance
  white_balance = Column(String)
  # Camera model
  camera = Column(String)
  # Camera id
  camera_id = Column(String)
  # Lens type
  lens_type = Column(String)
  # Lens serial no
  lens_serial = Column(String)
  # GPS Latitude
  gps_lat = Column(String)
  # GPS longitude
  gps_long = Column(String)
  # comments
  comments = Column(String)
  # thumbnail
  thumbnail = Column(LargeBinary)

  locations = relationship("Location")

  def __repr__(self):
    return "<Photo(name='%s', id=%d, date_original='%s')>" % (
      self.name, self.id, self.date_original)



class Backup(Base, to_dict_mixin):
  """backup table - list of backups."""
  __tablename__ = 'backup'

  # backup id
  id = Column(Integer, primary_key=True)
  # name of backup
  name = Column(String)
  # description
  description = Column(String)

  def __repr__(self):
    return "<Backup(name='%s', id=%d, description='%s')>" % (
      self.name, self.id, self.description)

  #photos = relationship("Location", back_populates="backup")


class Location(Base, to_dict_mixin):
  """location table - multible locations of one photo."""
  __tablename__ = 'location'

  # Photo id
  photo_id = Column(Integer, ForeignKey('photo.id'), primary_key=True)
  # Backup id
  backup_id = Column(Integer, ForeignKey('backup.id'), primary_key=True)
  # Path on location
  path = Column(String)

  backup = relationship("Backup")

  def __repr__(self):
    return "<Location(path='%s', photo_id=%d, backup_id=%d)>" % (
      self.path, self.photo_id, self.backup_id)

  # photo = relationship("photo", back_populates="backups")
  # backup = relationship("backup", back_populates="photos")




