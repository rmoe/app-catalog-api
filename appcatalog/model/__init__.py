from pecan import conf  # noqa
from pecan import conf  # noqa
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Session = scoped_session(sessionmaker())
metadata = MetaData()

Base = declarative_base()
Base.query = Session.query_property()

def _engine_from_config(configuration):
    configuration = dict(configuration)
    url = configuration.pop('url')
    return create_engine(url, **configuration)

def init_model():
    conf.sqlalchemy.engine = _engine_from_config(conf.sqlalchemy)
    create_db()


def create_db():
    import appcatalog.model.models
    Base.metadata.create_all(bind=conf.sqlalchemy.engine)

def drop_db():
    import appcatalog.model.models
    Base.metadata.drop_all(bind=conf.sqlalchemy.engine)


def start():
    Session.bind = conf.sqlalchemy.engine
    metadata.bind = Session.bind

def commit():
    Session.commit()

def rollback():
    Session.rollback()

def clear():
    Session.remove()
