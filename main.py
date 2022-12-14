import subprocess
subprocess.call(['pip', 'install', 'pygame'])
import pygame
from copy import deepcopy
from random import choice, randrange

############################################
# A játékmező 
Sz,M = 10,20
Csempe = 40
GAME_RES = Sz * Csempe, (M + 1) * Csempe
FPS = 60
pygame.init()
pygame.display.set_caption('Tetris')
GAME = pygame.display.set_mode(GAME_RES)
clock = pygame.time.Clock()
font = pygame.font.Font('font.ttf', Csempe-10)

FigurakKoordinatai = [  [(-1, 0), (-2, 0), (0, 0), (1, 0)],
                        [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                        [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                        [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                        [(0, 0), (0, -1), (0, 1), (-1, -1)],
                        [(0, 0), (0, -1), (0, 1), (1, -1)],
                        [(0, 0), (0, -1), (0, 1), (-1, 0)]]

Figurak = [[pygame.Rect(x + Sz // 2, y + 1, 1, 1) for x, y in FiguraHelyzet] for FiguraHelyzet in FigurakKoordinatai]
FiguraNegyzet = pygame.Rect(0,0, Csempe - 2, Csempe - 2)
Mezo = [[0 for i in range(Sz)] for j in range (M)]

animSzam, animSebesseg, animLimit = 0 ,8, 2000
Pont = 0
Pontok = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
getColor = lambda : (randrange(30,256), randrange(30,256), randrange(30,256) )
color = getColor()
Figura =  deepcopy(choice(Figurak))


#A grid létrehozása változóként, (x = oszop, y = sor, Szelesség, Magasság)
grid = [pygame.Rect(x * Csempe, y * Csempe, Csempe, Csempe) for x in range(Sz) for y in range(M)]   
PontokText = font.render('Pontok:', True, getColor())

def hitboxCheck():
    if Figura[i].x < 0 or Figura[i].x > Sz - 1:
        return False
    elif Figura[i].y > M - 1 or Mezo[Figura[i].y][Figura[i].x]:
        return False
    return True

while True:
    mozgasX, forgass = 0, False
    GAME.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mozgasX = -1
            elif event.key == pygame.K_RIGHT:
                mozgasX = 1
            elif event.key == pygame.K_DOWN:
                animLimit = 100 #gygorsab lesz az animacio
            elif event.key == pygame.K_UP:
                forgass = True # Forgatas
    # X tengelyen mozgás
    regi_Figura = deepcopy(Figura)
    for i in range(4):
        Figura[i].x += mozgasX
        if not hitboxCheck():
            Figura = deepcopy(regi_Figura)
            break
    # Y tengely mozgás
    animSzam += animSebesseg
    if animSzam > animLimit:
        animSzam = 0
        regi_Figura = deepcopy(Figura)
        for i in range(4):
            Figura[i].y += 1
            if not hitboxCheck():
                for i in range(4):
                   Mezo[regi_Figura[i].y][regi_Figura[i].x] = color
                color = getColor()
                Figura = deepcopy(choice(Figurak)) # uj random figurat felrak
                animLimit = 2000
                break

    #Forgatás
    forgoPont = Figura[0]
    regi_Figura = deepcopy(Figura)
    if forgass:
        for i in range(4):
            x = Figura[i].y - forgoPont.y
            y = Figura[i].x - forgoPont.x
            Figura[i].x = forgoPont.x - x
            Figura[i].y = forgoPont.y + y
            if not hitboxCheck():
                Figura = deepcopy(regi_Figura)
                break

    # Egész sor törlése
    vonal,vonalak = M-1, 0
    for sor in range(M -1,-1,-1):
        szamlalo = 0
        for i in range(Sz):
            if Mezo[sor][i]:
                szamlalo +=1
            Mezo[vonal][i] = Mezo[sor][i]
        if szamlalo < Sz:
            vonal -=1
        else:
            vonalak += 1
    Pont += Pontok[vonalak]

    #A grid kirajzolása: (Kijelző, (RGB szinek), i az maga a létrehozott grid ek tulajdonságai, milyne vastag a border)

    [pygame.draw.rect(GAME, (50,50,50), i , 1) for i in grid]         
    #Jelenleg eső figura rajzolása
    for i in range(4):
        FiguraNegyzet.x = Figura[i].x * Csempe
        FiguraNegyzet.y = Figura[i].y * Csempe
        pygame.draw.rect(GAME, color, FiguraNegyzet)

    #A befagyott figurák rajzolása
    for y, raw in enumerate(Mezo):
        for x, col in enumerate(raw):
            if col:
                FiguraNegyzet.x, FiguraNegyzet.y = x * Csempe, y * Csempe
                pygame.draw.rect(GAME, col, FiguraNegyzet)
    GAME.blit(PontokText, (10,M*Csempe-(Csempe*0.2)))
    GAME.blit(font.render(str(Pont), True, pygame.Color('white')), (4*Csempe,M*Csempe-(Csempe*0.2)))
    # GAME OVER
    for i in range(Sz):
        if Mezo[0][i]:
            Mezo = [[0 for i in range(Sz)] for j in range (M)]
            animSzam, animSebesseg, animLimit = 0 ,8, 2000
            Pont = 0
            for j in grid:
                pygame.draw.rect(GAME, getColor(), j)
                pygame.display.flip()
                clock.tick(200)
            pygame.time.delay(3000)
    pygame.display.flip()
    clock.tick()

