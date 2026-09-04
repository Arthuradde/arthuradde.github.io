import math
import yaml
import numpy as np
import opensimplex as simplex

import view

shallow_level = -0.20
sea_level = 0.20
sand_level = 0.20
mountain_level = 0.65
summit_level = 0.80

cold_level = -0.5
hot_level = 0.5

width = 60
height = 60

wavelength = 5
climate_wl = 10

def lerp(a, b, t):
    return (1 - t) * a + t * b 

def gen_test():
    
    # Base height map
    simplex.random_seed()
    noise_map = np.empty((width, height))
    for y in range(0, height):
        for x in range(0, width):
            noise_map[x, y] = simplex.noise2(x/wavelength, y/wavelength)
            #+ 0.5*simplex.noise2(2*x/wavelength, 2*y/wavelength)
            #+ 0.25*simplex.noise2(4*x/wavelength, 4*y/wavelength)
            
    height_map = noise_map
    # Adjust height map for sea border
    d_map = np.empty((width, height))
    for y in range(0, height):
        for x in range(0, width):
            d_map[x,y] = round( 1 - (1 - pow(2*x/(width-1)-1,2)) * (1 - pow(2*y/(height-1)-1,2)) ,2)
            height_map[x,y] = lerp(height_map[x,y], 2*(1-d_map[x,y])-1, pow(d_map[x,y],3))
    
    #print(d_map)
    #print(height_map)
    
    # Climate map : hot and cold regions
    simplex.random_seed()
    climate_map = np.empty((width, height))
    for y in range(0, height):
        for x in range(0, width):
            climate_map[x, y] = simplex.noise2(x/climate_wl, y/climate_wl)
    
    # Attribute biome to tiles
    tilemap = np.empty((width, height))
    for y in range(0, height):
        for x in range(0, width):
            if height_map[x, y] < shallow_level:
                if climate_map[x,y] < cold_level:
                    tilemap[x,y] = 9
                else:
                    tilemap[x,y] = 1
            elif height_map[x, y] < sea_level:
                if climate_map[x,y] < cold_level:
                    tilemap[x,y] = 9
                else:
                    tilemap[x,y] = 4
            elif height_map[x, y] < sand_level:
                tilemap[x,y] = 6
            elif height_map[x, y] < mountain_level:
                if climate_map[x,y] < cold_level:
                    tilemap[x,y] = 7
                elif climate_map[x,y] < hot_level:
                    tilemap[x,y] = 2
                else:
                    tilemap[x,y] = 8 
            elif height_map[x, y] < summit_level:
                tilemap[x,y] = 3
            else:
                tilemap[x,y] = 5
    
    # Transform into a map dict
    f = np.vectorize(lambda x: {"id" : 0,"tile" : x })
    tilemap2 = f(tilemap)
    newmap = {"name":"test","tiles":tilemap2}
    
    return newmap
    
    
    
    
newmap = gen_test()
#view.printmap(newmap)
print(view.maptostring(newmap))