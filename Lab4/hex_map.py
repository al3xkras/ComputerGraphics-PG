from collections import deque


class Hex:
    def __init__(self, hex_type, coordinates, neighbours:dict):
        assert hex_type in HexMap.hex_types
        self.coordinates=coordinates
        self.hex_type=hex_type
        self.neighbours=neighbours
        self.neigh_locations={
            "l":(0,-1),"r":(0,1),
            "lu":(1,-1),"ru":(1,1),
            "ld":(2,-1),"rd":(2,1)
        }
        self.inverse_loc={
            "l":"r","r":"l",
            "lu":"rd","rd":"lu",
            "ld":"ru","ru":"ld"
        }

    def draw(self,surface):
        pass

    def isContainedInRect(self,rect):
        return True

    def createNeighbour(self, location:str, hex_type, replace_if_exists=False):
        if location in self.neighbours and not replace_if_exists:
            return self.neighbours[location]
        coords = [x for x in self.coordinates]
        shift = self.neigh_locations[hex_type]
        coords[shift[0]]+=shift[1]
        self_loc_for_neigh=self.inverse_loc[location]
        hex = Hex(hex_type,coords,{
            self_loc_for_neigh:self
        })
        self.neighbours[location]=hex
        return hex

class HexMap:
    graphics_dir = "./graphics"
    hex_types = {
        "water": "water.png",
        "plains": "plains.png",
        "mountains": "mountains.png",
        "hills": "hills.png",
        "desert": "desert.png"
    }

    def __init__(self, map_size):
        self.map_size=map_size
        self.zoom_factor=1.0
        self.hex_dict=dict()

    def draw(self,surface):
        pass

    def _appendHex(self, hex):
        self.hex_dict[hex.coordinates]=hex

    def _fillMapRectangleWithHexes(self):
        first_hex=Hex("plains",(0,0,0))
        self._appendHex(first_hex)
        horizon=deque([first_hex])
        horizon_next=deque()




    def getHexByCoordinates(self, coordinates):
        pass