import pygame


def run(callback, title="Base", size_=(1000, 600)):
    pygame.init()
    size = size_

    surface = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    pygame.display.set_caption(title)

    running = True

    while running:
        events = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            events.append(event)
            
        surface.fill((0, 0, 0))

        callback(events, surface)
    
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run([])
