import view, mapgen


def genmap(seed):
    newmap = mapgen.gen_test(seed)
    view.printmap(newmap)


def testprintmap():
    
    file = open('maps/map1.json', 'r')
    map = json.load(file)

    view.printmap(map)

    #strmap = maptostring(map)
    #print(strmap)
    
genmap(seed=12334)
