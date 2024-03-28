from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,QTextEdit

# Define SQLAlchemy model for storing model JSON data in the database
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ModelJSON(Base):
    __tablename__ = 'model_json'

    id = Column(Integer, primary_key=True)
    json_data = Column(Text)

# Modify ModelBuilder to fetch model JSON data from the database
class ModelBuilder:
    def __init__(self, session):
        self.session = session

    def fetch_model_json(self):
        # Query the database to fetch the model JSON data
        model_json = self.session.query(ModelJSON).first()
        return model_json.json_data if model_json else None

# Modify AdminWidget to allow editing of model JSON data
class AdminWidget(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session

        self.layout = QVBoxLayout(self)

        self.json_editor = QTextEdit()
        self.layout.addWidget(self.json_editor)

        self.save_button = QPushButton("Save JSON")
        self.save_button.clicked.connect(self.save_json)
        self.layout.addWidget(self.save_button)

    def save_json(self):
        # Get the JSON data from the editor
        json_data = self.json_editor.toPlainText()

        # Save the JSON data to the database
        model_json = self.session.query(ModelJSON).first()
        if model_json:
            model_json.json_data = json_data
        else:
            model_json = ModelJSON(json_data=json_data)
            self.session.add(model_json)
        self.session.commit()
