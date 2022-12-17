from collections import deque

import pygame
from shapely.geometry import Polygon,Point
from math import sqrt
import pickle
import os
import threading


class Cache:
    cache_dir="./cache"
    postfix=".bin"
    @staticmethod
    def load_obj(key):
        f=open(Cache.cache_dir+key+Cache.postfix,"w+")
        obj=None
        try:
            obj = pickle.load(f)
            f.close()
        except:
            f.close()
        return obj
    @staticmethod
    def save_obj(key,obj):
        f=open(Cache.cache_dir+key+Cache.postfix,"w+")
        pickle.dump(file=f,obj=obj)
        f.close()
    @staticmethod
    def clear(key):
        os.remove(Cache.cache_dir+key+Cache.postfix)

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
    hex_width=18 #px
    scale=1
    color=(0xcc, 0xcc, 0xcc)
    def __init__(self, hex_type, coordinates):
        #if neighbours is None:
            #neighbours = dict()
        assert hex_type in HexMap.hex_types

        self.coordinates=(0,
            coordinates[1]+coordinates[0],
            coordinates[2]+coordinates[0]
        )
        self.hex_type=hex_type
        self.scale=Hex.scale
        #self.neighbours=neighbours
        self.hex_width=Hex.hex_width
        self.offset=[0,0]
        self.screen_offset=[0,0]
        self.hide=False

    def __str__(self) -> str:
        return "Hex("+self.hex_type+" "+str(self.coordinates)+")"

    @staticmethod
    def draw_arrow(surface,_from,_to,color):
        pygame.draw.line(surface,color,_from,_to)
        w=(_from[0]-_to[0])**2+(_from[1]-_to[1])**2
        w=int(w**0.5/5)
        d=(_to[0]-_from[0],_to[1]-_from[1])
        d=[x*2/w for x in d]
        d_ort=[-d[1]/5,d[0]/5]
        pygame.draw.line(surface,color,(_to[0]-d[0]+d_ort[0],_to[1]-d[1]+d_ort[1]),_to)
        pygame.draw.line(surface,color,(_to[0]-d[0]-d_ort[0],_to[1]-d[1]-d_ort[1]),_to)


    def draw(self,surface:pygame.Surface):
        if self.hide:
            return
        color="white"
        self.offset=[surface.get_width()//2+self.screen_offset[0],surface.get_height()//2+self.screen_offset[1]]
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
            pygame.draw.line(surface,color,start_pos=p1,end_pos=p2)
        #pygame.draw.circle(surface,color="black",center=center,radius=self.hex_width/5)
        """
        for _x in self.neigh_directions:
            if not _x in self.neighbours:
                continue
            x=self.neighbours[_x]
            c=[int(_) for _ in x.getCenterCoordsInPx()]
            c[0] += self.offset[0]
            c[1] += self.offset[1]
            #Hex.draw_arrow(surface,center,c,"green")"""

    def getCenterCoordsInPx(self, scale=False):
        w=self.hex_width*self.scale*2
        i,j,k=(x*w for x in self.coordinates)

        c = (i * sqrt(3) + j * sqrt(3) / 4 + k * sqrt(3) / 4,
                             j * 3 / 4 - k * 3 / 4)
        if not scale:
            return c
        return int(c[0]),int(c[1])

    @staticmethod
    def getHexCoordsByCenterCoords(center,width=None,scale=1):
        x,y=center
        if width is None:
            width=Hex.hex_width
        coords = 0, 2/sqrt(3)*x+2*y/3, 2/sqrt(3)*x-2*y/3
        coords=tuple(a//(2*width*scale) for a in coords)
        return coords

    def getHexCoords(self):
        x, y = self.getCenterCoordsInPx()
        i=self.hex_width*self.scale
        h1x = x - i * sqrt(3) / 2
        h1y = y - i / 2
        h2x = x - i * sqrt(3) / 2
        h2y = y + i / 2
        h3x = x
        h3y = y - i
        h4x = x
        h4y = y + i
        h5x = x + i * sqrt(3) / 2
        h5y = y - i / 2
        h6x = x + i * sqrt(3) / 2
        h6y = y + i / 2
        hex_coords = [
            (h1x, h1y), (h2x, h2y),
            (h4x, h4y), (h6x, h6y),
            (h5x, h5y), (h3x, h3y),
        ]
        hex_coords = [list(int(_x) for _x in _x2) for _x2 in hex_coords]

        return hex_coords

    def isContainedInPolygon(self, poly):
        if hasattr(poly,"can_draw_hex_at"):
            self.hide=poly.can_draw_hex_at(Point(self.getCenterCoordsInPx()))
        return poly.contains(Point(self.getCenterCoordsInPx()))

    def createNeighbour(self, hexmap, location:str, hex_type, rect, replace_if_exists=False):
        #if location in self.neighbours and not replace_if_exists:
        #    return self.neighbours[location], False
        coords = [x for x in self.coordinates]
        shift = Hex.neigh_directions[location]
        h=Hex.transform(coords,True)
        h[shift[0]]+=shift[1]
        coords=tuple(h)
        #self_loc_for_neigh=Hex.inverse_direction[location]
        _hex=None
        _created=True
        if coords in hexmap.hex_dict:
            _hex=hexmap.getHexByCoordinates(coords)
            _created=False
        else:
            _hex=Hex(hex_type,coords)
            if not _hex.isContainedInPolygon(rect):
                return None, False
            hexmap.hex_dict[coords]=_hex
        #_hex.neighbours[self_loc_for_neigh]=self
        #self.neighbours[location]=_hex
        return _hex, _created

    @staticmethod
    def transform(coordinates,lst=False):
        r=(0,
            coordinates[1]+coordinates[0],
            coordinates[2]+coordinates[0]
        )
        if lst:
            return list(r)
        return r


class HexMap:
    graphics_dir = "./graphics"
    hex_types = {
        "water": "water.png",
        "plains": "plains.png",
        "mountains": "mountains.png",
        "hills": "hills.png",
        "desert": "desert.png"
    }
    cache_surface_name="hexmap_hexes"
    def __init__(self, map_size, map_poly=None):
        self._hex_list = None
        self.map_size=map_size
        self.zoom_factor=1.0
        self.hex_dict=dict()
        self.offset=[0,0]
        if map_poly is None:
            x1,y1,x2,y2=(
                -self.map_size[0]//2,
                -self.map_size[1]//2,
                self.map_size[0]//2,
                self.map_size[1]//2
            )
            self.map_poly=Polygon([(x1, y1), (x2, y1), (x2, y2),(x1,y2)])
        else:
            self.map_poly=map_poly
        self._cached_surface=None
        self._op_threads=[]

    def is_preparing(self):
        if len(self._op_threads)==0:
            return False
        a=any([x.is_alive() for x in self._op_threads])
        if not a:
            self._op_threads=[]
        return a

    def prepare(self,surface):
        if self.is_preparing():
            return
        self._fillMapRectangleWithHexes()
        if self._cached_surface is None:
            self._cached_surface=pygame.Surface((surface.get_width(),surface.get_height()))
            self._cached_surface.fill(Hex.color)
            lst=list(self.hex_dict.values())
            def _f(a, b):
                for i in range(a,b):
                    x=lst[i]
                    x.isContainedInPolygon(self.map_poly)
                    x.draw(self._cached_surface)
            thr_count=1
            _k=len(lst)//thr_count
            _a=0
            _b=_k
            for j in range(thr_count):
                thr=threading.Thread(target=_f,args=(_a,_b),daemon=True)
                self._op_threads.append(thr)
                thr.start()
                _a+=_k
                _b+=_k

    def draw(self,surface):
        if self._cached_surface is None:
            self.prepare(surface)
        surface.blit(self._cached_surface.copy(),(0,0))

    def _appendHex(self, hex_obj):
        self.hex_dict[hex_obj.coordinates]=hex_obj

    def _nextRandomHexType(self):
        return "plains"

    def clear(self):
        if self.is_preparing():
            return
        self._cached_surface=None
        self.hex_dict.clear()

    def zoom_in(self,delta):
        if self.is_preparing():
            return
        self.zoom_factor=max(0.05,self.zoom_factor+delta)
        self.clear()

    def zoom_out(self,delta):
        self.zoom_in(-delta)

    def move(self,direction,delta):
        if self.is_preparing():
            return
        offset={
            'l':[-delta,0],
            'r':[delta,0],
            'u':[0,-delta],
            'd':[0,delta]
        }
        d=offset[direction]
        self.offset[0]+=d[0]
        self.offset[1]+=d[1]
        self.clear()

    def reset_pos(self):
        if self.is_preparing():
            return
        self.offset=[0,0]
        self.zoom_factor=1.0
        self.clear()

    def _fillMapRectangleWithHexes(self):
        if len(self.hex_dict)>0:
            return
        if hasattr(self.map_poly,"centroid"):
            p=self.map_poly.centroid
        else:
            p=Point(0,0)
        first_coords=Hex.getHexCoordsByCenterCoords((p.x,p.y))
        first_hex=Hex(hex_type="desert",coordinates=first_coords)
        first_hex.scale=self.zoom_factor
        first_hex.screen_offset=self.offset
        self._appendHex(first_hex)
        horizon=deque([first_hex])
        horizon_next=deque()
        hex_count_mock=3000
        hex_count=0
        while len(horizon)>0:
            for _hex in horizon:
                if not _hex.isContainedInPolygon(self.map_poly):
                    continue
                for direction in Hex.neigh_directions:
                    neighbour,_created=_hex.createNeighbour(self, direction, self._nextRandomHexType(), self.map_poly)
                    if not _created:
                        continue
                    neighbour.scale=self.zoom_factor
                    neighbour.screen_offset=self.offset
                    horizon_next.append(neighbour)
                    hex_count+=1
                    if hex_count_mock>0 and hex_count>hex_count_mock:
                        print("hex map overflow: ",hex_count)
                        return
            horizon=horizon_next
            horizon_next=deque()

    def getHexByCoordinates(self, coordinates):
        return self.hex_dict[coordinates]


if __name__ == '__main__':
    c=Hex.getHexCoordsByCenterCoords((0,100))

    h=Hex(coordinates=c,hex_type="plains")

    print(c)
    print(h.getCenterCoordsInPx())