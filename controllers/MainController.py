import ctypes
from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from controllers.ModelEditorScreen import ModelEditorScreen
from controllers.ModelsManagerScreen import ModelsManagerScreen
from env import TOOL_VERSION
from services.configurations.ConfigurationBusinessService import ConfigurationBusinessService
from services.model.modelDataServices import ModelDataService
from utils.utils import resourcePath, setSytle
from controllers.HomeController import HomeScreen
# from controllers.CreateRequestController import CreateRequestScreen
from PyQt6.uic.load_ui import loadUi
from PyQt6.QtWidgets import QApplication

class MainController(QMainWindow):
    """Main controller class for the application. This class is responsible for managing the main window and the different views."""
    def __init__(self):
        super(MainController, self).__init__()
        loadUi(resourcePath("views/mainWindow.ui"), self)
        self.setWindowTitle("Request Management System")
        self.threadpool = QThreadPool.globalInstance()
        self.setWindowIcon(QIcon(resourcePath("views/icons/rocket-solid.svg")))
        self.homePageBtn.setIcon(QIcon(resourcePath("views/icons/house-solid.svg")))
        self.adminPageBtn.setIcon(QIcon(resourcePath("views/icons/screwdriver-wrench-solid.svg")))
        self.createRequestBtn.setIcon(QIcon(resourcePath("views/icons/plus-solid.svg")))
        self.darkModeBtn.setIcon(QIcon(resourcePath("views/icons/moon-regular.svg")))
        self.lightModeBtn.setIcon(QIcon(resourcePath("views/icons/sun-regular.svg")))
        # hiding the dark mode button
        self.darkModeBtn.setVisible(False)

        self.user = QApplication.instance().user

        self.currentScreen = "home"
        self.screens = {}
        self.screenClasses = {
            "home": HomeScreen,
            "modelsManager": ModelsManagerScreen,
            "modelEditor": ModelEditorScreen
        }

        # Connect buttons to their corresponding functions
        self.homePageBtn.clicked.connect(lambda: self.switchScreens("home"))
        self.adminPageBtn.clicked.connect(lambda: self.switchScreens("modelsManager"))
        self.createRequestBtn.clicked.connect(lambda: self.switchScreens("create_request"))
        self.darkModeBtn.clicked.connect(self.toggleDarkMode)
        self.lightModeBtn.clicked.connect(self.toggleLightMode)

        setSytle(self, "dark")

        # Check if models exist in the database
        self.models = ModelDataService.getModels()
        if not self.models:
            # If no models found open Admin Page
            self.switchScreens("modelEditor")
        else:
            # Switch to Home Page
            self.switchScreens("home")

        # Check if the tool is up to date
        self.configurations = ConfigurationBusinessService.getConfiguration()
        LASTEST_TOOL_VERSION = self.configurations.get("tool_version")
        if TOOL_VERSION != LASTEST_TOOL_VERSION[0]:
            ctypes.windll.user32.MessageBoxW(0, f"Please update the tool to the latest version {LASTEST_TOOL_VERSION}", "Update Required", 1)
            self.close()


    def switchScreens(self, screenName,props={}):
        """Switch between different screens"""
        if self.currentScreen not in ('home'):
            self.stackedWidget.removeWidget(self.screens[self.currentScreen])
            del self.screens[self.currentScreen]

        # Create the screen if it doesn't exist
        if screenName not in self.screens:
            screenClass = self.screenClasses.get(screenName)
            if screenClass is not None:
                self.screens[screenName] = screenClass(self,props)
                self.stackedWidget.addWidget(self.screens[screenName])

        # Show the screen
        self.currentScreen=screenName
        self.stackedWidget.setCurrentWidget(self.screens[screenName])

    def toggleDarkMode(self):
        """Toggle dark mode"""
        setSytle(self, "dark")
        self.darkModeBtn.setVisible(False)
        self.lightModeBtn.setVisible(True)

    def toggleLightMode(self):
        """Toggle light mode"""
        setSytle(self, "light")
        self.darkModeBtn.setVisible(True)
        self.lightModeBtn.setVisible(False)