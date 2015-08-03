 # -*- coding: UTF-8 -*-
# Created: Yeguang, 2015-08-01

# Common modules import
from abaqus import *
from abaqusConstants import *
from caeModules import *

currentModel = mdb.models.values()[0]

young = 0.2
poisson = 0.49

currentModel.Material(name='HyperElastic')
Hyper_C10=young/(5*(1+poisson))
Hyper_C01=young/(20*(1+poisson))
Hyper_D1 =6*(1-2*poisson)/young
currentModel.materials['HyperElastic'].Hyperelastic(materialType=ISOTROPIC,
	testData=OFF, type=MOONEY_RIVLIN, volumetricResponse=VOLUMETRIC_DATA,
	table=(( Hyper_C10, Hyper_C01, Hyper_D1), ))