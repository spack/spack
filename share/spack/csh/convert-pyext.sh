#!/bin/bash --noprofile
PYEXT_REGEX=".*/.*/package.py"

find var/spack/repos/builtin/packages/ -type f -regextype sed -regex ${PYEXT_REGEX} -exec \
    sed -i 's/python('\''setup.py'\'', /setup_py(/' {} \;
