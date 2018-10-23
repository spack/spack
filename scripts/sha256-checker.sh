#!/bin/bash
printf '%s\n' "**  **  **  $(date) ${BASH_SOURCE[0]}"

export here="$(pwd)"

cd "/usr/projects/draco/vendors/spack.mirror/openmpi"
for filename in `ls -r *.tar.bz2`; do
# for filename in *; do
    #
    version=$(cut -d "-" -f 2 <<< ${filename}) # chop of leading v
    version=$(cut -d "t" -f 1 <<< ${version}) # chop off tar.gz
    version=${version%.*} # chop off trailing .
    # echo "version = ${version}"
    #
    sha="$(cut -d "=" -f 2 <<< "$(sha256sum ${filename})")";
    sha=${sha% *} # everything right of the blank
    sha=${sha%?} # remove last character (a blank)
    sha="${sha:1}"
    sha="SHA256='${sha}"
    # echo "${sha}"
    #
    export line="____version('${version}', ${sha}')"
    # echo "line = "
    echo ${line}
    #
done

cd $here
pwd

