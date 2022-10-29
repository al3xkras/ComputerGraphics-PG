import pygame.gfxdraw


class Spacecraft:
    def __init__(self):
        pass

    def draw(self, surface: pygame.Surface):
        pygame.draw.line(surface, "black", (0, 0), (100, 200))
        pass

    def move(self, pixels):
        pass

    def speed_up(self, delta):
        pass

    def stop(self):
        pass
