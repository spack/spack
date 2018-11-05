#! /bin/bash
printf '%s\n' "$(date) ${BASH_SOURCE[0]}"

export tpl="openmpi"
export versions="2.0.4 2.0.3 2.0.2 2.0.1 2.0.0"
export arch=$(spack arch)

for v in ${versions}; do
    echo ""
    echo "spack install ${tpl} @ ${v} % ${gcc_system_compiler} arch=${arch}"
          spack install ${tpl} @ ${v} % ${gcc_system_compiler} arch=${arch}

          spack clean --all
done

date

