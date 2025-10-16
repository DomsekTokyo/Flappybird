import time
from pygame import *
import random

# Inicializace mixeru a hudby
mixer.init()
mixer.music.load("puzzle.mp3")
mixer.music.set_volume(0.05)
mixer.music.play(-1)

# Inicializace Pygame
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
        self.czas = None

        # Obrazky
        self.image_pipe_down = transform.smoothscale(image.load("image_trubka.png"), (400, 800)).convert_alpha()
        self.image_pipe_up = transform.rotate(self.image_pipe_down, 180)
        self.image_back = transform.scale(image.load("pozadi.jpg"), (width, height)).convert()
        self.imagegrass = transform.scale(image.load("Vrstva 1.png"), (1000, 100))

        # Spawn trubek
        self.spawn_timer = 100
        self.spawn_interval = 150

        # Volume button
        self.pausevolume = True  # True = hudba zapnuta
        self.volume = Rect(width-120, 20, 100, 50)

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
        color = (0, 200, 0) if self.pausevolume else (200, 0, 0)

        textvol = self.font.render("Volume", True, (0, 0, 0))

        if not self.pause:
            self.trubky_pohyb()
            self.vykresli_trubky()
            self.ptak.pohyb()
            self.kolize_Podlaha()
            self.kolize_Strop()
            # Skóre
            text = self.font.render(f"Skóre: {self.score}", True, (0, 0, 0))
            draw.rect(okno, (0, 255, 0), (11, 11, 130, 60), border_radius=10)
            draw.rect(okno, (255, 255, 255), (10, 10, 130, 60), border_radius=10, width=5)
            okno.blit(text, (20, 20))
        else:
            text = self.biggerfont.render("Hra skončila", True, self.black)
            text2 = self.biggerfont.render("Stiskněte mezerník pro pokračování", True, self.black)
            textr = text.get_rect(center=(width//2, height//2))
            textr2 = text2.get_rect(center=(width//2, height//2 + 100))
            self.ptak.skok2 = False
            self.vykresli_trubky()
            draw.rect(okno, (0, 255, 0), (40, 350, 820, 200), border_radius=10)
            draw.rect(okno, (255, 255, 255), (40, 350, 820, 200), border_radius=10, width=5)
            okno.blit(text, textr)
            okno.blit(text2, textr2)
            if self.ptak.obrazek_rect.bottom < height - 80:
                self.ptak.rychlost += self.ptak.gravitace
                self.ptak.obrazek_rect.top += int(self.ptak.rychlost)
                if self.ptak.obrazek_rect.bottom > height - 80:
                    self.ptak.obrazek_rect.bottom = height - 80
                    self.ptak.rychlost = 0
        draw.rect(okno, color, self.volume, border_radius=5)
        okno.blit(textvol, (self.volume.x + 10, self.volume.y + 10))
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
        okno.blit(self.imagegrass, (0, 700))



    def smrt(self):
        self.pause = True
        self.czas = time.get_ticks()

    def zacatek(self):
        self.pozadi()
        zacatek = self.biggerfont.render("Stisknutím mezerníku hru začnete", True, self.black)
        textr = zacatek.get_rect(center=(width // 2, height // 2))
        draw.rect(okno, (0, 255, 0), (40, 350, 820, 100), border_radius=10)
        draw.rect(okno, (255, 255, 255), (40, 350, 820, 100), border_radius=10, width=5)
        okno.blit(zacatek, textr)

    def start(self):
        self.ptak.obrazek_rect.center = (100, height // 2)
        self.ptak.rychlost = 0
        self.ptak.skok2 = True
        self.pipes = []
        self.spawn_timer = 100
        self.score = 0
        self.pause = False

# Spuštění hry
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
        elif e.type == MOUSEBUTTONDOWN:
            if hra.volume.collidepoint(e.pos):
                hra.pausevolume = not hra.pausevolume
                mixer.music.set_volume(0.05 if hra.pausevolume else 0)
        elif e.type == KEYDOWN and e.key == K_SPACE:
            if not hra_zacala:
                hra.start()
                hra_zacala = True
            elif hra.pause and time.get_ticks() - hra.czas >= 1000:
                hra.start()
            else:
                hra.ptak.skok()

    if not hra_zacala:
        hra.zacatek()
    else:
        hra.update()

    display.update()
    clock.tick(fps)

quit()
