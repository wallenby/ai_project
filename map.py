import csv

class Map():

    def __init__(self):
        self.grid = []

    def get_grid(self, file_path):

        # Reading from the .csv file and filling grid array
        with open(file_path, newline='') as file:
            file_reader = csv.reader(file)

            for row in file_reader:
                grid_row = []
                for column in row:
                    grid_row.append(column)
                self.grid.append(grid_row)
                
    def draw(self):
        print(self.grid[9][1])
        print("+----------+")
        for x in range(len(self.grid)):
            print("|", end='')
            for y in range(len(self.grid[x])):
                print(self.grid[x][y], end='')
            print("|")
        print("+----------+")
        
    

# Square Node for the grid
class Square_Node():

    def __init__(self, position, prev=None, ):
        self.prev = prev
        self.position = position

        if (prev is None):
            self.g = 0
            self.h = 5
            self.f = self.g + self.h
            self.treasures = 0
        else:
            self.g = prev.f
            self.h = 5
            self.f = self.g + self.h
            self.treasures = prev.treasures

    def __lt__(self, other):
        return self.f < other.f


