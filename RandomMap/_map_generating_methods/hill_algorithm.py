#===============================================================================
# Hill Algorithm
#===============================================================================

import random
import math

#------------------------------------------------------------------------------ 
# Traditional
def HillAlgorithm(GAME_WIDTH,GAME_HEIGHT):
    """Generate many circles and raise all the coordinates within the circle by x"""
    
    #Generate the basic map where each coordinate is at z = 0
    world_coordinates = [] #(x,y,z)
    for x in range(GAME_WIDTH/10): #Divide by the width of each tile
        for y in range(GAME_HEIGHT/10):
            world_coordinates.append([x,y,0])
    
    ITERATIONS = 200
    height = 1
    
    for i in range(ITERATIONS):
        print 'Iteration: ', i
        
        #Generate a random circle
        radius = random.randrange(2,10)
        #Find the center of the circles 
        center_coordinate = world_coordinates[random.randrange(0,len(world_coordinates))]
        subsequence = []
        for coordinate in world_coordinates:
            #Choose all the coordinates within the circle
            if math.sqrt((center_coordinate[0]-coordinate[0])**2 + (center_coordinate[1]-coordinate[1])**2) <= radius:
                subsequence.append(coordinate)
        
        #Raise the height of each coordinate within the circle
        for s_coord in subsequence:
            index = world_coordinates.index(s_coord)
            world_coordinates[index][2] += 1
    
    return world_coordinates


#------------------------------------------------------------------------------ 
# Modified
def HillAlgorithm_mod(GAME_WIDTH,GAME_HEIGHT):
    """
    Generate many circles and raise all the coordinates within the circle by x
    Modified version, First generate, islands, then beaches, etc
    """
    
    #Generate the basic map where each coordinate is at z = 0
    world_coordinates = [] #(x,y,z)
    for x in range(GAME_WIDTH/10): #Divide by the width of each tile
        for y in range(GAME_HEIGHT/10):
            world_coordinates.append([x,y,0])
    
    height = 1
    
    def iterate(iterations,previous_section):
        for i in range(iterations):
            #Find a random coordinate
            center_coordinate = world_coordinates[random.randrange(0,len(world_coordinates))]
            
            #Generate multiple random geometrical formations around this coordinate to get a better landscape
            for i in range(5):
                moved_coordinate = [
                                    center_coordinate[0] + random.randrange(-5,5),
                                    center_coordinate[1] + random.randrange(-5,5),
                                    center_coordinate[2]
                                    ]
                
                #Generate a random radius - this is the size of the geometrical shape
                radius = random.randrange(1,8)
                
                subsequence = []
                #Choose either a square or a circle to get a more realistic environment
                if random.randrange(0,50) == 0:
                    for coordinate in world_coordinates:
                        #Choose all the coordinates within the square
                        if (
                            coordinate[0] >= moved_coordinate[0] - radius and #x-
                            coordinate[0] <= moved_coordinate[0] + radius and #x+
                            coordinate[1] >= moved_coordinate[1] - radius and #y-
                            coordinate[1] <= moved_coordinate[1] + radius     #y+
                            ):
                            subsequence.append(coordinate)
                else:
                    for coordinate in world_coordinates:
                        #Choose all the coordinates within the circle
                        if math.sqrt((moved_coordinate[0]-coordinate[0])**2 + (moved_coordinate[1]-coordinate[1])**2) <= radius:
                            subsequence.append(coordinate)
                
                #Raise the height of each coordinate within the circle
                for s_coord in subsequence:
                    index = world_coordinates.index(s_coord)
                    #So we don't get grass next to sea
                    if previous_section == 1: #If we add grass
                        #Check around the surrounding coordinates if they are water
                        x = world_coordinates[index][0]
                        y = world_coordinates[index][1]
                        #Check these coordinates if they are water
                        possible_coordinates = [
                                                (x-1,y-1),(x,y-1),(x+1,y-1),
                                                (x-1,y),(x,y),(x+1,y),
                                                (x-1,y+1),(x,y+1),(x+1,y+1)
                                                ]
                        water = False
                        for possible in possible_coordinates:
                            if [possible[0],possible[1],0] in world_coordinates:
                                water = True
                                break #Enough if one is water
                        if water == False:
                            if world_coordinates[index][2] == previous_section: #Don't raise the height of the land again
                                world_coordinates[index][2] += 1
                    #Mountain can be on both grass and sand
                    elif previous_section == 2:
                        if world_coordinates[index][2] == previous_section:
                            world_coordinates[index][2] += 1
                        elif world_coordinates[index][2] == 1:
                            world_coordinates[index][2] += 2 # Need to add 2 if we have a mountain on sand
                    else:
                        if world_coordinates[index][2] == previous_section: #Don't raise the height of the land again
                            world_coordinates[index][2] += 1
                    
    
    #Generate islands
    iterate(40,0) #(Iterations,previous height)
    #Grass
    iterate(20,1)
    #Mountains
    iterate(2,2)
        
    
    return world_coordinates