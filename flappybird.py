from pygame import *
init()

class Bird:
    def __init__(self):
        pass



class Game:
    def __init__(self):
        pass

    def update(self):
        self.pozadi()
        self.trubky()





    def trubky(self):
        image_pipe_down = image.load("image_trubka.png")
        image_pipe_down = transform.smoothscale(image_pipe_down, (400, 400))
        image_pipe_rect_down = image_pipe_down.get_rect()
        image_pipe_rect_down.bottomright= (width-100,height+100)

        image_pipe_up= image.load("image_trubka.png")
        image_pipe_up = transform.smoothscale(image_pipe_down, (400, 400))
        image_pipe_up = transform.rotate(image_pipe_up, 180)
        image_pipe_rect_up = image_pipe_up.get_rect()
        image_pipe_rect_up.topright = (width - 100,-100)

        okno.blit( image_pipe_up,image_pipe_rect_up)
        okno.blit(image_pipe_down, image_pipe_rect_down)


    def pozadi(self):
        image_back = image.load("image1.jpg")
        image_back_rect = image_back.get_rect()
        image_back_rect.center = (width // 2, height // 2)
        okno.blit(image_back, image_back_rect)




class Menu:
    def __init__(self):
        pass

width = 900
height = 800
okno = display.set_mode((width, height))
display.set_caption("Happy Bird")

hra = Game()
hra.trubky()
fps = 60
time = time.Clock()


yes = True
while yes:
    for a in event.get():
        if a.type == QUIT:
            yes = False
    display.update()

    time.tick(fps)
quit()