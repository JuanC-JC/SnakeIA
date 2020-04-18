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
        '''Update the snake with the key events and return what is the state for the snake'''

        self.__changeStatusMove(events)

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

    def drawBody(self):
        '''only draw the snake body'''

        for node in self.body:

            if node == self.head: self.__game.drawNode(node,(4, 182, 101))

            elif node == self.body[len(self.body)-1]: self.__game.drawNode(node,(60, 141, 188))

            else: self.__game.drawNode(node,(0, 166, 90))

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

        #crea un nuevo nuevo
        node =  Node(random.randint(0,self.columns-1),random.randint(0,self.rows-1))
        
        coordenadasBody = [(node.row,node.col) for node in self.body]

        #si el nodo creado esta en el cuerpo, repetir hasta encontrar uno que no este en el cuerpo.
        while (node.row,node.col) in coordenadasBody:
            
            node =  Node(random.randint(0,self.columns-1),random.randint(0,self.rows-1))

        #asigno el nodo como nueva comida
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

        snakeCopy.head = Node(self.head.col,self.head.row)

        snakeCopy.food = Node(self.food.col,self.food.row)

        snakeCopy.body =[snakeCopy.head]

        #lista del cuerpo sin la cabeza
        for node in self.body[1:]:
            
            snakeCopy.body.append(Node(node.col,node.row))
            

        return snakeCopy
