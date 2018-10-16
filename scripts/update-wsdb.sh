#! /bin/bash
printf '%s\n' "**  **  **  $(date) ${BASH_SOURCE[0]}"

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

for g in ${targets}; do
    export FileTime="${g}/build-time.txt"
    echo $(date)                             >  ${FileTime}
    echo "${install_line}"                   >> ${FileTime}
    echo "elapse time for build = ${time} s" >> ${FileTime}
done
