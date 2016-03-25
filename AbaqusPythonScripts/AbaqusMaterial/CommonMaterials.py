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

# Silicon
# Xu, Sheng, et al. "Assembly of micro/nanomaterials into complex, three-dimensional architectures by compressive buckling." Science 347.6218 (2015): 154-159.
currentModel.Material(name='Si')
currentModel.materials['Si'].Density(table=((2.32E-3, ), ))
currentModel.materials['Si'].Elastic(table=((130E3, 0.27), ))


# SU-8
# http://www.mit.edu/~6.777/matprops/su-8.htm
currentModel.Material(name='SU-8')
currentModel.materials['SU-8'].Density(table=((1.19E-3, ), ))
currentModel.materials['SU-8'].Elastic(table=((4.02E3, 0.22), ))