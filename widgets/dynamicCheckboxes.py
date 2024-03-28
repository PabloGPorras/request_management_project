from PyQt6.QtWidgets import QVBoxLayout,QWidget,QCheckBox,QLabel

class DynamicCheckboxes(QWidget):
    def __init__(self, checkList, refreshCallback=None, setAllChecked=False, setCheckedList=[], list_title=None):
        super(DynamicCheckboxes, self).__init__()
        self.layout = QVBoxLayout()
        self.checks = []
        self.refreshCallback = refreshCallback
        self.checkList = checkList
        self.setCheckedList = setCheckedList

        if list_title:
            title_label = QLabel(list_title)
            self.layout.addWidget(title_label)

        for item in range(len(self.checkList)):
            checkbox = QCheckBox(self.checkList[item])
            if self.checkList[item] in self.setCheckedList:
                checkbox.setChecked(True)
            if setAllChecked:
                checkbox.setChecked(True)
            if self.refreshCallback is not None:
                checkbox.stateChanged.connect(self.refreshCallback)
            self.layout.addWidget(checkbox)
            self.checks.append(checkbox)
        self.setLayout(self.layout)

    def addCheckbox(self,checkboxList: list, setAllChecked=False):
        if self.checkList == []:
            self.checkList.extend(checkboxList)
            for item in range(len(self.checkList)):
                checkbox = QCheckBox(self.checkList[item])
                if item in self.setCheckedList:
                    checkbox.setChecked(True)
                if setAllChecked:
                    checkbox.setChecked(True)
                if self.refreshCallback is not None:
                    checkbox.stateChanged.connect(self.refreshCallback)
                self.layout.addWidget(checkbox)
                self.checks.append(checkbox)
            self.setLayout(self.layout)

    def grabCheckedList(self):
        checkedList = []
        for item in range(len(self.checks)):
            if self.checks[item].isChecked():
                checkedList.append(self.checkList[item])
        return checkedList
    
    def grabUncheckedList(self):
        uncheckedList = []
        for item in range(len(self.checks)):
            if not self.checks[item].isChecked():
                uncheckedList.append(self.checkList[item])
        return uncheckedList
    
    def grabJson(self):
        dict = {}
        for item in self.checks:
            dict[item.text()] = item.isChecked()
        return dict
    
    def grabCsv(self):
        csv = ""
        for item in self.checks:
            csv += f"{item.text()},"
        if csv != "":
            csv = csv[:-1]

    def setChecked(self,text):
        for item in self.checks:
            checkText = item.text()
            if checkText == text:
                item.setChecked(True)

    def setItemUnchecked(self,text):
        for item in self.checks:
            checkText = item.text()
            if checkText == text:
                item.setChecked(False)

    def setAllChecked(self):
        for item in self.checks:
            item.setChecked(True)

    def setAllUnchecked(self):
        for item in self.checks:
            item.setChecked(False)