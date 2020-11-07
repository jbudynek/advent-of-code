
# coding: utf-8

# In[1]:

import time

import numpy as np
puzzle_input = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1002,1034,1,1039,101,0,1036,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,1002,1034,1,1039,101,0,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1105,1,124,1001,1034,-1,1039,1008,1036,0,1041,101,0,1035,1040,101,0,1038,1043,1002,1037,1,1042,1105,1,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,102,1,1038,1043,1002,1037,1,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,39,1032,1006,1032,165,1008,1040,39,1032,1006,1032,165,1101,0,2,1044,1105,1,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,74,1044,1106,0,224,1101,0,0,1044,1106,0,224,1006,1044,247,102,1,1039,1034,102,1,1040,1035,1002,1041,1,1036,1002,1043,1,1038,1002,1042,1,1037,4,1044,1105,1,0,15,82,44,17,88,23,99,42,83,68,98,44,75,66,15,14,89,20,34,89,18,1,84,70,84,69,55,89,65,10,76,63,83,20,80,60,48,47,98,65,82,84,68,89,52,76,63,86,61,75,4,52,82,79,24,28,93,94,95,40,66,76,81,50,31,94,81,54,19,91,92,61,18,28,79,77,43,69,19,5,87,35,14,23,94,10,76,32,73,90,20,86,67,90,80,8,86,25,89,89,26,48,37,81,49,25,87,92,17,46,84,96,95,60,79,52,19,13,93,30,93,99,17,13,89,96,36,93,81,89,18,2,97,42,45,63,86,20,26,76,97,29,75,56,7,97,93,2,78,9,79,8,57,84,38,80,53,98,89,34,71,85,17,96,50,31,93,64,7,81,72,85,32,83,31,99,69,90,88,33,88,81,41,80,46,47,93,75,34,95,8,98,24,7,76,77,17,23,95,72,82,98,24,91,95,50,38,92,91,32,95,40,77,80,84,82,7,90,23,13,92,40,82,37,80,56,24,79,99,64,90,55,58,46,33,4,88,92,7,84,19,45,16,75,94,40,93,21,87,94,79,39,83,52,92,14,21,77,82,5,84,85,48,75,19,26,91,28,99,87,81,86,24,53,98,52,25,2,75,39,82,24,51,77,47,92,53,94,27,34,85,22,25,36,92,79,29,2,10,19,95,13,96,82,56,99,3,91,62,99,43,49,7,91,96,77,89,7,99,86,24,92,57,24,49,3,96,77,35,75,11,86,21,1,82,67,84,90,75,96,9,83,1,47,78,7,98,30,11,88,52,78,58,98,47,90,46,78,14,77,88,3,97,87,70,75,24,98,5,80,87,93,95,22,37,59,85,23,41,89,91,9,7,90,61,3,95,96,92,25,57,47,38,88,14,15,84,31,79,20,79,77,22,33,90,70,89,78,51,24,93,81,21,79,82,17,75,88,78,26,87,24,38,96,50,81,6,46,93,39,91,92,81,39,91,5,79,58,9,87,50,83,63,87,2,29,92,37,81,55,59,99,91,35,9,96,18,82,66,4,89,44,87,92,6,79,88,9,9,63,88,71,77,91,35,29,87,87,51,20,94,19,57,93,72,89,4,77,10,87,20,67,80,79,71,1,75,28,87,88,87,55,37,80,85,5,55,5,97,12,62,88,82,27,6,99,93,42,91,16,75,80,6,20,96,6,84,6,46,84,23,92,93,32,90,79,3,54,7,97,92,92,33,79,9,5,10,90,76,19,76,1,85,83,58,2,91,83,77,59,63,89,26,97,67,96,52,88,62,65,23,91,94,51,31,80,24,5,72,40,81,9,85,79,12,98,44,45,81,25,30,60,5,76,92,62,18,32,78,25,16,76,97,18,96,39,96,60,78,78,47,99,48,82,98,57,96,98,73,89,18,12,91,8,66,85,57,94,22,76,88,98,39,58,96,91,61,98,89,7,77,91,13,96,20,86,2,88,91,27,75,32,29,79,51,81,4,86,10,37,79,84,67,49,75,20,94,91,23,33,92,38,91,37,76,79,55,91,43,80,25,98,77,91,88,44,15,97,45,3,86,73,87,30,91,62,80,80,16,85,54,88,54,75,88,65,18,85,22,90,79,36,10,77,86,65,30,38,85,3,90,44,48,75,81,80,32,59,90,91,41,95,72,79,11,66,26,96,20,4,68,88,23,95,31,98,12,98,56,94,95,80,68,78,39,79,93,85,55,96,4,77,14,80,46,95,84,84,6,93,35,95,46,85,92,81,69,85,92,87,0,0,21,21,1,10,1,0,0,0,0,0,0]


