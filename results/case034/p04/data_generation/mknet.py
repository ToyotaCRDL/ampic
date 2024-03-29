#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import math
import optparse
import random
import xml.etree.ElementTree as ET

random.seed(1395)

M = 6  # number in column
N = 6  # number in row
NN = M*N  # total num of nodes
LE = 100.  # Edge length
LD = 0  # Deviation

DF = [[1000, 1000]]
# DF=[[4,3],[5,3],[4,4],[5,4],[4,5],[5,5],[4,6],[5,6]]
# DE=[[1,0,1,1],[2,0,2,1]] # [x1,y1,x2,y2] deletes edge (x1,y1)-(x2,y2) (both directions)
# DE=[[1,1,2,1],[3,1,4,1],[5,1,6,1],[7,1,8,1]] # [x1,y1,x2,y2] deletes edge (x1,y1)-(x2,y2) (both directions
DE = [[1000, 1000, 1000, 1000]]

FL = [[0]*N for i in range(M)]
for k in range(0):
    i = random.randint(1, 8)
    j1 = random.randint(0, 8)
    j2 = j1+1
#    print(k,i,j1,j2)
    if random.random() < 0.5:
        #      print([i,j1,i,j2])
        #      print(FL[i][j1],FL[i][j2])
        if FL[i][j1] == 0 and FL[i][j2] == 0:
            DE.append([i, j1, i, j2])
            FL[i][j1] = 1
            FL[i][j2] = 1
    else:
        #      print([j1,i,j2,i])
        #      print(FL[j1][i],FL[j2][i])
        if FL[j1][i] == 0 and FL[j2][i] == 0:
            DE.append([j1, i, j2, i])
            FL[j1][i] = 1
            FL[j2][i] = 1

RN = list(range(NN))

networkData = 'sq'
args = sys.argv
if 1 < len(args):
    networkData = args[1]

################################


def generate_networkfile():
    global RN
#    random.seed(42)  # make tests reproducible
    # demand per second from different directions
    with open(networkData+".network.xml", "w") as net:
        print('<network>', file=net)
        print('   <map scale="%i">' % int(LE), file=net)
        for j in range(N):
            nodexx = "x"*M
            print('      <row data="'+nodexx+'"/>', file=net)
        print('   </map>', file=net)
        print('   <nodes>', file=net)
        for i in range(NN):
            ii = i % M
            jj = i // M
            RN[i] = 1
            for defe in DF:
                if defe[0] == ii and defe[1] == jj:
                    #                    print(i,ii,jj,"defect")
                    RN[i] = 0
            if RN[i] == 1:
                #                print(i,ii,jj)
                xx = (-0.5+random.random())*LD*LE
                yy = (-0.5+random.random())*LD*LE
#                print(i,ii,jj)
#                rr=LE + LE*ii
#                th=math.pi/float(N-1)*jj
#                xx=rr*math.cos(th)+(-0.5+random.random())*LD*LE
#                yy=rr*math.sin(th)+(-0.5+random.random())*LD*LE
                print('      <node id="%i" offsetX="%.2f" offsetY="%.2f" weight="1"/>' %
                      (i, xx, yy), file=net)
        print('   </nodes>', file=net)

        print('   <lines>', file=net)
# perimeter line
        print('      <line id="peri">', file=net)
        j = 0
        for i in range(M):
            print('         <node id="%i"/>' % (i+j*M), file=net)
        i = M-1
        for j in range(1, N-1):
            print('         <node id="%i"/>' % (i+j*M), file=net)
        j = N-1
        for i in reversed(range(M)):
            print('         <node id="%i"/>' % (i+j*M), file=net)
        i = 0
        for j in reversed(range(0, N-1)):
            print('         <node id="%i"/>' % (i+j*M), file=net)
        print('      </line>', file=net)

# col and row lines
        for i in range(1, M-1):
            print('      <line id="col%i">' % i, file=net)
            for j in range(N):
                print('         <node id="%i"/>' % (i+j*M), file=net)
            print('      </line>', file=net)
        for j in range(1, N-1):
            print('      <line id="row%i">' % j, file=net)
            for i in range(M):
                print('         <node id="%i"/>' % (i+j*M), file=net)
            print('      </line>', file=net)

        print('   </lines>', file=net)
        print('</network>', file=net)


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--defect", "-d", default="0",
                         help="number of defect node")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # first, generate the route file for this simulation
    generate_networkfile()
