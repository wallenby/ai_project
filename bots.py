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
        
        
    def set_bots(self, bots):
        self.bots = bots
    
    


    def move_to_next_spot(self):
        
        
        # If the bot has reached it's destination
        if len(self.optimal_path)-1 == self.optimal_path_index:

            self.optimal_path_index = 1

            # If it was going to pickup location, then go to the drop off location
            if self.is_going_to_pickup:
                self.is_going_to_pickup = False
                self.is_going_to_dropoff = True
                self.find_optimal_path(self.dropoff_location)

            # If it was going to droppff location
            elif self.is_going_to_dropoff:
                
                self.resource_pickup_count -= 1
                
                # If there is nothing left to pickup, go back to starting spot
                if self.resource_pickup_count == 0:
                    self.is_going_to_dropoff = False
                    self.is_going_to_start = True
                    self.find_optimal_path(self.start_location)

                # If there are things left, go back to pickup location
                else:
                    self.is_going_to_dropoff = False
                    self.is_going_to_pickup = True
                    # Just reverse the path so we don't need to any additional computation
                    self.optimal_path = self.optimal_path[::-1]

            # If the bot has reached it's starting spot after delivering all the items, then it's done working
            # (for now anyways)
            elif self.is_going_to_start:
                self.optimal_path_index -= 1
                self.optimal_path = [self.start_location]
        
        else:
            self.optimal_path_index += 1
        
        
        #if self.optimal_path_index < len(self.optimal_path):
        self.current_location = self.optimal_path[self.optimal_path_index]
        
        
        


    # ~~~ Helper Functions ~~~
    
    # Checks if the position given is on the grid
    def is_position_valid(self, position):
        return ((position[0] < len(self.grid) and position[0] >= 0)
                and (position[1] < len(self.grid[0]) and position[1] >= 0)
                and (self.grid[position[0]][position[1]] != 'X'))


    # Checks if the position given is on the grid
    def is_position_occupied(self, position):
        return (self.grid[position[0]][position[1]] != ' ' and self.grid[position[0]][position[1]] != 'P'
                and self.grid[position[0]][position[1]] != 'D' and self.grid[position[0]][position[1]] != 'S')
        
        
    def look_for_better_spot(self):
        
        # print("BEEP BEEP, LOOKING FOR BETTER SPOT!")
        
        # ADJACENT - RIGHT
        if ( self.is_position_valid([self.current_location[0], self.current_location[1] + 1]) and
        not self.is_position_occupied([self.current_location[0], self.current_location[1] + 1]) and 
        [self.current_location[0], self.current_location[1] + 1] != self.next_spot()):
            
            self.current_location = [self.current_location[0], self.current_location[1] + 1]
                
        # ADJACENT - DOWN
        elif ( self.is_position_valid([self.current_location[0] + 1, self.current_location[1]]) and
        (not self.is_position_occupied([self.current_location[0] + 1, self.current_location[1]])) and 
       [self.current_location[0] + 1, self.current_location[1]] != self.next_spot()):
            self.current_location = [self.current_location[0] + 1, self.current_location[1]]

        # ADJACENT - UP
        elif ( self.is_position_valid([self.current_location[0] - 1, self.current_location[1]]) and
        not self.is_position_occupied([self.current_location[0] - 1, self.current_location[1]]) and 
        [self.current_location[0] - 1, self.current_location[1]] != self.next_spot()):
            self.current_location = [ self.current_location[0] - 1, self.current_location[1]]

        # ADJACENT - LEFT 
        elif ( self.is_position_valid([self.current_location[0], self.current_location[1]-1]) and 
        not self.is_position_occupied([ self.current_location[0], self.current_location[1] - 1]) and 
        [self.current_location[0], self.current_location[1]-1] != self.next_spot()):
            self.current_location = [ self.current_location[0], self.current_location[1] - 1]
            
        else:
            self.optimal_path_index += 1
        
        if self.optimal_path_index < 0:
            self.optimal_path_index -= 1
        
            
            
            
            
    # ~~~ The star of the show ;) ~~~
    def find_optimal_path(self, destination):

        frontier = []
        start_square = Square_Node(self.current_location)
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
            self.explore_sqaure(temp_position, min_f, frontier)

            # ADJACENT - DOWN
            temp_position = [min_f.position[0] + 1, min_f.position[1]]
            self.explore_sqaure(temp_position, min_f, frontier)

            # ADJACENT - UP
            temp_position = [min_f.position[0] - 1, min_f.position[1]]
            self.explore_sqaure(temp_position, min_f, frontier)

            # ADJACENT - LEFT
            temp_position = [min_f.position[0], min_f.position[1] - 1]
            self.explore_sqaure(temp_position, min_f, frontier)


        curr_node = min_f
        optimal_path_list = []
        while (curr_node != None):
            optimal_path_list.append([curr_node.position[0], curr_node.position[1]])
            curr_node = curr_node.prev
        self.optimal_path = optimal_path_list[::-1]
        


    # ~~~ Helper Functions - Related to optimal path finding algorithm ~~~
    
    # Checks if the square should be explored -> if it should, it checks it by adding
    # it to the frontier
    def explore_sqaure(self, new_position, current_node, frontier):
        if (self.is_position_valid(new_position) and not self.is_square_explored(current_node, new_position) 
            and not self.is_occupied(current_node, new_position) ):
            new_square = Square_Node(new_position, current_node)
            bisect.insort(frontier, new_square)
            
   # Checks if the square has been explored (position and coming from the same square)
    def is_square_explored(self, current_node, position):
        temp_node = current_node

        while (temp_node != None):
            if (temp_node.position == position):
                return True
            if (temp_node.prev is None):
                return False
            temp_node = temp_node.prev
            
            
            
    def is_occupied(self, current_node, new_position):
        
        counter = 0
        temp_node = current_node
        while temp_node != None:
            temp_node = temp_node.prev
            counter += 1
        
        # counter +=1
        for bot in self.bots:
            
            
            # if self != bot and (len(bot.optimal_path)) > bot.optimal_path_index + counter:
            #     return new_position == bot.optimal_path[bot.optimal_path_index+counter] or current_node.position == bot.optimal_path[bot.optimal_path_index+counter-1]
            
            # if some other bot is on the same location as the square being explored and at the sime time
            if self != bot and (len(bot.optimal_path) - bot.optimal_path_index) >= counter :
                
                return new_position == bot.optimal_path[counter + bot.optimal_path_index-1] 
            
            
            # and current_node.position == bot.optimal_path[bot.optimal_path_index+counter-1]
            
            # elif self != bot and (len(bot.optimal_path) - bot.optimal_path_index) >= counter :
            #     return current_node.position == bot.optimal_path[bot.optimal_path_index+counter-1]
            

            
            
        return False
                 