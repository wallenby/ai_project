
import time
from bots import Bot
from map import Map

move_rate = 0.15



if __name__ == '__main__':

    file_path = "map.csv"
    my_map = Map()
    my_map.get_grid(file_path)


    bot1 = Bot([0,0], [8,1], [1,9], my_map.grid, 'c')
    bot2 = Bot([0,1], [8,4], [1,9], my_map.grid, 'o')
    #bot3 = Bot([0,2], [8,7], [1,9], my_map.grid)
    bots = [bot1]
    
    bot1.resource_pickup_count = 7
    bot2.resource_pickup_count = 5
    #bot3.resource_pickup_count = 5
    
    

    # # Finding the optimal paths for each robot and for each location
    # for bot in bots:
    #     bot.optimal_path = bot.find_optimal_path(bot.pickup_location)
   
    # Update map based on the movements of each robot
    # characters_replaced = []
    
    while(True):
        
        # Update map based on the movements of each robot
        
        characters_replaced = []
        
        #counter = 0
        
        for bot in bots:
            
            # if len(characters_replaced) > 0:
            #     my_map.grid[bot.current_location[1]][bot.current_location[0]] = characters_replaced[counter]
            #     counter += 1
            
            bot.move_to_next_spot()
            
            # characters_replaced = [" "]
            
            characters_replaced.append(my_map.grid[bot.current_location[0]][bot.current_location[1]])
            #print([bot.current_location[0],bot.current_location[1]])
            
            # if bot.is_position_occupied([bot.current_location[0],bot.current_location[1]], my_map.grid):
                
            #     # my_map.grid[bot.current_location[1]][bot.current_location[0]] = characters_replaced[counter]
                
            #     bot.optimal_path_index -= 2
            #     bot.move_to_next_spot()
                
            #     print("AAAAAAAAAH!!!!!!!!!!!!")
                
            #     my_map.grid[bot.current_location[1]][bot.current_location[0]] = bot.symbol
            # else:                
                
            my_map.grid[bot.current_location[0]][bot.current_location[1]] = bot.symbol

        my_map.draw()
        time.sleep(move_rate)
        
        
    
        counter = 0
        for bot in bots:
            my_map.grid[bot.current_location[0]][bot.current_location[1]] = characters_replaced[counter]
            counter += 1
    