from pygame import *
init()

class Bird:
    def __init__(self):
        pass



class Game:
    def __init__(self):
        self.pohyb = 3
        self.count = 0
        self.mili_count = 0
        self.pipes = []

        self.image_pipe_down = image.load("image_trubka.png")
        self.image_pipe_down = transform.smoothscale(self.image_pipe_down, (400, 400)).convert_alpha()
        self.image_pipe_up = transform.rotate(self.image_pipe_down, 180)

        self.image_back = image.load("image1.jpg")
        self.image_back = transform.scale(self.image_back, (width, height)).convert()

        self.trubky_vytvoreni()

    def update(self):
        self.pozadi()
        self.trubky_pohyb()

    def trubky_pohyb(self):
        self.mili_count += 3
        if self.mili_count > fps:
            self.count += 1
            self.mili_count = 0
        if self.count == 5:
            self.count = 0
            self.trubky_vytvoreni()

        new_pipes = []
        for image, rect in self.pipes:
            rect.left -= self.pohyb
            if rect.right > 0:
                new_pipes.append((image, rect))
                okno.blit(image, rect)
        self.pipes = new_pipes

    def trubky_vytvoreni(self):
        image_pipe_rect_down = self.image_pipe_down.get_rect()
        image_pipe_rect_down.bottomright = (width + 300, height)

        image_pipe_rect_up = self.image_pipe_up.get_rect()
        image_pipe_rect_up.topright = (width + 300, -100)

        self.pipes.append((self.image_pipe_down.copy(), image_pipe_rect_down))
        self.pipes.append((self.image_pipe_up.copy(), image_pipe_rect_up))

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

hra = Game()

fps = 60
time = time.Clock()


yes = True
while yes:
    for a in event.get():
        if a.type == QUIT:
            yes = False


    hra.update()
    display.update()
    time.tick(fps)
quit()