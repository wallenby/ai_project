
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
    bot1.resource_pickup_count = 2
    bot2.resource_pickup_count = 3
    #bot3 = Bot([0,2], [8,7], [1,9], my_map.grid)
    bots = [bot1, bot2]
    

    #bot3.resource_pickup_count = 5
    
    
    
    
    while(True):
        
        # Update map based on the movements of each robot
        
        characters_replaced = []
        
        for bot in bots:
            
            bot.move_to_next_spot()
        
            characters_replaced.append(my_map.grid[bot.current_location[0]][bot.current_location[1]])      
                
            my_map.grid[bot.current_location[0]][bot.current_location[1]] = bot.symbol

        my_map.draw()
        time.sleep(move_rate)
    
        counter = 0
        for bot in bots:
            my_map.grid[bot.current_location[0]][bot.current_location[1]] = characters_replaced[counter]
            counter += 1
    