import requests
from pecan import core
from pecan import conf
from appcatalog.model import models
from sqlalchemy.orm import scoped_session, sessionmaker

URL = 'http://apps.openstack.org/api/v1/assets'
core.load_app('config.py')
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=True,
                                 bind=conf.sqlalchemy.engine))
def import_data():
    data = fetch_from_api(URL)
    for app in data['assets']:
        app_db = models.App(
            name=app['name'],
            description=app['description'],
            attributes=create_attrs(app),
            provider_id=get_or_create(models.Provider, **app['provided_by']).id,
            license_id=get_or_create(
                models.License,
                name=app['license'],
                url=app.get('license_url')
            ).id,
            service_id=get_or_create(models.Service, **app['service']).id,
        )
        if 'icon' in app:
            app_db.icon_id = get_or_create(models.Icon, **app['icon']).id

        for tag in app.get('tags', []):
            t = get_or_create(models.Tag, name=tag)
            app_db.tags.append(t)

        for release in app.get('release', []):
            r = get_or_create(models.Release, release=release)
            app_db.releases.append(r)

        db.add(app_db)
    db.commit()

def get_or_create(model, **data):
    existing_obj = db.query(model).filter_by(**data).first()

    if not existing_obj:
        existing_obj = model(**data)
        db.add(existing_obj)
        db.commit()

    return existing_obj

def create_attrs(app):
    attrs = []
    for key, value in app.get('attributes', {}).items():
        attr_db = models.Attribute(
            key=key,
            value=value
        )
        db.add(attr_db)
        attrs.append(attr_db)

    db.commit()
    return attrs

def fetch_from_api(url):
    resp = requests.get(url)
    return resp.json()

if __name__ == "__main__":
    import_data()
