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
echo "Scope => $1"

echo "Determine the CPU architecture; sandybridge, haswell, knightlanding."
if [[ $HOST == "*knl*" ]]; then
	PLATFORM="knightlanding"
elif [[ $HOST == "*nv*" ]]; then
	PLATFORM="haswell"
else
	PLATFORM="sandybridge"
fi
echo "Architecture => $PLATFORM"

SPACK_ROOT=`pwd`
echo "SPACK_ROOT => $SPACK_ROOT"

echo "Check if the user is rpm(system builder)."
if [ $1 = "system" ]; then
	SPACKPREFIX=/lustre/spack/tools
elif [ $1 = "rpm" ]; then 
	SPACKPREFIX=/lustre/spack/$PLATFORM
else
	SPACKPREFIX="$SPACK_ROOT"
fi

export SPACKSTAGE=/tmp/`whoami`/pytest-of-rpm/pytest-4/test_fetch0/tmp
export SPACKCACHE=/tmp/`whoami`/spack_misc_cache
export SPACKSOURCECACHE=/tmp/`whoami`/spack_source_cache

cat << EOF > $SPACK_ROOT/etc/spack/config.yaml
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

rm -f ~/.spack/config.yaml
cp -f compilers.yaml  $SPACK_ROOT/etc/spack/compilers.yaml
if [ $1 = "system" ]; then
	cp -f packages_system.yaml   $SPACK_ROOT/etc/spack/packages.yaml
else
	cp -f packages.yaml   $SPACK_ROOT/etc/spack/packages.yaml
fi

echo "Make Spack configuration take effect."
echo "SPACKPREFIX => $SPACKPREFIX"
echo "SPACKSTAGE  => $SPACKSTAGE"
echo "SPACKCACHE  => $SPACKCACHE"
echo "SPACKSOURCECACHE => $SPACKSOURCECACHE"
source $SPACK_ROOT/share/spack/setup-env.sh

if [[ $2 == "--install" ]]; then
	echo "Installing packages..."
	./build_${1}.sh
fi
