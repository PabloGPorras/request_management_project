

from database.engine import getSession
from models.configuration import Configuration


class ConfigurationsDataService:

    def getConfiguration():
        with getSession() as session:
            return session.query(Configuration).first()
        
    def updateConfigurations(self, configuration):
        return self.db.update_configurations(configuration)