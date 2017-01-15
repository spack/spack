#!/bin/bash

bin/spack install cmake%gcc

bin/spack install netlib-lapack%xl_r^cmake%gcc

bin/spack install netlib-scalapack%xl_r^netlib-lapack^ibm-mpi^cmake%gcc

bin/spack install fftw%xl_r

bin/spack install matio%xl_r

bin/spack install boost%xl_r^zlib%gcc^bzip2%gcc

bin/spack install hdf5%xl_r+mpi^ibm-mpi^zlib%gcc

bin/spack install metis@5.1.0%xl_r^cmake%gcc

bin/spack install parmetis%xl_r^ibm-mpi^cmake%gcc

bin/spack install netcdf%xl_r+mpi^ibm-mpi^m4%gcc^curl%gcc

bin/spack install suite-sparse%xl_r^netlib-lapack^cmake%gcc

bin/spack install superlu-dist%xl_r^netlib-lapack^ibm-mpi^cmake%gcc

bin/spack install mumps%xl_r+mpi^netlib-lapack^ibm-mpi^cmake%gcc

bin/spack install hypre%xl_r^netlib-lapack^ibm-mpi^cmake%gcc 

bin/spack install trilinos%xl_r^netlib-lapack^ibm-mpi^openssl%gcc^curl%gcc^cmake%gcc

bin/spack install petsc%xl_r+mpi^netlib-lapack^ibm-mpi^cmake%gcc^bzip2%gcc^ncurses%gcc^zlib%gcc^openssl%gcc^python%gcc

bin/spack install magma%xl_r^netlib-lapack^cmake%gcc


