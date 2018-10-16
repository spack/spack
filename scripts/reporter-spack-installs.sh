#! /bin/bash
printf '%s\n' "**  **  **  $(date) ${BASH_SOURCE[0]}"

# # # input
# # set in bash init
#   dir_wsdb  host_name partition

# sample call
# queries ${dir_hypre} hypre

function header(){
    echo ""
    echo "writing ${1}..."
    date                                  >  ${1}
    echo "pwd = $(pwd)"                   >> ${1}
    echo "\${SPACK_ROOT} = ${SPACK_ROOT}" >> ${1}
    echo ""                               >> ${1}
    sync
}

function queries(){
    echo "queries for ${1}..."

    cd "${mySpack}"  # set at login
    cd "spack.${partition}.${2}"

    fileName="${1}/${2}-find.txt"
    header ${fileName}
    echo "bin/spack find ${2}"      >> ${fileName}
          bin/spack find ${2}       >> ${fileName}

    fileName="${1}/${2}-find-ldf.txt"
    header ${fileName}
    echo "bin/spack find -ldf ${2}" >> ${fileName}
          bin/spack find -ldf ${2}  >> ${fileName}

    fileName="${1}/${2}-info.txt"
    header ${fileName}
    echo "bin/spack info ${2}"      >> ${fileName}
          bin/spack info ${2}       >> ${fileName}

    fileName="${1}/${2}-versions.txt"
    header ${fileName}
    echo "bin/spack versions ${2}"  >> ${fileName}
          bin/spack versions ${2}   >> ${fileName}
          sync
}

function compilers() {
    fileName="${1}/compilers-summary.txt"
    header ${fileName}
    echo "bin/spack compilers"            >> ${fileName}
          bin/spack compilers             >> ${fileName}

    fileName="${1}/compilers-detail.txt"
    header ${fileName}
    echo "bin/spack config get compilers" >> ${fileName}
          bin/spack config get compilers  >> ${fileName}
          sync
}

function tag_spack(){
    fileName="${1}/profile-summary.txt"
    header ${fileName}
    echo "bin/spack arch"                 >> ${fileName}
          bin/spack arch                  >> ${fileName}
    echo "$\{SPACK_ROOT} = ${SPACK_ROOT}" >> ${fileName}
    echo "\${host_name} = ${host_name}"   >> ${fileName}
    echo "\${partition} = ${partition}"   >> ${fileName}
    echo "\${node_name} = ${node_name}"   >> ${fileName}
    echo "\${prefix}    = ${prefix}"      >> ${fileName}
    echo "\${ego}       = ${ego}"         >> ${fileName}
    echo "\${id}        = ${id}"          >> ${fileName}
    echo "\${vault}     = ${vault}"       >> ${fileName}
    sync
}

# presumes ${SPACK_ROOT} assigned
myArch=$(spack arch)
# directory structure in Performance_Benchmarking
     dir_base="${dir_wsdb}/spack-installs/${host_name}/${myArch}"
    dir_hypre="${dir_base}/hypre"
  dir_openmpi="${dir_base}/openmpi"
   dir_zoltan="${dir_base}/zoltan"
dir_allbuilds="${dir_base}/all-builds"

mkdir -p "${dir_hypre}"
mkdir -p "${dir_openmpi}"
mkdir -p "${dir_zoltan}"
mkdir -p "${dir_allbuilds}"

# spack queries
queries ${dir_hypre} hypre
queries ${dir_zoltan} zoltan
# queries ${dir_openmpi} openmpi

cd ${SPACK_ROOT}
fileName="${dir_allbuilds}/spack-find.txt"
header ${fileName}
echo "bin/spack find"     >> ${fileName}
      bin/spack find ${2} >> ${fileName}

tag_spack ${dir_hypre}
tag_spack ${dir_openmpi}
tag_spack ${dir_zoltan}

compilers ${dir_base}

gowsdb
git add .
git commit -m "${host_name} ${partition} $(date)"

cd ${dir_base}
