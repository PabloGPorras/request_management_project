import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.configuration import Configuration
from models.user import User
from models.model import Model
from utils.utils import Base

userName = str(os.getlogin()).upper()

engine = create_engine('sqlite:///database.db',echo=False)
engine.connect()

try:
    Base.metadata.create_all(engine)
    # Explicitly commit changes
    session = Session(bind=engine)
    session.commit()
    print("Tables created successfully!")
except Exception as e:
    print("An error occurred during table creation:", e)

def getEngine():
    return engine

def getSession() -> Session:
    return Session(bind=engine)




