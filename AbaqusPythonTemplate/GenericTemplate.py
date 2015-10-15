
################################################################################
# Imports

# Abaqus CAE Import
from abaqus import *
from abaqusConstants import *
from caeModules import *

# Abaqus Viewer Import
from odbAccess import *

# Math Library
import math
import numpy as np
################################################################################


################################################################################
## Create Step
currentModel.StaticStep(name='Step-1', previous='Initial')
################################################################################


################################################################################
# Apply BC

# Create Displacement BC
region = a.instances['Device-1'].sets['LeftEdge']
currentModel.DisplacementBC(name='BC-1', createStepName='Step-1',
	region=region, u1=0.0, u2=0.0, u3=0.0, ur1=UNSET, ur2=0.0, ur3=UNSET)

# Modify BC
currentModel.boundaryConditions['BC-1'].setValuesInStep(
	stepName='Step-2', u1= DeviceSpan*0.005)

# Deactive BC
currentModel.boundaryConditions['BC-3'].deactivate('Step-3')
################################################################################




################################################################################
# Advanced Step Solution Control

targetStep = currentModel.steps['Step-1']

targetStep.setValues(nlgeom=ON)
targetStep.setValues(maxNumInc=2000, minInc=1e-10)
targetStep.setValues(initialInc=0.05, maxInc=0.05)

# Solution control parameters (?????)

# Accuracy / convergence criteria (?????)
targetStep.control.setValues(allowPropagation=OFF,resetDefaultValues=OFF)
targetStep.control.setValues(
    displacementField=(0.001, 0.002, 0.0, 0.0, 0.002, 1e-06, 0.0005, 1e-09, 1.0, 1e-06, 1e-08),
    rotationField=(0.001, 0.002, 0.0, 0.0, 0.002, 1e-06, 0.0005, 1e-09, 1.0, 1e-06) )

# Time Increment Settings (?????)
targetStep.control.setValues(discontinuous=ON)
targetStep.control.setValues(timeIncrementation=(
    8.0, 10.0, 9.0, 16.0, 10.0, 4.0, 12.0, 30.0, 6.0, 3.0, 50.0))
################################################################################
