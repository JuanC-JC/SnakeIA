import pygame
from Snake import Snake
from grid import Grid
from Algoritms import pathFinder


class Game():

    manually = 0
    automatic = 1


    #renderizando la busqueda dijkstra cuadro por cuadro
    AnimationDijkstraSearch = 1

    #renderizando la serpiente
    AnimationSnake = 2

    AnimationNone = 3

    AnimationWining = 4

    #iterando la serpiente por un camino hasta la comida
    foodPath = 3

    #iterando hasta la cola
    tailPath = 4

    #no encontro ruta por ningun
    WithoutPath = 5

    #no esta haciendo nada, a espera
    Waiting = 6

    #wining
    Win = 7



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

        self.grid = Grid(rows,columns)

        self.snake = Snake(rows,columns,self)

        self.run = True

        self.FPS = 5

        self.mode = Game.manually

        self.statusAnimation = Game.AnimationNone

        self.statusSearch = Game.WithoutPath

        self.PathFinder = pathFinder(self.grid,self.snake)

        self.shortPath = []

        self.longPath = []

        self.visitInOrder = []

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
                self.snake.update(events)

            else:
                pass
                #cuando deberia ejecutarse esto?

                #generar una ruta corta
                    #si encuentro la ruta corta


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


            if self.mode == Game.manually:
                self.drawBackground((64, 62, 65))
                self.snake.drawBody()
                self.snake.drawFood()
                self.drawGrid((160,160,160))

            #si el modo es automatico
            elif self.mode == Game.automatic:
                self.update()

                #buscar la ruta corta, si

            pygame.display.update()

            self.clock.tick(self.FPS)
    
    def drawNode(self,nodo,color):

        newSize = self.sizeSquare * 0.8

        suma = self.sizeSquare * 0.1

        newPosx = (nodo.col * self.sizeSquare) + suma

        newPosy = (nodo.row * self.sizeSquare) + suma

        # pygame.draw.rect(self.window,color,(nodo.col*self.sizeSquare,nodo.row*self.sizeSquare, self.sizeSquare,self.sizeSquare))
        pygame.draw.rect(self.window,color,(newPosx,newPosy, newSize , newSize))


    def drawNodeLine(self,nodo,color):
        pygame.draw.line(self.window,(x,y,grosor))

    def drawBackground(self,color):

        pygame.draw.rect(self.window,color,(0,0,self.width,self.height))

    def drawGrid(self,color):

        #lineas en el eje x
        for pos_x in range(self.columns):
            pygame.draw.line(self.window,color,(pos_x*self.sizeSquare,0),(pos_x*self.sizeSquare,self.height))

        #lineas en el eje y 
        for pos_y in range(self.rows):
            pygame.draw.line(self.window,color,(0,pos_y*self.sizeSquare),(self.width,pos_y*self.sizeSquare))

    def update(self):

        #si no he ganado
        if self.statusSearch != Game.Win:

            #generar una ruta corta si no me encuentro ya en una ruta hasta la comida, osea o esta esperando o esta en una ruta larga
            if self.statusSearch != Game.foodPath:
                values = self.PathFinder.dijkstra(self.snake.head,self.snake.food)

                #si encuentro la ruta corta
                if values[0]:

                    #crear una serpiente fake y moverla hasta la comida 
                    snakeCopy = self.snake.copy()

                    shortpathCopy = values[1][1:].copy()

                    #mueve la serpiente
                    while len(shortpathCopy) >0:
                    
                        #si el gana no necesito nada mas del algoritmo
                        snakeCopy.updateIA(shortpathCopy.pop(0))

                    #si el gana no necesito nada mas del algoritmo
                    if snakeCopy.status == Snake.wining:

                        #ruta corta sin cabeza
                        self.shortPath = values[1][1:]

                        #elimino la cabeza y la comida del orden de visita para que no los dibuje 
                        self.visitInOrder = values[2][1:-1]

                        self.statusSearch = Game.foodPath

                        self.statusAnimation = Game.AnimationDijkstraSearch

                    #si no gano con esa ruta corta, debo seguir con el algoritmo
                    else:
                        #luego averiguar si existe una ruta corta hasta la cola
                        pathFinderFake = pathFinder(self.grid,snakeCopy)
                        
                        valuesFake = pathFinderFake.dijkstra(snakeCopy.head, snakeCopy.body[len(snakeCopy.body)-1])

                        #si existe esa ruta hasta la cola
                        if valuesFake[0]:
                            
                            #ruta corta sin cabeza
                            self.shortPath = values[1][1:]

                            #elimino la cabeza y la comida del orden de visita para que no los dibuje 
                            self.visitInOrder = values[2][1:-1]

                            self.statusSearch = Game.foodPath

                            self.statusAnimation = Game.AnimationDijkstraSearch

                        #si no encuentra camino hasta la cola con la serpiente fake
                        else:
                            
                            #me encuentro en un camino largo?
                            if self.statusSearch == Game.tailPath:

                                if len(self.shortPath) >0:
                                    node = self.shortPath.pop(0)
                                    self.snake.updateIA(node)
                                else:
                                    self.statusSearch = Game.Waiting


                            #hacer un camino hasta la cola pero con la serpiente original antes de morir
                            elif self.statusSearch == Game.Waiting:

                                #genero la ruta hasta la cola desde la serpiente original
                                values = self.PathFinder.dijkstra(self.snake.head,self.snake.body[len(self.snake.body)-1])
                                                    #si encontro el camino hasta la cola
                                if values[0]:

                                    longPath = self.PathFinder.ExtendRute(values[1])
                                
                                    #ruta larga sin cabeza ni cola, asi evito morir ya que no puedo moverme hasta la cola
                                    self.shortPath = longPath[1:]

                                    self.statusSearch = Game.tailPath

                                    # #dibuja cuando es camino hacia la cola
                                    if self.statusSearch == Game.tailPath:
                                        for node in range(len(longPath)):
                                            

                                            first = longPath[node]
                                            firstx = first.col * self.sizeSquare + (self.sizeSquare//2)
                                            firsty = first.row * self.sizeSquare + (self.sizeSquare//2)


                                            if node < len(longPath)-1:
                                                second = longPath[node+1]
                                                secondx = second.col * self.sizeSquare + (self.sizeSquare//2)
                                                secondy = second.row * self.sizeSquare + (self.sizeSquare//2)

                                                pygame.draw.line(self.window,(243, 156, 18),(firstx,firsty),(secondx,secondy),1)


                                        pygame.display.update()

                                    #animo la serpiente hasta la cola
                                    self.statusAnimation = Game.AnimationSnake

                                    print("encontre un camino a la comida pero no me sirve as iq ue me voy por un camino hasta la cola")

                                else:
                                    print("morire")
                                    

                
                #si no encuentra la primer ruta corta
                else: 
                    
                    if self.statusSearch == Game.tailPath:
                        if len(self.shortPath) >0:
                            node = self.shortPath.pop(0)
                            self.snake.updateIA(node)

                        else:
                            self.statusSearch = Game.Waiting


                    #si no me encuentro en un camino largo, osea acabe de comer, waiting
                    elif self.statusSearch == Game.Waiting:

                        #genero la ruta hasta la cola desde la serpiente original
                        values = self.PathFinder.dijkstra(self.snake.head,self.snake.body[len(self.snake.body)-1])

                        #si encontro el camino hasta la cola
                        if values[0]:

                            longPath = self.PathFinder.ExtendRute(values[1])
                        
                            #ruta larga sin cabeza ni cola, asi evito morir ya que no puedo moverme hasta la cola
                            self.shortPath = longPath[1:]

                            self.statusSearch = Game.tailPath

                            # #dibuja cuando es camino hacia la cola
                            if self.statusSearch == Game.tailPath:
                                for node in range(len(longPath)):
                                    

                                    first = longPath[node]
                                    firstx = first.col * self.sizeSquare + (self.sizeSquare//2)
                                    firsty = first.row * self.sizeSquare + (self.sizeSquare//2)


                                    if node < len(longPath)-1:
                                        second = longPath[node+1]
                                        secondx = second.col * self.sizeSquare + (self.sizeSquare//2)
                                        secondy = second.row * self.sizeSquare + (self.sizeSquare//2)

                                        pygame.draw.line(self.window,(243, 156, 18),(firstx,firsty),(secondx,secondy),1)


                                pygame.display.update()

                            #animo la serpiente hasta la cola
                            self.statusAnimation = Game.AnimationSnake

                            print("no encontre ruta a comida, voy hasta la cola")

                        else:
                            print("")


            #si ya me encuentro en una ruta hasta la comida
            else:
                
                #si estoy animando la serpiente debo evaluar esto 
                if self.statusAnimation == Game.AnimationSnake:
                    #nodo a moverme

                    node = self.shortPath.pop(0)

                    #si esta comiendo
                    self.snake.updateIA(node) 

                    if self.snake.status == Snake.eating:
                        self.statusSearch = Game.Waiting
                        self.statusAnimation = Game.AnimationNone

                    elif self.snake.status == Snake.wining:
                        self.statusAnimation = Game.AnimationWining
                        self.statusSearch = Game.Win

                    else: 
                        self.statusAnimation = Game.AnimationSnake


        #SOLO DIBUJO

        #si esta animando la busqueda dijkstra y el estatus de busqueda es hacia la comida o hacia la cola
        if self.statusAnimation == Game.AnimationDijkstraSearch:
            self.FPS = 100
            #no necesito renderizar de nuevo todo, solo dibujar la busqueda encima de lo que exista
            
            #dibujar si el search es para la busqueda ha la comida
            if self.statusSearch == Game.foodPath:
            
                #dibujar nodo por nodo 
                if len(self.visitInOrder)>0:
                    node = self.visitInOrder.pop(0)

                    self.drawNode(node,(75, 0, 130))

                #terminado de dibujar todo el dijkstra
                else:
                    #cambia el estado de animacion para dibujar la serpiente
                    self.statusAnimation = Game.AnimationSnake


                #dibujo el grid encima de todo
                self.drawGrid((160,160,160))

        #dibujar la serpiente
        elif self.statusAnimation == Game.AnimationSnake:
            self.FPS = 40
            #dibujar el fondo
            self.drawBackground((64, 62, 65))


            #dibuja cuando es camino a comida
            if self.statusSearch == Game.foodPath:
                #dibujar la ruta corta, si no existe no hay problema
                for node in self.shortPath:
                    self.drawNode(node,(243, 156, 18))

            #dibuja cuando es camino hacia la cola
            elif self.statusSearch == Game.tailPath:

                for node in range(len(self.shortPath)):
                    

                    first = self.shortPath[node]
                    firstx = first.col * self.sizeSquare + (self.sizeSquare//2)
                    firsty = first.row * self.sizeSquare + (self.sizeSquare//2)


                    if node < len(self.shortPath)-1:
                        second = self.shortPath[node+1]
                        secondx = second.col * self.sizeSquare + (self.sizeSquare//2)
                        secondy = second.row * self.sizeSquare + (self.sizeSquare//2)

                        pygame.draw.line(self.window,(243, 156, 18),(firstx,firsty),(secondx,secondy),1)

            #dibujar la serpiente
            self.snake.drawBody()
            self.snake.drawFood()

            #dibujar las lineas
            self.drawGrid((160,160,160))
        
        #dibuja la serpiente sin ruta corta
        elif self.statusAnimation == Game.AnimationNone:
            self.FPS = 40
            #dibujar el fondo
            self.drawBackground((64, 62, 65))

            #dibujar la serpiente
            self.snake.drawBody()
            self.snake.drawFood()

            #dibujar las lineas
            self.drawGrid((160,160,160))
        
        elif self.statusAnimation == Game.AnimationWining:
            self.FPS = 10
            #dibujar el fondo
            self.drawBackground((64, 62, 65))

            #dibujar la serpiente
            self.snake.drawBody()

            #dibujar las lineas
            self.drawGrid((160,160,160))

            print("GANADORRRRR OE OE OE OE ")
            
if __name__ == "__main__":
    
    juego = Game(10,10,40)

    juego.controlador()
