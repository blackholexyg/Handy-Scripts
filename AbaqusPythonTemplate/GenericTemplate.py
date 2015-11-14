
################################################################################
# 1. Imports

# Abaqus/CAE Import
from abaqus import *
from abaqusConstants import *
from caeModules import *

# Abaqus/Viewer Import
from odbAccess import *

# Abaqus Compatibility
import testUtils
testUtils.setBackwardCompatibility()

# Math Libraries
import math
import numpy as np
################################################################################








from abaqus import *
from abaqusConstants import *
from caeModules import *
from odbAccess import *
import math

class AbqModel:
    "A class for Abaqus Model"

    def __init__(self, UserVar):
        self.UserVar = UserVar
        self.Database = Mdb()

        ############################## Model ##################################

        currentModel = self.Database.Model(name=UserVar['modelName'])
        # del self.Database.models['Model-1']

        ##### Materials & Sections
        young = 0.5
        poisson = 0.49

        currentModel.Material(name='PDMS')
        Hyper_C10=young/(5*(1+poisson))
        Hyper_C01=young/(20*(1+poisson))
        Hyper_D1 =6*(1-2*poisson)/young
        currentModel.materials['PDMS'].Hyperelastic(materialType=ISOTROPIC,
            testData=OFF, type=MOONEY_RIVLIN, volumetricResponse=VOLUMETRIC_DATA,
            table=(( Hyper_C10, Hyper_C01, Hyper_D1), ))

        currentModel.HomogeneousSolidSection(name='subSec',
            material='PDMS', thickness=1.0)

        currentModel.Material(name='Au')
        currentModel.materials['Au'].Elastic(table=((78E3, 0.44), ))

        #####################
        # Part: substrate
        #####################

        ##### Sketch
        thickness = UserVar['Thickness']
        radius1 = UserVar['Radius']
        radius2 = UserVar['Radius'] + UserVar['Thickness']
        s = currentModel.ConstrainedSketch(name='substrate', sheetSize=5.0)

        s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(radius1, 0.0))
        s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(radius2, 0.0))
        s.Line(point1=( -radius2, 0.0), point2=( radius2, 0.0))

        # Trim
        g = s.geometry

        ptarget = (0.0, radius1)
        gtarget = g.findAt(ptarget)
        s.autoTrimCurve(curve1=gtarget, point1=ptarget)

        ptarget = (0.0, radius2)
        gtarget = g.findAt(ptarget)
        s.autoTrimCurve(curve1=gtarget, point1=ptarget)

        ptarget = (0.0, 0.0)
        gtarget = g.findAt(ptarget)
        s.autoTrimCurve(curve1=gtarget, point1=ptarget)

        ##### Part
        subPart = currentModel.Part(name='substrate', dimensionality=TWO_D_PLANAR,
            type=DEFORMABLE_BODY)
        subPart.BaseShell(sketch=s)

        ##### Partition
        edge1 = subPart.edges.findAt(( 0.0, -radius1, 0.0))
        edge2 = subPart.edges.findAt(( 0.0, -radius2, 0.0))
        mypoint1=subPart.InterestingPoint(edge=edge1, rule=MIDDLE)
        mypoint2=subPart.InterestingPoint(edge=edge2, rule=MIDDLE)
        subPart.PartitionFaceByShortestPath(point2=mypoint2,point1=mypoint1,faces=subPart.faces)

        ##### Set
        f = subPart.faces
        subPart.Set( name='All', faces = f)

        edges = subPart.edges

        theta = math.pi/6.0
        pickedEdges1 = edges.findAt((( radius1*math.sin(theta), -radius1*math.cos(theta), 0.0) ,), )
        pickedEdges2 = edges.findAt((( -radius1*math.sin(theta), -radius1*math.cos(theta), 0.0) ,), )
        subPart.Set( name='top', edges = pickedEdges1 + pickedEdges2)
        pickedEdges1 = edges.findAt((( radius2*math.sin(theta), -radius2*math.cos(theta), 0.0) ,), )
        pickedEdges2 = edges.findAt((( -radius2*math.sin(theta), -radius2*math.cos(theta), 0.0) ,), )
        subPart.Set( name='bottom', edges = pickedEdges1 + pickedEdges2)

        v = subPart.vertices
        pickedVertices = v.findAt( (( 0.0, -radius1, 0.0),),)
        subPart.Set(name='Ref', vertices=pickedVertices)

        ##### Section
        subPart.SectionAssignment(region=subPart.sets['All'],
            sectionName='subSec', thicknessAssignment=FROM_SECTION)

        ##### Mesh
        f = subPart.faces
        subPart.setMeshControls(regions=f, elemShape=QUAD)
        subPart.seedPart(size=0.01, deviationFactor=0.1, minSizeFactor=0.1)

        pickedRegions = f
        subPart.setMeshControls(regions=pickedRegions, technique=STRUCTURED)
        subPart.generateMesh()

        CPE_Quad = mesh.ElemType(elemCode=CPE4R, elemLibrary=STANDARD,
            secondOrderAccuracy=ON, hourglassControl=ENHANCED)
        CPE_Tri = mesh.ElemType(elemCode=UNKNOWN_TRI, elemLibrary=STANDARD)

        pickedRegions =(f, )
        subPart.setElementType(regions=pickedRegions, elemTypes=(CPE_Quad, CPE_Tri))

        #####################
        # Part: electrode
        #####################

        # Sketch
        s = currentModel.ConstrainedSketch(name='electrode', sheetSize=5.0)
        L_electrode = UserVar['ElectrodeL']
        L_bond = UserVar['BondL']
        s.Line(point1=(-L_electrode/2, 0.0), point2=(L_electrode/2, 0.0))

        # Part
        elecPart = currentModel.Part(name='Device', dimensionality=TWO_D_PLANAR,
            type=DEFORMABLE_BODY)
        elecPart.BaseWire(sketch=s)

        # Partition
        edges = elecPart.edges
        pickedEdge = edges.findAt( (0.0,0.0,0.0) )
        elecPart.PartitionEdgeByPoint(edge=pickedEdge, point=( (L_electrode/2-L_bond),0,0))
        pickedEdge = edges.findAt( (0.0,0.0,0.0) )
        elecPart.PartitionEdgeByPoint(edge=pickedEdge, point=(-(L_electrode/2-L_bond),0,0))

        # Sets
        edges = elecPart.edges
        elecPart.Set(name='All',edges=edges)

        # Section
        elecPart.SectionAssignment(region=elecPart.sets['All'], sectionName='electrodeSec',
            offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
            thicknessAssignment=FROM_SECTION)

        # Mesh

        elecPart.generateMesh()

        #####################
        # Assembly
        #####################

        ##### Assembly
        a = currentModel.rootAssembly
        subIns = a.Instance(name='sub', part=subPart, dependent=ON)

        ## Sets & Surfaces
        side1Edges1 = subIns.sets['top'].edges
        a.Surface(side1Edges=side1Edges1, name='m_Surf')

        edges = elecIns.edges
        side2Edges1 = edges.findAt( (( (L_electrode-L_bond)/2, 0.0, 0.0),), )
        a.Surface(side2Edges=side2Edges1, name='bond-1')
        side2Edges2 = edges.findAt( ((-(L_electrode-L_bond)/2, 0.0, 0.0),), )
        a.Surface(side2Edges=side2Edges2, name='bond-2')

        ############################# History #################################

        ##### Step

        ## Initial

        ## Step-1
        currentModel.StaticStep(name='Step-1', previous='Initial')

        ##### Step Control
        stepList = (currentModel.steps['Step-1'],)

        for targetStep in stepList:
            targetStep.setValues(nlgeom=ON)
            targetStep.setValues(maxNumInc=1500, minInc=1e-8)
            targetStep.setValues(initialInc=0.05, maxInc=0.05)


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
        odb=openOdb(jobName+'.odb')
        pass
        odb.close()

###############################################################################

if __name__ == "__main__":
    UserVar = {}
    UserVar['modelName'] = 'substrateTest'
    UserVar['Radius'] = 0.300 # Unit: mm
    UserVar['Thickness'] = 0.300
    UserVar['ElectrodeT'] = 200E-6
    UserVar['ElectrodeL'] = 0.2
    UserVar['BondL'] = 0.02

    tmpModel = AbqModel(UserVar)

    jobInfo = {}
    jobInfo['jobName'] = 'test'
    jobInfo['jobDescription'] = 'This is a test job'
    jobInfo['nCPUs'] = 2

    tmpModel.CreateJob(jobInfo)
    tmpModel.SubmitJob(jobInfo)