SLEEP = 0.02
#SLEEP = 0.001
# In[2]:


# OPCODE INT MACHINE

def decode(c): # returns mode_a,mode_b,mode_c,opcode
    code_5="{:05d}".format(c)
    return int(code_5[0]),int(code_5[1]),int(code_5[2]),10*int(code_5[3])+int(code_5[4])

def code_to_dictcode(code):
    dictcode = {i: code[i] for i in range(0, len(code))}
    return dictcode

def get_dictcode(i, dictcode): # handle negative?
    if not i in dictcode:
        return 0
    return dictcode[i]

def set_dictcode(i, value, dictcode): # handle negative?
    dictcode[i] = value

# if one_output=True --> returns OUTPUT - array of outputs
# else
# returns output,dictcode,i,input_signals,input_index,relative_base
def opcode_machine(dictcode, i, input_signals,input_index,relative_base,one_output=True,DBG=False):
    
    code_i = get_dictcode(i,dictcode)
    mode_a,mode_b,mode_c,opcode = decode(code_i)
    
    output = []
    
    while(True):

        if (DBG==True): print(code_i,mode_a,mode_b,mode_c,opcode)
        
        if mode_c==0: # position mode
            i1=get_dictcode(i+1,dictcode)
        elif mode_c==1: # immediate mode
            i1=i+1
        elif mode_c==2: # relative mode
            i1=get_dictcode(i+1,dictcode)+relative_base

            
        if mode_b==0: # position mode
            i2=get_dictcode(i+2,dictcode)
        elif mode_b==1: # immediate mode
            i2=i+2
        elif mode_b==2: # relative mode
            i2=get_dictcode(i+2,dictcode)+relative_base
            
        if mode_a==0: # position mode
            i3=get_dictcode(i+3,dictcode)
        elif mode_a==1: # immediate mode
            i3=i+3
        elif mode_a==2: # relative mode
            i3=get_dictcode(i+3,dictcode)+relative_base
            
        code_i1 = get_dictcode(i1,dictcode)
        code_i2 = get_dictcode(i2,dictcode)
        code_i3 = get_dictcode(i3,dictcode)

        if (opcode==99):
            if (DBG==True): print("HALT")
            if (one_output):
                return ('HALT',dictcode,i,input_signals,input_index,relative_base)
            else:
                return output
        elif (opcode== 1): # addition
            set_dictcode(i3, code_i1+code_i2, dictcode)
            i = i +4
        elif (opcode == 2): # multiplication
            set_dictcode(i3, code_i1*code_i2, dictcode)
            i = i +4
        elif (opcode == 3): # input
            set_dictcode(i1, input_signals[input_index], dictcode)
            if (input_index<len(input_signals)-1):
                input_index += 1
            else:
                input_index += 0
                #print("no more input signals")
            i = i+2
        elif (opcode == 4): # output
            output = output + [code_i1]
            if (DBG==True): print(code_i1)
            i = i+2
            if (one_output):
                return (output,dictcode,i,input_signals,input_index,relative_base)
        elif (opcode == 5): #jump-if-true
            if code_i1!=0:
                i = code_i2
            else:
                i=i+3
        elif (opcode == 6): #jump-if-false
            if code_i1==0:
                i = code_i2
            else:
                i=i+3
        elif (opcode == 7): #less than
            if code_i1<code_i2:
                set_dictcode(i3,1,dictcode)
            else:
                set_dictcode(i3,0,dictcode)
            i = i+4
        elif (opcode == 8): #equals
            if code_i1==code_i2:
                set_dictcode(i3,1,dictcode)
            else:
                set_dictcode(i3,0,dictcode)
            i = i+4
        elif (opcode == 9): # relative base update
            relative_base += code_i1
            i = i+2
                
        if(DBG):
            print("i",i)
            print("relative_base",relative_base)
            print("dictcode",dictcode)
        code_i = get_dictcode(i,dictcode)
        mode_a,mode_b,mode_c,opcode = decode(code_i)

    # we never get there
    return "NEVER"


