#!/bin/bash

# Usage
if [ -z $1 ]; then
	echo "Usage: ./bootstrap <system|rpm|user> [--install]"
	echo "- system: For system administrators to install compilers globally."
	echo "- rpm: For rpm builder to install packages on specific architectures."
	echo "- user: For Pi users to install packages in ~/spack."
	echo "- --install: Build and install."
	exit 1
fi

# PLATFORM, SPACK_ROOT, SPACKPREFIX, SPACKSTAGE, SPACKCACHE, SPACKSOURCECACHE
echo 'Determine the PLATFORM sandybridge, haswell, knightlanding.'
if [[ $HOST == *"knl"* ]]; then
	PLATFORM="knightlanding"
elif [[ $HOST == *"nv"* ]]; then
	PLATFORM="haswell"
elif [[ $HOST == *"uv"* ]]; then
	PLATFORM="ivybridge"
else
	PLATFORM="sandybridge"
fi

SPACK_ROOT=`pwd`

echo "Check if the user is rpm(system builder)."
if [ $1 = "system" ]; then
	SPACKPREFIX=/lustre/spack/tools
elif [ $1 = "rpm" ]; then 
	SPACKPREFIX=/lustre/spack/$PLATFORM
else
	SPACKPREFIX=$SPACK_ROOT/opt
fi

export SPACKSTAGE=/tmp/`whoami`/spack_stage
export SPACKCACHE=/tmp/`whoami`/spack_cache
export SPACKSOURCECACHE=/tmp/`whoami`/spack_source_cache

#Summarizing
echo ">>>"
for var in PLATFORM SPACK_ROOT SPACKPREFIX SPACKSTAGE SPACKCACHE SPACKSOURCECACHE
do
	echo "$var => ${!var}"
done
echo ">>>"

# Rendering CONFIG_YAML 
for var in SPACKSTAGE SPACKPREFIX SPACKCACHE SPACKSOURCECACHE
do
	sed -i s=$var=${!var}=g config.yaml.template
done

# CONFIG_YAML, COMPILER_YAML, PACKAGE_YAML
CONFIG_YAML=config.yaml.template

if [[ $HOST == *"uv"* ]]; then
	COMPILER_YAML="compilers_sgi.yaml"
else
	COMPILER_YAML="compilers.yaml"
fi

if [[ $HOST == *"uv"* ]]; then
	PACKAGE_YAML="packages_sgi.yaml"
elif [ $1 = "system" ]; then
	PACKAGE_YAML="packages_system.yaml"
else
	PACKAGE_YAML="packages.yaml"
fi

# Deploying
cp -f ${CONFIG_YAML} ~/.spack/config.yaml
cp -f ${PACKAGE_YAML} $SPACK_ROOT/etc/spack/packages.yaml
cp -f ${COMPILER_YAML} $SPACK_ROOT/etc/spack/compilers.yaml 
source $SPACK_ROOT/share/spack/setup-env.sh

# Installing packages
if [[ $2 == "--install" ]]; then
	echo "Installing packages..."
	./build_${1}.sh
fi

# Reset config.yaml.template
git co -- config.yaml.template
