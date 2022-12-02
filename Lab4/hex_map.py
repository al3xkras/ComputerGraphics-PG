from collections import deque

import pygame
from shapely.geometry import Polygon
import sympy as sp

class Hex:
    neigh_directions={
        "l":(0,-1),"r":(0,1),
        "lu":(1,-1),"ru":(1,1),
        "ld":(2,-1),"rd":(2,1)
    }
    inverse_direction = {
        "l": "r", "r": "l",
        "lu": "rd", "rd": "lu",
        "ld": "ru", "ru": "ld"
    }
    hex_width=100 #px
    i,j,k=sp.symbols("i,j,k")
    center_coordinates_eq = (i * sp.sqrt(3) / 2 + (j * 3) / 4 + (k * 3) / 4, j * sp.sqrt(3) / 2 - k * sp.sqrt(3) / 2)
    scale=100

    def __init__(self, hex_type, coordinates, neighbours=None):
        if neighbours is None:
            neighbours = dict()
        assert hex_type in HexMap.hex_types
        self.coordinates=coordinates
        self.hex_type=hex_type
        self.neighbours=neighbours
        self.hex_width=Hex.hex_width

    def __str__(self) -> str:
        return "Hex("+self.hex_type+" "+str(self.coordinates)+")"

    def draw(self,surface:pygame.Surface):
        center_coords=self.getCenterCoordsInPx(True)
        hex_coords=self.getHexCoords()
        for i in range(len(hex_coords)):
            p1=hex_coords[i]
            p2=hex_coords[i%len(hex_coords)]
            pygame.draw.line(surface,color="white",start_pos=p1,end_pos=p2)
        pygame.draw.circle(surface,center=center_coords,radius=Hex.hex_width/2,color="red")


    def getCenterCoordsInPx(self, scale=False):
        c = tuple(x.subs(Hex.i,self.coordinates[0]).subs(Hex.j,self.coordinates[1]).subs(Hex.k,self.coordinates[2]).evalf()
                for x in Hex.center_coordinates_eq)
        if not scale:
            return c
        return [int(x*Hex.scale) for x in c]

    def getHexCoords(self):
        x, y = self.getCenterCoordsInPx()
        h1x = x - Hex.i * sp.sqrt(3) / 2
        h1y = y - Hex.i / 2
        h2x = x - Hex.i * sp.sqrt(3) / 2
        h2y = y + Hex.i / 2
        h3x = x
        h3y = y - Hex.i
        h4x = x
        h4y = y + Hex.i
        h5x = x + Hex.i * sp.sqrt(3) / 2
        h5y = y - Hex.i / 2
        h6x = x + Hex.i * sp.sqrt(3) / 2
        h6y = y + Hex.i / 2
        hex_coords = [
            (h1x, h1y), (h2x, h2y),
            (h3x, h3y), (h4x, h4y),
            (h5x, h5y), (h6x, h6y),
        ]
        hex_coords = [tuple(int(_x.subs(Hex.i, self.hex_width)*Hex.scale) for _x in _x2) for _x2 in hex_coords]
        return hex_coords

    def isContainedInRectangle(self,rect):
        #rect: x1 y1 x2 y2
        x1,y1,x2,y2=rect
        rect_poly = Polygon([(x1, y1), (x2, y1), (x2, y2),(x1,y2)])
        hex_poly = Polygon(self.getHexCoords())
        return rect_poly.intersects(hex_poly)

    def createNeighbour(self, hexmap, location:str, hex_type, replace_if_exists=False):
        if location in self.neighbours and not replace_if_exists:
            return self.neighbours[location], False
        coords = [x for x in self.coordinates]
        shift = Hex.neigh_directions[location]
        coords[shift[0]]+=shift[1]
        coords=tuple(x for x in coords)
        self_loc_for_neigh=Hex.inverse_direction[location]
        _hex=None
        if coords in hexmap.hex_dict:
            _hex=hexmap.getHexByCoordinates(coords)
        else:
            _hex=Hex(hex_type,coords,dict())
        _hex.neighbours[self_loc_for_neigh]=self
        self.neighbours[location]=_hex
        hexmap.hex_dict[_hex.coordinates]=_hex
        return _hex, True

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
        self.map_rect=(
            -self.map_size[0]//2,
            self.map_size[1]//2,
            -self.map_size[1]//2,
            self.map_size[1]//2
        )

    def draw(self,surface):
        self._fillMapRectangleWithHexes()
        for x in self.hex_dict.values():
            x.draw(surface)

    def _appendHex(self, hex_obj):
        self.hex_dict[hex_obj.coordinates]=hex_obj

    def _nextRandomHexType(self):
        return "plains"

    def _fillMapRectangleWithHexes(self):
        first_hex=Hex(hex_type="plains",coordinates=(0,0,0))
        self._appendHex(first_hex)
        horizon=deque([first_hex])
        horizon_next=deque()
        hex_count_mock=5
        hex_count=0
        while len(horizon)>0:
            for _hex in horizon:
                for direction in Hex.neigh_directions:
                    neighbour,created=_hex.createNeighbour(self,direction,self._nextRandomHexType())
                    if not created or not neighbour.isContainedInRectangle(self.map_rect):
                        continue
                    horizon_next.append(neighbour)
                    hex_count+=1
                    if hex_count>hex_count_mock:
                        print("hex map overflow: ",hex_count)
                        return
            horizon=horizon_next

    def getHexByCoordinates(self, coordinates):
        return self.hex_dict[coordinates]

if __name__ == '__main__':
    hm=HexMap((100,100))

    h1=Hex("plains",(0,0,0))
    h2,created=h1.createNeighbour(hm,"r","plains")
    _,created1=h2.createNeighbour(hm, "rd", "plains")
    print(h2,_,created,created1)

    print(h1.getCenterCoordsInPx())