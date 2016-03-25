from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

import numpy as np

print '-----------------New Degug-----------------'

currentModel = mdb.models.values()[0]
p = currentModel.parts['Part-1']

t0 = 200E-3
tol = 1E-6
L_crictal_upper = 37.2E-3
L_crictal_lower = 37.1E-3

pickedVertices = tuple(p.vertices.getByBoundingBox(zMin=t0-tol))
num_vertices = len(pickedVertices)
print 'Totally we have ', num_vertices, ' vertices!'

part_pairs = []
for ii in range(0,num_vertices-1):
    for jj in range(ii+1,num_vertices):
        v1 = pickedVertices[ii]
        v2 = pickedVertices[jj]
        x_v1 = np.array(v1.pointOn[0])
        x_v2 = np.array(v2.pointOn[0])
        dist = np.linalg.norm(x_v1 - x_v2)
        if dist>L_crictal_lower and dist<L_crictal_upper:
            part_pairs.append((x_v1,x_v2))
            # print v1.index, v2.index
            # print v1.pointOn[0], v2.pointOn[0]
print 'Totally we have ', len(part_pairs), ' pairs!'

for pairs in part_pairs:
    pickedFaces = p.faces.getByBoundingBox(zMin=t0-tol)
    x_v1 = pairs[0]
    x_v2 = pairs[1]
    try:
        p.PartitionFaceByShortestPath(faces=pickedFaces,point1=x_v1,point2=x_v2)
    except:
        print 'Feature Creation Failed'
        pass

p.regenerate()

# pickedFaces = p.faces.getByBoundingBox(zMin=t0-tol)
# leaf = dgm.LeafFromGeometry(faceSeq=pickedFaces)
# session.viewports['Viewport: 1'].partDisplay.displayGroup.replace(leaf=leaf)
