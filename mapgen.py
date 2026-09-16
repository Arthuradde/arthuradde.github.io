import math
import yaml
import random

import numpy as np
import opensimplex as simplex

import view

SEED_MAX = 2147483647

default_params = {
    'WIDTH' : 120,
    'HEIGHT' : 120,

    'WAVELENGTH' : 15,
    'CLIMATE_WL' : 30,

    'SHALLOW_LEVEL' : -0.20,
    'SEA_LEVEL' : -0.50,
    #'SAND_LEVEL' : 0.20,
    'MOUNTAIN_LEVEL' : 0.65,
    'SUMMIT_LEVEL' : 0.80,

    'COLD_LEVEL' : -0.5,
    'HOT_LEVEL' : 0.5,

    'FREEZE_LEVEL' : -0.60
}

def lerp(a, b, t):
    return (1 - t) * a + t * b 

def get_sources(width, height, height_map, sea_level):
    sources = []
    for i in range(0,10):
        # Initialize climber with random non-border tile
        climber = [random.randint(2, width-3),random.randint(2, height-3)]
        # Move to the highest neighbour up to a local maxima
        maxima_found = False
        iteration = 0
        while maxima_found == False:
            climber_height = height_map[tuple(climber)]
            neighbours = [ [climber[0],climber[1]-1], [climber[0]+1,climber[1]], [climber[0],climber[1]+1], [climber[0]-1,climber[1]] ]
            neighbours_heights = [height_map[x[0],x[1]] for x in neighbours] 
            if climber_height == max(neighbours_heights + [climber_height]):
                if climber not in sources:
                    sources.append(climber)
                maxima_found = True
            else:
                for neighbour in neighbours:
                    if height_map[tuple(neighbour)] == max(neighbours_heights):
                        climber = neighbour
                        break
    
    source_min_dist = 3
    
    to_remove = []
    for source_a in sources:
        for source_b in sources:
            if source_a != source_b:
                if abs(source_a[0]-source_b[0]) < source_min_dist or abs(source_a[1]-source_b[1]) < source_min_dist:
                    if height_map[tuple(source_a)] > height_map[tuple(source_b)]:
                        to_remove.append(source_b)
                    else:
                        to_remove.append(source_a)
    
    sources = [source for source in sources if source not in to_remove]
    sources = [source for source in sources if height_map[tuple(source)] > sea_level]
        
    return sources
    


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
    freeze_lvl = default_params['FREEZE_LEVEL'],
    gen_rivers = True,
    gen_trees = True
    ):
    
    # Random seed initialization
    if seed != None:
        random.seed(seed)
    
    # Base height map
    simplex.seed(random.randint(0, SEED_MAX))
    noise_map = np.empty((width, height))
    for y in range(0, height):
        for x in range(0, width):
            noise_map[x, y] = (simplex.noise2(x/wavelength, y/wavelength)
            + 0.5 * simplex.noise2(2*x/wavelength, 2*y/wavelength)
            + 0.25 * simplex.noise2(4*x/wavelength, 4*y/wavelength)
            )/1.75
            
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
    simplex.seed(random.randint(0, SEED_MAX))
    climate_map = np.empty((width, height))
    for y in range(0, height):
        for x in range(0, width):
            climate_map[x, y] = simplex.noise2(x/climate_wl, y/climate_wl)

    # Tree map : "Tree" value of each tile
    simplex.seed(random.randint(0, SEED_MAX))
    tree_map = np.empty((width, height))
    for y in range(0, height):
        for x in range(0, width):
            tree_map[x, y] = simplex.noise2(x, y)
    
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
                
                # Hot/cold
                if climate_map[x,y] < cold_lvl:
                    tilemap[x,y] = 7
                elif climate_map[x,y] > hot_lvl:
                    tilemap[x,y] = 8
                else:
                    tilemap[x,y] =  2
                    
                # Tree placement
                if gen_trees == True:
                    if (tree_map[x,y]*2)-1 > abs(climate_map[x,y]):
                        if tilemap[x,y] == 2:
                            tilemap[x,y] = [10,11][random.randint(0,1)]
                        elif tilemap[x,y] == 7:
                            tilemap[x,y] = 13
                        elif tilemap[x,y] == 8:
                            tilemap[x,y] = 14
                    
            elif height_map[x, y] < summit_lvl:
                tilemap[x,y] = 3
            else:
                tilemap[x,y] = 5
                
                
    # Create rivers
    if gen_rivers == True:
        sources = get_sources(width, height, height_map, sea_lvl)
        orig_height_map = height_map
        for source in sources:
            river = []
            lakes = []
            step = source
            minima_found = False
            while True:
                river.append(step)
                step_height = height_map[tuple(step)]
                
                # If we're at the sea level, stop
                if step_height < sea_lvl:  
                    break
                
                # Check nearby tiles
                neighbours = [ [step[0],step[1]-1], [step[0]+1,step[1]], [step[0],step[1]+1], [step[0]-1,step[1]] ]
                neighbours_heights = [height_map[x[0],x[1]] for x in neighbours] 
                
                # If there's a lower neighbour, select it for the next step
                if step_height != min(neighbours_heights + [step_height]):
                    for neighbour in neighbours:
                        if height_map[tuple(neighbour)] == min(neighbours_heights):
                            step = neighbour
                            break

                # If we're at a minima, make a lake
                else:
                    lake = []
                    lake.append(step)
                    lake_level = step_height
                    lake_edges = neighbours
                    
                    #print("Starting lake")
                    #print(step)
                    #print(lake_level)
                    
                    while True: 
                        # Raise the water level to the lowest bordering tiles
                        edges_heights = [height_map[x[0],x[1]] for x in lake_edges] 
                        lake_level = min(edges_heights)
                        exit_candidate = lake_edges[edges_heights.index(lake_level)]
                        #print(exit_candidate)
                        #print(lake_level)
                        candidate_neighbours = [ [exit_candidate[0],exit_candidate[1]-1], [exit_candidate[0]+1,exit_candidate[1]],
                                                [exit_candidate[0],exit_candidate[1]+1], [exit_candidate[0]-1,exit_candidate[1]] ]
                        
                        candidate_neighbours = [x for x in candidate_neighbours if x not in lake]
                        candidate_neighbours = [x for x in candidate_neighbours if x not in lake_edges]
                        
                        neighbours_heights = [height_map[x[0],x[1]] for x in candidate_neighbours] 
                        # If none of these bordering tiles have a valid candidate to continue the river, repeat
                        if all(neighbour >= lake_level for neighbour in neighbours_heights):
                            lake.append(exit_candidate)
                            lake_edges.remove(exit_candidate)
                            lake_edges += candidate_neighbours
                            
                        # Else, end the lake
                        else:
                            step = exit_candidate
                            lakes.append(lake)
                            for tile in lake:
                                tilemap[tuple(tile)] = 29
                                height_map[tuple(tile)] = lake_level
                            break
                        
            all_lakes = []
            for lake in lakes:
                all_lakes += lake
            
            # Assign tiles for all non-lake river steps
            tilemap[tuple(source)] = 20
            for i in range(1,len(river)-1):
                step = river[i]
                if step not in all_lakes:
                    if river[i-1] not in all_lakes:
                        if abs(river[i+1][0]-river[i-1][0]) == 2:
                            tilemap[tuple(step)] = 21
                        elif abs(river[i+1][1]-river[i-1][1]) == 2:
                            tilemap[tuple(step)] = 22
                        elif river[i-1][0] == step[0] - 1 or river[i+1][0] == step[0] - 1:
                            if river[i-1][1] == step[1] - 1 or river[i+1][1] == step[1] - 1:
                                tilemap[tuple(step)] = 28
                            else:
                                tilemap[tuple(step)] = 25
                        else:
                            if river[i-1][1] == step[1] - 1 or river[i+1][1] == step[1] - 1:
                                tilemap[tuple(step)] = 27
                            else:
                                tilemap[tuple(step)] = 26
                    else:
                        if abs(river[i+1][0]-river[i][0]) == 1:
                            tilemap[tuple(step)] = 21
                        elif abs(river[i+1][1]-river[i][1]) == 1:
                            tilemap[tuple(step)] = 22
                        
                
    
    # Transform into a map dict
    f = np.vectorize(lambda x: {"id" : 0,"tile" : x })
    tilemap2 = f(tilemap)
    newmap = {"name":"New Map","tiles":tilemap2}
    
    return newmap
