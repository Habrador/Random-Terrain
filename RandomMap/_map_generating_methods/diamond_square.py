#===============================================================================
# Diamond Square from Notch
# http://paulboxley.com/blog/2011/03/terrain-generation-mark-one
# http://sv.twitch.tv/notch/b/302867302 3:28:00
#===============================================================================

import random
import math
    
def GenerateNoise(GAME_WIDTH):
    #The size has to be 2^n+1
    w = GAME_WIDTH 
    
    #Generate a list where every value is zero
    noise = [] #(x,y,z)
    for y in range(w):
        noise_row = []
        for x in range(w):
            noise_row.append(0)
        
        noise.append(noise_row)
    
    #print noise
    
    
    def sample(x,y):
        """Get value from list"""
        return noise[x][y]
    
    def setSample(x,y,e):
        """Add value to list"""
        noise[x][y] = e
    
    def scaling(scale,stepSize):
        return (random.uniform(0,1)*2-1)*stepSize*scale #The Notch way
        #return (random.uniform(-scale,scale)) #This is the recommended way
    
    
    stepSize = w-1 #First coordinate is 0,0
    
    #scale = 2**-1
    scale = 1.0/w
        
    #Add init values to the 4 corners
    setSample(0,  0,  scaling(scale,stepSize))
    setSample(w-1,0,  scaling(scale,stepSize))
    setSample(0,  w-1,scaling(scale,stepSize))
    setSample(w-1,w-1,scaling(scale,stepSize))
    
    while stepSize >= 2:
        
        #Diamond step
        #
        #a     b
        #
        #   e
        #
        #c     d
        #
        halfStep = stepSize/2
        x = 0
        while x < w-1:
            y = 0
            while y < w-1:
                a = sample(x,y) #Top-left corner
                b = sample(x+stepSize,y) #Top-right corner
                c = sample(x,y+stepSize) #Bottom-left
                d = sample(x+stepSize,y+stepSize) #Bottom-right
                
                middle_point = (a+b+c+d)/4 + scaling(scale,stepSize)
                
                setSample(x+halfStep,y+halfStep,middle_point)
                
                y += stepSize
            
            x += stepSize
        
        #Square step
        #
        #a  g  b
        #
        #f  e  h
        #
        #c  i  d
        #
        x = 0
        while x < w-1:
            y = 0
            while y < w-1:
                #print x,y
                a = sample(x,y) #Top-left corner
                b = sample(x+stepSize,y) #Top-right corner
                c = sample(x,y+stepSize) #Bottom-left
                d = sample(x+stepSize,y+stepSize) #Bottom-right
                e = sample(x+halfStep,y+halfStep)
                
                f = (a+e+c)/3 + scaling(scale,stepSize)
                setSample(x,y+halfStep,f)
                
                g = (a+e+b)/3 + scaling(scale,stepSize)
                setSample(x+halfStep,y,g)
                
                h = (e+b+d)/3 + scaling(scale,stepSize)
                setSample(x+halfStep+halfStep,y+halfStep,h)
                
                i = (c+e+d)/3 + scaling(scale,stepSize)
                setSample(x+halfStep,y+halfStep+halfStep,i)
                
                y += stepSize
            
            x += stepSize
        
        stepSize /= 2
        #scale *= scale
        scale *= 1.6
    
    
    #Smooth the map = take the average of the squares around each coordinate
    smooth = True
    if smooth == True:
        for y in range(w):
            for x in range(w):
                average = 0.0
                times = 0.0
                
                # x
                #xox
                # x
                if x - 1 >= 0:
                    average += noise[y][x-1]
                    times += 1
                if x + 1 < w-1:
                    average += noise[y][x+1]
                    times += 1
                if y - 1 >= 0:
                    average += noise[y-1][x]
                    times += 1
                if y + 1 < w-1:
                    average += noise[y+1][x]
                    times += 1
                
                #x x
                # o
                #x x
                if x - 1 >= 0 and y - 1 >= 0:
                    average += noise[y-1][x-1]
                    times += 1
                if x + 1 < w and y - 1 >= 0:
                    average += noise[y-1][x+1]
                    times += 1
                if x - 1 >= 0 and y + 1 < w:
                    average += noise[y+1][x-1]
                    times += 1
                if x + 1 < w and y + 1 < w:
                    average += noise[y+1][x+1]
                    times += 1

                average += noise[y][x]
                times += 1

                average /= times

                noise[y][x] = average
    
    
    #Standardize the coordinates [x,y,z]
    world_coordinates = []
    for y,row in enumerate(noise):
        for x,c in enumerate(row):
            world_coordinates.append([x,y,c])
    
    return world_coordinates

def MakeIsland(coordinates,w,shift_y=1.0):
    """Make an island - Minicraft 03:45:00"""
    y = 0
    while y < w:
        x = 0
        while x < w:
            i = x + y * w
            xd = x/(w-1.0) * 2 - 1
            yd = y/(w-shift_y) * 2 - 1
            coordinates[i][2] = ((coordinates[i][2] + 1.3 - math.sqrt(xd*xd + yd*yd) * 3)*60+120) #1.4 is the size of the island
            
            x += 1
        y += 1
    
    return coordinates

def DiamondSquare(GAME_WIDTH):
    w = GAME_WIDTH
    
    noise1 = GenerateNoise(w)
    """
    noise1 = MakeIsland(noise1,w,200)
    
    noise2 = GenerateNoise(w)
    noise2 = MakeIsland(noise2,w,-200.0)
    
    #print noise2[0:10]
    
    final_noise = []
    for counter,item in enumerate(noise1):
        #print item
        average = (item[2] + (noise2[counter][2]))/2.0
        final_noise.append([item[0],item[1],average])
    """
    
    #No island
    for item in noise1:
        item[2] = item[2]*60+120
    
    
   
    return noise1
    