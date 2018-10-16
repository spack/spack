#!/bin/bash
printf '%s\n' "**  **  **  $(date) ${BASH_SOURCE[0]})"
# dantopa@tt-fey1:spack.standard.hypre $ gcc --version
# gcc (GCC) 6.3.0 20161221 (Cray Inc.)

export l_compilers=""
## cray
l_compilers="${l_compilers} cce@8.7.2  cce@8.6.5"
## gcc
l_compilers="${l_compilers} gcc@7.3.0 gcc@6.3.0"
## intel
l_compilers="${l_compilers} intel@18.0.2 intel@17.0.4"

census=( ${l_compilers} )
echo "${#census[@]} Spack-recognized compilers loaded:"
echo "${l_compilers}"
echo ""

