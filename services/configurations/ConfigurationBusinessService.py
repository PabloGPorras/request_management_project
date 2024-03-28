import json
from services.configurations.ConfigurationDataService import ConfigurationsDataService

class ConfigurationBusinessService:
    def getConfiguration():
        configuration = ConfigurationsDataService.getConfiguration()
        if configuration is not None:
            return json.loads(configuration.json)
        else:
            # Handle the case where configuration is None
            # For example, you might want to return an empty dictionary, log an error, raise an exception, etc.
            return {"tool_version":["1"] }