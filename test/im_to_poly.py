from shapely.geometry import Point,Polygon
import cv2
from math import floor

class FrameIterator:
    def __init__(self,fname,limit=-1):
        self.vidcap = cv2.VideoCapture(fname)
        self.count = 0
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        success, image = self.vidcap.read()
        self.count+=1
        if not success or self.limit>0 and self.count>self.limit:
            raise StopIteration
        return image

class ImagePolygon:
    def __init__(self,image,eps,rect:Polygon):
        self.image=image
        self.eps=eps
        self.rect=rect
        _x,_y=self.rect.exterior.coords.xy
        _x,_y=_y,_x
        w=len(image)
        h=len(image[0])
        self.offset=-_x[0],-_y[0]
        rect_w=abs(_x[0]-_x[2])
        rect_h=abs(_y[0]-_y[2])

        self.ratio_x= w / rect_w
        self.ratio_y= h / rect_h

    def metrics(self, r,g,b):
        #metrics for a pixel
        return int(r)+g+b

    def contains(self,point:Point):
        return self.rect.contains(point)

    def can_draw_hex_at(self,point:Point):
        if not self.rect.contains(point):
            return False
        x, y = point.y, point.x
        x,y=x+self.offset[0],y+self.offset[1]
        x,y=floor(x * self.ratio_x), floor(y * self.ratio_y)
        try:
            return self.metrics(*self.image[x, y]) < self.eps
        except:
            return False

if __name__ == '__main__':
    it=FrameIterator("test.mp4",limit=10)
    i=0
    for im in it:
        i+=1
        ip=ImagePolygon(im,10)
        r=ip.can_draw_hex_at(Point(100,100))
        print(r)
