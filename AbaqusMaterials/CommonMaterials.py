# -*- coding: UTF-8 -*-
# Created: Yeguang, 2015-07-20

# Common modules import
from abaqus import *
from abaqusConstants import *
from caeModules import *

currentModel = mdb.models.values()[0]

# Gold,Au
currentModel.Material(name='Au')
currentModel.materials['Au'].Density(table=((19.3E-3, ), ))
currentModel.materials['Au'].Elastic(table=((78E3, 0.44), ))

# PI
currentModel.Material(name='PI')
currentModel.materials['PI'].Density(table=((1.42E-3, ), ))
currentModel.materials['PI'].Elastic(table=((2.5E3, 0.34), ))