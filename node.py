
class Node():

    def __init__(self,row,col):

        self.col = col
        self.row = row

        self.visited = False
        self.distance = 9999
        self.previousNode = None

        self.body = False
        self.sidePrevious = None
