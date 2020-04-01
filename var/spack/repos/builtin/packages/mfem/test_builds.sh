#!/bin/bash

builds=(
    # preferred version:
    'mfem'
    'mfem~mpi~metis~gzstream'
    'mfem+mpi+superlu-dist+suite-sparse+petsc \
        +sundials+pumi+mpfr+netcdf+gzstream+gnutls+libunwind \
        ^hypre~internal-superlu ^petsc+suite-sparse+mumps'
    'mfem~mpi+suite-sparse+sundials+mpfr+netcdf \
        +gzstream+gnutls+libunwind'
    # develop version:
    'mfem@develop+shared~static'
    'mfem@develop+shared~static~mpi~metis~gzstream'
    # TODO: Replace '^conduit~python~hdf5' with '^conduit~python' when conduit
    # is fixed to accept '^hdf5+mpi'.
    # NOTE: Skip PUMI since it conflicts with '+shared'.
    'mfem@develop+shared~static+mpi \
        +superlu-dist+suite-sparse+petsc+sundials+mpfr+netcdf+gzstream \
        +gnutls+libunwind+conduit ^hypre~internal-superlu \
        ^petsc+suite-sparse+mumps ^conduit~python~hdf5'
    # TODO: The options '^netcdf~mpi ^hdf5@1.8.19~mpi' are added just to make
    # conduit happy.
    'mfem@develop+shared~static~mpi \
        +suite-sparse+sundials+mpfr+netcdf+gzstream+gnutls+libunwind \
        +conduit ^conduit~python ^netcdf~mpi ^hdf5@1.8.19~mpi'
)

builds2=(
    # preferred version
    'mfem+superlu-dist'
    'mfem+suite-sparse~mpi'
    'mfem+suite-sparse'
    'mfem+sundials~mpi'
    'mfem+sundials'
    'mfem+pumi'
    'mfem+netcdf~mpi'
    'mfem+netcdf'
    'mfem+mpfr'
    'mfem+gnutls'
    'mfem+petsc+mpi ^hypre~internal-superlu ^petsc+suite-sparse+mumps'
    # develop version
    'mfem@develop+superlu-dist'
    'mfem@develop+suite-sparse~mpi'
    'mfem@develop+suite-sparse'
    'mfem@develop+sundials~mpi'
    'mfem@develop+sundials'
    'mfem@develop+pumi'
    'mfem@develop+netcdf~mpi'
    'mfem@develop+netcdf'
    'mfem@develop+mpfr'
    'mfem@develop+gnutls'
    'mfem@develop+conduit~mpi ^conduit~python'
    'mfem@develop+conduit ^conduit~python'
    'mfem@develop+petsc+mpi ^hypre~internal-superlu \
        ^petsc+suite-sparse+mumps'
)

trap 'printf "\nScript interrupted.\n"; exit 33' INT

SEP='=========================================================================='
sep='--------------------------------------------------------------------------'

for bld in "${builds[@]}" "${builds2[@]}"; do
    printf "\n%s\n" "${SEP}"
    printf "    %s\n" "${bld}"
    printf "%s\n" "${SEP}"
    eval bbb="\"${bld}\""
    spack spec -I $bbb || exit 1
    printf "%s\n" "${sep}"
    spack install --test=root $bbb || exit 2
done

# Uninstall all mfem builds:
# spack uninstall --all mfem
