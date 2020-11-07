
# coding: utf-8

# In[9]:


import numpy as np
import re
import copy
import sys
import networkx as nx
import matplotlib.pyplot as plt
import operator
from collections import defaultdict
import time



puzzle_input = """1 GZJM, 2 CQFGM, 20 SNPQ, 7 RVQG, 3 FBTV, 27 SQLH, 10 HFGCF, 3 ZQCH => 3 SZCN
4 FCDL, 6 NVPW, 21 GZJM, 1 FBTV, 1 NLSNB, 7 HFGCF, 3 SNPQ => 1 LRPK
15 FVHTD, 2 HBGFL => 4 BCVLZ
4 GFGS => 4 RVQG
5 BCVLZ, 4 LBQV => 7 TWSRV
6 DWKTF, 4 VCKL => 4 KDJV
16 WZJB => 4 RBGJQ
8 RBGJQ, 5 FCDL, 2 LWBQ => 1 MWSX
100 ORE => 7 WBRL
7 PGZGQ => 5 FVHTD
1 JCDML, 2 TWSRV => 9 JSQSB
3 WZJB, 1 NXNR => 6 XFPVS
7 JPCPK => 8 JCDML
11 LWBQ, 8 XFPVS => 9 PSPFR
2 TWSRV => 8 NVPW
2 LBQV => 1 PMJFD
2 LCZBD => 3 FBTV
1 WBQC, 1 ZPNKQ => 8 JPCPK
44 HFGCF, 41 PSPFR, 26 LMSCR, 14 MLMDC, 6 BWTHK, 3 PRKPC, 13 LRPK, 50 MWSX, 8 SZCN => 1 FUEL
1 XFPVS => 4 BJRSZ
1 GWBDR, 1 MBQC => 4 HZPRB
2 BJRSZ, 9 KDJV, 1 XFPVS => 8 SNVL
7 PMJFD, 30 SNVL, 1 BJRSZ => 2 JMTG
8 SNVL, 1 RBGJQ => 9 FCDL
2 HZPRB => 6 NLSNB
2 GRDG => 9 VCKL
1 FVHTD => 9 WZJB
130 ORE => 2 GRDG
3 WZJB, 1 GFGS, 1 NXNR => 9 SNPQ
9 VCKL => 5 WBQC
1 WBRL, 11 FPMPB => 7 PGZGQ
118 ORE => 3 LMSCR
3 SQLH, 1 PMJFD, 4 XJBL => 7 MLMDC
1 LMSCR, 10 GRDG => 2 TBDH
6 DWKTF => 2 SQLH
2 BJRSZ, 1 PGZGQ, 3 NXNR => 7 MBQC
5 PRKPC => 7 NXNR
9 SQLH => 5 LCZBD
1 FCDL => 9 CQFGM
5 PGZGQ, 1 TBDH => 8 HBGFL
15 JSQSB => 5 HFGCF
2 PGZGQ, 1 VCKL => 4 ZPNKQ
3 FBTV, 3 JMTG => 5 QLHKT
1 ZGZST, 2 LCZBD => 7 GFGS
2 RVQG => 4 ZQCH
1 ZPNKQ => 5 LBQV
3 LWBQ => 8 XJBL
1 LBQV, 9 JCDML => 3 GWBDR
8 VCKL, 6 FVHTD => 9 DWKTF
3 JCDML => 3 ZGZST
160 ORE => 5 FPMPB
3 SQLH, 22 LBQV, 5 BCVLZ => 6 PRKPC
1 WZJB => 2 GZJM
10 ZGZST => 2 LWBQ
5 TBDH, 19 NXNR, 9 QLHKT, 2 KDJV, 1 SQLH, 1 GWBDR, 6 HFGCF => 4 BWTHK"""


# In[164]:



def build_world(ccc, DBG=True):
    if(DBG): print("build_world")
    reactions={}
    idx=0
    for line in ccc.splitlines():
        if(DBG): print("line",line)
        lhs = line.split(' => ')[0] 
        rhs = line.split(' => ')[1] 
        nk = rhs.strip().split(' ')
        nn = int(nk[0])
        kk = nk[1]
        reactions[kk]= [nn]
        if (DBG): print("nn,kk",nn,kk)

        rr = lhs.split(',')
        for r in rr:
            nk = r.strip().split(' ')
            n = int(nk[0])
            k = nk[1]
            reactions[kk].append((n,k))
            if (DBG): print("n,k",n,k)
        idx += 1
    if (DBG): print("reactions",reactions)
    return reactions    

def run_loop(how_many, target, reactions, DBG=True):    
    if (DBG): print("run_loop", how_many, target, reactions)

    chem_to_how_many=defaultdict(int)
    chem_to_how_many[target] = how_many

    while (1):
        done = True
        kkk = list(chem_to_how_many.keys())
        for chem in kkk:
            if chem=='ORE' or chem_to_how_many[chem]<=0:continue
            done = False
            how_many = chem_to_how_many[chem]
            chems_to_use = reactions[chem]
            multiplier = int(np.ceil(how_many/chems_to_use[0]))
            chem_to_how_many[chem] -= multiplier * chems_to_use[0]

            for n_k in range(1,len(chems_to_use)):
                how_much_of_chem_source = chems_to_use[n_k][0]
                chem_source = chems_to_use[n_k][1]

                chem_to_how_many[chem_source] += multiplier * how_much_of_chem_source
        if (DBG):print(chem_to_how_many)
        if (done):break
    return chem_to_how_many['ORE']



def function(reactions, DBG=True):
    
    # find how much fuel you can produce with 1 trillion OREs

    TRILLION = 1000000000000

    min_fuel = 1
    max_fuel = TRILLION//1000
        
    idx =0
    while(min_fuel+1!=max_fuel):
        idx+=1
        if (DBG): print("min_fuel,max_fuel",min_fuel, max_fuel)

        half_fuel = (min_fuel+max_fuel)//2

        #total_ores_min = run_loop(min_fuel,'FUEL',reactions,DBG)
        total_ores_half = run_loop(half_fuel,'FUEL',reactions,False)
        #total_ores_max = run_loop(max_fuel,'FUEL',reactions,DBG)
        if (DBG): print("half_fuel, total_ores_half",half_fuel, total_ores_half, (total_ores_half>TRILLION))     

        if (total_ores_half>TRILLION):
            max_fuel = half_fuel
        else:
            min_fuel = half_fuel
        if (idx==10000):break

    
    return min_fuel


# In[165]:


def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    world = build_world(cc,DBG)
    result = str(function(world,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("***"+str(cc) + " -> "+str(result), " -> "+ str(flag) + " vs " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t3="""157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

test(t3,82892753,False) # 


t4="""2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""

test(t4,5586022,False) # 


t5="""171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""

test(t5,460664,False) # 


# In[14]:


test(puzzle_input,0,False)

