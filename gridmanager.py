import pytmx


class GridManager:

    def __init__(self, tmxFile):
        tiled_map = pytmx.TiledMap(tmxFile)

        self.grids = {}

        for layer in tiled_map:
            self.grids[layer.name] = []
            data = list(layer.iter_data())
            
            i = 0
            for x in range(tiled_map.width):
                row = []

                for y in range(tiled_map.height):
                    row.append(True if data[i][2] != 0 else False)
                    i += 1

                self.grids[layer.name].append(row)

    def getGridNames(self):
        return list(self.grids.keys())
    
    def checkForTile(self, x, y, layerName=None):
        if not layerName is None:
            return self.grids[layerName][x][y]
        else:
            for layer in self.grids:
                tile = self.grids[layer][x][y]

                if tile:
                    return layer
