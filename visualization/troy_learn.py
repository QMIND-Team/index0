"""Learning Pygame"""
import sys

import pygame
import pygame.freetype

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Device(pygame.sprite.Sprite):
    """Device Object, extends Sprite.  ID is name"""
    def __init__(self, font, name, x, y):
        super(Device, self).__init__()
        self.active = True
        self.name = name
        self.images = []
        base_images = [
            pygame.image.load("resources/computer-clip-art.png").convert_alpha(),
            pygame.image.load("resources/computer-clip-art-black.png").convert_alpha()
        ]
        for temp_image in base_images:
            temp_rect = temp_image.get_rect()
            new_image = pygame.transform.smoothscale(
                temp_image,
                (120, round((temp_rect.height/temp_rect.width)*120))
            )
            self.images.append(new_image)
        self.surf = self.images[0]
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
        self.text_surf, self.text_rect = pygame.freetype.Font.render(font, name)
        self.text_rect.center = (self.rect.centerx, self.rect.centery+100)
    
    # def update(self, pressed_keys):
    #     if pressed_keys[pygame.K_UP]:
    #         self.rect.move_ip(0, -5)
    #     if pressed_keys[pygame.K_DOWN]:
    #         self.rect.move_ip(0, 5)
    #     if pressed_keys[pygame.K_LEFT]:
    #         self.rect.move_ip(-5, 0)
    #     if pressed_keys[pygame.K_RIGHT]:
    #         self.rect.move_ip(5, 0)

    def change_pic(self):
        """Toggle the sprite's image.
        We don't need to worry about the rects because the images are the same size.
        """
        if self.active:
            self.active = False
            self.surf = self.images[1]
        else:
            self.active = True
            self.surf = self.images[0]


def reposition_workers(workers, lines_surf):
    """Helper to reposition the workers once one is added or removed
    Also update the lines
    """
    num = len(workers)
    if num % 2 == 0:
        for i, worker in enumerate(workers):
            worker.rect.centerx = (SCREEN_WIDTH // 2) + 120 + (240 * (i - (num//2)))
            worker.text_rect.centerx = worker.rect.centerx
    else:
        for i, worker in enumerate(workers):
            worker.rect.centerx = (SCREEN_WIDTH // 2) + (240 * (i - (num//2)))
            worker.text_rect.centerx = worker.rect.centerx
    lines_surf.fill((255, 255, 255))
    for worker in workers:
        pygame.draw.aaline(
            lines_surf,
            (0, 0, 0),
            (worker.rect.centerx, worker.rect.centery - 85),
            (SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 120)
        )


def add_worker(lines_surf, devices, workers, font, name):
    """Add a worker"""
    new_device = Device(font, name, 0, (SCREEN_HEIGHT // 4)*3)
    devices.add(new_device)
    workers.add(new_device)
    reposition_workers(workers, lines_surf)


def remove_worker(lines_surf, devices, workers, name):
    """Remove a worker"""
    sprites = workers.sprites()
    to_remove = None
    for sprite in sprites:
        if sprite.name == name:
            to_remove = sprite
            break
    devices.remove(to_remove)
    workers.remove(to_remove)
    reposition_workers(workers, lines_surf)


def init():
    """Initialize pygame and main game elements"""
    pygame.init()
    myfont = pygame.freetype.SysFont('consolas', 30)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("CUCAI 2020 - Distributed Computing")
    clock = pygame.time.Clock()

    # Create the lines surface
    lines_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    lines_surf.fill((255, 255, 255))

    # Create the sprites
    manager = Device(myfont, "Manager", SCREEN_WIDTH//2, SCREEN_HEIGHT//4)

    # Collect the devices
    devices = pygame.sprite.Group()
    devices.add(manager)

    # Group for workers
    workers = pygame.sprite.Group()

    # Create User Events
    CHANGE = pygame.USEREVENT+1
    ADD = pygame.USEREVENT+2
    REMOVE = pygame.USEREVENT+3

    return screen, lines_surf, clock, devices, workers, CHANGE, ADD, REMOVE, myfont


def main():
    """Main"""
    # Initialize
    screen, lines_surf, clock, devices, workers, CHANGE, ADD, REMOVE, myfont = init()


    # Main loop
    running = True
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    my_event = pygame.event.Event(CHANGE)
                    pygame.event.post(my_event)
                elif event.key == pygame.K_a:
                    my_event = pygame.event.Event(ADD, name="A")
                    pygame.event.post(my_event)
                elif event.key == pygame.K_b:
                    my_event = pygame.event.Event(ADD, name="B")
                    pygame.event.post(my_event)
                elif event.key == pygame.K_c:
                    my_event = pygame.event.Event(ADD, name="C")
                    pygame.event.post(my_event)
                elif event.key == pygame.K_s:
                    my_event = pygame.event.Event(REMOVE, name="A")
                    pygame.event.post(my_event)
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == CHANGE:
                for device in devices:
                    device.change_pic()
            elif event.type == ADD:
                add_worker(lines_surf, devices, workers, myfont, event.name)
            elif event.type == REMOVE:
                remove_worker(lines_surf, devices, workers, event.name)

        # # Respond to keypresses
        # pressed_keys = pygame.key.get_pressed()
        # for device in devices:
        #     device.update(pressed_keys)

        # Draw
        screen.fill((255, 255, 255))

        screen.blit(lines_surf, lines_surf.get_rect())

        for device in devices:
            screen.blit(device.surf, device.rect)
            screen.blit(device.text_surf, device.text_rect)

        pygame.display.flip()

        # Run at 30 fps (max)
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