# In[5]:



CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'
import sys

def delete_last_lines(n=1):
    for _ in range(n):
        #print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write(CURSOR_UP_ONE)

def print_field(xyids, DBG=True):
    coords = xyids.keys()
    if(DBG): print(xyids)
    x_min = min(coords, key = lambda t: t[0])[0]
    x_max = max(coords, key = lambda t: t[0])[0]
    y_min = min(coords, key = lambda t: t[1])[1]
    y_max = max(coords, key = lambda t: t[1])[1]
    
    if(DBG): print(x_min,x_max,y_min,y_max)

    delete_last_lines(y_max-y_min)

    for yy in range(y_min,y_max+1):
        ss = ""
        for xx in range(x_min,x_max+1):
            if (xx,yy) in xyids:
                ss += xyids[(xx,yy)]
            else:
                ss += " "
        print(ss)
    
    time.sleep( SLEEP )


# In[6]:


#north (1), south (2), west (3), and east (4).
DBG=False
dictcode = code_to_dictcode(puzzle_input)
# opcode_machine(dictcode, i, input_signals,input_index,relative_base,one_output=True,DBG=False):
i=0
relative_base=0
input_signals=[1] 
input_index=0

# output=opcode_machine(dictcode,i,input_signals,input_index,relative_base,False,DBG=False)
output = -1
output_list = []
jdx=0
curx=0
cury=0
direction = 1
xyids={}
xyids[(curx,cury)] = "D"

#north (1), south (2), west (3), and east (4).

def test_around(x,y,dictcode,i,relative_base):
    
    # test north
    input_signals_test=[1] 
    input_index_test=0
    output,dictcode,i,input_signals_test,input_index_test,relative_base =     opcode_machine(dictcode,i,input_signals_test,input_index_test,relative_base,one_output=True,DBG=False)
    if(DBG):print("output",output)
    if (output[0]==0):
        xyids[(x,y+1)] = "#"
    elif (output[0]>=1): # MOVE OK
        xyids[(x,y+1)] = '.'
        # backtrack
        input_signals_test=[2] 
        input_index_test=0
        output,dictcode,i,input_signals_test,input_index_test,relative_base =         opcode_machine(dictcode,i,input_signals_test,input_index_test,relative_base,one_output=True,DBG=False)

    # test south
    input_signals_test=[2] 
    input_index_test=0
    output,dictcode,i,input_signals_test,input_index_test,relative_base =     opcode_machine(dictcode,i,input_signals_test,input_index_test,relative_base,one_output=True,DBG=False)
    if(DBG):print("output",output)
    if (output[0]==0):
        xyids[(x,y-1)] = "#"
    elif (output[0]>=1): # MOVE OK
        xyids[(x,y-1)] = '.'
        # backtrack
        input_signals_test=[1] 
        input_index_test=0
        output,dictcode,i,input_signals_test,input_index_test,relative_base =         opcode_machine(dictcode,i,input_signals_test,input_index_test,relative_base,one_output=True,DBG=False)

    # test west
    input_signals_test=[3] 
    input_index_test=0
    output,dictcode,i,input_signals_test,input_index_test,relative_base =     opcode_machine(dictcode,i,input_signals_test,input_index_test,relative_base,one_output=True,DBG=False)
    if(DBG):print("output",output)
    if (output[0]==0):
        xyids[(x-1,y)] = "#"
    elif (output[0]>=1): # MOVE OK
        xyids[(x-1,y)] = '.'
        # backtrack
        input_signals_test=[4] 
        input_index_test=0
        output,dictcode,i,input_signals_test,input_index_test,relative_base =         opcode_machine(dictcode,i,input_signals_test,input_index_test,relative_base,one_output=True,DBG=False)

    # test east
    input_signals_test=[4] 
    input_index_test=0
    output,dictcode,i,input_signals_test,input_index_test,relative_base =     opcode_machine(dictcode,i,input_signals_test,input_index_test,relative_base,one_output=True,DBG=False)
    if(DBG):print("output",output)
    if (output[0]==0):
        xyids[(x+1,y)] = "#"
    elif (output[0]>=1): # MOVE OK
        xyids[(x+1,y)] = '.'
        # backtrack
        input_signals_test=[3] 
        input_index_test=0
        output,dictcode,i,input_signals_test,input_index_test,relative_base =         opcode_machine(dictcode,i,input_signals_test,input_index_test,relative_base,one_output=True,DBG=False)

    return dictcode,i,relative_base
        
