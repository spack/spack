#!/bin/bash

# Usage
if [ -z $1 ]; then
	echo "Usage: ./bootstrap <system|rpm|user> [--install]"
	echo "- system: For system administrators to install compilers globally."
	echo "- rpm: For rpm builder to install packages on specific architectures."
	echo "- user: For Pi users to install packages in ~/spack."
	echo "- --install: Build and install."
	echo "- --sync: Sync cached packages to the mirror site."
	exit 1
fi

# PLATFORM, SPACK_ROOT, SPACKPREFIX
echo "Determine ${HOSTNAME} PLATFORM within sandybridge, haswell, knightlanding, minsky."
if [[ $HOSTNAME == *"knl"* ]]; then
	PLATFORM="knightlanding"
elif [[ $HOSTNAME == *"nv"* ]]; then
	PLATFORM="haswell"
elif [[ $HOSTNAME == *"uv"* ]]; then
	PLATFORM="ivybridge"
elif [[ $HOSTNAME == *"minsky"* ]]; then
	PLATFORM="powerpc"
else
	PLATFORM="sandybridge"
fi

SPACK_ROOT=`pwd`

if [ $1 = "system" ]; then
	SPACKPREFIX=/lustre/spack/tools
elif [ $1 = "rpm" ]; then
	SPACKPREFIX=/lustre/spack/$PLATFORM
else
	SPACKPREFIX=$SPACK_ROOT/opt
fi

#Summarizing
echo ">>>"
for var in PLATFORM SPACK_ROOT SPACKPREFIX
do
	echo "$var => ${!var}"
done
echo ">>>"

# Rendering CONFIG_YAML 
for var in SPACKPREFIX
do
	sed -i s=$var=${!var}=g config.yaml.template
done

# CONFIG_YAML, COMPILERS_YAML, PACKAGE_YAML, MIRRORS_YAML
CONFIG_YAML=config.yaml.template

if [[ $HOSTNAME == *"uv"* ]]; then
	COMPILERS_YAML="compilers_sgi.yaml"
elif [[ $HOSTNAME == *"minsky"* ]]; then
	COMPILERS_YAML="compilers_minsky.yaml"
else
	COMPILERS_YAML="compilers.yaml"
fi

if [[ $HOSTNAME == *"uv"* ]]; then
	PACKAGE_YAML="packages_sgi.yaml"
elif [[ $HOSTNAME == *"minsky"* ]]; then
	PACKAGE_YAML="packages_minsky.yaml"
elif [ $1 = "system" ]; then
	PACKAGE_YAML="packages_system.yaml"
else
	PACKAGE_YAML="packages.yaml"
fi

MIRRORS_YAML=mirrors.yaml

# Deploying
mkdir -p ~/.spack
cp -f ${CONFIG_YAML} ~/.spack/config.yaml
cp -f ${PACKAGE_YAML} ~/.spack/packages.yaml
mkdir -p ~/.spack/linux
cp -f ${COMPILERS_YAML} ~/.spack/linux/
cp -f ${MIRRORS_YAML} ~/.spack/linux/
source ${SPACK_ROOT}/share/spack/setup-env.sh

# Reset config.yaml.template
git checkout -- config.yaml.template

# Installing packages
if [[ $2 == "--install" ]]; then
    echo "Installing packages..."
    spack clean --all
    ./build_${1}.sh PLATFORM
fi

# Sync cached source packages to the HTTP servers
if [[ $2 == "--sync" ]]; then
    echo "Sync cached packages to mirror site..."
    rsync -ar --progress --exclude=cudnn ${SPACK_ROOT}/var/spack/cache/ root@lb://var/lib/www/spack.pi.sjtu.edu.cn/mirror/
fi
