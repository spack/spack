#! /bin/bash
printf '%s\n' "**  **  **  $(date) ${BASH_SOURCE[0]}"
# . profiler-machine.sh $myDir

echo "$(date) ${BASH_SOURCE[0]}"                           >  ${1}
echo ""                                                    >> ${1}
echo "\${host-name}   = ${host_name}"                      >> ${1}
echo "\${HOSTNAME}    = ${HOSTNAME}"                       >> ${1}
echo "\${partition}   = ${partition}"                      >> ${1}
echo "\${USER}        = ${USER}"                           >> ${1}
echo "\${HOME}        = ${HOME}"                           >> ${1}
echo "\${SPACK_ROOT}  = ${SPACK_ROOT}"                     >> ${1}
echo "spack arch      = $(spack arch)"                     >> ${1}
echo ""                                                    >> ${1}
echo "uname:"                                              >> ${1}
echo "-m    machine name:          $(uname -m)"            >> ${1}
echo "-n    network node hostname: $(uname -n)"            >> ${1}
echo "-i    hardware platform:     $(uname -i)"            >> ${1}
echo "-p    processor type:        $(uname -p)"            >> ${1}
echo "-o    operating system:      $(uname -o)"            >> ${1}
echo "-svr  kernel name:           $(uname -svr)"          >> ${1}
echo ""                                                    >> ${1}
echo "cpu info"                                            >> ${1}
echo   "grep -i 'model name' /proc/cpuinfo | sort | uniq"  >> ${1}
echo "$(grep -i 'model name' /proc/cpuinfo | sort | uniq)" >> ${1}
echo ""                                                    >> ${1}
echo "full query set in directory ${id}"                   >> ${1}
echo ""                                                    >> ${1}
