import yaml
import numpy as np
import opensimplex as simplex
import view

shallow_level = -0.25
sea_level = 0.25
mountain_level = 0.60
summit_level = 0.80

feature_size = 5

def gen_test(width, height):
    
    simplex.random_seed()
    heightmap = np.empty((width, height))
    
    for y in range(0, height):
        for x in range(0, width):
            value = simplex.noise2(x / feature_size, y / feature_size)
            heightmap[x, y] = value
    print(heightmap)
    
    tilemap = np.empty((width, height))
    
    for y in range(0, height):
        for x in range(0, width):
            if heightmap[x, y] < shallow_level:
                tilemap[x,y] = 1
            elif heightmap[x, y] < sea_level:
                tilemap[x,y] = 4
            elif heightmap[x, y] < mountain_level:
                tilemap[x,y] = 2
            elif heightmap[x, y] < summit_level:
                tilemap[x,y] = 3
            else:
                tilemap[x,y] = 5
    
    f = np.vectorize(lambda x: {"id" : 0,"tile" : x })
    tilemap2 = f(tilemap)
    newmap = {"name":"test","tiles":tilemap2}
    view.printmap(newmap)
    
gen_test(60, 60)