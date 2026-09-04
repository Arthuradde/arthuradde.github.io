import yaml
import json

colors = {
    'BLUE' : '\033[94m',
    'CYAN' : '\033[96m',
    'GREEN' : '\033[92m',
    'YELLOW' : '\033[93m',
    'RED' : '\033[91m',
    'WHITE' : '\033[0m',
    'PINK' : '\033[95m',
    'END' : '\033[0m',
    'BOLD' : '\033[1m',
    'UNDERLINE' : '\033[4m',
    'BROWN' : '\033[33m',
    'DBLUE' : '\033[34m',
    'BG_CYAN' : '\033[106m',
}

html_colors = {
    'BLUE' : 'Blue',
    'CYAN' : 'Cyan',
    'GREEN' : 'green',
    'YELLOW' : 'yellow',
    'RED' : 'red',
    'WHITE' : 'white',
    'PINK' : 'pink',
    'END' : 'white',
    'BOLD' : '\033[1m',
    'UNDERLINE' : '\033[4m',
    'BROWN' : '#7B3F00',
    'DBLUE' : 'darkBlue',
    'BG_CYAN' : '\033[106m',
}

file = open('tiles.yml', 'r')
tiles = yaml.safe_load(file)['tiles']


        
def printmap(map):
    print("#" * (len(map['name']) + 4))
    print(f"# {map['name']} #")
    print("#" * (len(map['name']) + 4))
    
    for line in map['tiles']:
        for case in line:
            tile = next((x for x in tiles if x['id'] == case['tile']), tiles[0])
            print(f"{colors[tile['color']]} {tile['tile']} {colors['END']}", end='')
        print('')
        
    print('--------')
    
    for tile in tiles[1:]:
        print(f"{colors[tile['color']]} {tile['tile']} {colors['END']}   {tile['name']}")

def maptostring(map):
    map_string = ""
    map_string += "#" * (len(map['name']) + 4) + '\n\r'
    map_string += f"# {map['name']} #" + '\n\r'
    map_string += "#" * (len(map['name']) + 4) + '\n\r'
    
    for line in map['tiles']:
        for case in line:
            tile = next((x for x in tiles if x['id'] == case['tile']), tiles[0])
            map_string += f"{colors[tile['color']]} {tile['tile']} {colors['END']}"
        map_string += '\n\r'
        
    map_string += '--------' + '\n\r'
    
    for tile in tiles[1:]:
        map_string += f"{colors[tile['color']]} {tile['tile']} {colors['END']}   {tile['name']}" + '\n\r'
        
    return map_string

def maptohtml(map):
    map_string = ""
    map_string += "<span style='color:white;'>#" * (len(map['name']) + 4) + '</span>' + '<br>'
    map_string += f"<span style='color:white;'># {map['name']} #</span>" + '<br>'
    map_string += "<span style='color:white;'>#" * (len(map['name']) + 4) + '</span>' + '<br>'
    
    for line in map['tiles']:
        for case in line:
            tile = next((x for x in tiles if x['id'] == case['tile']), tiles[0])
            map_string += f"<span style='color:{html_colors[tile['color']]};'> {tile['tile']} </span>"
        map_string += '<br>'
        
    map_string += "<span style='color:white;'>---------------</span>" + '<br>'
    
    for tile in tiles[1:]:
        map_string += f"<span style='color:{html_colors[tile['color']]};'>{tile['tile']}</span> <span style='color:white;'>  {tile['name']} </span> " + '<br>'
        
    return map_string
    

#file = open('maps/map1.json', 'r')
#map = json.load(file)

#printmap(map)

#strmap = maptostring(map)
#print(strmap)