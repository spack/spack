#!/bin/bash
printf '%s\n' "**  **  **  $(date) ${BASH_SOURCE[0]}"

export versions="3.1.2  3.1.1  3.1.0"
export versions="${versions} 3.0.2  3.0.1  3.0.0"
export versions="${versions} 2.1.2  2.1.1  2.1.0"
export versions="${versions} 2.0.2  2.0.1  2.0.0"

for v in ${versions}; do
          spack install openmpi @ ${v} % gcc @ 7.3.0
    echo "spack install openmpi @ ${v} % gcc @ 7.3.0"
    spack clean -a
done

date

