
# coding: utf-8

# In[18]:


import copy
import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import operator
from collections import deque
import time



puzzle_input = """#################################################################################
#.......#...#...#...........#.....#...#.#.....#m......#.......#.....#........u..#
#####.#.#.#.#.#.###.#######.###.#.#.#.#.#.###.###.#####.#.###.###.#.###########.#
#.....#...#...#.....#.#.....#...#...#...#.#....e#.......#...#.....#.....#.......#
#.###################.#.#####.#########.#.#####.###########.###########.#.#######
#.#...#...#...........#.#.....#.......#.#.....#.....#.....#...#.......#.#.#.....#
#.#S#.###.#.#####.#####.#.###.#.###.###.#####.#####.#.###.###.#.#.#####.#.#.###.#
#.#.#...#.#...#.#.......#.#.#.#.#...#...#.D.#.#...#...#.#.#...#.#.#.....#j..#...#
#.#.###.#.###.#.#########.#.#.###.###.###.#.#.#.#.#####.#.#.###.###.#########.###
#.#...#.#...#...#.#.........#...#.#...#.#.#...#.#.....#...#...#...#.#.#.....#...#
#.###.#.###.###.#.#.#########.#.#.#.###.#.#####.#####.#.#####.###.#.#.#.#.#.###.#
#...#.#c..#.....#.......#...#.#.#.#.#...#...#.....#.#.#.#.....#...#.#...#.#...#.#
#.###.###.#.#############.#.###.#.#.#.#.###.#####.#.#.#.#.#####.###.#.###.###.#.#
#.#...#.#.#.........#.....#...#.#.....#.#.#...#.#...#.#...#...#.....#.#...#...K.#
#.#.###.#.#########.#.#######.#.#########.###.#.###.#.#####.#.#.#######.#########
#.......#.#.......#h..#.....#.#.........#...#.#.....#.......#...#.....#.#...#...#
#.#######.#O#####.#######.#.#.#.#######.###.#.#.#######.#######.#.###F#.#.#.#.#.#
#.#....y..#...#...#.....#.#.#.#.#.#.....#...#.#.#.....#.#.....#...#.#.#...#.#.#.#
###.#####.###.#.###.###.#.###.#.#.#.###.#.#.#.###.###.#.#.###.#####.#.#.###.#.#.#
#...#.....#.#.#...#.#.Z.#...#.#.#.#.#...#.#.#.....#.#.#.#.#.#...#.....#...#...#.#
#.###.#####.#.###A#.#.###.#.#.#.#.#.#####.#########.#.#.#.#.###.#.#########.###.#
#.#.#.#.....#.#.#...#.#...#...#...#.....#.#.........#.#.#.#.#...#.#.......#.#...#
#.#.#.#####.#.#.#######.#########.#####.#.#.#####.#.#.#.#.#.#####.#.###.#.###.#.#
#.#.#...#...#.#...#.....#.....#.......#.#.#.#.#...#.#.#.#.#.....#.#.#...#.....#.#
#.#.###.#.#.#.###.#.#######.#.#####.###.#.#.#.#.#####.#.#.#.#.###.###.#########X#
#.#...#...#.#...#.#...#.....#.....#.#...#.....#.#...#.#.#.#.#...#...#.....#.....#
#.#W#.#####.###N#.###.#.#.#######.###.#.#######.#.#.#.###.#.###.###.#####.###.###
#i#.#.....#.#.#.#...#.#.#.#.....#.....#.#..r..#...#.#...#.#.#.....#.#...#...#.#.#
#.#######.#.#.#.#.###.###.#.###########.#.###.#.###.###.#.###.#####.#.#.###.#.#.#
#.......#...#.#.#...#...#.#.............#.#.#.#.#.#...#...#...#.....#.#.....#.#.#
#.#####.#.###.#.#.#.###.#.#.#############.#.#.#.#.###.#####.###.#####.#######.#.#
#.#.#...#.....#.#.#...#..t#...#.#.......#.#.#.#...#.....#.....#...#...#.....#.#.#
#.#.#.#######.#.#.###.#######.#.#.#.#####.#.#.#.###.###.#####.###.###.#.###.#.#.#
#...#.#...#...#.#...#.....#.#.#...#.....#.#.#.#.#...#.........#.#...#...T.#.#...#
###.#.#.#.#.###.###.#.###.#.#.#########.#.#.#.###.###########.#.###.#####.#.###.#
#...#...#.#.#...#...#...#...#.......#...#.#.#...#.#.....#...#...#...#...#.#...#.#
#.#######.###.###.#####.###########.#.###.#.###.#.#.###.#.#.###.#.###.#.#####.###
#.#...#v#...#.#.#.....#.........#...#...#.#.......#...#..l#...#.#.....#.....#.P.#
#.#.#.#.###.#.#.#####.#########.#.#####.#.###########.#######.#############.###.#
#...#.....#...#...............#........1#2..................#....b..............#
#################################################################################
#...#.#.........#.....#...........#....3#4....#...#.....#.......#...#.....Q.#...#
#.#.#.#.#####.###.#.#.#.#####.###.#.###.#.###.#.#.#.###.#.#####.#.#.#.#.###.###.#
#.#.#.#.#...#.....#.#.#.#.#...#...#...#.#.#.....#.#...#...#.....#.#.#.#...#.#...#
#.#.#.#.#.#.#######.###.#.#.#####.###.#.#.#######.###.#####.#####.#.#.###.#.#.#.#
#.#...#.#.#.....#.#.#.B...#.....#.#...#.#.....#.....#.#...#.......#.#.#...#...#.#
#.#####.#.#####.#.#.#.#######.#.###.###.#.###.###.###.#.#####.#####.#.#.#######.#
#.#...#q#..f#.....#...#.....#.#...#.#...#.#.#...#.#.....#...#.#...#...#.#.....#.#
#.#.#.#.#.#.#######.###.###.###.#.#.#.###.#.###.###.#####.#.#.###.#####.#.###.#.#
#...#.#.#.#...#...#p..#.#.#...#.#...#...#.....#...#.#.....#.#.....#...#...#...#.#
#####.#.#####.#.#.###.#.#.###.#########.#####.###.#.#.#####.#####.###.#####.###.#
#.....#.......#.#.#...#.#...#.#.......#.#...#.#.#...#.#...#.....#.....#.#...#.#.#
#.###########.#.#.#####.###.#L#.#####R#.#.#.#.#.#####.#.#.#####.#####.#.#.###.#.#
#...........#.#.#.......#...#...#...#...#.#.#.....#...#.#.....#...#...#.#...#...#
#######.###.#.#.#########.#.#####.#.#######.#####.#.#######.#.###.#.###.###.###.#
#.......#...#.#.#.........#.......#.....#...#.....#.#.....#.#...#.#...#...#...#.#
#.#######.###.#.#.###.#################.#.###.#####.#.#.#.###.###.###.###.###.#.#
#.#.........#.#.#...#.............#.....#.........#.#.#.#.....#...#.#.......#.#.#
#.###.#######.#.###########.#####.#.###############.###.#####.#.###.#.#####.#.###
#...#.#.......#.#.........#.#...#.#.#...#.......#...#...#.#...#.#.....#...#.#...#
#.#G###.#######.#.#######.#.###.#.###.#.#.#####.#.###.###.#.###.#######.#.#####.#
#.#...#....x#.#.#.#z#.....#.....#.....#.#.....#...#...#...#.#...#.......#.#...#.#
#.###.#####.#.#.#.#.#########.#########.#####.#######.#.###.#####.#######.#.#.#.#
#k#.#.....#...#...#.#.....#...#.......#.#...#.#.......#.#...#.....#.#...#...#.#.#
#.#.#####.###.#####.#.###.#.###.#####.#.#.#.#.#.#.#####.#.###.#####.#.#.#####.#H#
#.#.....#...#.....#.#...#.#.#...#...#...#.#...#.#.#.....#.#...#...#...#...#.#.#.#
#.#.###.###.#####.#.###.#.#.#.###.#.###.#.#######.#.###.#.#.###.#.#.###.#Y#.#.#.#
#...#...#.#...#...#.....#..o#.#.#.#.....#.#.......#.#...#...#...#...#...#...#..g#
#####.###.#.###.#######.#####.#.#.#######.#####.###.###.#############.#####.###.#
#...#.#...#.....#.....#.....#.#.#...#...#.......#.....#...#...........#.#...#...#
#.#.#.###.#######.###.#######.#.###.#.###########.###.###.#.###########.#.###.###
#.#.#.#.....#.#.....#.#.......#...#.#...#...#...#...#.#...#.......#...#.I.#.#...#
#.#.#.#.###.#.#.###.#.#.#######.#.#.###.#.###.#.#.###.#.#########.###.#.###.###.#
#.#.#.#.#...#s....#.#.#.......#a#.#.....#.#...#.#.#...#.....#.....#...#.....#.#.#
#.###M#U###.#####.#.#.###.###.###.#####.#.#.###.#.#.#.#####.#.#####.#V#####.#.#.#
#.....#...#...#...#.#...#...#.#...#....n#.#...#d..#.#.#.J.#...#.....#...#..w#.#.#
#.#######.###.#####.###.#####.#.###.#####.###.#####.#.#.#.###.#####.#####.###.#.#
#.......#.#.#...#...#.#.....#.#...#.#...#...#.#.#...#.#.#.#...#...#...........#.#
#######.#.#.###E#.###.#####.#.#.#.#.###.#.###.#.#.#####.#.#####.#.#############.#
#.........#.......#.........C.#.#.......#.......#.......#.......#...............#
#################################################################################"""


