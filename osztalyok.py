import random as rnd

szinek = [
    (229,18,18),
    (0,204,0),
    (96,96,96),
    (255,153,51),
    (255,155,51),
    (204,51,255),
    (51,204,204)
]

class Alak:
    x = 0
    y = 0
    alakok = [
        [[1,2,5,6]],
        [[1,5,9,13],[4,5,6,7]], #Ez a vonal és a forgatésai
        [[4,5,9,10],[2,6,5,9]],
        [[6,7,9,10],[1,5,6,10]],
        [[1,2,5,9],[0,4,5,6],[1,5,9,8],[4,5,6,10]],
        [[1,2,6,10],[5,6,7,9],[2,6,10,11],[3,5,6,7]],
        [[1,4,5,6],[1,4,5,9],[4,5,6,9],[1,5,6,9]]
    ]

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tipus = rnd.randint(0,len(self.alakok)-1)
        self.szin = rnd.randint(1,len(szinek)-1)
        self.forgatas = 0

    def kep(self):
        return self.alakok[self.tipus][self.forgatas]

    def forgat(self):
        self.forgatas = (self.forgatas + 1) % len(self.alakok[self.tipus])



class Tetris:
    level = 2
    pont = 0
    allapot = "start"
    mezo = []
    magassag = 0
    szelesseg = 0
    x = 100
    y = 60
    zoom = 20
    alak = None

    def __init__(self,magassag,szelesseg):
        self.magassag = magassag
        self.szelesseg = szelesseg
        self.mezo = []
        self.pont = 0
        self.state = "start"
        for i in range(magassag):
            ujSor = []
            for j in range(szelesseg):
                ujSor.append(0)
            self.mezo.append(ujSor)
        
    def ujAlak(self): # Uj alakot hoz létre és a kezdő koordinétékra helyezi
        self.alak = Alak(3,0)
    
    def erintkezik(self): # Meg kell nézni hogy érintkezik e az alak egy másikkal, 0 jelenti hogy üres a mező
        erint = False
        for i in range(4):
            for j in range(4):
                if i*4 + j in self.alak.kep():
                    if i + self.alak.y > self.magassag - 1 or j + self.alak.x > self.szelesseg - 1 or j + self.alak.x < 0 or self.mezo[i + self.alak.y][j + self.alak.x] > 0:
                        erint = True
        return erint

    def elhelyez(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.alak.kep():
                    self.mezo[i + self.alak.y][j + self.alak.x] = self.alak.szin
        self.sorTores()
        self.ujAlak()
        if self.erintkezik():
            self.allapot = "gameover"

    def sorTores(self):
            lines = 0
            for i in range(1, self.magassag):
                nullak = 0
                for j in range(self.szelesseg):
                    if self.mezo[i][j] == 0:
                        nullak += 1
                if nullak == 0:
                    lines += 1
                    for i1 in range(i, 1, -1):
                        for j in range(self.szelesseg):
                            self.mezo[i1][j] = self.mezo[i1 - 1][j]
            self.pont += lines ** 2

    def ugras(self):
        while not self.erintkezik():
            self.alak.y += 1
        self.alak.y -= 1
        self.elhelyez()

    def lefele(self):
        self.alak.y += 1
        if self.erintkezik():
            self.alak.y -= 1
            self.elhelyez()

    def oldalra(self, dx):
        old_x = self.alak.x
        self.alak.x += dx
        if self.erintkezik():
            self.alak.x = old_x

    def Forgat(self):
        regiForgatas = self.alak.forgatas
        self.alak.forgat()
        if self.erintkezik():
            self.alak.forgatas = regiForgatas