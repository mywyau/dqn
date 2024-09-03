import pygame


class Renderer:
    def __init__(self, screen, car, environment):
        self.screen = screen
        self.car = car
        self.environment = environment

    def render(self):
        self.environment.draw(self.screen)
        self.car.draw(self.screen)
        pygame.display.flip()
