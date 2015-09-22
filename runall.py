#!/usr/bin/env python

# Runs all jobs specified in an input file using threading

### Imports
import sys
from multiprocessing import Pool
#from subprocess import check_call, call
import os

def run_command(cmd):
    command = cmd.split()[0]
    tmp_args = cmd.split()[1:]

    args = ""
    for arg in tmp_args:
        args += arg + " "

    print "command = ", command
    print "args = ", args

    #check_call([command,args])
    #call(command, args)
    os.system(cmd)


if __name__ == '__main__':

    usage="  Usage:   runall  job-file  nprocs"

    ### Exit conditions if input != usage
    if len(sys.argv) != 3:
        print usage
        sys.exit(1)

    f_jobs = sys.argv[1]
    nprocs = int(sys.argv[2])
    print "nprocs = ", nprocs

    if nprocs < 1:
        print "Error."
        sys.exit(1)

    debug = True


    f = open(f_jobs, "r")
    Jobs = f.readlines()
    f.close()

    N_jobs = len(Jobs)
    print "N_jobs = ", N_jobs

    if N_jobs < 1:
        print "Error."
        sys.exit(1)

   
    pool = Pool(processes=nprocs)
    pool.map(run_command, Jobs)    

