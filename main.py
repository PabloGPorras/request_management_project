import ctypes
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QInputDialog
from controllers.MainController import MainController
from services.user.userDataService import UserDataService


ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

class RequestManagementSystem(QApplication):
    """Main application class"""
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        try:
            self.user = UserDataService.getUser()
        except:
            try:
                import win32com.client as win32
                outlook = win32.Dispatch('Outlook.Application')
                mapi = outlook.GetNamespace("MAPI")
                inbox = mapi.GetDefaultFolder(6)
                email_from = inbox.Parent.Name.lower()
            except:
                email_from, ok = QInputDialog.getText(None, "Email", "Enter your email address:")
                if ok is False:
                    return
                            
            self.user = UserDataService.createUser(self,{
                "email_from": email_from 
            })
        


if __name__ == '__main__':
    app = RequestManagementSystem(sys.argv)
    controller = MainController()
    controller.show()
    app.exec()
