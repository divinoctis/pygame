import pygame as py

screen = py.display.set_mode((1600, 900))

class Platform :

    def __init__(self):
        rect = py.Rect(0, 0, 20, 20)
        rect.center = screen.get_rect().center