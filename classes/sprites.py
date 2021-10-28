import pygame, math

class Sprite:
    def __init__(self, rSprite_pos, height, width, img, bGoalSpot=False):
        self.pos = rSprite_pos
        self.x = rSprite_pos[0]
        self.y = rSprite_pos[1]
        self.height = height
        self.width = width
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        nRed = 0 if bGoalSpot else 255
        self.surface.fill((nRed, 255, 255, 128)) #128
        self.surface.blit(img, (0, 0))
        self.angle = rSprite_pos[2]
        self.turn = 0.9
        self.speed = 0
        self.accel = 1.5
        self.bGoalSpot = bGoalSpot

    def draw(self):
        self.rect.topleft = (int(self.x), int(self.y))
        rotated = pygame.transform.rotate(self.surface, self.angle)
        surface_rect = self.surface.get_rect(topleft=self.rect.topleft)
        new_rect = rotated.get_rect(center=surface_rect.center)
        self.rect = new_rect
        #print("rotated",rotated,"surface_rect",surface_rect,"new_rect",new_rect)
        return rotated, new_rect.topleft