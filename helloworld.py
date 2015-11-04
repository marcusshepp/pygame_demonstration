import pygame

""" Screen """
pygame.init()
screen = pygame.display.set_mode((800, 600)) # must be tuple
pygame.display.set_caption("FIRE UP CHIPS")
""" Background """
bg = pygame.Surface(screen.get_size())
bg = bg.convert()
bg.fill((250, 250, 250))
""" Text """
font = pygame.font.Font(None, 36)
text = font.render("Hello World", 1, (10, 10, 10))
textpos = text.get_rect()
# get_rect() is the rectangular area around the obj
textpos.centerx = bg.get_rect().centerx 
textpos.centery = bg.get_rect().centery
bg.blit(text, textpos)
""" Blit everything to screen """
screen.blit(bg, (0, 0))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            print("KEYDOWN")
    screen.blit(bg, (0, 0)) # same as css
    pygame.display.flip()