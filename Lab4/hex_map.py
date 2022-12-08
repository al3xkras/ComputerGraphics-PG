from collections import deque

import pygame
from shapely.geometry import Polygon
import sympy as sp
from numpy import dot

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
    hex_width=60 #px
    i,j,k=sp.symbols("i,j,k")
    center_coordinates_eq = (i * sp.sqrt(3) + j * sp.sqrt(3) / 4 + k * sp.sqrt(3) / 4,
                             j * 3 / 4 - k * 3 / 4)
    scale=1

    def __init__(self, hex_type, coordinates, neighbours=None):
        if neighbours is None:
            neighbours = dict()
        assert hex_type in HexMap.hex_types

        self.coordinates=(0,
            coordinates[1]+coordinates[0],
            coordinates[2]+coordinates[0]
        )
        self.hex_type=hex_type
        self.neighbours=neighbours
        self.hex_width=Hex.hex_width
        self.offset=[0,0]

    def __str__(self) -> str:
        return "Hex("+self.hex_type+" "+str(self.coordinates)+")"

    @staticmethod
    def draw_arrow(surface,_from,_to,color):
        pygame.draw.line(surface,color,_from,_to)
        w=(_from[0]-_to[0])**2+(_from[1]-_to[1])**2
        w=int(max(2,w**0.5/5))
        d=(_to[0]-_from[0],_to[1]-_from[1])
        d=[x*5/w for x in d]
        d_ort=[-d[1]/5,d[0]/5]
        pygame.draw.line(surface,color,(_to[0]-d[0]+d_ort[0],_to[1]-d[1]+d_ort[1]),_to)
        pygame.draw.line(surface,color,(_to[0]-d[0]-d_ort[0],_to[1]-d[1]-d_ort[1]),_to)


    def draw(self,surface:pygame.Surface):
        self.offset=[surface.get_width()//2,surface.get_height()//2]
        hex_coords=self.getHexCoords()
        center=self.getCenterCoordsInPx()
        center=[int(x) for x in center]
        center[0] += self.offset[0]
        center[1] += self.offset[1]
        for x in hex_coords:
            x[0] += self.offset[0]
            x[1] += self.offset[1]

        for i in range(len(hex_coords)):
            p1=hex_coords[i]
            p2=hex_coords[(i+1)%len(hex_coords)]
            pygame.draw.line(surface,color="black",start_pos=p1,end_pos=p2)
        #pygame.draw.circle(surface,center=center,radius=Hex.hex_width//2,color="red")
        for _x in self.neigh_directions:
            if not _x in self.neighbours:
                continue
            x=self.neighbours[_x]
            c=[int(_) for _ in x.getCenterCoordsInPx()]
            c[0] += self.offset[0]
            c[1] += self.offset[1]
            Hex.draw_arrow(surface,center,c,"green")


    def getCenterCoordsInPx(self, scale=False):
        w=self.hex_width*2
        c = tuple(x.subs(Hex.i,self.coordinates[0]*w).subs(Hex.j,self.coordinates[1]*w).subs(Hex.k,self.coordinates[2]*w).evalf()
                for x in Hex.center_coordinates_eq)
        if not scale:
            return c
        return int(c[0]*Hex.scale),int(c[1]*Hex.scale)

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
            (h4x, h4y), (h6x, h6y),
            (h5x, h5y), (h3x, h3y),
        ]
        hex_coords = [list(int(_x.subs(Hex.i, self.hex_width)*Hex.scale) for _x in _x2) for _x2 in hex_coords]

        return hex_coords

    def isContainedInRectangle(self,rect):
        #rect: x1 y1 x2 y2
        x1,y1,x2,y2=rect
        rect_poly = Polygon([(x1, y1), (x2, y1), (x2, y2),(x1,y2)])
        hex_poly = Polygon(self.getHexCoords())
        return rect_poly.contains(hex_poly)

    def createNeighbour(self, hexmap, location:str, hex_type, rect, replace_if_exists=False):
        if location in self.neighbours and not replace_if_exists:
            return self.neighbours[location], False
        coords = [x for x in self.coordinates]
        shift = Hex.neigh_directions[location]
        coords[shift[0]]+=shift[1]
        coords=tuple(x for x in coords)
        self_loc_for_neigh=Hex.inverse_direction[location]
        _hex=None
        _created=True
        if coords in hexmap.hex_dict:
            _hex=hexmap.getHexByCoordinates(coords)
            _created=False
        else:
            _hex=Hex(hex_type,coords,dict())
            if not _hex.isContainedInRectangle(rect):
                return None, False
            hexmap.hex_dict[coords]=_hex
        _hex.neighbours[self_loc_for_neigh]=self
        self.neighbours[location]=_hex
        return _hex, _created

    @staticmethod
    def transform(coordinates):
        return (0,
            coordinates[1]+coordinates[0],
            coordinates[2]+coordinates[0]
        )


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
        self._hex_list = None
        self.map_size=map_size
        self.zoom_factor=1.0
        self.hex_dict=dict()
        self.map_rect=(
            -self.map_size[0]//2,
            -self.map_size[1]//2,
            self.map_size[0]//2,
            self.map_size[1]//2
        )
        self._cached_surface=None

    def prepare(self,surface):
        self._fillMapRectangleWithHexes()
        if self._cached_surface is None:
            self._cached_surface=pygame.Surface((surface.get_width(),surface.get_height()))
            self._cached_surface.fill((0xff, 0xff, 0xff))
            for x in self.hex_dict.values():
                x.draw(self._cached_surface)
        pygame.draw.rect(surface,"black",self.map_rect)

    def draw(self,surface):
        if self._cached_surface is None:
            self.prepare(surface)
        surface.blit(self._cached_surface.copy(),(0,0))

    def _appendHex(self, hex_obj):
        self.hex_dict[hex_obj.coordinates]=hex_obj

    def _nextRandomHexType(self):
        return "plains"

    def _fillMapRectangleWithHexes(self):
        first_hex=Hex(hex_type="plains",coordinates=(0,0,0))
        self._appendHex(first_hex)
        horizon=deque([first_hex])
        horizon_next=deque()
        hex_count_mock=300
        hex_count=0
        while len(horizon)>0:
            for _hex in horizon:
                if not _hex.isContainedInRectangle(self.map_rect):
                    continue
                for direction in Hex.neigh_directions:
                    neighbour,_created=_hex.createNeighbour(self,direction,self._nextRandomHexType(),self.map_rect)
                    if not _created:
                        continue
                    if not neighbour.isContainedInRectangle(self.map_rect):
                        print("a",neighbour)
                        continue
                    horizon_next.append(neighbour)
                    hex_count+=1
                    if hex_count>hex_count_mock:
                        print("hex map overflow: ",hex_count)
                        return
                for x in horizon_next:
                    print(x,end=" ")
                print()
            horizon=horizon_next
            horizon_next=deque()
        print(first_hex.neighbours)

    def getHexByCoordinates(self, coordinates):
        coordinates=Hex.transform(coordinates)
        return self.hex_dict[coordinates]

if __name__ == '__main__':
    hm=HexMap((100,100))

    #h1=Hex("plains",(-16,31,30))
    h1=Hex("plains",(0,1,30))

    p=h1.isContainedInRectangle([
        -450,-300,450,300
    ])
    print(p)
    print(h1.getCenterCoordsInPx())
    print(h1.getHexCoords())