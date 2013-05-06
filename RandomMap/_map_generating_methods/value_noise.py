#===============================================================================
# Value Noise - often confused with Perlin Noise
# http://devmag.org.za/2009/04/25/perlin-noise/
# http://lodev.org/cgtutor/randomnoise.html
# http://breinygames.blogspot.co.nz/2012/06/generating-terrain-using-perlin-noise.html
# http://freespace.virgin.net/hugo.elias/models/m_perlin.htm
#===============================================================================

import random
import math

#------------------------------------------------------------------------------ 
# Method 1 (poor result?) from http://freespace.virgin.net/hugo.elias/models/m_perlin.htm
def ValueNoise1(GAME_WIDTH,GAME_HEIGHT):
    """Similar to Minecraft?"""
    
    frequency = 1 #frequency = 1/wavelength
    octaves = 16
    amplitude = 64 #the difference between the minimum and maximum values
    
    #Generate the basic map where each coordinate is at 0 < z < 1 randomly
    random_coordinates = [] #(x,y,z)
    for x in range(GAME_WIDTH): #Divide by the width of each tile
        for y in range(GAME_HEIGHT):
            z = random.randint(0, 1000)/1000.0
            random_coordinates.append([x,y,z])
    
    
    def get_random(x,y):
        """Returns the random z value at position x,y"""
        for item in random_coordinates:
            n = random.randint(0, 1000)/1000.0 #Default if the coordinate doesn't exist
            if item[0] == x and item[1] == y:
                n = item[2]
            
            return n
    
    
    def cosine_interpolation(a,b,x):
        ft = x * math.pi
        f = (1 - math.cos(ft)) * .5

        return  a*(1-f) + b*f
    
    
    def smoothed_noise(x,y):
        #Get the weighted average value of the 9 random z-values
        #(x-1,y-1),(x,y-1),(x+1,y-1),
        #(x-1,y),(x,y),(x+1,y),
        #(x-1,y+1),(x,y+1),(x+1,y+1)
        #print get_random(x-1,y-1)
        corners = sum([get_random(x-1,y-1),get_random(x+1,y-1),get_random(x-1,y+1),get_random(x+1,y+1)]) / 16. #weights???
        sides   = sum([get_random(x,y-1),get_random(x-1,y),get_random(x+1,y),get_random(x,y+1)]) / 8.
        center  = sum([get_random(x,y)]) / 4.       
        
        return corners + sides + center
    
    
    def interpolated_noise(x,y):
        integer_X    = int(x)
        fractional_X = x - integer_X
    
        integer_Y    = int(y)
        fractional_Y = y - integer_Y
        
        v1 = smoothed_noise(integer_X,     integer_Y)
        v2 = smoothed_noise(integer_X + 1, integer_Y)
        v3 = smoothed_noise(integer_X,     integer_Y + 1)
        v4 = smoothed_noise(integer_X + 1, integer_Y + 1)
        
        i1 = cosine_interpolation(v1 , v2 , fractional_X)
        i2 = cosine_interpolation(v3 , v4 , fractional_X)
        
        return cosine_interpolation(i1 , i2 , fractional_Y)
    
    
    #Calculate the total noise in one point x y
    def calculate_noise(x,y):
        total_noise = 0
        p = 1./4
        for i in range(octaves):
            frequency = 2**i
            amplitude = p**i
            total_noise += interpolated_noise(x*frequency,y*frequency) * amplitude
        
        return total_noise
    
    
    #The final calculations
    world_coordinates = [] #(x,y,z)
    for x in range(GAME_WIDTH): #Divide by the width of each tile
        for y in range(GAME_HEIGHT):
            z = calculate_noise(x,y)
            world_coordinates.append([x,y,z*128.])
    
    return world_coordinates 



#------------------------------------------------------------------------------ 
# Method 2 from http://lodev.org/cgtutor/randomnoise.html
def ValueNoise2(GAME_WIDTH,GAME_HEIGHT):
    #------------------------------------------------------------------------------ 
    #Methods
    def smooth_noise(x, y):
    
        """Returns the average value of the 4 neighbors of (x, y) from the
           noise array."""
        
        fractX = x - int(x)
        fractY = y - int(y)
        
        x1 = (int(x) + GAME_WIDTH) % GAME_WIDTH
        y1 = (int(y) + GAME_HEIGHT) % GAME_HEIGHT
        
        x2 = (x1 + GAME_WIDTH - 1) % GAME_WIDTH
        y2 = (y1 + GAME_HEIGHT - 1) % GAME_HEIGHT
        
        #Bilinear interpolation http://en.wikipedia.org/wiki/Bilinear_interpolation
        value = 0.0
        value += fractX       * fractY       * noise[y1][x1]
        value += fractX       * (1 - fractY) * noise[y2][x1]
        value += (1 - fractX) * fractY       * noise[y1][x2]
        value += (1 - fractX) * (1 - fractY) * noise[y2][x2]
        
        return value
    
    
    def turbulence(x, y, size):
        """
        This function controls how far we zoom in/out of the noise array.
        The further zoomed in gives less detail and is more blurry.
        """
        
        value = 0.0
        initial_size = size
        
        while size >= 1:
            value += smooth_noise(x / size, y / size) * size
            size /= 2.0 #The zooming factor started at 16 here, and is divided through two each time. Keep doing this until the zooming factor is 1.
        
        return 128.0 * value / initial_size #The return value is normalized so that it'll be a number between 0 and 255
    
    
    
    
    #------------------------------------------------------------------------------ 
    # Main
    
    frequency = 0.4 #A smaller number generates a more "zoomed-in" terrain with fewer details
    octaves = 10.0 #Smaller number generates more lakes, 0.4 and 10 gives a good result if 320*240 in 2 seconds
    
    #Generate a list with random noise between 0 and 1
    noise = []
    for y in range(0, GAME_HEIGHT):
        noise_row = []
        for x in range(0, GAME_WIDTH):
            noise_row.append(random.randint(0, 1000)/1000.0)
        
        noise.append(noise_row)

    
    result = []
    for y in range(0, GAME_HEIGHT):
        row = []
        for x in range(0, GAME_WIDTH):
            noise_smooth_turbulent = int(turbulence(x*frequency,y*frequency,octaves))
            row.append(noise_smooth_turbulent)
        
        result.append(row)
    
    
    #Standardize the coordinates [x,y,z]
    world_coordinates = []
    for y,row in enumerate(result):
        for x,c in enumerate(row):
            world_coordinates.append((x,y,c))

    return world_coordinates