###########
        
    
def turn_right(direction):
    #north (1), south (2), west (3), and east (4).
    if (direction==1): return 4
    elif (direction==2): return 3
    elif (direction==3): return 1
    elif (direction==4): return 2

def turn_left(direction):
    #north (1), south (2), west (3), and east (4).
    if (direction==1): return 3
    elif (direction==2): return 4
    elif (direction==3): return 2
    elif (direction==4): return 1

def turn_back(direction):
    #north (1), south (2), west (3), and east (4).
    if (direction==1): return 2
    elif (direction==2): return 1
    elif (direction==3): return 4
    elif (direction==4): return 3

def free_right(direction,xyids,curx,cury):
    if (direction==1): return xyids[(curx+1,cury)]=='.' 
    elif (direction==2): return xyids[(curx-1,cury)]=='.'
    elif (direction==3): return xyids[(curx,cury+1)]=='.'
    elif (direction==4): return xyids[(curx,cury-1)]=='.'

def free_left(direction,xyids,curx,cury):
    if (direction==1): return xyids[(curx-1,cury)]=='.'
    elif (direction==2): return xyids[(curx+1,cury)]=='.'
    elif (direction==3): return xyids[(curx,cury-1)]=='.'
    elif (direction==4): return xyids[(curx,cury+1)]=='.'

def free_forward(direction,xyids,curx,cury):
    if (direction==1): return xyids[(curx,cury+1)]=='.'
    elif (direction==2): return xyids[(curx,cury-1)]=='.'
    elif (direction==3): return xyids[(curx-1,cury)]=='.'
    elif (direction==4): return xyids[(curx+1,cury)]=='.'

    
def finished(xyids):
    coords = xyids.keys()
    x_min = min(coords, key = lambda t: t[0])[0]
    x_max = max(coords, key = lambda t: t[0])[0]
    y_min = min(coords, key = lambda t: t[1])[1]
    y_max = max(coords, key = lambda t: t[1])[1]
    
    if(DBG): print(x_min,x_max,y_min,y_max)

    for yy in range(y_min,y_max+1):
        for xx in range(x_min,x_max+1):
            if (xx,yy) in xyids:
                if xyids[(xx,yy)]==".": return False

    for yy in range(y_min,y_max+1):
        for xx in range(x_max+1,x_min,-1):
            if (xx,yy) in xyids:
                if xyids[(xx,yy)]==".": return False

    for xx in range(x_min,x_max+1):
        for yy in range(y_min,y_max+1):
            if (xx,yy) in xyids:
                if xyids[(xx,yy)]==".": return False

    for xx in range(x_min,x_max+1):
        for yy in range(y_max+1,y_min,-1):
            if (xx,yy) in xyids:
                if xyids[(xx,yy)]==".": return False

    return True
    
# test right, test left, test forward, test backward
# if right is free, turn right and move forward
# repeat
    
