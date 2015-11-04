import pygame

""" Screen """
pygame.init()
screen = pygame.display.set_mode((800, 600)) # must be tuple
pygame.display.set_caption("The real flying C")
""" Color definitions """
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
""" Background """
bg = pygame.Surface(screen.get_size())
bg = bg.convert()
bg.fill((250, 250, 250))
""" Blit everything to screen """
screen.blit(bg, (0, 0))
pygame.display.flip()


class FlyingC(pygame.sprite.Sprite):
    """
    The Flying CMU!
    """
    def __init__(self):
        self.image = pygame.image.load("assets/CMU.jpg").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 250
        
    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 12
        if key[pygame.K_RIGHT]:
            self.rect.x += dist
        elif key[pygame.K_LEFT]:
            self.rect.x -= dist
        elif key[pygame.K_UP]:
            self.rect.y -= dist
        elif key[pygame.K_DOWN]:
            self.rect.y += dist

    def draw(self, surface):
        """ Draw on surface """
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        
flying_cmu = FlyingC()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            print(event.type)
    screen.blit(bg, (0, 0)) # same as css
    flying_cmu.draw(screen)
    flying_cmu.handle_keys()
    pygame.display.flip()
    