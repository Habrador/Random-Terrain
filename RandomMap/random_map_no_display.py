#===============================================================================
# Create random coordinates to better measure time
#===============================================================================

import time

#Map generation techniques
from _map_generating_methods.hill_algorithm import * #@UnusedWildImport
from _map_generating_methods.particle_deposition import * #@UnusedWildImport
from _map_generating_methods.sparks import * #@UnusedWildImport
from _map_generating_methods.value_noise import * #@UnusedWildImport
from _map_generating_methods.diamond_square import * #@UnusedWildImport


GAME_WIDTH = 640
GAME_HEIGHT = 640

SCALING = 2 #The size of the generated map, 3 is best, 2 works, 1 breaks the system (when displaying it)


time_before = time.time()

#coordinates = Sparks(GAME_WIDTH/SCALING,GAME_HEIGHT/SCALING)
#coordinates = ParticleDeposition(GAME_WIDTH/SCALING,GAME_HEIGHT/SCALING)
#coordinates = HillAlgorithm(GAME_WIDTH/SCALING,GAME_HEIGHT/SCALING)
#coordinates = HillAlgorithm_mod(GAME_WIDTH/SCALING,GAME_HEIGHT/SCALING)
#coordinates = ValueNoise2(GAME_WIDTH/SCALING,GAME_HEIGHT/SCALING)
coordinates = DiamondSquare(513)

print 'It took', time.time()-time_before, 'seconds to generate the heightmap'