from collections import deque
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
    hex_width=10 #px
    i,j,k=sp.symbols("i,j,k")
    center_coordinates_eq=(i*sp.srqt(3)/2+(j*3)/4+(k*3)/4,j*sp.srqt(3)/2-k*sp.srqt(3)/2)

    def __init__(self, hex_type, coordinates, neighbours:dict):
        assert hex_type in HexMap.hex_types
        self.coordinates=coordinates
        self.hex_type=hex_type
        self.neighbours=neighbours
        self.hex_width=Hex.hex_width

    def draw(self,surface):
        pass

    def getCenterCoordsInPx(self):
        return [x.subs((Hex.i,Hex.j,Hex.k),self.coordinates).evalf()]

    def isContainedInRectangle(self,rect):
        #rect: x1 y1 x2 y2
        x1,y1,x2,y2=rect
        rect_poly = Polygon([(x1, y1), (x2, y1), (x2, y2),(x1,y2)])
        x,y = hex_center=self.getCenterCoordsInPx()
        h1x = x-Hex.i*sp.sqrt(3) / 2
        h1y = y-i / 2
        h2x = x - Hex.i * sp.sqrt(3) / 2
        h2y = y + i / 2
        h3x = x
        h3y = y - Hex.i
        h4x = x
        h4y = y + Hex.i
        h5x = x + Hex.i * sp.sqrt(3) / 2
        h5y = y - i / 2
        h6x = x + Hex.i * sp.sqrt(3) / 2
        h6y = y + i / 2
        hex_coords = [
            (h1x,h1y),(h2x,h2y),
            (h3x,h3y),(h4x,h4y),
            (h5x,h5y),(h6x,h6y),
        ]
        hex_coords = [tuple(_x.subs(Hex.i,self.hex_width) for _x in _x2) for _x2 in hex_coords]
        hex_poly = Polygon(hex_coords)

        return rect_poly.intersects(hex_poly)

    def createNeighbour(self, hexmap, location:str, hex_type, replace_if_exists=False):
        if location in self.neighbours and not replace_if_exists:
            return (self.neighbours[location],False)
        coords = [x for x in self.coordinates]
        shift = Hex.neigh_directions[hex_type]
        coords[shift[0]]+=shift[1]
        coords=tuple(x for x in coords)
        self_loc_for_neigh=Hex.inverse_direction[location]
        hex=None
        if coords in hexmap.hex_dict:
            hex=hexmap.getHexByCoordinates(coords)
        else:
            hex=Hex(hex_type,coords,dict())
        hex.neighbours[self_loc_for_neigh]=self
        self.neighbours[location]=hex
        return (hex,True)

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
        self.map_rect=(-self.map_size[0]//2,self.map_size[1]//2,
                       -self.map_size[1]//2,self.map_size[1]//2)
    def draw(self,surface):
        pass

    def _appendHex(self, hex):
        self.hex_dict[hex.coordinates]=hex

    def _fillMapRectangleWithHexes(self):
        first_hex=Hex("plains",(0,0,0))
        self._appendHex(first_hex)
        horizon=deque([first_hex])
        horizon_next=deque()
        hex_count_mock=500
        hex_count=0
        while len(horizon)>0:
            for hex in horizon:
                for direction in Hex.neigh_directions:
                    created,neighbour=hex.createNeighbour(self,direction,self._nextRandomHexType())
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