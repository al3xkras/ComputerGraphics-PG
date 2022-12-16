import pygame.gfxdraw


class Spacecraft:
    graphics_path = "./graphics/"
    spaceship_size = 150
    bgspeed = 10
    initialSpeed = 5

    def __init__(self, displaySize, x=100, y=100, sprite="spaceship.png"):
        self.speed = 0
        self.displaySize = displaySize
        self.sprite = sprite
        self.y = y
        self.x = x
        self.vertices2 = (x, y)
        self.spaceship = None
        self._load_spaceship()

    def _load_spaceship(self):
        self.spaceship = pygame.image.load(Spacecraft.graphics_path + self.sprite)
        self.spaceship = pygame.transform.scale(self.spaceship, (
            int(self.spaceship_size * self.spaceship.get_width() / self.spaceship.get_height()), self.spaceship_size))

    def draw(self, layer: pygame.Surface):
        layer.blit(self.spaceship, (self.x+self.speed, self.y))

    def draw2(self, layer: pygame.Surface):
        layer.blit(self.spaceship, self.vertices2)

    def move(self, delta):
        clock = pygame.time.Clock()
        execTime = 500
        delay = 60
        n = execTime // delay
        y_initial = self.y
        for i in range(n + 1):
            clock.tick(delay)
            self.y = min(self.displaySize[1] - self.spaceship_size, max(0, y_initial + delta * i / n))

    def speed_up(self, delta):
        self.speed = delta

    def slow_down(self, delta):
        self.speed = delta

    def stop(self):
        self.speed = 0
