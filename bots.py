import bisect
from map import Map, Square_Node

class Bot():
    def __init__(self, starting_location, pickup_location, dropoff_location, grid, symbol):
        self.current_location = self.start_location = starting_location
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location

        self.optimal_path = []
        self.optimal_path_index = 0

        self.grid = grid

        self.is_going_to_pickup = True
        self.is_going_to_dropoff = False
        self.is_going_to_start = False

        # Symbol that it displayed on terminal
        self.symbol = symbol

        # Number of resources bot needs to pickup and deliver to the drop-off destination
        self.resource_pickup_count = 0
        
        self.find_optimal_path(self.pickup_location)


    def move_to_next_spot(self):
        
    
        self.current_location = self.optimal_path[self.optimal_path_index]
        print(self.optimal_path)

        # If the bot has reached it's destination
        if len(self.optimal_path) == self.optimal_path_index+1:
            
            # print("HERE!", self.optimal_path_index, len(self.optimal_path))

            self.optimal_path_index = -1

            # If it was going to pickup location, then go to the drop off location
            if self.is_going_to_pickup:
                self.is_going_to_pickup = False
                self.is_going_to_dropoff = True
                print(self.optimal_path)
                self.find_optimal_path([self.dropoff_location[1],self.dropoff_location[0]])
                
                #self.optimal_path = self.optimal_path[::-1]
                print(self.optimal_path)

            # If it was going to droppff location
            if self.is_going_to_dropoff:
                
                # If there is nothing left to pickup, go back to starting spot
                if self.resource_pickup_count == 0:
                    self.is_going_to_dropoff = False
                    self.is_going_to_start = True
                    self.find_optimal_path(self.start_location)

                # If there are things left, go back to pickup location
                else:
                    self.is_going_to_dropoff = False
                    self.is_going_to_pickup = True
                    self.find_optimal_path(self.pickup_location)

            # If the bot has reached it's starting spot after delivering all the items, then it's done working
            # (for now anyways)
            if self.is_going_to_start:
                self.is_going_to_start = False
                self.optimal_path_index -= 1
        
        self.optimal_path_index += 1


    # ~~~ The star of the show ;) ~~~
    def find_optimal_path(self, destination):

        optimal_path = 0
        optimal_path_cost = 0
        #num_squares_explored = 0

        frontier = []
        start_square = Square_Node( [self.current_location[1],self.current_location[0]])
        frontier.append(start_square)

        # While A* search is being performed
        while (True):

            #num_squares_explored += 1

            min_f = frontier[0]

            # If current square being explored is the goal destination
            if ([min_f.position[0], min_f.position[1]] == destination):
                break

            # Done exploring current square, remove it from the frontier
            frontier.remove(min_f)

            # Checking adjacent squares...
            # ADJACENT - RIGHT
            temp_position = [min_f.position[0], min_f.position[1] + 1]
            self.explore_sqaure(temp_position, self.grid, min_f, frontier)

            # ADJACENT - DOWN
            temp_position = [min_f.position[0] + 1, min_f.position[1]]
            self.explore_sqaure(temp_position, self.grid, min_f, frontier)

            # ADJACENT - UP
            temp_position = [min_f.position[0] - 1, min_f.position[1]]
            self.explore_sqaure(temp_position, self.grid, min_f, frontier)

            # ADJACENT - LEFT
            temp_position = [min_f.position[0], min_f.position[1] - 1]
            self.explore_sqaure(temp_position, self.grid, min_f, frontier)

        curr_node = min_f
        optimal_path_cost = -1
        optimal_path_list = []
        while (curr_node != None):
            #optimal_path_cost += 1
            optimal_path_list.append([curr_node.position[0], curr_node.position[1]])
            curr_node = curr_node.prev
        self.optimal_path = optimal_path_list[::-1]
        

        #return [optimal_path, optimal_path_cost, num_squares_explored]






    # ~~~ Helper Functions ~~~

    # Checks if the position given is on the grid
    def is_position_valid(self, position, grid):
        return ((position[0] < len(grid) and position[0] >= 0)
                and (position[1] < len(grid[0]) and position[1] >= 0)
                and (grid[position[0]][position[1]] != 'X'))

        # Checks if the position given is on the grid
    def is_position_occupied(self, position, grid):
        return (grid[position[0]][position[1]] != ' ' and grid[position[0]][position[1]] != 'P'
                and grid[position[0]][position[1]] != 'D' and grid[position[0]][position[1]] != 'S')

    # Checks if the square has been explored (position and coming from the same square)
    def is_square_explored(self, curr_node, position):
        temp_node = curr_node

        while (curr_node != None):
            if (temp_node.position == position):
                return True
            if (temp_node.prev is None):
                return False
            temp_node = temp_node.prev

    # Checks if the square should be explored -> if it should, it checks it by adding
    # it to the frontier
    def explore_sqaure(self, new_position, grid, min_f, frontier):
        if (self.is_position_valid(new_position, grid) and not self.is_square_explored(min_f, new_position)):
            new_square = Square_Node(new_position, min_f)
            bisect.insort(frontier, new_square)
