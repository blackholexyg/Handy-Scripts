# -*- coding: UTF-8 -*-
# Created: Yeguang, 2015-08-03

def CreateFullJob(jobName,ncpus=1):

	jobfile = open("job."+jobName, "w")

	print >> jobfile, "#!/bin/bash"
	print >> jobfile, ""

	print >> jobfile, "#MSUB -N periodic"
	print >> jobfile, "#MSUB -A %s" 
	print >> jobfile, "#MSUB -m abe"
	print >> jobfile, "#MSUB -l nodes=1:ppn=%d" %(ncpus)
	print >> jobfile, "#MSUB -l walltime=3:59:00"
	print >> jobfile, ""

	print >> jobfile, "module load abaqus 2>/dev/null"
	print >> jobfile, "module load intel/2011.3 2>/dev/null"
	print >> jobfile, "module load mpi/openmpi-1.6.3-intel2011.3 2>/dev/null"
	print >> jobfile, ""

	print >> jobfile, "cd $PBS_O_WORKDIR"

	print >> jobfile, "abaqus job=%s cpus=%d double interactive" %(jobName,ncpus)
	
	# inputname = jobName+"_modified.inp"
	# print >> jobfile, "abaqus job=%s input=%s cpus=%d double interactive" %(jobName,inputname,ncpus)

	jobfile.close()
	
def CreateRestartJob(jobName,oldjobName,ncpus=1):

	jobfile = open("job."+jobName, "w")

	print >> jobfile, "#!/bin/bash"
	print >> jobfile, ""

	print >> jobfile, "#MSUB -N periodic"
	print >> jobfile, "#MSUB -A %s" 
	print >> jobfile, "#MSUB -m abe"
	print >> jobfile, "#MSUB -l nodes=1:ppn=%d" %(ncpus)
	print >> jobfile, "#MSUB -l walltime=3:59:00"
	print >> jobfile, ""

	print >> jobfile, "module load abaqus 2>/dev/null"
	print >> jobfile, "module load intel/2011.3 2>/dev/null"
	print >> jobfile, "module load mpi/openmpi-1.6.3-intel2011.3 2>/dev/null"
	print >> jobfile, ""

	print >> jobfile, "cd $PBS_O_WORKDIR"

	print >> jobfile, "abaqus job=%s oldjob=%s cpus=%d double interactive" %(jobName, oldjobName, ncpus)
	
	# inputname = jobName+"_modified.inp"
	# print >> jobfile, "abaqus job=%s input=%s cpus=%d double interactive" %(jobName,inputname,ncpus)

	jobfile.close()