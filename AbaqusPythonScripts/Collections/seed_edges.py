from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

import numpy as np

print '-----------------New Degug-----------------'

currentModel = mdb.models.values()[0]
p = currentModel.parts['Part-1']

print 'Number of edges: ', len(p.edges)

pickedEdges = []
for edge in p.edges:
    (id1,id2) = edge.getVertices()
    x_v1 = np.array(p.vertices[id1].pointOn[0])
    x_v2 = np.array(p.vertices[id2].pointOn[0])

    cut_pos = 50E-3
    check = lambda x: x[2] - cut_pos
    if  check(x_v1)*check(x_v2)<0 :
        pickedEdges.append(edge)

    cut_pos = 150E-3
    check = lambda x: x[2] - cut_pos
    if  check(x_v1)*check(x_v2)<0 :
        pickedEdges.append(edge)

p.seedEdgeByNumber(edges=tuple(pickedEdges),number=4,constraint=FIXED)
print 'Number picked: ', len(pickedEdges)


t0 = 200E-3
tol = 1E-6
L_crictal_upper = 37.2E-3
L_crictal_lower = 37.1E-3
pickedVertices = tuple(p.vertices.getByBoundingBox(zMin=t0-tol))
num_vertices = len(pickedVertices)

pickedEdges = []
for edge in p.edges:
    (id1,id2) = edge.getVertices()
    x_v1 = np.array(p.vertices[id1].pointOn[0])
    x_v2 = np.array(p.vertices[id2].pointOn[0])
    dist = np.linalg.norm(x_v1 - x_v2)
    if dist>L_crictal_lower and dist<L_crictal_upper:
        pickedEdges.append(edge)

p.seedEdgeByNumber(edges=tuple(pickedEdges),number=4,constraint=FINER)
print 'Number picked: ', len(pickedEdges)
