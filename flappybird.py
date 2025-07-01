from pygame import *
import random

init()

class Bird:
    def __init__(self):
        self.pohybek = 3
        self.mili_count = 0
        self.count = 0

        self.obrazek = image.load("ptak.png")
        self.obrazek_rect = self.obrazek.get_rect()
        self.obrazek_rect.center = (100, height // 2)

        self.rychlost = 0
        self.gravitace = 0.5
        self.skok_sila = -10

    def pohyb(self):
        self.rychlost += self.gravitace  # gravitace přidává akceleraci do rychlosti
        self.obrazek_rect.top += int(self.rychlost)  # rychlost pak posune ptáka



    def skok(self):
        self.rychlost = self.skok_sila







class Game:
    def __init__(self, ptak):
        self.pohyb = 3
        self.count = 0
        self.mili_count = 0
        self.pipes = []
        self.difficult = 2
        self.image_pipe_down = image.load("image_trubka.png")
        self.image_pipe_down = transform.smoothscale(self.image_pipe_down, (400, 800)).convert_alpha()
        #ta nahore ktera je smerem dolu
        self.image_pipe_up = transform.rotate(self.image_pipe_down, 180)
        self.ptak = ptak
        self.image_back = image.load("image1.jpg")
        self.image_back = transform.scale(self.image_back, (width, height)).convert()

        self.trubky_vytvoreni(height+400)

    def update(self):
        self.pozadi()
        self.trubky_pohyb()
        self.ptak.pohyb()
        okno.blit(self.ptak.obrazek, self.ptak.obrazek_rect)


    def trubky_pohyb(self):
        self.mili_count += 2
        if self.mili_count > fps:
            self.count += 1
            self.mili_count = 0
        if self.count == 5:
            self.count = 0
            height1 = random.randint(height+200, height + 500)

            self.trubky_vytvoreni(height1)

        new_pipes = []
        for image, rect in self.pipes:
            rect.left -= self.pohyb
            if rect.right > 0:
                new_pipes.append((image, rect))
                okno.blit(image, rect)
        self.pipes = new_pipes

    def trubky_vytvoreni(self, height1):
        #ta horni smerem dolu
        image_pipe_rect_down = self.image_pipe_down.get_rect()
        #prevedolni strana
        image_pipe_rect_down.bottomright = (width + 300, height1)

        image_pipe_rect_up = self.image_pipe_up.get_rect()
        image_pipe_rect_up.bottomright= (width + 300, height1 - height)

        self.pipes.append((self.image_pipe_down.copy(), image_pipe_rect_down))
        self.pipes.append((self.image_pipe_up.copy(), image_pipe_rect_up))
    #xd
    def pozadi(self):
        okno.blit(self.image_back, (0, 0))
        draw.rect(okno, (0, 255, 0), (0, height - 100, width, 80))
        draw.rect(okno, (181, 101, 29), (0, height - 30, width, 100))



class Menu:
    def __init__(self):
        pass

width = 900
height = 800
okno = display.set_mode((width, height))
display.set_caption("Happy Bird")

ptak = Bird()
hra = Game(ptak)

fps = 60
time = time.Clock()


yes = True
while yes:
    for a in event.get():
        if a.type == QUIT:
            yes = False
        if a.type == KEYDOWN and a.key == K_SPACE:
            ptak.skok()


    hra.update()
    display.update()
    time.tick(fps)
quit()