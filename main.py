import pygame


pygame.init()
windowsize = (1900, 860)
screen = pygame.display.set_mode(windowsize)
done = False
pen_weight = PendulumWeight()

while not done:

    for event in pygame.event.get():

        if event == pygame.QUIT:
            done = True
        
        if event == pygame.KEYDOWN:
            pen_weight.detach

pygame.quit()
exit(0)