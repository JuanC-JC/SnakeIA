import pygame
from Snake import Snake


class Game():

    manually = 0
    automatic = 1

    #iterando la serpiente por el camino mas largo
    longPath = 0

    #renderizando la busqueda dijkstra cuadro por cuadro
    DijkstraSearch = 1

    #iterando la serpiente por un camino hasta la comida
    shortPath = 2

    #no esta haciendo nada, a espera
    Waiting = 3

    #dibujandola normal
    normally = 4

    #inicializar el juego, crear todo
    def __init__(self,rows,columns,sizeSquare):

        #inicializo pygame
        self.width = sizeSquare * columns
        self.height =  sizeSquare * rows

        self.sizeSquare = sizeSquare

        self.rows = rows
        
        self.columns = columns
 
        self.window = pygame.display.set_mode((self.width,self.height))

        pygame.display.set_caption("Dijkstra IA")

        self.clock = pygame.time.Clock()

        self.snake = Snake(rows,columns,self)

        #creo el grid
        # self.grid = Grid(rows,columns,sizeSquare,self)

        self.run = True

        self.FPS = 5

        self.mode = Game.manually

        self.statusAnimation = Game.Waiting

    def controlador(self):
        
        while self.run:

            events = pygame.event.get()


            if pygame.QUIT in [event.type for event in events]:

                self.run = False


            #permite cambiar el modo de juego
            if pygame.K_SPACE in [event.key for event in events if event.type == pygame.KEYUP]:

                if self.mode == Game.manually:self.mode = Game.automatic

                else: self.mode = Game.manually

            #si el modo de juego es manual
            if self.mode == Game.manually:

                self.statusAnimation = Game.normally
                
                self.snake.update(events)

            else:
                
                #aca se actualizarian los eventos para el modo automatico
                pass
                    
                #generar una ruta corta

                    #si encuentro al ruta corta
                        #crear una sepriente fake y moverla hasta la comida

                        #luego averiguar si existe una ruta corta hasta la cola

                            #si no encuentra camino hasta la cola con la serpiente fake

                                #si me encuentro ya en un camino largo
                                    #seguir en el

                                #si no me encuentro en un camino largo
                                    #generar el camino mas largo desde la serpiente original hasta la cola

                            

                    #si no existe ruta corta

                            #si me encuentro ya en un camino largo
                                #seguir en el

                            #si no me encuentro en un camino largo
                                #generar el camino mas largo desde la serpiente original hasta la cola

                

            if self.statusAnimation == Game.normally:
                self.drawbackground((64, 62, 65))
                self.snake.drawBody()
                self.snake.drawFood()
                self.drawgrid((160,160,160))

            pygame.display.update()

            self.clock.tick(self.FPS)
    
    def drawNode(self,nodo,color):

        pygame.draw.rect(self.window,color,(nodo.col*self.sizeSquare,nodo.row*self.sizeSquare, self.sizeSquare,self.sizeSquare))
    
    def drawbackground(self,color):

        pygame.draw.rect(self.window,color,(0,0,self.width,self.height))

    def drawgrid(self,color):

        #lineas en el eje x
        for pos_x in range(self.columns):
            pygame.draw.line(self.window,color,(pos_x*self.sizeSquare,0),(pos_x*self.sizeSquare,self.height))

        #lineas en el eje y 
        for pos_y in range(self.rows):
            pygame.draw.line(self.window,color,(0,pos_y*self.sizeSquare),(self.width,pos_y*self.sizeSquare))



if __name__ == "__main__":
    
    juego = Game(15,15,30)

    juego.controlador()
