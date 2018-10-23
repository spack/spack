#!/bin/bash
printf '%s\n' "**  **  **  $(date) ${BASH_SOURCE[0]}"

export here="$(pwd)"

cd "/usr/projects/draco/vendors/spack.mirror/openmpi"

for filename in `ls -r *.tar.bz2`; do
# for filename in *; doi
        #
    # ${filename} = openmpi-3.1.2.tar.bz2
    version=$(cut -d "-" -f 2 <<< ${filename}) # chop of leading name
    version=$(cut -d "t" -f 1 <<< ${version})  # chop off tar.bz2
    version=${version%.*}                      # chop off trailing .
        #
    # echo "version = ${version}"
    # sha256sum openmpi-3.1.2.tar.bz2
    # c654ed847f34a278c52a15c98add40402b4a90f0c540779f1ae6c489af8a76c5  openmpi-3.1.2.tar.bz2
    sha="$(sha256sum ${filename})";
    sha=${sha% *} # everything right of the blank
    sha=${sha%?}  # remove last character (a blank)
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

