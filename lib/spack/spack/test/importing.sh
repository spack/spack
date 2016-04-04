#!/bin/bash

# Test importing Spack as modules independently from ./bin/spack.

testdir=$(dirname $(realpath $BASH_SOURCE))
srcdir=$(dirname $testdir)
libdir=$(dirname $srcdir)
topdir=$(dirname $(dirname $libdir))
export PYTHONPATH=$libdir

set -e
set -x
python -c 'import spack'


cd $topdir

for mod in $(ls lib/spack/spack/*/__init__.py|awk -F/ '{print $4}')
do
    echo "Importing spack.$mod"
    python -c "import spack.$mod"
done

for mod in $(ls lib/spack/spack/*.py|awk -F/ '{print $4}'|sed 's|\.py||')
do
    if [ "$mod" = "__init__" ] ; then
	continue
    fi
    echo "Importing spack.$mod"
    python -c "import spack.$mod"
done

	     