# In[19]:


CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

def delete_last_lines(n=1):
    for _ in range(n):
        print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
#        sys.stdout.write(CURSOR_UP_ONE)
#        sys.stdout.write(ERASE_LINE)

def print_field(xyids, DBG=True):
    coords = xyids.keys()
    if(DBG): print(xyids)
    x_min = min(coords, key = lambda t: t[0])[0]-1
    x_max = max(coords, key = lambda t: t[0])[0]+1
    y_min = min(coords, key = lambda t: t[1])[1]-1
    y_max = max(coords, key = lambda t: t[1])[1]+1
    
    if(DBG): print(x_min,x_max,y_min,y_max)

    for yy in range(y_min,y_max+1):
        ss = ""
        for xx in range(x_min,x_max+1):
            if (xx,yy) in xyids:
                ss += str(xyids[(xx,yy)])
            else:
                ss += "#"
        print(ss)
    
    #delete_last_lines(y_max-y_min)
    


# In[20]:


def connect(xx,yy,kkk,g_all,field):
    k_c = (xx,yy)
    if (k_c in field):# and (field[k_c]==1):
        kkc = (xx,yy,field[k_c])
        g_all.add_node(kkc)
        g_all.add_edge(kkc,kkk)

def create_world(ccc, DBG=True):
    field = {}
    keys = {}
    doors = {}
    entries = {}
    g_all = nx.Graph()
    level = 0
    in_out =''
    x=-1
    y=-1
        
    for line in ccc.splitlines():
        y+=1
        x=-1
        for c in line:
            x+=1
            if c==' ' or c=='#':
                continue
            else: field[(x,y)]=c

    if DBG:print(field)
    if DBG:print_field(field)
    
    for k in field.keys():
        (x,y) = k
        kkk = (x,y,field[k])
        # connect
        # left
        connect(x-1,y,kkk,g_all,field)
        # right
        connect(x+1,y,kkk,g_all,field)
        # up
        connect(x,y-1,kkk,g_all,field)
        # down
        connect(x,y+1,kkk,g_all,field)
        #
        if (field[k]>='a') and(field[k]<='z'):
            keys[field[k]] = kkk
        elif (field[k]>='A') and(field[k]<='Z'):
            doors[field[k]] = kkk
        elif (field[k]=='@' or (field[k]>='1' and field[k]<='4')):
            entries[field[k]] = kkk
    
    if(DBG):print("***FINAL GRAPH")
    if(DBG):print("nodes",len(g_all.nodes), list(g_all.nodes))
    if(DBG):print("edges",len(g_all.edges), list(g_all.edges))
    if(DBG):print("#nodes",len(g_all.nodes))
    if(DBG):print("#edges",len(g_all.edges))
    if(DBG):print("keys",len(keys), keys)
    if(DBG):print("doors",len(doors), doors)
    if(DBG):print("entries",len(entries), entries)
    if(DBG):print("***END FINAL GRAPH")
    if(DBG):
        pass
        #nx.draw(g, with_labels=True, font_weight='bold')
        #nx.draw_shell(g, with_labels=True, font_weight='bold')
        #nx.draw_circular(g, with_labels=True, font_weight='bold')
        #nx.draw_kamada_kawai(g_all, with_labels=True, font_weight='bold')
        #nx.draw_random(g, with_labels=True, font_weight='bold')
        #nx.draw_spectral(g, with_labels=True, font_weight='bold')
        #nx.draw_spring(g_all, with_labels=True, font_weight='bold')
    

    # sp all keys to all keys and memo what door you need


    setset = keys.copy()
    setset.update(entries.copy())
    sp = {}

    ssl = list(setset.keys())

    for i in range(len(ssl)):
        for j in range(i,len(ssl)):
            k1 = ssl[i]
            k2 = ssl[j]
            if(DBG):print(k1,k2)
            if not (k1,k2) in sp:
                path = None
                try:
                    path = nx.shortest_path(g_all,setset[k1],setset[k2])
                except (nx.NetworkXNoPath):
                    pass
                if (path != None):
                    doors_on_way_lower = set()
                    for p in path:
                        if p[2]>='A' and p[2]<='Z':
                            doors_on_way_lower.add(p[2].lower())
                    sp[(k1,k2)] = (len(path)-1,doors_on_way_lower)
                    sp[(k2,k1)] = sp[(k1,k2)]
                    if(DBG):print(k1,k2,sp[(k1,k2)])
    if(DBG):print("***")

    return g_all,field,keys,doors,entries,sp


