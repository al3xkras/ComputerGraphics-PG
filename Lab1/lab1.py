import math

from pygame.locals import *
import pygame.gfxdraw
from math import sqrt
from sys import exit
import os

pygame.init()

WINDOW_SIZE = (800, 800)
WINDOW_POSITION = (100, 100)

FONT_SIZE = 24
FONT_BOLD = False

FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % WINDOW_POSITION

screen = pygame.display.set_mode(WINDOW_SIZE, FLAGS)

color1 = Color("yellow")
color2 = Color("black")


def rotate_around_point(xy, radians, origin=(0, 0)):
    """Rotate a point around a given point.

    I call this the "high performance" version since we're caching some
    values that are needed >1 time. It's less readable than the previous
    function but it's faster.
    """
    x, y = xy
    offset_x, offset_y = origin
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
    return qx, qy


def rotate(polygon, radians, origin):
    return [rotate_around_point(x, radians, origin) for x in polygon]


triangleSide = screen.get_width() / 4

centerPoint = (screen.get_width() / 2, screen.get_height() / 2)
zeroTranslate = (centerPoint[0] - screen.get_width() / 4, centerPoint[0] - screen.get_height() / 4)
points = [(0, 0), (0, triangleSide), (triangleSide, 0)]


def translate(points, center):
    return list(tuple(x[i] + center[i] for i in range(len(x))) for x in points)


points = translate(points, [zeroTranslate[0], zeroTranslate[1]])
points = rotate(points, 0, (zeroTranslate[0] + 50, zeroTranslate[0] + 50))

angleIncrement = 9
colorIncrement = 30
alphaIncrement = 25
segmentSize = 10
segmentLength = 2
segmentsPerNumber = 5


def drawSegments(surface, lineStart, lineEnd, coordinate, number0):
    coordinate2 = 0 if coordinate == 1 else 1

    i = 0
    number = number0
    for x in range(round(lineStart[coordinate]), round(lineEnd[coordinate]), segmentSize):
        l = segmentLength
        linewidth = 1
        i += 1
        if i % segmentsPerNumber == 0:
            l *= 2
            linewidth = 2
        start = [0, 0]
        end = [0, 0]
        start[coordinate] = x
        start[coordinate2] = lineStart[coordinate2] - l
        end[coordinate] = x
        end[coordinate2] = lineStart[coordinate2] + l
        fontSize = 13
        if i % segmentsPerNumber == 0:
            font = pygame.font.Font(pygame.font.get_default_font(), fontSize)
            text = font.render(str(number), False, "black")
            loc = []
            if coordinate != 0:
                loc = [start[0] - 2 * fontSize, start[1] - fontSize / 2]
            else:
                loc = [start[0] - fontSize, start[1] + fontSize]
            surface.blit(text, loc)
            number += abs(number0)
        pygame.draw.line(surface, "black", start, end, width=linewidth)


while True:
    # get events
    for event in pygame.event.get():
        # if QUIT
        if event.type == pygame.QUIT:
            # clean up
            pygame.quit()
            # bye bye
            exit()

    screen.fill((0xff, 0xff, 0xff))

    angle = 0

    initialColor = Color("yellow")

    parentSurface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
    parentSurface = parentSurface.convert_alpha()

    for angle in range(0, 360, angleIncrement):
        if initialColor.r > 255 - colorIncrement:
            initialColor.r = 0
            initialColor.g = 0
        else:
            initialColor.r += colorIncrement
            initialColor.g += colorIncrement

        if initialColor.a <= alphaIncrement:
            initialColor.a = 255
        else:
            initialColor.a -= alphaIncrement

        s = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
        s = s.convert_alpha()
        pygame.draw.polygon(s, initialColor, rotate(points, angle / 180 * math.pi, centerPoint))

        parentSurface.blit(s, (0, 0))

        angle += angleIncrement

    s = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
    s = s.convert_alpha()

    line_x_start = translate([(0, -WINDOW_SIZE[1] / 8)], zeroTranslate)[0]
    line_x_end = translate([(0, WINDOW_SIZE[1] / 2 * 1.2)], zeroTranslate)[0]
    line_y_start = translate([(WINDOW_SIZE[1] / 2 - WINDOW_SIZE[1] / 2 * 1.2, WINDOW_SIZE[1] / 2)], zeroTranslate)[0]
    line_y_end = translate([(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)], zeroTranslate)[0]
    pygame.draw.line(s, "black", line_x_start, line_x_end)
    pygame.draw.line(s, "black", line_y_start, line_y_end)
    drawSegments(s, list(line_y_start), line_y_end, 0, -0.25)
    segmentSize *= -1
    drawSegments(s, line_x_end, list(line_x_start), 1, -0.25)
    segmentSize *= -1
    radius_outer = centerPoint[0] - zeroTranslate[0]
    radius_inner = radius_outer / 2 * sqrt(2)
    pygame.draw.circle(s, "black", centerPoint, radius_outer, width=1)
    pygame.draw.circle(s, "black", centerPoint, radius_inner, width=2)
    parentSurface.blit(s, (0, 0))
    screen.blit(parentSurface, (0, 0))
    # update windows and flip buffers
    pygame.display.flip()
