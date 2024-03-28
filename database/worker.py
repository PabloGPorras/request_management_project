from PyQt6.QtCore import pyqtSignal, QObject,QRunnable

class DataFetcherSignals(QObject):
    dataFetched = pyqtSignal(object,int)
    error = pyqtSignal(Exception)

class DataFetcher(QRunnable):
    """A class for fetching data from the database in a separate thread"""
    def __init__(self, fetchData: callable,queryID=None):
        super().__init__()
        self.fetchData = fetchData
        self.queryID = queryID
        self.signals = DataFetcherSignals()

    def run(self):
        try:
            data = self.fetchData()
            self.signals.dataFetched.emit(data,self.queryID)
        except Exception as e:
            self.signals.error.emit(e)