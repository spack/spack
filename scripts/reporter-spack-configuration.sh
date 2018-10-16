#! /bin/bash
printf '%s\n' "**  **  **  $(date) ${BASH_SOURCE[0]}"

# # # input
# # set in bash init
#   dir_wsdb  host_name
# # set in other routines
#   myTPL partition

# exempli gratia
# ${lap}    = /scratch/users/dantopa/repos/master-lap
# ${prefix} = darwin-general-cn128

# # output
#   targetDirectory

export ymd=$(date +%Y-%m-%d)  # date tag to distinguish runs

export targetDirectory="${dir_wsdb}/spack-configurations/${host_name}/${partition}/$(spack arch)/${ymd}"
# ${lap}, ${prefix} created in bash init script; e.g.

mkdir -p "${targetDirectory}/config"
mkdir -p "${targetDirectory}/providers"
mkdir -p "${targetDirectory}/yaml"

function grab_configuration(){
    myFile="${targetDirectory}/config/${1}-config.out"
    echo "$(date) ${BASH_SOURCE[0]}" >  ${myFile}
    echo ""                          >> ${myFile}
    echo "spack config get ${1}"     >> ${myFile}
    echo ""                          >> ${myFile}
          spack config get ${1}      >> ${myFile}
    sync
}

# providers hypre
function providers() {
    myFile="${targetDirectory}/providers/${1}-provider.out"
    echo "$(date) ${BASH_SOURCE[0]}" >  ${myFile}
    echo ""                          >> ${myFile}
    echo "spack providers ${1}"      >> ${myFile}
          spack providers ${1}       >> ${myFile}
    sync
}

configurations="compilers  config  mirrors  modules  packages  repos"

for c in ${configurations}; do
    grab_configuration ${c}
done

spack providers > "${targetDirectory}/providers/spack-providers.out"

virtual_packages="D  awk  blas  daal  elf  gl  glu  golang  ipp  java  jpeg  lapack  mkl  mpe  mpi"
virtual_packages="${virtual_packages} opencl  openfoam  pil  pkgconfig  scalapack  szip  tbb"

for p in ${virtual_packages}; do
    providers ${p}
done

# grab etc/spack/defaults/*.yaml
cp ${SPACK_ROOT}/etc/spack/defaults/*.yaml "${targetDirectory}/yaml"
# gowsdb
# git add .
# git commit -m "${host_name}-${partition}-${tpl} $(date)"

echo "cd ${targetDirectory}"
