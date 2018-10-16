#! /bin/bash
printf '%s\n' "**  **  **  $(date) ${BASH_SOURCE[0]}"

source "${host_name}-${partition}-flag-compilers.sh"

tpl_name="openblas"
tpl_versions="0.3.3  0.3.2  0.3.1"

export options_debug=""
export options_install=""
export flags=""

export        arch="$(spack arch)"
export  spack_arch="arch=${arch}"
export myLog=screen-log.txt

source ${novus_bash}/reporter-spack-configuration.sh

for v in ${tpl_versions}; do
    for c in ${l_compilers}; do
        echo "calling ${novus_bash}/action.sh"
        echo "passing ${tpl_name} ${v} ${c}"
        source ${novus_bash}/action.sh ${tpl_name} ${v} ${c}
        echo "spack clean -a"
    done
done

source ${novus_bash}/update-wsdb.sh
