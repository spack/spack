#!/bin/bash

# Usage
if [ -z $1 ]; then
	echo "Usage: ./bootstrap <system|rpm|user>"
	echo "- system: For system administrators to install compilers globally."
	echo "- rpm: For rpm builder to install packages on specific architectures."
	echo "- user: For Pi users to install packages in ~/spack."
	exit 1
fi
echo "=> $1"

echo "Determine the CPU architecture; sandybridge, haswell, knightlanding."
if [[ $HOST == "*knl*" ]]; then
	PLATFORM="knightlanding"
elif [[ $HOST == "*nv*" ]]; then
	PLATFORM="haswell"
else
	PLATFORM="sandybridge"
fi
echo "=> $PLATFORM"

echo "Check if the user is rpm(system builder)."
if [ $1 = "system" ]; then
	SPACKPREFIX=/lustre/spack/tools
elif [ $1 = "rpm" ]; then 
	SPACKPREFIX=/lustre/spack/$PLATFORM
else
	SPACKPREFIX=~/spack
fi

export SPACKSTAGE=/tmp/`whoami`/pytest-of-rpm/pytest-4/test_fetch0/tmp
export SPACKCACHE=/tmp/`whoami`/spack_misc_cache
export SPACKSOURCECACHE=/tmp/`whoami`/spack_source_cache

echo "Apply Spack configuration."
mkdir -p ~/.spack

if [ -e ~/.spack/config.yaml ]
then
	mv ~/.spack/config.yaml ~/.spack/config.yaml.bak
fi

cat << EOF > ~/.spack/config.yaml
config:
  build_stage:
  - $SPACKSTAGE
  checksum: true
  dirty: false
  install_tree: $SPACKPREFIX
  misc_cache: $SPACKCACHE
  module_roots:
    dotkit: \$spack/share/spack/dotkit
    lmod: \$spack/share/spack/lmod
    tcl: \$spack/share/spack/modules
  source_cache: $SPACKSOURCECACHE
  verify_ssl: true
EOF

if [ -e ~/.spack/linux/compilers.yaml ]
then
	mv ~/.spack/linux/compilers.yaml ~/.spack/linux/compilers.yaml.bak
fi
mkdir -p ~/.spack/linux
cp -f compilers.yaml  ~/.spack/linux/compilers.yaml

if [ -e ~/.spack/packages.yaml ]
then
	mv ~/.spack/packages.yaml ~/.spack/packages.yaml.bak
fi
cp -f packages.yaml  ~/.spack/packages.yaml

echo "Make Spack configuration take effect."
echo "=> $SPACKPREFIX"
echo "=> $SPACKSTAGE"
echo "=> $SPACKCACHE"
echo "=> $SPACKSOURCECACHE"
source ~/spack/share/spack/setup-env.sh

echo "Installing packages..."
./build_${1}.sh
