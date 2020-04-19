import queue

#recibe el grid y la serpiente donde quiere calcular la ruta, el grid para saber cuales paredes tiene y la snake para saber el cuerpo


#averiguar en que direccion va la serpiente y no tomar ese nodo para evaluar..

class pathFinder():

    def __init__(self,grid,snake):

        #capto una copia de la Matriz de nodos nuevesita
        self.grid = grid

        #capto una copia de la serpiente
        self.snake = snake
    


    def dijkstra(self,initNode,finishNode):
        '''retorna (true,shortpath,visitInOrder) si encuentra un camino, retorna (false,None,visitInOrder) si no encuentra camino'''

        self.Matriz = self.grid.copy()

        self.snakeMatriz = self.snake.copy()

        self.initNode = self.Matriz[initNode.row][initNode.col]
        self.finishNode = self.Matriz[finishNode.row][finishNode.col]


        #coloca como cuerpo, los nodos del grid
        for node in self.snake.body:
            self.Matriz[node.row][node.col].body = True 

        #nodos visitados en orden
        self.visitedInOrder = []

        #cola de nodos para visitar
        self.UnvisitedNodes = queue.Queue()

        if self.__travelGrid():
            
            #lista pa almacenar el camino corto
            shortPath =[]

            #nodo final
            currentNode = self.finishNode

            #jamas toma el nodo inicial, ya que el no tiene nodo previo y si no dara error el putito
        
            while(currentNode.previousNode != False and currentNode != self.initNode ):
                
                #agrego el nodo a la lista
                shortPath.append(currentNode)

                #asigno el nodo previo como nodo_actual
                currentNode = currentNode.previousNode

            #retorna la ruta desde la cabeza hasta el final
            return (True,shortPath[::-1],self.visitedInOrder)

        # si dijkstra no encontro un camino 
        else:
            return (False,[],self.visitedInOrder)




    def __travelGrid(self):


        #asignar distancia 0 al nodo inicial
        self.initNode.distance = 0

        #agrego a la lista de pendientes el nodo inicial
        self.UnvisitedNodes.put(self.initNode)

        #itera cada elemento de la cola
        while self.UnvisitedNodes.qsize() > 0:
            
            #obtiene el primer elemento de la cola de nodos por visitar
            node = self.UnvisitedNodes.get()

            #si el nodo mas cercano tiene distancia infinita debemos detener el algoritmo tambien, estamos atrapados
            if node.distance == 9999: return False
        
            node.visited = True

            self.visitedInOrder.append(node)

            #si el nodo es el nodo.final detener el algoritmo
            if (node == self.finishNode): return True

            #actualizar los nodos sin visitar
            self.__updateUnvisitedNeighbors(node)


    def __updateUnvisitedNeighbors(self,node):

        #obtener primero los nodos sin visitar
        unvisitedNeighbors = self.getUnvisitedNeighbors(node)

        for neighbor in unvisitedNeighbors:
            neighbor.distance = node.distance +1
            neighbor.previousNode = node


            #revisar si ya esta en la lista de espera
            lista = list(self.UnvisitedNodes.queue)

            #si se encuentra en la lista de espera o el nodo es un cuerpo evitarlo
            if neighbor not in lista:
                #si el nodo no es una parte del cuerpo, o si es el nodo final
                if neighbor.body == False or neighbor == self.finishNode:
                     self.UnvisitedNodes.put(neighbor)


    def getUnvisitedNeighbors(self,node):

        #pensar si es lo mismo aca bloquear los nodos "wall" osea eliminarnos de la lista desde aca o ñe
        neighbors =[]

        #nodo superior
        if (node.row >0): neighbors.append(self.Matriz[node.row-1][node.col])
        
        #nodo derecho
        if (node.col < len(self.Matriz[0])-1): neighbors.append(self.Matriz[node.row][node.col +1])

        #nodo inferior
        if (node.row < len(self.Matriz)-1): neighbors.append(self.Matriz[node.row+1][node.col])

        #nodo izquierdo

        if (node.col > 0): neighbors.append(self.Matriz[node.row][node.col-1])

        #devuelve una lista solo con los nodos que no han sido visitados
        return [neighbor for neighbor in neighbors if neighbor.visited == False]
        
        