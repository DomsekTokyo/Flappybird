from pygame import *
import random

init()

width = 900
height = 800
okno = display.set_mode((width, height))
display.set_caption("Happy Bird")

class Bird:
    def __init__(self):
        self.rychlost = 0
        self.gravitace = 0.5
        self.skok_sila = -10
        self.skok2 = True
        self.obrazek = image.load("ptak.png")
        self.obrazek_rect = self.obrazek.get_rect()
        self.obrazek_rect.center = (100, height // 2)

    def pohyb(self):
        self.rychlost += self.gravitace
        self.obrazek_rect.top += int(self.rychlost)

    def skok(self):
        if self.skok2:
            self.rychlost = self.skok_sila


class Game:
    def __init__(self, ptak):
        self.score = 0
        self.pohyb = 3
        self.pipes = []
        self.black = (0, 0, 0)
        self.font = font.SysFont("Arial", 30)
        self.biggerfont = font.SysFont("Arial", 60)
        self.ptak = ptak
        self.pause = False

        self.image_pipe_down = image.load("image_trubka.png")
        self.image_pipe_down = transform.smoothscale(self.image_pipe_down, (400, 800)).convert_alpha()
        self.image_pipe_up = transform.rotate(self.image_pipe_down, 180)

        self.image_back = image.load("image1.jpg")
        self.image_back = transform.scale(self.image_back, (width, height)).convert()

        self.spawn_timer = 100
        self.spawn_interval = 150



    def kolize_Podlaha(self):
        if self.ptak.obrazek_rect.bottom > height - 100:
            self.smrt()
    def kolize_Strop(self):
        if self.ptak.obrazek_rect.top < 0:
            self.ptak.obrazek_rect.top = 0
            self.ptak.rychlost = 0

    def update(self):
        self.pozadi()
        okno.blit(self.ptak.obrazek, self.ptak.obrazek_rect)
        text = self.font.render(f"Skóre: {self.score}", True, self.black)
        okno.blit(text, (20, 20))



        if not self.pause:
            self.trubky_pohyb()
            self.vykresli_trubky()
            self.ptak.pohyb()
            self.kolize_Podlaha()
            self.kolize_Strop()

        else:
            text = self.biggerfont.render("Hra skončila", True, self.black)
            textr = text.get_rect()
            textr.center = (width // 2, height // 2)
            okno.blit(text, textr)
            self.ptak.skok2 = False
            self.vykresli_trubky()
            if self.ptak.obrazek_rect.bottom < height - 80:
                self.ptak.rychlost += self.ptak.gravitace
                self.ptak.obrazek_rect.top += int(self.ptak.rychlost)
                if self.ptak.obrazek_rect.bottom > height - 80:
                    self.ptak.obrazek_rect.bottom = height - 80
                    self.ptak.rychlost = 0

    #blabla

    def trubky_pohyb(self):
        if self.pause:

            return

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            height1 = random.randint(height + 200, height + 500)
            self.pipes.append({
                'down': self.image_pipe_down.copy(),
                'up': self.image_pipe_up.copy(),
                'rect_down': self.image_pipe_down.get_rect(bottomright=(width + 300, height1)),
                'rect_up': self.image_pipe_up.get_rect(bottomright=(width + 300, height1 - height)),
                'passed': False
            })

        new_pipes = []
        for pipe in self.pipes:
            pipe['rect_down'].left -= self.pohyb
            pipe['rect_up'].left -= self.pohyb

            kolizni_rect_down = pipe['rect_down'].inflate(-260, -260)
            kolizni_rect_up = pipe['rect_up'].inflate(-260, -260)

            if self.ptak.obrazek_rect.colliderect(kolizni_rect_up) or self.ptak.obrazek_rect.colliderect(kolizni_rect_down):
                self.smrt()
                break

            pipe_center_x = pipe['rect_down'].left + pipe['rect_down'].width // 2
            if not pipe['passed'] and self.ptak.obrazek_rect.centerx > pipe_center_x:
                pipe['passed'] = True
                self.score += 1

            if pipe['rect_down'].right > 0:
                new_pipes.append(pipe)

        self.pipes = new_pipes

    def vykresli_trubky(self):
        for pipe in self.pipes:
            okno.blit(pipe['down'], pipe['rect_down'])
            okno.blit(pipe['up'], pipe['rect_up'])

    def pozadi(self):
        okno.blit(self.image_back, (0, 0))
        draw.rect(okno, (0, 255, 0), (0, height - 100, width, 80))
        draw.rect(okno, (181, 101, 29), (0, height - 30, width, 100))

    def smrt(self):

        self.pause = True

    def zacatek(self):
        self.pozadi()
        zacatek = self.biggerfont.render("Stisknutím mezerníku hru začnete", True, self.black)
        textr = zacatek.get_rect()
        textr.center = (width // 2, height // 2)
        okno.blit(zacatek, textr)
    def start(self):
        # reset ptáka
        self.ptak.obrazek_rect.center = (100, height // 2)
        self.ptak.rychlost = 0
        self.ptak.skok2 = True
        # reset trubek
        self.pipes = []
        self.spawn_timer = 100
        # reset skóre a pauza
        self.score = 0
        self.pause = False



ptak = Bird()
hra = Game(ptak)

fps = 60
clock = time.Clock()
hra_zacala = False
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            if not hra_zacala:
                hra.start()
                hra_zacala = True
            else:
                hra.ptak.skok()
    if not hra_zacala:
        hra.zacatek()
    else:

        hra.update()

    display.update()
    clock.tick(fps)

quit()



