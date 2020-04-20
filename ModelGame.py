import pygame
from Snake import Snake
from grid import Grid
from Algoritms import pathFinder


class Game():

    manually = 0
    automatic = 1

    #ESTADOS DE ANIMACION
    #renderizando la busqueda dijkstra cuadro por cuadro
    AnimationDijkstraSearch = 1

    #renderizando movimiento de serpiente, puede ser hata ruta larga o ruta corta
    AnimationSnake = 2

    #no esta animando nada, ejemplo, la serpiente acabo de comer y durante un frame, el apenas esta recalcundo el algoritmo
    AnimationNone = 3

    #animando cuando gano, es igual a la animacion de none, sin embargo imprime que "gano" en la siguiente version saldra un texto
    #diciendo que gano o algo asi :v
    AnimationWining = 4


    #ESTADOS DE BUSQUEDA, son diferentes a los estados de animacion 
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

        #crea un objeto grid, que contiene nodos 
        self.grid = Grid(rows,columns)

        #crea una serpiente principal
        self.snake = Snake(rows,columns,self)

        self.run = True

        self.FPS = 5

        self.mode = Game.manually

        self.statusAnimation = Game.AnimationNone

        self.statusSearch = Game.WithoutPath

        #objeto para permitir busquedas desde la serpiente original
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



            if self.mode == Game.manually:
                self.FPS = 5
                self.snake.update(events)

                self.drawBackground((64, 62, 65))
                self.snake.drawBody()
                self.snake.drawFood()
                self.drawGrid((160,160,160))

            #si el modo es automatico
            elif self.mode == Game.automatic:
                self.update()
                self.Render()

                #buscar la ruta corta, si

            pygame.display.update()

            self.clock.tick(self.FPS)
    
    def drawNode(self,nodo,color):

        '''Dibuja un nodo centrado respecto a la posicion del grid que le corresponde y
        con solo un 80 % del tamaño'''

        newSize = self.sizeSquare * 0.8

        suma = self.sizeSquare * 0.1

        newPosx = (nodo.col * self.sizeSquare) + suma

        newPosy = (nodo.row * self.sizeSquare) + suma

        pygame.draw.rect(self.window,color,(newPosx,newPosy, newSize , newSize))

    def drawBackground(self,color):
        '''dibuja el color del fondo'''
        pygame.draw.rect(self.window,color,(0,0,self.width,self.height))

    def drawGrid(self,color):
        '''dibuja las lineas del grid'''
        #lineas en el eje x
        for pos_x in range(self.columns):
            pygame.draw.line(self.window,color,(pos_x*self.sizeSquare,0),(pos_x*self.sizeSquare,self.height))

        #lineas en el eje y 
        for pos_y in range(self.rows):
            pygame.draw.line(self.window,color,(0,pos_y*self.sizeSquare),(self.width,pos_y*self.sizeSquare))

    def update(self):
        '''controlador general para el funcionamiento de la IA'''

        #si el estado actual de la busqueda es diferente a "ganar"
        if self.statusSearch != Game.Win:

            #si no me encuentro en una ruta hacia la comida, estados posibles "esperando"- "camino hacia la cola" 
            if self.statusSearch != Game.foodPath:

                #1) BUSQUEDA (Serpiente original cabeza hasta la comida)
                #una tupla con la informacion de la busqueda, recibe como parametro punto de partida - punto de llegada
                values = self.PathFinder.dijkstra(self.snake.head,self.snake.food)

                #si encuentro una ruta hasta la comida
                if values[0]:

                    #debo crear una copia de la serpiente 
                    snakeCopy = self.snake.copy()

                    #creo una copia del camino corto, para no modificar el original, la copia no incluye el nodo inicial
                    shortpathCopy = values[1][1:].copy()

                    #ciclo para mover la serpiente virtual, hasta que tenga nodos en la copia de la ruta corta
                    while len(shortpathCopy) >0:
                    
                        #muevo la serpiente pasandole el nodo al cual debo moverme [inicial,1,2,3,4,final]
                        #por ende siempre voy obteniendo el dato 0, por que es el orden desde inicial hasta el final
                        snakeCopy.updateIA(shortpathCopy.pop(0))

                    #en resumen se crea una copia de la serpiente y la muevo en un espacio virtual, simulando ir hasta la comida
                    #de esa manera obtengo el cuerpo de la serpiente ya ubicada en la comida, y al finalizar el movimiento total
                    #la serpienteCopia terminara en un estado "ganador" o "comiendo"

                    #si el estatus de la serpiente "virtual-copia" es ganador
                    if snakeCopy.status == Snake.wining:

                        #asigno como ruta corta la primer busqueda
                        self.shortPath = values[1][1:]

                        #asigno todo el orden de visita de dijkstra de la primer busqueda
                        self.visitInOrder = values[2][1:-1]

                        #cambio el estado de busqueda ha, "camino hacia la comida"
                        self.statusSearch = Game.foodPath

                        #antes de animar el movimiento de la serpiente, debo animar la busqueda completa
                        self.statusAnimation = Game.AnimationDijkstraSearch

                    #si el estado de la serpiente "virtual-copia" no es ganador
                    else:
                        
                        #creo otro objeto pathFinder pero ahora con la copia de la serpiente
                        pathFinderFake = pathFinder(self.grid,snakeCopy)
                        
                        #2) BUSQUEDA (Serpiente copia hasta la cola)
                        valuesFake = pathFinderFake.dijkstra(snakeCopy.head, snakeCopy.body[len(snakeCopy.body)-1])

                        #si encuentro una ruta hasta la cola para la serpiente falsa, significa que aunque vaya por la comida, no
                        #me quedare encerrado por que tengo acceso a la cola
                        if valuesFake[0]:
                            
                            #asigno como ruta corta la primer busqueda
                            self.shortPath = values[1][1:]

                            #asigno todo el orden de visita de dijkstra de la primer busqueda
                            self.visitInOrder = values[2][1:-1]

                            #cambio el estado de busqueda ha, "camino hacia la comida"
                            self.statusSearch = Game.foodPath

                            #antes de animar el movimiento de la serpiente, debo animar la busqueda completa
                            self.statusAnimation = Game.AnimationDijkstraSearch

                        
                        #si no encuentra camino hasta la cola con la serpiente fake, significa que si tengo acceso a la comida, pero
                        #si voy por esa comida me quedare encerrado y morire
                        else:
                            
                            #si estoy en un camino hasta la cola, debo seguir en el ya que, pudo haber encontrado un camino hacia la comida
                            #sin embargo no encontro un camino hasta la cola por eso entre aca
                            if self.statusSearch == Game.tailPath:
                                
                                #si el ingresa en esta iteracion, el shortPath seria igual a un "camino largo hasta la cola" y muevo la serpiente
                                #iteracion por iteracion
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
                                
                                #nunca muere por que siempre tendra acceso a la cola, dada la logica del algoritmo general
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


    def Render(self):
        '''solo se encarga de renderizar lo que halla pasado'''

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
