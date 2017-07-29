#!/bin/bash

function s {
    spack find $@ | grep 'No package'
    if [ $? -eq 0 ]
    then
        spack install $@
    else
        echo "$@ has been installed."
    fi
}

cc=%gcc@4.8.5

intelsuites=(
    intel-parallel-studio@cluster.2015.6+all
    intel-parallel-studio@cluster.2016.4+all
    intel-parallel-studio@cluster.2017.4+all
)

intelcompilers=(
    %intel@15.0.6
    %intel@16.0.4
    %intel@17.0.4
)

buiddeps=(
    autoconf
    binutils
    flex
    gettext
    help2man
    m4
    sigsegv
    libxml2
    ncurses
    pkg-config
    tar
    xz
    zlib
)


jdk='jdk@8u141-b15'

# Compilers
s gcc@4.9.4~binutils    $cc
s gcc@5.4.0~binutils    $cc
s gcc@6.4.0~binutils    $cc
s cmake         $cc
s cuda@8.0.61   $cc
s cuda@7.5.18   $cc
s cuda@6.5.14   $cc
s pgi@16.10     $cc
s $jdk $cc
s maven@3.3.9   ^$jdk $cc
s gradle@3.4    ^$jdk $cc
s ant@1.9.9     ^$jdk $cc
s bazel@0.4.5   ^$jdk $cc
s sbt@0.13.12   ^$jdk $cc

for ((i=0; i<${#intelsuites[@]}; ++i))
do
    rm -f $HOME/spack/etc/spack/licenses/intel/license.lic
    s ${intelsuites[i]} $cc
    rm -f $HOME/spack/etc/spack/licenses/intel/license.lic
    s ${intelsuites[i]} ${intelcompilers[i]}
done

# Uninstall build-time dependency packages
for pkg in "${builddeps[@]}"
do
    spack uninstall -y --all $pkg
done