while (1):
    jdx+=1
    if(DBG):print("curx,cury",curx,cury)
    dictcode,i,relative_base = test_around(curx,cury,dictcode,i,relative_base)
    
    # test right, test left, test forward, test backward
    # if right is free, turn right and move forward
    # else if forward is free, move forward
    # else if left is free, turn right and move forward
    # else turn twice and move backward
    # repeat

    
    #print_field(xyids, False)
    #a = input()
    #print(a)

    if (free_right(direction,xyids,curx,cury)):
        direction = turn_right(direction)
    elif (free_forward(direction,xyids,curx,cury)):
        direction = direction
    elif (free_left(direction,xyids,curx,cury)):
        direction = turn_left(direction)
    else: 
        direction = turn_back(direction)
        
    input_signals=[direction]
    
    if(DBG):print("input_signals",input_signals)
    output,dictcode,i,input_signals,input_index,relative_base =     opcode_machine(dictcode,i,input_signals,input_index,relative_base,one_output=True,DBG=False)
    if(DBG):print("output",output)
    if(output=='HALT'):break
    #north (1), south (2), west (3), and east (4).
    if (output[0]==0): # WALL - TURN
        if (input_signals[0] == 1): 
            xyids[(curx,cury+1)] = "#"
            input_signals[0] = 3
        elif (input_signals[0] == 2): 
            xyids[(curx,cury-1)] = "#"
            input_signals[0] = 4
        elif (input_signals[0] == 3): 
            xyids[(curx-1,cury)] = "#"
            input_signals[0] = 2
        elif (input_signals[0] == 4): 
            xyids[(curx+1,cury)] = "#"
            input_signals[0] = 1
    elif (output[0]==1): # MOVE OK
        xyids[(curx,cury)] = "."        
        if (input_signals[0] ==1): cury +=1
        elif (input_signals[0] ==2): cury -=1
        elif (input_signals[0] ==3): curx -=1
        elif (input_signals[0] ==4): curx +=1
        xyids[(curx,cury)] = "D"        
    elif (output[0]==2): # BINGO
        xyids[(curx,cury)] = "X"        
        if (input_signals[0] ==1): cury +=1
        elif (input_signals[0] ==2): cury -=1
        elif (input_signals[0] ==3): curx -=1
        elif (input_signals[0] ==4): curx +=1
        print("          *** found at ",curx,cury)
        print_field(xyids, False)
        print("          *** found at ",curx,cury)
        #sys.exit()
    print("***",jdx)
    print_field(xyids, False)
    print("***",jdx)
    if (finished(xyids)):
        print_field(xyids, False)
        print("****FINISHED EXPLORING")
        sys.exit()
        break

    #a = input()
    #print(a)
    if(jdx==1300):break



print("****FINISHED EXPLORING")
#sys.exit()

# In[10]:


endX, endY = 18,-18     # Ending X and Y values of maze

xyids2 = xyids.copy()

coords = xyids.keys()
x_min = min(coords, key = lambda t: t[0])[0]
x_max = max(coords, key = lambda t: t[0])[0]
y_min = min(coords, key = lambda t: t[1])[1]
y_max = max(coords, key = lambda t: t[1])[1]

if(DBG): print(x_min,x_max,y_min,y_max)

xyids2[(endX, endY)] = "O"

def count_dots(tt):
    return(sum(value == "." for value in tt.values()))

minutes=0
dots = count_dots(xyids2)
print("dots",dots)
while dots>0 :
    minutes +=1
    for yy in range(y_min,y_max+1):
        for xx in range(x_min,x_max+1):
            if (xx,yy) in xyids2:
                if xyids2[(xx,yy)]=="O": 
                    if (xx+1,yy) in xyids2 and xyids2[(xx+1,yy)]!="#" and xyids2[(xx+1,yy)]!="O": xyids2[(xx+1,yy)]="o"
                    if (xx-1,yy) in xyids2 and xyids2[(xx-1,yy)]!="#" and xyids2[(xx-1,yy)]!="O": xyids2[(xx-1,yy)]="o"
                    if (xx,yy+1) in xyids2 and xyids2[(xx,yy+1)]!="#" and xyids2[(xx,yy+1)]!="O": xyids2[(xx,yy+1)]="o"
                    if (xx,yy-1) in xyids2 and xyids2[(xx,yy-1)]!="#" and xyids2[(xx,yy-1)]!="O": xyids2[(xx,yy-1)]="o"

    for yy in range(y_min,y_max+1):
        for xx in range(x_min,x_max+1):
            if (xx,yy) in xyids2:
                if xyids2[(xx,yy)]=="o": 
                    xyids2[(xx,yy)]="O"
    
    print_field(xyids2,False)
    dots = count_dots(xyids2)
    print("*** minutes, dots",minutes, dots)                
print("DONE in ",minutes," minutes    ")

