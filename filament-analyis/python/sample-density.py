#!/usr/bin/env python3

from actinfilaments import loadSegments, Segment

import sys
from math import sqrt, fabs


def guessHeightAndWidth(nodes):
    
    minX = min(nodes[n].x for n in nodes)
    minY = min(nodes[n].y for n in nodes)
    maxX = max(nodes[n].x for n in nodes)
    maxY = max(nodes[n].y for n in nodes)
    
    return (minX, minY, maxX, maxY)    

def verticalIntersection(ptA, ptB, x, minY, maxY):
    left = ptA
    right = ptB
    if ptA.x > ptB.x:
        left = ptB
        right = ptA
    dx = right.x - left.x
    toLine = x - left.x
    
    if dx==0 or toLine<0 or toLine>dx:
        #parallel, to the left of segment, to far away.
        return None
    dy = right.y - left.y
    y = dy*toLine/dx + left.y
    if y<minY or y>maxY:
        return None
    return (x, y)

def horizontalIntersection(ptA, ptB, y, minX, maxX):
    top = ptB
    bottom = ptA
    if ptA.y>ptB.y:
        top = ptA
        bottom = ptB
    dy = top.y - bottom.y
    toLine = y - bottom.y
    if dy==0 or toLine<0 or toLine>dy:
        #parallel, segment below bottom, above top.
        return None
    dx = top.x - bottom.x
    x = dx*toLine/dy + bottom.x
    if x<minX or x>maxX:
        return None
    return (x, y)
    

def fractionContained(segment, rectangle):
    """
        Finds the length of the segment contained within the rectangle.
    """


    if contains(rectangle, segment.a):
        #first point is contained
        if contains(rectangle, segment.b):
            return 1.0
        dy = segment.b.y - segment.a.y
        dx = segment.b.x - segment.a.x
        if segment.b.y>rectangle[3] :
            #fraction contained
            f = (rectangle[3] - segment.a.y)/dy
            nx = f*dx + segment.a.x
            if nx>=rectangle[0] and nx<=rectangle[2]:
                return f
        if segment.b.y<rectangle[1]:
            f = (rectangle[1] - segment.a.y)/dy
            nx = f*dx + segment.a.x
            if nx>=rectangle[0] and nx<=rectangle[2]:
                return f
        if segment.b.x<rectangle[0]:
            f = (rectangle[0] - segment.a.x)/dx
            ny = f*dy + segment.a.y
            if ny>=rectangle[1] and ny<=rectangle[3]:
                return f
        if segment.b.x>rectangle[2]:
            f = (rectangle[2] - segment.a.x)/dx
            ny = f*dy + segment.a.y
            if ny>=rectangle[1] and ny<=rectangle[3]:
                return f
        
    elif contains(rectangle, segment.b):
        #contains b but not a. swap and repeat.
        return fractionContained(Segment(-1, segment.b, segment.a), rectangle)
    #if it crosses it should touch two borders.
    crossed = []
    pt = verticalIntersection(
        segment.a, segment.b, 
        rectangle[0], rectangle[1], rectangle[3] )
    if pt:
        crossed.append(pt)
    pt = verticalIntersection(
        segment.a, segment.b, 
        rectangle[2], rectangle[1], rectangle[3] )
    if pt:
        crossed.append(pt)
    pt = horizontalIntersection(
        segment.a, segment.b, 
        rectangle[1], rectangle[0], rectangle[2] )
    if pt:
        crossed.append(pt)
    pt = horizontalIntersection(
        segment.a, segment.b, 
        rectangle[3], rectangle[0], rectangle[2] )
    if pt:
        crossed.append(pt)
    pts = len(crossed)
    if pts==0:
        return 0
    elif pts==2:
        #crosses 2 points
        ds = segment.a.x - segment.b.x
        delta = crossed[0][0] - crossed[1][0]
        if ds==0:
            ds = segment.a.y - segment.b.y
            delta = crossed[0][1] - crossed[1][1]
        if ds==0:
            print("special case")
            return 0
        
        return fabs(delta/ds)
        
    else:
        print("#", crossed[0])
        boxAndLine(segment.a, segment.b, rectangle)
    return 0;

def boxAndLine(ptA, ptB, box):
    print("%s\t%s\t%s\t%s"%(box[0], box[1], ptA.x, ptA.y))
    print("%s\t%s\t%s\t%s"%(box[0], box[3], ptB.x, ptB.y))
    print("%s\t%s\t%s\t%s"%(box[2], box[3], "", "" ))
    print("%s\t%s\t%s\t%s"%(box[2], box[1], "", ""))
    print("%s\t%s\t%s\t%s"%(box[0], box[1], "", "" ))
    print("")
    


def contains(rectangle, node):
    if node.x < rectangle[0] or node.x > rectangle[2]:
        return False
    if node.y < rectangle[1] or node.y > rectangle[3]:
        return False
    return True

def restrict(i, mx):
    if i==mx:
     return mx-1
    return i    
    

if __name__=="__main__":
    
    if len(sys.argv)<4:
        print("use with number of boxes blebfile and output density file")
        print("sample-density.py boxnumber blebfile.txt density.txt")
        sys.exit(0)
    nodes, segments = loadSegments(sys.argv[2])
    rect = guessHeightAndWidth(nodes)
    #just use the max values for now. the +10 prevents the max index.
    length = rect[2] + 10 if rect[2]>rect[3] else rect[3] + 10
     
    outputBoxes=int(sys.argv[1])

    boxWidth = length*1.0/outputBoxes

    data = [ [0.0]*outputBoxes for i in range(outputBoxes)]



    for segment in segments:
        total = segment.length()
        #get the first box
        ix1 = int(segment.a.x/boxWidth)
        iy1 = int(segment.a.y/boxWidth)
        ix2 = int(segment.b.x/boxWidth)
        iy2 = int(segment.b.y/boxWidth)
        if ix1==ix2 and iy1==iy2:
            #starts and stops in same box
            data[iy1][ix1] += total
        else:
            lowX = ix1 if ix1<ix2 else ix2
            lowY = iy1 if iy1<iy2 else iy2
            highX = ix1 if ix1>ix2 else ix2
            highY = iy1 if iy1>iy2 else iy2
            x = lowX
            
            while(x<=highX):
                y=lowY
                while(y<=highY):
                    rect = (x*boxWidth, y*boxWidth, (x+1)*boxWidth, (y+1)*boxWidth)
                    data[y][x] += total*fractionContained(segment, rect)
                    y+=1
                x+=1
            
        
    output = open(sys.argv[3], 'w')
    for row in data:
        output.write("\t".join(str(a) for a in row))
        output.write("\n")
    output.close()
