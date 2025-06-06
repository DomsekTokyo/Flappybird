from pygame import *
init()



width = 900
height = 800
okno = display.set_mode((width, height))

fps = 60
time = time.Clock()


yes = True
while yes:
    for a in event.get():
        if a.type == QUIT:
            yes = False

quit()