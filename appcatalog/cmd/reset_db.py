import pecan
from pecan import conf
from appcatalog.model import Base
import appcatalog.model.models

class GetCommand(pecan.commands.BaseCommand):
    """
    Drop and recreate all database tables
    """

    def run(self, args):
        super(GetCommand, self).run(args)
        self.load_app()
        Base.metadata.drop_all(bind=conf.sqlalchemy.engine)
        Base.metadata.create_all(bind=conf.sqlalchemy.engine)
