from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout
from models.model import Model  # Assuming Model is your model class
from controllers.ModelEditorScreen import ModelEditorScreen
from services.model.modelDataServices import ModelDataService

class ModelsManagerScreen(QWidget):
    def __init__(self,parent=None,props={}):
        super(ModelsManagerScreen,self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Models Manager")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.models_list = QListWidget()
        self.layout.addWidget(self.models_list)

        self.load_models()

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_model)
        self.layout.addWidget(self.edit_button)

        self.new_model_button = QPushButton("New Model")
        self.new_model_button.clicked.connect(self.new_model)
        self.layout.addWidget(self.new_model_button)

        self.delete_button = QPushButton("Delete Model")
        self.delete_button.clicked.connect(self.delete_model)
        self.layout.addWidget(self.delete_button)

    def load_models(self):
        # Load models from the database and add them to the list
        
        models = ModelDataService.getModels()  # Assuming you have a query method like this
        for model in models:
            item = QListWidgetItem(model.model_name)
            item.setData(1, model)  # Use item.setData to store the model object
            self.models_list.addItem(item)

    def edit_model(self):
        selected_item = self.models_list.currentItem()
        if selected_item:
            model = selected_item.data(1)  # Retrieve the model object
            self.parent.switchScreens('modelEditor',props={"model": model})

    def new_model(self):
        self.parent.switchScreens('modelEditor')

    def delete_model(self):
        selected_item = self.models_list.currentItem()
        if selected_item:
            model = selected_item.data(1)  # Retrieve the model object
            ModelDataService.deleteModel(model)  # Assuming you have a delete method in your service
            self.models_list.takeItem(self.models_list.row(selected_item))  # Remove item from list
