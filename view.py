import yaml
import json

colors = {
    'BLUE' : '\033[94m',
    'CYAN' : '\033[96m',
    'GREEN' : '\033[92m',
    'YELLOW' : '\033[93m',
    'RED' : '\033[91m',
    'PINK' : '\033[95m',
    'END' : '\033[0m',
    'BOLD' : '\033[1m',
    'UNDERLINE' : '\033[4m',
    'BROWN' : '\033[33m',
    'DBLUE' : '\033[34m'
}

file = open('tiles.yml', 'r')
tiles = yaml.safe_load(file)['tiles']


def legend():
    for tile in tiles[1:]:
        print(f"{colors[tile['color']]} {tile['tile']} {colors['END']}   {tile['name']}")
        
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
    legend()
    


file = open('maps/map1.json', 'r')
map = json.load(file)
printmap(map)