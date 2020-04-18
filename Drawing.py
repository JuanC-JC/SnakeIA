
import pygame
from ModelGame import juego
#creo un grid y que hago?

#metodos de dibujado, osea como renderizzara todo  #necesito unos fps

class draw():

    Game = juego

    @staticmethod
    def Node(window,nodo,color):

        pygame.draw.rect(draw.Game.window,color,(nodo.col*draw.Game.sizeSquare,nodo.row*draw.Game.sizeSquare, draw.Game.sizeSquare,draw.Game.sizeSquare))
    
    @staticmethod
    def background(window,color):

        pygame.draw.rect(draw.Game.window,color,(0,0,draw.Game.width,draw.Game.height))

    @staticmethod
    def grid(window,color):

        #lineas en el eje x
        for pos_x in range(draw.Game.columns):
            pygame.draw.line(draw.Game.window,color,(pos_x*draw.Game.sizeSquare,0),(pos_x*draw.Game.sizeSquare,draw.Game.height))

        #lineas en el eje y 
        for pos_y in range(draw.Game.rows):
            pygame.draw.line(draw.Game.window,color,(0,pos_y*draw.Game.sizeSquare),(draw.Game.width,pos_y*draw.Game.sizeSquare))
    
