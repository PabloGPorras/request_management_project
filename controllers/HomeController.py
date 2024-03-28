import json
from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication
from database.worker import DataFetcher
from services.dynamicModel.dynamicModelDataService import DynamicModelDataService
from services.model.modelDataServices import ModelDataService
from models.modelBuilder import ModelBuilder
from utils.utils import loadData, resourcePath
from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QIcon

from widgets.dynamicCheckboxes import DynamicCheckboxes


class HomeScreen(QWidget):
    """Home Screen Controller"""
    
    def __init__(self,parent=None,props={}):
        super(HomeScreen, self).__init__(parent)
        self.parent = parent
        self.props = props
        self.currentQueryID = 0
        self.user = QApplication.instance().user
        self.threadPool = QThreadPool.globalInstance()
        # self.configurations = QApplication.instance().configurations
        loadUi(resourcePath("views/home.ui"), self)
        
        # Load appConfigurations JSON
        with open('appConfigurations.json') as file:
            self.appConfigurations = json.load(file)

        # Determine the table name to display on the home screen
        tableName = self.appConfigurations.get("homePageTable")
        self.tableModel = ModelDataService.getModelByName(tableName)
        self.loadFilterOptions()
        
        # set icons
        self.refreshBtn.setIcon(QIcon(resourcePath("views/icons/arrows-rotate-solid.svg")))
        self.filterBtn.setIcon(QIcon(resourcePath("views/icons/filter-solid.svg")))

        # hide the filter button
        self.filterOptions.hide()

        self.fetchData()


    def fetchData(self):
        self.requestCountLabel.setText("Fetching Data...")
        self.currentQueryID += 1
        queryID = self.currentQueryID
        dataFetcher = DataFetcher(
            lambda: DynamicModelDataService.getDynamicModelItems(self.tableModel),
            queryID
        )
        dataFetcher.signals.dataFetched.connect(self.displayData)
        dataFetcher.signals.error.connect(self.displayError)
        self.threadPool.start(dataFetcher)

    def displayData(self, data, queryID):
        self.props["data"] = data
        if queryID == self.currentQueryID:
            self.requestCountLabel.setText(f"Total Items: {len(data)}")
            loadData(self.tableWidget,data["rows"],data["columns"])
            

    def displayError(self, error):
        self.requestCountLabel.setText("Error Fetching Data")
        print(error)

    def loadFilterOptions(self):
        model_json = json.loads(self.tableModel.model_json)
        for column in model_json["table_columns"]:
            if "options" in column:
                column_name = column["name"]
                options = column["options"]
                self.searchItemsComboBox.addItem(column_name)
                checkboxes = DynamicCheckboxes(options, self.fetchData, list_title=column_name)
                self.filterOptionsLayout.addWidget(checkboxes)
        
