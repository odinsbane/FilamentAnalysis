#!/usr/bin/env python3

import sys, math
"""
This is a small library for loading from a bleb file.
"""
class Node:
    def __init__(self, id, x, y, z):
        self.id = x
        self.x = x
        self.y = y
        self.z = z
    


class Segment:
    def __init__(self, id, a, b):
        self.a = a
        self.b = b
        self.id = id
    def length(self):
        dx = self.b.x - self.a.x
        dy = self.b.y - self.a.y
        dz = self.b.z - self.a.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
        
def loadSegments(filename):
    nodes = {}
    segments = []
    
    lines = open(filename, 'r').readlines();
    segmentIds = []
    
    for line in lines:
        if len(line)==0 or line[0]=="#":
            continue
        tokens = line.split("\t")    
        if len(tokens[0])>0:
            #contains a line segment.
            segmentIds.append((int(tokens[0]), int(tokens[1]), int(tokens[2])))
        if len(tokens[3])>0:
            #contains a node
            id = int(tokens[3])
            x = float(tokens[4])
            y = float(tokens[5])
            z = float(tokens[6])
            nodes[id] = Node(id, x, y, z)
        
    for id in segmentIds:
        segments.append( Segment(id[0], nodes[id[1]], nodes[id[2]] ))
    return nodes, segments
        

if __name__=="__main__":
    if len(sys.argv)==1:
        print("You must supply a file to analyze:")
        print("actinfilaments.py bleb-file.txt")
    nodes, segments = loadSegments(sys.argv[1])
    print("%d nodes and %d segments loaded"%(len(nodes), len(segments)))
