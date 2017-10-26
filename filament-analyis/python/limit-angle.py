#!/usr/bin/env python3
from math import pi, sqrt, fabs, cos, sin
from actinfilaments import loadSegments, Segment
import sys

if len(sys.argv)<3:
    print("must provide blebfile, and angle:")
    print("limit-angle.py blebfile.txt 15")
    sys.exit(0)

maxAngleDeg = float(sys.argv[2])
maxAngle = pi*maxAngleDeg/180.0
cutoff = sin(maxAngle)

def getDot(segment):
    """
        gets the projection along the z axis.
        
    """
    dx = segment.b.x - segment.a.x
    dy = segment.b.y - segment.a.y
    dz = segment.b.z - segment.a.z
    l = sqrt(dx*dx + dy*dy + dz*dz)
    return dz/l

#loads the segments and nodes.
nodes, segments = loadSegments(sys.argv[1])

#filters out the segments.
good = [segment for segment in segments if abs(getDot(segment))<=cutoff]

print("#%d segments out of %d are less than %f degrees"%(len(good), len(segments), maxAngleDeg))

for segment in good:
    print(segment.id)
