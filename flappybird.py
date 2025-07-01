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
        self.score = 0
        self.pohyb = 3
        self.pipes = []
        self.black = (0, 0, 0)
        self.font = font.SysFont("Arial", 30)
        self.ptak = ptak

        self.image_pipe_down = image.load("image_trubka.png")
        self.image_pipe_down = transform.smoothscale(self.image_pipe_down, (400, 800)).convert_alpha()
        self.image_pipe_up = transform.rotate(self.image_pipe_down, 180)

        self.image_back = image.load("image1.jpg")
        self.image_back = transform.scale(self.image_back, (width, height)).convert()

        self.spawn_timer = 100
        self.spawn_interval = 150

    def update(self):
        self.pozadi()
        self.trubky_pohyb()
        self.ptak.pohyb()
        okno.blit(self.ptak.obrazek, self.ptak.obrazek_rect)

        text = self.font.render(f"Skóre: {self.score}", True, self.black)
        okno.blit(text, (20, 20))

    def trubky_pohyb(self):
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

            okno.blit(pipe['down'], pipe['rect_down'])
            okno.blit(pipe['up'], pipe['rect_up'])


            pipe_center_x = pipe['rect_down'].left + pipe['rect_down'].width // 2


            if not pipe['passed'] and self.ptak.obrazek_rect.centerx > pipe_center_x:
                pipe['passed'] = True
                self.score += 1


            if pipe['rect_down'].right > 0:
                new_pipes.append(pipe)

        self.pipes = new_pipes

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