#!/bin/bash

builds=(
    # preferred version:
    'mfem'
    'mfem~mpi~metis~gzstream'
    'mfem+mpi+superlu-dist+suite-sparse+petsc \
        +sundials+mpfr+netcdf+gzstream+gnutls+libunwind \
        ^hypre~internal-superlu ^petsc~boost+suite-sparse+mumps'
    'mfem~mpi+suite-sparse+sundials+mpfr+netcdf \
        +gzstream+gnutls+libunwind'
    # develop version:
    'mfem@develop+shared~static'
    'mfem@develop+shared~static~mpi~metis~gzstream'
    'mfem@develop+shared~static+mpi \
        +superlu-dist+suite-sparse+petsc+sundials+mpfr+netcdf+gzstream \
        +gnutls+libunwind ^hypre~internal-superlu \
        ^petsc~boost+suite-sparse+mumps'
    'mfem@develop+shared~static~mpi \
        +suite-sparse+sundials+mpfr+netcdf+gzstream+gnutls+libunwind')

builds2=(
    # preferred version
    'mfem+superlu-dist'
    'mfem+suite-sparse~mpi'
    'mfem+suite-sparse'
    'mfem+sundials~mpi'
    'mfem+sundials'
    'mfem+netcdf~mpi'
    'mfem+netcdf'
    'mfem+mpfr'
    'mfem+gnutls'
    'mfem+petsc+mpi ^hypre~internal-superlu ^petsc~boost+suite-sparse+mumps'
    # develop version
    'mfem@develop+superlu-dist'
    'mfem@develop+suite-sparse~mpi'
    'mfem@develop+suite-sparse'
    'mfem@develop+sundials~mpi'
    'mfem@develop+sundials'
    'mfem@develop+netcdf~mpi'
    'mfem@develop+netcdf'
    'mfem@develop+mpfr'
    'mfem@develop+gnutls'
    'mfem@develop+petsc+mpi ^hypre~internal-superlu \
        ^petsc~boost+suite-sparse+mumps'
)

trap 'printf "\nScript interrupted.\n"; exit 33' INT

SEP='=========================================================================='
sep='--------------------------------------------------------------------------'

for bld in "${builds[@]}" "${builds2[@]}"; do
    printf "\n%s\n" "${SEP}"
    printf "    %s\n" "${bld}"
    printf "%s\n" "${SEP}"
    eval bbb="\"${bld}\""
    spack spec -I $bbb || continue
    printf "%s\n" "${sep}"
    spack install --test=root $bbb || break
done

# Uninstall all mfem builds:
# spack uninstall --all mfem
