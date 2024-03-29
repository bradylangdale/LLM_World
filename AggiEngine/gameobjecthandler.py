from AggiEngine.contactlistener import ContactListener
import math

from Box2D import *


class GameObjectHandler:

    def __init__(self, window, scale=16):
        self.timing = 1 / window.targetFixedFPS
        self.window = window
        
        self.world = Box2D.b2World(gravity=(0, 0))  # create instance of box 2d world
        self.world.contactListener = ContactListener()
        
        self.scale = scale  # scaling parameter, is equal to pixels to meter
        self.gameObjects = []  # game object list
        self.removeList = []

    def setScale(self, scale):
        self.scale = scale

    def update(self):
        for gameObject in self.gameObjects:
            if gameObject.active:
                gameObject.update()

    def fixedUpdate(self):
        self.world.Step(self.timing, 6, 2)
        self.world.ClearForces()

        for gameObject in self.gameObjects:
            if gameObject.renderUpdate:
                self.window.gameScreen.renderInfoList[gameObject.id] = [gameObject.textureID]

                if gameObject.textureID == -1:
                    if len(gameObject.color) < 4:
                        gameObject.color.append(1)
                    self.window.gameScreen.renderInfoList[gameObject.id] += [gameObject.vertices, gameObject.color]
                else:
                    self.window.gameScreen.renderInfoList[gameObject.id] += [gameObject.width, gameObject.height]

                self.window.gameScreen.renderInfoList[gameObject.id] += [gameObject.position, math.degrees(gameObject.rotation)]

                gameObject.renderUpdate = False

            if gameObject.active:
                gameObject.fixedUpdate()
                if gameObject.body is not None:
                    gameObject.position = gameObject.body.position / self.scale
                    gameObject.rotation = gameObject.body.angle
                self.window.gameScreen.renderInfoList[gameObject.id][-1] = math.degrees(gameObject.rotation)
                self.window.gameScreen.renderInfoList[gameObject.id][-2] = gameObject.position

        for gameObject in self.removeList:
            self.gameObjects.remove(gameObject)
            self.world.DestroyBody(gameObject.body)
        self.removeList = []

    def add(self, gameObject, bodyDef=None, bodyFixtureDef=None, color=None):
        gameObject.id = len(self.gameObjects)
        self.gameObjects.append(gameObject)  # adds game object to list of game objects
        gameObject.gameObjectHandler = self

        if bodyDef:
            body = self.world.CreateBody(bodyDef)
            body.CreateFixture(bodyFixtureDef)
            gameObject.body = body
            gameObject.body.userData = gameObject

            gameObject.body.userData = gameObject

            if type(bodyFixtureDef.shape) is b2PolygonShape:
                gameObject.vertices.clear()
                for vertex in bodyFixtureDef.shape.vertices:
                    gameObject.vertices.append([vertex[0] / self.scale, vertex[1] / self.scale])
            elif type(bodyFixtureDef.shape) is b2CircleShape:
                vertices = []
                for i in range(0, 30):
                    rad = (2 * math.pi * i) / 30
                    r = bodyFixtureDef.shape.radius / self.scale
                    vertices.append([(r * math.cos(rad) - (bodyFixtureDef.shape.pos[0] / self.scale)),
                                     (r * math.sin(rad) - (bodyFixtureDef.shape.pos[1] / self.scale))])
                gameObject.vertices = vertices

            if color is None:
                gameObject.color = [1, 1, 1, 1]
            else:
                gameObject.color = color
            gameObject.position = body.position / self.scale

        self.window.gameScreen.renderInfoList[gameObject.id] = [gameObject.textureID]

        if gameObject.textureID == -1:
            if len(gameObject.color) < 4:
                gameObject.color.append(1)
            self.window.gameScreen.renderInfoList[gameObject.id] += [gameObject.vertices, gameObject.color]
        else:
            self.window.gameScreen.renderInfoList[gameObject.id] += [gameObject.width, gameObject.height]

        if gameObject.body is not None:
            gameObject.position = gameObject.body.position / self.scale
            gameObject.rotation = gameObject.body.angle
            gameObject.active = True

        self.window.gameScreen.renderInfoList[gameObject.id] += [gameObject.position, math.degrees(gameObject.rotation)]

        gameObject.window = self.window
        gameObject.start()

    def getGameObject(self, typeOf):
        for gameObject in self.gameObjects:
            if isinstance(gameObject, typeOf):
                return gameObject

    def getGameObjects(self, typeOf):
        gameObjects = []
        for gameObject in self.gameObjects:
            if isinstance(gameObject, typeOf):
                gameObjects.append(gameObject)
        return gameObjects

    def removeGameObject(self, toRemove):
        self.removeList.append(toRemove)

    def removeGameObjects(self, typeOf):
        for gameObject in self.gameObjects:
            if isinstance(gameObject, typeOf):
                self.removeList.append(gameObject)

    def exit(self):
        for gameObject in self.gameObjects:
            gameObject.exit()

    def keyPressed(self, event):
        for gameObject in self.gameObjects:
            gameObject.keyPressed(event)

    def keyReleased(self, event):
        for gameObject in self.gameObjects:
            gameObject.keyReleased(event)

    def mouseMoved(self, event):
        for gameObject in self.gameObjects:
            gameObject.mouseMoved(event)

    def mousePressed(self, event):
        for gameObject in self.gameObjects:
            gameObject.mousePressed(event)

    def mouseReleased(self, event):
        for gameObject in self.gameObjects:
            gameObject.mouseReleased(event)
