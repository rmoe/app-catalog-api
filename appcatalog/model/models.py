from appcatalog.model import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Unicode
from sqlalchemy import UniqueConstraint
from sqlalchemy import types
from sqlalchemy.orm import relationship, backref


RELEASES = (
    'Icehouse',
    'Juno',
    'Kilo'
)

tag_assoc_table = Table('app_tags', Base.metadata,
    Column('app_id', Integer, ForeignKey('apps.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

release_assoc_table = Table('app_releases', Base.metadata,
    Column('app_id', Integer, ForeignKey('apps.id')),
    Column('release_id', Integer, ForeignKey('releases.id'))
)

class App(Base):
    __tablename__ = 'apps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255))
    description = Column(Text)
    provider_id = Column(Integer, ForeignKey('providers.id'))
    service_id = Column(Integer, ForeignKey('services.id', ondelete='CASCADE'))
    license_id = Column(Integer, ForeignKey('licenses.id'))
    icon_id = Column(Integer, ForeignKey('icons.id'))
    release = Column(Unicode(255))
    tags = relationship('Tag',
        secondary=tag_assoc_table,
        backref='apps'
    )
    releases = relationship('Release',
        secondary=release_assoc_table,
        backref='apps'
    )

class Provider(Base):
    __tablename__ = 'providers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255))
    href = Column(Unicode(255))
    company = Column(Unicode(255))
    apps = relationship('App')

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Unicode(255))
    format = Column(Unicode(255))
    environment = Column(Text)
    disk_type = Column(Unicode(255))
    disk_format = Column(Unicode(255))
    min_ram = Column(Integer)
    min_disk = Column(Integer)
    container_format = Column(Unicode(255))
    package_name = Column(Unicode(255))
    murano_package_name = Column(Unicode(255))


class License(Base):
    __tablename__ = 'licenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255))
    url = Column(Unicode(255))
    apps = relationship('App')

class Attribute(Base):
    __tablename__ = 'attributes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(Unicode(255))
    value = Column(Unicode(255))
    app_id = Column(Integer, ForeignKey('apps.id'))
    app = relationship('App', backref='attributes')

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255))

class Icon(Base):
    __tablename__ = 'icons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255))
    top = Column(Integer)
    left = Column(Integer)
    height = Column(Integer)

class Release(Base):
    __tablename__ = 'releases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    release = Column(Enum(*RELEASES, name='release'))
