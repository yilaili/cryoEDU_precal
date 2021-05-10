#!/bin/bash

#SBATCH --job-name=$$jobname
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=$$queuename
#SBATCH --ntasks=$$mpinodes
#SBATCH --cpus-per-task=$$threads
#SBATCH --output=$$stdout
#SBATCH --error=$$stderr
#SBATCH --open-mode=append
#SBATCH --export=NONE
#SBATCH --time=$$time
#SBATCH --mem-per-cpu=3g
#SBATCH
#SBATCH

module purge
$$modules

srun --mem-per-cpu=3g --mpi=pmi2 $$command_to_run
