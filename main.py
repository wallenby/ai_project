
import time
from bots import Bot
from map import Map

move_rate = 0.15


if __name__ == '__main__':

    file_path = "map.csv"
    my_map = Map()
    my_map.get_grid(file_path)


    bot1 = Bot([0,0], [8,1], [1,9], my_map.grid, 'c')
    bot2 = Bot([1,0], [8,4], [1,9], my_map.grid, 'o')
    bot3 = Bot([2,0], [8,7], [1,9], my_map.grid, 'h')
    
    bots = [bot1, bot2, bot3]
    
    bot1.resource_pickup_count = 3
    bot2.resource_pickup_count = 5
    bot3.resource_pickup_count = 1
    
    my_map.draw()
    time.sleep(move_rate)
    
    while(True):
        
        # Update map based on the movements of each robot
        
        characters_replaced = []
        
        for bot in bots:
            
            # Collision Avoidance!
            # If there ISN'T a bot in the next spot, move there!
            if not bot.is_bot_on_location(bots):
                bot.move_to_next_spot()
            # else if it IS occupied, then...
                
            else:
                bot.look_for_better_spot()
                
            #print(bot.symbol , "at", bot.current_location)  
            
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
            if bot.resource_pickup_count == 0:
                counter += 1
        
        if len(bots) == counter:
            print("ALL DONE!")
            break
            
    