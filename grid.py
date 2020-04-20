from node import Node


class Grid():

    def __init__(self,rows,columns):
        

        self.rows = rows
        self.columns = columns

        self.Matriz = [[Node(row,column) for column in range(self.columns)] for row in range(self.rows)]

        #es utilizada solo para dibujar mas rapido, y no recorrer toda la matriz
        self.walls =[]


    def copy(self):
        
        #crea una copia de la matriz original, con nodos nuevesitos
        copyMatriz = [[Node(row,column) for column in range(self.columns)] for row in range(self.rows)]

        return copyMatriz