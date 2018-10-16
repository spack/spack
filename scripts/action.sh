#! /bin/bash
printf '%s\n' "**  **  **  $(date) ${BASH_SOURCE[0]}"

# # slot arguments
# #  #1 ${tpl_name}
# #  #2 ${tpl_version}
# #  #3 ${compiler@version}

# gcc@8.2.0 -> gcc, 8.2.0
export         compiler=${3}
export  compiler_family=$(echo ${compiler} | cut -d '@' -f1)
export compiler_version=$(echo ${compiler} | cut -d '@' -f2)


export compiler_path="${compiler_family}/${compiler}"
export      tpl_path="${tpl}/${tpl}-${tpl_version}"
export     host_path="${host_name}/${arch}"
export host_tpl_path="${host_path}/${tpl_path}"

# convert ^ to -
export      dirTargetHPC=$(echo "${dir_wsdb}/hpc/${host_tpl_path}/${compiler_path}"         | tr ^ -)
export      dirTargetTPL=$(echo "${dir_wsdb}/tpl/${tpl_path}/${host_path}/${compiler_path}" | tr ^ -)
export dirTargetCompiler=$(echo "${dir_wsdb}/compiler/${compiler_path}/${host_tpl_path}"    | tr ^ -)

export targets="${dirTargetHPC} ${dirTargetTPL} ${dirTargetCompiler}"

for g in ${targets}; do
    mkdir -p ${g}
done

export g="${dirTargetHPC}"

# open log file
echo "$(date) ${BASH_SOURCE[0]}"               >  ${g}/${myLog}
echo ""                                        >> ${g}/${myLog}
echo "spack configuration: ${targetDirectory}" >> ${g}/${myLog}
echo ""                                        >> ${g}/${myLog}

# write system profile
source ${novus_bash}/profiler-machine.sh ${g}/${myProfile}
cd
cd ${SPACK_ROOT} # to ward off stale file handles
echo ""

install_line="spack "
install_line="${install_line} ${options_debug}"            # spack -sd
install_line="${install_line} install ${options_install}"  # spack -sd install --dont-restage
install_line="${install_line} ${tpl}"                      # spack -sd install --dont-restage openmpi @ 3.1.2
install_line="${install_line} % ${compiler}"               # spack -sd install --dont-restage openmpi @ 3.1.2 % gcc @ 8.2.0
install_line="${install_line} ${flags}"                    # spack -sd install --dont-restage openmpi @ 3.1.2 % gcc @ 8.2.0 +pmix
install_line="${install_line} ${specifications}"           # spack -sd install --dont-restage openmpi @ 3.1.2 % gcc @ 8.2.0 +pmix ^cmake/hash
install_line="${install_line} ${spack_arch}"               # spack -sd install --dont-restage openmpi @ 3.1.2 % gcc @ 8.2.0 +pmix ^cmake/hash arch=cray-cnl6-haswell

export SECONDS=0

echo "${install_line} >>  ${g}/${myLog} 2>&1" >> ${spack_command_file}
echo "${install_line} >> \${g}/${myLog} 2>&1" >> ${g}/${myLog}
echo "${install_line} >>  ${g}/${myLog} 2>&1"
      sync
echo "spack install..."
      #spack ${install_line} 2>&1

echo ""
echo "#  #  #  #  \${install_line} = "
echo "${install_line}"
echo ""

export time=SECONDS

echo "writing build times..."
for g in ${targets}; do
    export FileTime="${g}/build-time.txt"
    echo $(date)                             >  ${FileTime}
    echo "${install_line}"                   >> ${FileTime}
    echo "elapse time for build = ${time} s" >> ${FileTime}
done

# 10,000 lines of SCHILY
# sed -i '' '/SCHILY/d' ${spack_command_file}
# sed -i '' '/SCHILY/d' ${g}/${myLog}
sed -i '/SCHILY/d' ${spack_command_file}
sed -i '/SCHILY/d' ${g}/${myLog}

echo "copying data to ${wsdb}..."
cp ${g}/${myLog} ${dirTargetTPL}/${myLog}
cp ${g}/${myLog} ${dirTargetCompiler}/${myLog}

echo "sweeping for build failures..."
# check for a crash in the dependency chain
export working_file="/tmp/${USER}/copy-list.txt"
find "/tmp/${USER}/spack-stage/." -name spack-build.* >  ${working_file}
find "/tmp/${USER}/spack-stage/." -name config.log    >> ${working_file}
if [[ -s ${working_file} ]]; then
#    echo "cat ${working_file}"
          cat ${working_file}
          mkdir -p ${dirTargetHPC}/debug
          while read line
          do
              # for example,
              # /tmp/dantopa/spack-stage/spack-stage-PP_V46/openmpi-3.1.0/spack-build.out
              # -> openmpi-3.1.0-spack-build.out
              new_name=$(echo ${line} | rev | cut -d '/' -f-2 | rev | tr / -)
#              echo "\${new_name} = ${new_name}"
              cp ${line} "${dirTargetHPC}/debug/${new_name}"
          done < ${working_file}
    rm  -rf ${working_file}
fi

# duplicate entries in dir_wsdb
cp -a ${dirTargetHPC}/debug ${dirTargetTPL}
cp -a ${dirTargetHPC}/debug ${dirTargetCompiler}

