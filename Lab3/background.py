import pygame.gfxdraw
from random import randint


class Stars:
    graphics_path = "/graphics/"
    star_sprite = "star_%d.png"
    max_sprite_index = 5

    @staticmethod
    def index(speed):
        factor = 2
        s = 0
        index = 0
        while s < speed:
            if index >= Stars.max_sprite_index:
                return min(Stars.max_sprite_index, index)
            s = s * factor if s != 0 else factor
            index += 1
        return index

    @staticmethod
    def random_coords(surface: pygame.Surface, count: int):
        assert count > 0
        return [(randint(0, surface.get_width()), randint(0, surface.get_height())) for _ in range(count)]

    def __init__(self, distance, speed):
        assert distance >= 0 and speed >= 0
        self.distance = distance
        self.speed = speed
        self.star = None
        self.sprite_index = Stars.index(self.speed)
        self._load_sprites()

    def _load_sprites(self):
        assert self.sprite_index is not None
        self.star = pygame.image.load(Stars.graphics_path + Stars.star_sprite % self.sprite_index)

    def draw(self, layer: pygame.Surface, count: int, blink=True):
        coordinates = Stars.random_coords(layer, count)

        alpha = 1.0
        for coords in coordinates:
            if blink:
                alpha = 0.6 + 0.4 / randint(1, 3)
            self.star.set_alpha(alpha)
            layer.blit(self.star, coords)

        self.star.set_alpha(1.0)


class FalseDepthBackground:
    depth_delta = 10
    depth_factor = 0.8  # depth_factor size & speed for depth = depth_delta; depth_factor^2 for depth = 2*depth_delta, ...

    def __init__(self, layer_count=2, initial_speed=0, background_depth=100):
        assert layer_count > 0 and type(layer_count) == int
        assert initial_speed >= 0
        assert background_depth >= layer_count * 10 and type(background_depth) == int

        self.layer_count = layer_count
        self.movement_speed = initial_speed
        self.background_depth = background_depth
        self.layers = []
        self.layers_distance = []
        self.layers_speed = []
        self.layers_translate = [0] * layer_count

    def _eval_layer_params(self):
        cur_layer_distance = self.background_depth
        cur_layer_speed_percent = pow(FalseDepthBackground.depth_factor,
                                      self.background_depth // FalseDepthBackground.depth_delta)
        d_distance = self.background_depth // self.layer_count

        for i in range(self.layer_count):
            self.layers_distance.append(cur_layer_distance)
            cur_layer_distance = max(0, cur_layer_distance - d_distance)
            cur_layer_speed = self.movement_speed * cur_layer_speed_percent
            cur_layer_speed_percent /= FalseDepthBackground.depth_factor
            self.layers_speed.append(cur_layer_speed)

    def _init_layers(self, screen: pygame.Surface):
        for i in range(self.layer_count):
            layer = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA, 32)
            self.layers.append(layer)

    def _draw_layer(self, layer_index, screen: pygame.Surface):
        layer = self.layers[layer_index]
        distance = self.layers_distance[layer_index]
        speed = self.layers_speed[layer_index]

        count = 10
        Stars(distance, speed).draw(layer, count, True)

        screen.blit(layer, (0, 0))

    def draw(self, screen: pygame.Surface):
        if len(self.layers) <= self.layer_count:
            self.layers = []
            self._init_layers(screen)
        self._eval_layer_params()
        self.layers_translate = [(self.layers_translate[i] + self.layers_speed[i]) % screen.get_width()
                                 for i in range(self.layer_count)]
        for i in range(self.layer_count):
            self._draw_layer(i, screen)

    def speed_up(self, delta):
        self.movement_speed += delta

    def slow_down(self, delta):
        self.movement_speed = max(0, self.movement_speed - delta)

    def stop(self):
        self.movement_speed = 0
