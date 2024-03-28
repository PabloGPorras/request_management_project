import os
import sys
import qdarkstyle
from qdarkstyle.light.palette import LightPalette
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def loadData(table,rows,columns,columnNameFilter=[]):
    colmnNames = [column for column in columns if column not in columnNameFilter]
    table.setRowCount(len(rows))
    table.setColumnCount(len(colmnNames))
    table.setHorizontalHeaderLabels(colmnNames)

def resourcePath(relativePath):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativePath)
    return os.path.join(os.path.abspath('.'), relativePath)


def setSytle(self,style):
    """Set the style of the application"""
    qss = """
    QPushButton {
        text-align: left;
        height: 25px;
    }
    
    # QPushButton {
    #     background-color: #2a2a2a;
    #     color: #f0f0f0;
    #     border: 1px solid #2a2a2a;
    #     border-radius: 4px;
    #     padding: 5px;
    # }

    QPushButton:hover {
        background-color: #3e3e3e;
    }

    QPushButton:pressed {
        background-color: #4c4c4c;
    }

    QComboBox {
        background-color: #2a2a2a;
        color: #f0f0f0;
        border: 1px solid #2a2a2a;
        border-radius: 4px;
        padding: 5px;
    }

    QComboBox:hover {
        background-color: #3e3e3e;
    }

    QComboBox:pressed {
        background-color: #4c4c4c;
    }

    QComboBox::drop-down {
        border: none;
    }

    # QComboBox::down-arrow {
    #     image: url(views/icons/chevron-down-solid.svg);
    # }

    # QComboBox::down-arrow:pressed {
    #     image: url(views/icons/chevron-down-solid.svg);
    # }

    
    """
    stylesheet = qdarkstyle.load_stylesheet(qt_api='PyQt6') + qss
    if style != "dark":
        stylesheet = qdarkstyle.load_stylesheet(qt_api='PyQt6', palette=LightPalette) + qss
    self.setStyleSheet(stylesheet)