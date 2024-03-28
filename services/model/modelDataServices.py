from database.engine import getSession
from models.model import Model

class ModelDataService:

    def getModels():
        with getSession() as session:
            return session.query(Model).all()

    def getModelByName(modelName):
        with getSession() as session:
            return session.query(Model).filter(Model.model_name == modelName).first()
        
    def deleteModel(model):
        with getSession() as session:
            session.delete(model)
            session.commit()
