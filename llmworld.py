from PySide2.QtWidgets import QPushButton, QFileDialog, QLineEdit

import AggiEngine as ag
from life import Life


class Menu(ag.State):

    def __init__(self, ui_path):
        ag.State.__init__(self, ui_path)

    def start(self):
        self.window.findChild(QPushButton).clicked.connect(
            lambda: self.window.stateManager.changeState(Life('Assets/game.ui')))


state = Menu('Assets/menu.ui')
app = ag.Application(state)  # starts the application at 60 hz screen, and 60 hz physics
app.run()
