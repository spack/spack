#!/bin/sh
echo "This version of Spack (openmpi ~legacylaunchers schedulers=slurm) "
echo "is installed without the mpiexec/mpirun commands to prevent "
echo "unintended performance issues. See https://github.com/spack/spack/pull/10340 "
echo "for more details."
echo "If you understand the potential consequences of a misconfigured mpirun, you can"
echo "use spack to install 'openmpi+legacylaunchers' to restore the executables."
echo "Otherwise, use srun to launch your MPI executables."
exit 2