def function(positions,keys_left_to_get,memory,DBG=False):
    global g_all,keys_all,doors_all, graphs_all, sp_all

    if DBG:print("positions",positions)
    if DBG:print("keys_left_to_get",keys_left_to_get)

    if (len(keys_left_to_get)==0):
        return 0

    index_to_memory =(frozenset(keys_left_to_get), positions.values())

    if index_to_memory in memory:
        return memory[index_to_memory]

    ret=np.iinfo(np.int32).max//10


    # FIND REACHABLE KEYS AND WHAT DISTANCE THEY ARE AT

    index_to_graph_memory = frozenset(keys_left_to_get)

    if not index_to_graph_memory in graphs_all:

        sp = {}

        setset = keys_all.copy()
        for pos in positions:
            ppp = pos
            if not ppp in setset:
                setset[ppp] = positions[pos]

        ssl = list(setset.keys())

        for i in range(len(ssl)):
            for j in range(len(ssl)):
                k1 = ssl[i]
                k2 = ssl[j]
                if(DBG):print(k1,k2)
                if not (k1,k2) in sp:
                    if (k1,k2) in sp_all:
                        (dist, doors_on_way_lower) = sp_all[(k1,k2)]
                        if len(doors_on_way_lower & keys_left_to_get) == 0:
                            sp[(k1,k2)] = dist
                            sp[(k2,k1)] = sp[(k1,k2)]
                            if(DBG):print(k1,k2,sp[(k1,k2)])
        graphs_all[index_to_graph_memory] = sp
        if(DBG):print("***")

    sp = graphs_all[index_to_graph_memory]


    # WE HAVE DISTANCE AND DOORS TO ALL REACHABLE KEYS

    keys_left_to_get2 = {}

    # TODO LOOP ON POSITIONS DIFFERENTLY

    for ipos in positions:
        if(DBG):print("ret",ret)

        if(DBG):print("ipos",ipos)

        pos = positions[ipos]
        ppp = pos[2]

        for k in keys_left_to_get:
            if(DBG):print("ppp,k",ppp,k)

            if (not (ppp,k) in sp):
                if(DBG):print("ppp,k not in sp")
                continue
            else:
                dist_to_key = sp[(ppp,k)]
            if(DBG):print("dist_to_key",dist_to_key)

            keys_left_to_get2[k] = copy.deepcopy(keys_left_to_get)
            keys_left_to_get2[k].remove(k)

            positions2 = copy.deepcopy(positions)
            positions2[ipos] = keys_all[k]

            d = dist_to_key + function(positions2, keys_left_to_get2[k], memory)
            ret = min(d,ret)

    if(DBG):print("ret",ret)

    memory[index_to_memory] = ret

    return ret







