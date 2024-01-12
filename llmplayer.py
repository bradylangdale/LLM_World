from random import randint
import AggiEngine as ag
from llm import LLM


class LLMPlayer(ag.GameObject):

    def __init__(self, client, prompt, gridManager):
        ag.GameObject.__init__(self)
        self.system = prompt
        self.messages = []
        self.gridManager = gridManager

        self.client = client
        self.llm = LLM(client, model_name='starling-lm-7b-alpha.Q5_K_M.mixtral')

        #self.addMessage('You have four choice, UP, DOWN, LEFT, RIGHT. Which direction do you want to go?')

    def start(self):
        self.body = None

        self.textureID = self.window.gameScreen.loadImageTexture('Assets/character1.png')
        self.width = 1.0 / 24
        self.height = 1.0 / 24
        self.renderUpdate = True

    def update(self):
        pass

    def fixedUpdate(self):
        #self.messages = []
        sight = '''I am currently starving and have collected zero!
To avoid dying I must collect food which are the "F" tiles on the grid.
In order to collect them I must navigate on to that grid square.
I must avoid "X" tiles. I can NOT move on to them because they are obstacles and will make starve even faster.

Here is what I can see surroundings:\n''' + self.getSurroundings() + '''\nThe "C" on the grid represents me and will always be in the center.
If I see any food to go it. I be careful and think about step carefully!'''
        self.addMessage(sight + '\n\n' + 'I have four choice, NORTH, SOUTH, EAST, WEST. Which direction do I want to go?')

        response = self.llm.inference(self.messages, system=self.system)
        self.addMessage(response, role='assistant')

        print("{" + response + "}")

        words = response.lower().replace('\n', ' ').replace('!', ' ').replace('.', ' ').replace(',', ' ').split(' ')
        print(words)

        if 'north' in words:
            self.position[1] += 1.0 / 16
            print('moving north')
        elif 'south' in words:
            self.position[1] -= 1.0 / 16
            print('moving south')
        
        if 'west' in words:
            self.position[0] += 1.0 / 16
            print('moving west')
        elif 'east' in words:
            self.position[0] -= 1.0 / 16
            print('moving east')

        if len(self.messages) > 10:
            self.messages.pop(0)

    def addMessage(self, content, role='user'):
        self.messages.append({ 'role': role, 'content': content })

    def getSurroundings(self):
        grid_str = ''

        for x in range(-3, 4):
            row = ''
            for y in range(-3, 4):
                if x == 0 and y == 0:
                    row += 'C,'
                    continue

                tile = self.gridManager.checkForTile(int((-self.position[1] * 16.0) + x), int((-self.position[0] * 16.0) + y))

                if tile is None:
                    tile = ' '
                elif tile != 'flower':
                    tile = 'X'#tile.upper()[0]
                else:
                    tile = 'F'

                row += tile + ','

            grid_str += row[:len(row) - 1] + '\n'

        return grid_str
