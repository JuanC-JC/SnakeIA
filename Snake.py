from node import Node
import random
import pygame

#que hacer con esta perra
class Snake():

    #variables estaticas de clase
    up = 0
    right = 1
    down = 2
    left = 3

    moving = 0
    eating = 1
    dead = 2
    wining = 3

    def __init__(self,rows,columns,game = None):

        self.__game = game

        self.rows = rows

        self.columns = columns
        
        self.head = Node(random.randint(0,columns-1),random.randint(0,self.rows-1))

        self.food = Node(random.randint(0,self.columns-1),random.randint(0,rows-1))

        self.statusMove = Snake.up

        self.body = [self.head]

        self.virtual = False

        self.status = Snake.moving

    def __changeStatusMove(self,events):

        '''update the statusMove for the snake'''
        events = [event.key for event in events if event.type == pygame.KEYDOWN]
        
        if len(events)>0:
            if pygame.K_LEFT == events[0] and self.statusMove != Snake.right:
                    
                self.statusMove = Snake.left

            elif pygame.K_RIGHT ==  events[0] and self.statusMove != Snake.left:

                self.statusMove = Snake.right

            elif pygame.K_UP == events[0]  and self.statusMove != Snake.down:

                self.statusMove = Snake.up

            elif pygame.K_DOWN == events[0]  and self.statusMove != Snake.up:

                self.statusMove = Snake.down

    def update(self,events):
        '''Update the snake with the key events and return what is the state for the snake, eating, moving or dying'''

        self.__changeStatusMove(events)

        return self.__Move()

    def updateIA(self,node):
        '''Update the snake to the node and return what is the state for the snake, eating, moving or dying'''

        self.__changeStatusMoveIA(node)

        return self.__Move()

    def __Move(self):
        '''Move the snake body in the matriz and return his new status, eating,moving or dying'''
        #crea una nueva cabeza
        node = self.__newHead()

        if self.status == Snake.moving:
            
            #asigna el nodo como la cabeza
            self.head = node

            #agrega la nueva cabeza al cuerpo
            self.body.insert(0,self.head)

            #elimina la cola de la serpiente
            self.body.pop()
            
        elif self.status == Snake.eating:

            #asigna el nodo como la cabeza
            self.head = node

            #agrega la nueva cabeza al cuerpo
            self.body.insert(0,self.head)

            #crea una nueva comida
            self.__newFood()

        #always return the status of the snake, eating, moving or dead
        return self.status

    def __changeStatusMoveIA(self,node):
        '''move the snake to node'''

        #si la cabeza esta mas a la derecha que el nodo a moverme, me muevo a la izquierda
        if self.head.col > node.col:   self.statusMove = Snake.left
        
        #si la cabeza esta mas a la izquierda que el nodo, me muevo a la derecha
        elif self.head.col < node.col:  self.statusMove = Snake.right

        #si estoy mas abajo que el nodo, me muevo hacia arriba
        elif self.head.row > node.row:    self.statusMove = Snake.up

        #si la cabeza esta mas arriba que el nodo, me muevo hacia abajo
        elif self.head.row < node.row:   self.statusMove = Snake.down

    def drawBody(self):
        '''only draw the snake body'''


        sizeSquare = self.__game.sizeSquare

        for node in range(len(self.body)):
            self.__game.drawNode(self.body[node],(4, 182, 101))


            #una vez dibujado el primero debo calcular hacia donde dibujar el compañero
            if len(self.body) > 1 and node < len(self.body)-1:

                second = self.body[node+1]

                sig = self.__nextNeighborh(self.body[node],second)

                if sig == Snake.left:


                    newX = second.col * sizeSquare + (sizeSquare*0.9)

                    newY = second.row * sizeSquare + (sizeSquare*0.1)

                    pygame.draw.rect(self.__game.window,(4,182,101),(newX,newY, sizeSquare*0.2, sizeSquare * 0.8))

                elif sig == Snake.right:

                    newX = second.col * sizeSquare - (sizeSquare*0.1)

                    newY = second.row * sizeSquare + (sizeSquare*0.1)

                    pygame.draw.rect(self.__game.window,(4,182,101),(newX,newY, sizeSquare*0.2, sizeSquare * 0.8))


                elif sig == Snake.down:

                    newX = second.col * sizeSquare + (sizeSquare*0.1)

                    newY = second.row * sizeSquare - (sizeSquare*0.1)

                    pygame.draw.rect(self.__game.window,(4,182,101),(newX,newY, sizeSquare*0.8, sizeSquare * 0.2))

                elif sig == Snake.up:

                    newX = second.col * sizeSquare + (sizeSquare*0.1)

                    newY = second.row * sizeSquare + (sizeSquare*0.9)

                    pygame.draw.rect(self.__game.window,(4,182,101),(newX,newY, sizeSquare*0.8, sizeSquare * 0.2))

    def drawFood(self):
        '''only draw the food'''

        self.__game.drawNode(self.food,(221, 75, 57))

    def __newHead(self):

        '''create a new node for be head and change the status of snake, according to the new head'''
        
        col = self.head.col
        row = self.head.row

        #siempre esta muerto hasta que se compruebe lo contrario
        self.status = Snake.dead

        #evaluar a la izquierda
        if self.statusMove == Snake.right:
            col +=1

            if col >= self.columns: return None

        elif self.statusMove == Snake.left:

            col -=1

            if col < 0: return None

        elif self.statusMove == Snake.up:

            row -=1

            if row < 0: return None


        elif self.statusMove == Snake.down:

            row +=1

            if row >= self.rows: return None


        if self.__isInBody(row,col):
            self.status = Snake.dead
            return None


        if self.__isInFood(row,col):
            self.status = Snake.eating
        else:
            self.status = Snake.moving

        return Node(row,col)

    def __newFood(self):
        '''asign a new food for the snake'''

        if self.status != Snake.wining:
        #crea un nuevo nuevo
            node =  Node(random.randint(0,self.columns-1),random.randint(0,self.rows-1))
            
            coordenadasBody = [(node.row,node.col) for node in self.body]

            #si el nodo creado esta en el cuerpo, repetir hasta encontrar uno que no este en el cuerpo.
            count = 0
            while (node.row,node.col) in coordenadasBody:
                if count == 1000:
                    self.status = Snake.wining
                    break
                node =  Node(random.randint(0,self.columns-1),random.randint(0,self.rows-1))
                count += 1

            #asigno el nodo como nueva comida

            if self.status == Snake.wining:
                print("gano mi prro")
            else:
                self.food = node

    def __isInBody(self,row,col):
        '''Return true if the new head is touching the body'''
        for node in self.body[:-1]:
            if (row,col) == (node.row,node.col):
                return True

        return False

    def __isInFood(self,row,col):
        '''Return true if the starNode is eating'''
        if (row,col) != (self.food.row,self.food.col): return False
        else: return True
       
    def copy(self):
        '''return a copy of snake, without the functions to draw'''

        #no le pasamos el "game" por que no necesitamos las opciones para dibujar
        snakeCopy = Snake(self.rows,self.columns)

        snakeCopy.virtual = True

        snakeCopy.status = self.status

        snakeCopy.head = Node(self.head.row,self.head.col)


        snakeCopy.food = Node(self.food.row,self.food.col)

        snakeCopy.body =[snakeCopy.head]

        #lista del cuerpo sin la cabeza
        for node in self.body[1:]:
            
            snakeCopy.body.append(Node(node.row,node.col))
            

        return snakeCopy

    def __nextNeighborh(self,fNode,sNode):

        #si la cabeza esta mas a la derecha que el nodo a moverme, me muevo a la izquierda
        if fNode.col > sNode.col:   return Snake.left
        
        #si la cabeza esta mas a la izquierda que el nodo, me muevo a la derecha
        elif fNode.col < sNode.col:  return Snake.right

        #si estoy mas abajo que el nodo, me muevo hacia arriba
        elif fNode.row > sNode.row:    return Snake.up

        #si la cabeza esta mas arriba que el nodo, me muevo hacia abajo
        elif fNode.row < sNode.row:   return  Snake.down