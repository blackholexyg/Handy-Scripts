
################################################################################
# Imports

# Abaqus/CAE Import
from abaqus import *
from abaqusConstants import *
from caeModules import *

# Abaqus/Viewer Import
from odbAccess import *

# Abaqus Compatibility
import testUtils
# testUtils.setBackwardCompatibility()

# Math Libraries
import math
import numpy as np

# System Libraries
import os
import time

################################################################################

class AbqModel:
    "A class for Abaqus Model"

    def __init__(self, UserVar):
        self.UserVar = UserVar
        self.Database = Mdb()

        ############################## Model ###################################

        currentModel = self.Database.Model(name=UserVar['modelName'])
        # del self.Database.models['Model-1']

        ##### Parameters

        ## geometry

        ## materials

        ## other control parameters

        ##### Materials, Sections and Commons Shared by Parts

        #####################
        # Part: 'PartName'
        #####################

        ##### Create part

        ## Sketch
        s = currentModel.ConstrainedSketch(name='s_PartName', sheetSize=10.0)

        ## Part
        tmpPart = currentModel.Part(name='PartName',
            dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)

        ##### Partition

        ## Sketch

        ##### Set (Geometry)

        ##### Section Assignments

        ## Sketch

        ##### Mesh

        ##### Set (Elements/Nodes)

        ##### Surface

        #####################
        # Assembly
        #####################

        ##### Assembly
        a = currentModel.rootAssembly
        tmpIns = a.Instance(name='sub', part=tmpPart, dependent=ON)

        ## Translate

        ## Sets & Surfaces

        ##### Constraints

        ############################# History #################################

        ##### Step
        currentModel.StaticStep(name='Step-1', previous='Initial')

        ## Initial

        ## Step-1

        ##### Output Control


        ##### Step Control
        targetStep = currentModel.steps['Step-1']
        targetStep.setValues(nlgeom=ON, maxNumInc=1500,
            initialInc=0.05, minInc=1e-8, maxInc=0.05)

        ##### Step Control (Advanced Control)

        ############################### Save ###################################

        self.Database.saveAs(UserVar['modelName']+'.cae')


    def CreateJob(self, jobInfo):
        modelname = self.UserVar['modelName']
        jobname = jobInfo['jobName']
        description = jobInfo['jobDescription']
        ncpus = jobInfo['nCPUs']
        ##### Job
        targetJob = self.Database.Job(name=jobname, model=modelname)
        targetJob.setValues(description=description)
        targetJob.setValues(numCpus=ncpus, numDomains=ncpus)
        targetJob.setValues(nodalOutputPrecision=FULL)


    def SubmitJob(self, jobInfo):
        jobname = jobInfo['jobName']
        ##### submit
        self.Database.jobs[jobname].submit(consistencyChecking=OFF)


    def CloseDatabase(self, pathName='defaultsave.cae'):
        ##### save CAE file
        self.Database.saveAs(pathName)
        ##### close
        self.Database.close()


    def ReadResults(self, jobInfo):
        jobname = jobInfo['jobName']
        odb=openOdb(jobname+'.odb')
        pass
        odb.close()

###############################################################################

if __name__ == "__main__":
    UserVar = {}
    UserVar['modelName'] = 'template'

    jobInfo = {}
    jobInfo['jobName'] = 'template-test'
    jobInfo['jobDescription'] = 'This is a test job'
    jobInfo['nCPUs'] = 2

    tmpModel = AbqModel(UserVar)
    tmpModel.CreateJob(jobInfo)
    tmpModel.SubmitJob(jobInfo)
    tmpModel.CloseDatabase(jobInfo)