def test(cc=None, expected=None, DBG=True):
    global g_all,field,keys_all,doors_all, graphs_all,sp_all

    start_millis = int(round(time.time() * 1000))
    graphs_all= {}
    memory = {}
    g_all,field,keys_all,doors_all,entry,sp_all = create_world(cc,DBG)
    print("WOK")
    #function(position,keys_left_to_get,memory,DBG=True):
    position = entry
    keys_left_to_get=set(keys_all)
    full_path_length = function(position,keys_left_to_get,memory,DBG)
    stop_millis = int(round(time.time() * 1000))

    result = str(full_path_length)
    expected = str(expected)
    flag = (result == expected)
    print("***"+str(cc) + " -> "+str(result), " -> "+ str(flag) + " vs " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1 = """#######
#a.#Cd#
##1#2##
#######
##3#4##
#cB#Ab#
#######"""

test(t1,8,False)


t11="""###############
#d.ABC.#.....a#
######1#2######
###############
######3#4######
#b.....#.....c#
###############"""

test(t11,24,False)


t2="""#############
#DcBa.#.GhKl#
#.###1#2#I###
#e#d#####j#k#
###C#3#4###J#
#fEbA.#.FgHi#
#############"""

test(t2,32,False)



t3 = """#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba1#2BcIJ#
#############
#nK.L3#4G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""

test(t3,72,False)


#raise

# In[54]:


test(puzzle_input,0,False)
# TOO LONG - see chch.py
