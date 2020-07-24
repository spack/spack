#!/bin/bash

# Set a compiler to test with, e.g. '%gcc', '%clang', etc.
compiler=''

mfem='mfem'${compiler}
mfem_dev='mfem@develop'${compiler}

backends='+occa+raja+libceed'
# Using occa@develop to help the spack concretization
backends_specs='^occa@develop~cuda ^raja~openmp'

# As of 03/20/20 +mpfr breaks one of the unit tests in both @4.1.0 and @develop,
# so it is disabled here for now.
# mpfr='+mpfr'
mpfr=''

builds=(
    # preferred version:
    ${mfem}
    ${mfem}'~mpi~metis~zlib'
    # NOTE: Skip +strumpack since mfem needs hypre < 2.16.0 in that case
    ${mfem}"$backends"'+superlu-dist+suite-sparse+petsc \
        +sundials+pumi+gslib'${mpfr}'+netcdf+zlib+gnutls+libunwind+conduit \
        ^petsc+suite-sparse+mumps'" $backends_specs"
    ${mfem}'~mpi \
        '"$backends"'+suite-sparse+sundials+gslib'${mpfr}'+netcdf \
        +zlib+gnutls+libunwind+conduit'" $backends_specs"
    # develop version:
    ${mfem_dev}'+shared~static'
    ${mfem_dev}'+shared~static~mpi~metis~zlib'
    # NOTE: Skip +strumpack since mfem needs hypre < 2.16.0 in that case
    # NOTE: Shared build with +gslib works on mac but not on linux
    ${mfem_dev}'+shared~static \
        '"$backends"'+superlu-dist+suite-sparse+petsc \
        +sundials+pumi'${mpfr}'+netcdf+zlib+gnutls+libunwind+conduit \
        ^petsc+suite-sparse+mumps'" $backends_specs"
    ${mfem_dev}'+shared~static~mpi \
        '"$backends"'+suite-sparse+sundials'${mpfr}'+netcdf \
        +zlib+gnutls+libunwind+conduit'" $backends_specs"
)

builds2=(
    # preferred version
    ${mfem}"$backends $backends_specs"
    ${mfem}'+superlu-dist'
    # NOTE: On mac +strumpack works only with gcc, as of 03/20/20.
    ${mfem}'+strumpack ^hypre@2.15.1'
    ${mfem}'+suite-sparse~mpi'
    ${mfem}'+suite-sparse'
    ${mfem}'+sundials~mpi'
    ${mfem}'+sundials'
    ${mfem}'+pumi'
    ${mfem}'+gslib'
    ${mfem}'+netcdf~mpi'
    ${mfem}'+netcdf'
    ${mfem}${mpfr}
    ${mfem}'+gnutls'
    ${mfem}'+conduit~mpi'
    ${mfem}'+conduit'
    ${mfem}'+petsc ^petsc+suite-sparse+mumps'
    # develop version
    ${mfem_dev}"$backends $backends_specs"
    ${mfem_dev}'+superlu-dist'
    # NOTE: On mac +strumpack works only with gcc, as of 03/20/20.
    ${mfem_dev}'+strumpack ^hypre@2.15.1'
    ${mfem_dev}'+suite-sparse~mpi'
    ${mfem_dev}'+suite-sparse'
    ${mfem_dev}'+sundials~mpi'
    ${mfem_dev}'+sundials'
    ${mfem_dev}'+pumi'
    ${mfem_dev}'+gslib'
    ${mfem_dev}'+netcdf~mpi'
    ${mfem_dev}'+netcdf'
    ${mfem_dev}${mpfr}
    ${mfem_dev}'+gnutls'
    ${mfem_dev}'+conduit~mpi'
    ${mfem_dev}'+conduit'
    ${mfem_dev}'+petsc ^petsc+suite-sparse+mumps'
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
