from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

import numpy as np

print '-----------------New Degug-----------------'

currentModel = mdb.models.values()[0]
p = currentModel.parts['Part-1']

count = 0
for edge in p.edges:
    (id1,id2) = edge.getVertices()
    x_v1 = np.array(p.vertices[id1].pointOn[0])
    x_v2 = np.array(p.vertices[id2].pointOn[0])
    cut_pos = 150E-3
    check = lambda x: x[2] - cut_pos
    if  check(x_v1)*check(x_v2)<0 :
        highlight(edge)
        count = count + 1

print 'Number picked: ',count
