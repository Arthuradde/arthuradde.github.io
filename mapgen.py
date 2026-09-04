import math
import yaml
import numpy as np
import opensimplex as simplex

import view

default_params = {
    'WIDTH' : 60,
    'HEIGHT' : 60,

    'WAVELENGTH' : 5,
    'CLIMATE_WL' : 10,

    'SHALLOW_LEVEL' : -0.20,
    'SEA_LEVEL' : 0.20,
    #'SAND_LEVEL' : 0.20,
    'MOUNTAIN_LEVEL' : 0.65,
    'SUMMIT_LEVEL' : 0.80,

    'COLD_LEVEL' : -0.5,
    'HOT_LEVEL' : 0.5,

    'FREEZE_LEVEL' : -0.60
}


def lerp(a, b, t):
    return (1 - t) * a + t * b 

def gen_test(
    seed = None,
    width = default_params['WIDTH'],
    height = default_params['HEIGHT'],
    wavelength = default_params['WAVELENGTH'],
    climate_wl = default_params['CLIMATE_WL'],
    shallow_lvl = default_params['SHALLOW_LEVEL'],
    sea_lvl = default_params['SEA_LEVEL'],
    mountain_lvl = default_params['MOUNTAIN_LEVEL'],
    summit_lvl = default_params['SUMMIT_LEVEL'],
    cold_lvl = default_params['COLD_LEVEL'],
    hot_lvl = default_params['HOT_LEVEL'],
    freeze_lvl = default_params['FREEZE_LEVEL']
    ):
    
    # Base height map
    if seed == None:
        simplex.random_seed()
    else:
        simplex.seed(seed)
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
    if seed == None:
        simplex.random_seed()
    else:
        simplex.seed(seed*3-9)
    climate_map = np.empty((width, height))
    for y in range(0, height):
        for x in range(0, width):
            climate_map[x, y] = simplex.noise2(x/climate_wl, y/climate_wl)
    
    # Attribute biome to tiles
    tilemap = np.empty((width, height))
    for y in range(0, height):
        for x in range(0, width):
            if height_map[x, y] < shallow_lvl:
                if climate_map[x,y] < freeze_lvl:
                    tilemap[x,y] = 9
                else:
                    tilemap[x,y] = 1
            elif height_map[x, y] < sea_lvl:
                if climate_map[x,y] < freeze_lvl:
                    tilemap[x,y] = 9
                else:
                    tilemap[x,y] = 4
            #elif height_map[x, y] < sand_lvl:
            #    tilemap[x,y] = 6
            elif height_map[x, y] < mountain_lvl:
                if climate_map[x,y] < cold_lvl:
                    tilemap[x,y] = 7
                elif climate_map[x,y] < hot_lvl:
                    tilemap[x,y] = 2
                else:
                    tilemap[x,y] = 8 
            elif height_map[x, y] < summit_lvl:
                tilemap[x,y] = 3
            else:
                tilemap[x,y] = 5
    
    # Transform into a map dict
    f = np.vectorize(lambda x: {"id" : 0,"tile" : x })
    tilemap2 = f(tilemap)
    newmap = {"name":"New Map","tiles":tilemap2}
    
    return newmap
