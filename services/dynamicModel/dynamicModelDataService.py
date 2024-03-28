from database.engine import getSession
from models.modelBuilder import ModelBuilder
from services.model.modelDataServices import ModelDataService

class DynamicModelDataService:

    def getDynamicModelItems(model):
        modelBuilder = ModelBuilder()
        DynamicModel = modelBuilder.createModel(model)
        with getSession() as session:
            query = session.query(DynamicModel)
            return {
                "rows": query.all(),
                "columns": [column["name"] for column in query.column_descriptions]
            }

        # Validate the bad data before inserting
        validated_data = model_builder.validate_data(user_table, bad_data)
        query = user_table.insert().values(bad_data)
        with engine.connect() as connection:
            result = connection.execute(query)