from Box2D import b2BodyDef, Box2D, b2FixtureDef, b2PolygonShape

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel

import AggiEngine as ag
from gridmanager import GridManager
from llmplayer import LLMPlayer

from oobabooga import Oobabooga

class Life(ag.State):

    def __init__(self, ui_path):
        ag.State.__init__(self, ui_path)

        self.label = None
        self.camera_motion = [0, 0]
        self.client = Oobabooga()

    def start(self):
        self.label = self.window.findChild(QLabel)
        self.label.setVisible(False)
        self.loadMap('Assets/world.tmx')
        self.window.gameScreen.cameraScale = 1
        self.window.gameScreen.cameraPosition = [-2, -2]
        self.gridManager = GridManager('Assets/world.tmx')

        self.addBot('''You are an expert explorer who is enjoys the thrill of exploration!
DO NOT HALLICINATE AND DO NOT REPEAT YOU PROMPTS!
YOU ARE PROMPTING YOURSELF THIS IS ALL YOUR OWN THOUGHTS! UTILIZED YOUR SURROUNDINGS TO SURVIVE!
You love F letters on the grid because they represent food. You must collect them to survive.
But you must be careful and avoid the rocks and trees. To keep from starving you search for food.''', -32, -32)

    def update(self):
        if self.label.isVisible():
            self.label.setText('Fixed FPS: {:.3f}\nScreen FPS: {:.3f}'.format(
                self.window.fixedFps, self.window.screenFps))

        self.window.gameScreen.cameraPosition[0] += self.camera_motion[0]
        self.window.gameScreen.cameraPosition[1] += self.camera_motion[1]

    def keyPressed(self, event):
        if event.key() == Qt.Key_I:
            self.label.setVisible(False if self.label.isVisible() else True)

        if event.key() == Qt.Key_W:
            self.camera_motion[1] = 0.01
        
        if event.key() == Qt.Key_S:
            self.camera_motion[1] = -0.01

        if event.key() == Qt.Key_A:
            self.camera_motion[0] = 0.01
        
        if event.key() == Qt.Key_D:
            self.camera_motion[0] = -0.01

    def keyReleased(self, event):
        if event.key() == Qt.Key_W:
            self.camera_motion[1] = 0
        
        if event.key() == Qt.Key_S:
            self.camera_motion[1] = 0

        if event.key() == Qt.Key_A:
            self.camera_motion[0] = 0
        
        if event.key() == Qt.Key_D:
            self.camera_motion[0] = 0

    def addBot(self, prompt, x, y):
        bodyDef = b2BodyDef()
        bodyDef.type = Box2D.b2_dynamicBody
        bodyDef.position = (x, y)

        bodyFixtureDef = b2FixtureDef(shape=b2PolygonShape(box=(0.5, 0.5)))
        bodyFixtureDef.friction = 0.75
        bodyFixtureDef.density = 1

        bot = LLMPlayer(self.client, prompt, self.gridManager)
        bot.position = [x, y]
        self.gameObjectHandler.add(bot, bodyDef, bodyFixtureDef, [1, 1, 1])
