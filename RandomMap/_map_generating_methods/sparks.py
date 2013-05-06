#===============================================================================
# Sparks method
# http://www.cartania.com/alexander/generation.html
#===============================================================================

import random

def Sparks(GAME_WIDTH,GAME_HEIGHT):
    """Some kind of random map generator from http://www.cartania.com/alexander/generation.html"""
        
    coordinates = []
    land_only = []
    for x in range(GAME_WIDTH/10):
        for y in range(GAME_HEIGHT/10):
            if random.randrange(0,6) == 0:
                z = 0
                land_only.append((x,y,z))
            else:
                z = -1
            coordinates.append([x,y,z])
    
    for item in land_only:
        #Get the 8 neighbor points
        #We are on the edge
        if item[0] == 0 or item [0] == 47 or item[1] == 0 or item[1] == 63:
            #Add water
            for world_coordinate in coordinates:
                if world_coordinate[0] == item[0] and world_coordinate[1] == item[1]:
                    #Check if we have land
                    world_coordinate[2] = -1
        #Choose all the neighbors
        else:
            x = item[0]
            y = item[1]
            possible_coordinates = [
                                    (x-1,y-1),(x,y-1),(x+1,y-1),
                                    (x-1,y),(x+1,y),
                                    (x-1,y+1),(x,y+1),(x+1,y+1)
                                    ]
            #Assign all of the possible coordinates to land or water
            rd_land_or_water = random.randrange(0,10)
            if rd_land_or_water == 1:
                land_or_water = -1
            else:
                land_or_water = 0
                
            for coord in possible_coordinates:
                #find the coordinates in the world array
                for world_coordinate in coordinates:
                    if world_coordinate[0] == coord[0] and world_coordinate[1] == coord[1]:
                        #Check if we have land
                        if world_coordinate[2] == 0:
                            world_coordinate[2] = 0
                        else:
                            world_coordinate[2] = land_or_water
                        

    return coordinates