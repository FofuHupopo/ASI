import pygame


def draw(surface: pygame.Surface):
    surface.fill((0, 0, 0))

    pygame.draw.rect(
        surface, pygame.Color((255, 0, 0, 255)),
        pygame.Rect(
            (117, 60), (789, 465)
        )
    ), 10
    pygame.draw.rect(
        surface, pygame.Color((255, 0, 0, 255)),
        pygame.Rect(
            (307, 172), (209, 181)
        )
    ), 10
    pygame.draw.polygon(
        surface, pygame.Color((0, 255, 0, 255)),
        [(248, 128), (814, 271), (404, 432), (110, 310), (403, 261)], 10
    )
