# -*- coding: UTF-8 -*-
# Created: Yeguang, 2015-08-03

# Common modules import
from abaqus import *
from abaqusConstants import *
from caeModules import *

para1 = 1
para2 = 1

jobName = 'run'
jobDescription = 'para1 = %6.3f, para2 = %6.3f' %(para1,para2)

mdb.Job(name=jobName, model=currentModel.name, description=jobDescription)
mdb.jobs[jobName].writeInput(consistencyChecking=OFF)