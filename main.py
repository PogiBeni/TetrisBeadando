import pygame
import osztalyok as o

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (350, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
vege = False
ora = pygame.time.Clock()
fps = 25
jatek = o.Tetris(20, 10)
szamlalo = 0

leNyomas = False

while not vege:
    if jatek.alak is None:
        jatek.ujAlak()
    szamlalo += 1
    if szamlalo > 100000:
        szamlalo = 0

    if szamlalo % (fps // jatek.level // 2) == 0 or leNyomas:
        if jatek.state == "start":
            jatek.lefele()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vege = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                jatek.Forgat()
            if event.key == pygame.K_DOWN:
                leNyomas = True
            if event.key == pygame.K_LEFT:
                jatek.oldalra(-1)
            if event.key == pygame.K_RIGHT:
                jatek.oldalra(1)
            if event.key == pygame.K_SPACE:
                jatek.ugras()
            if event.key == pygame.K_ESCAPE:
                jatek.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                leNyomas = False

    screen.fill(GRAY)

    for i in range(jatek.magassag):
        for j in range(jatek.szelesseg):
            pygame.draw.rect(screen, BLACK, [jatek.x + jatek.zoom * j, jatek.y + jatek.zoom * i, jatek.zoom, jatek.zoom], 1)
            if jatek.mezo[i][j] > 0:
                pygame.draw.rect(screen, o.szinek[jatek.mezo[i][j]],
                                 [jatek.x + jatek.zoom * j + 1, jatek.y + jatek.zoom * i + 1, jatek.zoom - 2, jatek.zoom - 1])

    if jatek.alak is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in jatek.alak.kep():
                    pygame.draw.rect(screen, o.szinek[jatek.alak.szin],
                                     [jatek.x + jatek.zoom * (j + jatek.alak.x) + 1,
                                      jatek.y + jatek.zoom * (i + jatek.alak.y) + 1,
                                      jatek.zoom - 2, jatek.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Pont: " + str(jatek.pont), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if jatek.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    ora.tick(fps)

pygame.quit()