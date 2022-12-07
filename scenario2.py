
import time
from bots import Bot
from map import Map

move_rate = 0.2


if __name__ == '__main__':

    file_path = "map2.csv"
    my_map = Map()
    my_map.get_grid(file_path)


    bot1 = Bot([2,0], [6,1], [0,3], my_map.grid, '1')
    bot2 = Bot([0,7], [8,4], [0,3], my_map.grid, '2')
    bot3 = Bot([1,9], [5,7], [0,3], my_map.grid, '3')
    
    bots = [bot1, bot2, bot3]
    
    for bot in bots:
        bot.bots = bots 
        bot.find_optimal_path(bot.pickup_location)
    
    bot1.resource_pickup_count = 3
    bot2.resource_pickup_count = 5
    bot3.resource_pickup_count = 1
    
    my_map.draw()
    time.sleep(move_rate)
    
    
    # visually drawing and moving the bots
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
            
        counter = 0
        for bot in bots:
            if bot.resource_pickup_count == 0 and bot.current_location == bot.start_location:
                counter += 1
            print("bot #", bot.symbol, " -> drop-offs left: ", bot.resource_pickup_count)
        
        if len(bots) == counter:
            print("ALL DONE!")
            break
            
    