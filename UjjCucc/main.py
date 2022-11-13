import pygame
from copy import deepcopy

############################################
# A játékmező 10 * 50 pixel Széles és 20 * 50 pixel magas lesz
Sz,M = 10,20
Csempe = 45
GAME_RES = Sz * Csempe, M * Csempe
############################################
FPS = 60

pygame.init()

############################################
#Ez az ablak ami megnyílik egy változó ként
GAME = pygame.display.set_mode(GAME_RES) 
###########################################
clock = pygame.time.Clock()


FigurakKoordinatai = [  [(-1, 0), (-2, 0), (0, 0), (1, 0)],
                        [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                        [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                        [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                        [(0, 0), (0, -1), (0, 1), (-1, -1)],
                        [(0, 0), (0, -1), (0, 1), (1, -1)],
                        [(0, 0), (0, -1), (0, 1), (-1, 0)]]

Figurak = [[pygame.Rect(x + Sz // 2, y + 1, 1, 1) for x, y in FiguraHelyzet] for FiguraHelyzet in FigurakKoordinatai]
FiguraNegyzet = pygame.Rect(0,0, Csempe - 2, Csempe - 2)

Figura =  deepcopy(Figurak[3])

############################################
#A grid létrehozása változóként, (x = oszop, y = sor, Szelesség, Magasság)
grid = [pygame.Rect(x * Csempe, y * Csempe, Csempe, Csempe) for x in range(Sz) for y in range(M)]       
############################################

def hitboxChech():
    if Figura[i].x < 0 or Figura[i].x > Sz - 1:
        return False
    return True

while True:
    mozgasX = 0
    GAME.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mozgasX = -1
            elif event.key == pygame.K_RIGHT:
                mozgasX = 1

    regi_Figura = deepcopy(Figura)
    for i in range(4):
        Figura[i].x += mozgasX
        if not hitboxChech():
            Figura = deepcopy(regi_Figura)
            break
    ############################################
    #A grid kirajzolása: (Kijelző, (RGB szinek), i az maga a létrehozott grid ek tulajdonságai, milyne vastag a border)
    [pygame.draw.rect(GAME, (50,50,50), i , 1) for i in grid]                          
    ############################################        

    for i in range(4):
        FiguraNegyzet.x = Figura[i].x * Csempe
        FiguraNegyzet.y = Figura[i].y * Csempe
        pygame.draw.rect(GAME, pygame.Color('white'), FiguraNegyzet)

    pygame.display.flip()
    clock.tick()