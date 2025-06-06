#!/bin/bash
#
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Set USE_SYTHETIC_VERSION to use a unique, non-semantic version

set -e

# Reclone this repo into the package tree
mkdir spack-package
pushd spack-package
SPACK_REPO_ROOT="$(git rev-parse --show-toplevel)"
git clone "${SPACK_REPO_ROOT}" spack
SPACK_PKG_SRC="${PWD}"
popd

# Python 3.7 is the minimum version due to a cryptography dependency.
if ! [[ -e build-tools-venv ]]; then
    python3 -m venv build-tools-venv
fi
source build-tools-venv/bin/activate

# Presume this is a clean release tree synced with upstream. How to check?
if ! [[ "$USE_SYNTHETIC_VERSION" == "" ]]; then
    pushd "${SPACK_PKG_SRC}/spack"
    SYNTH_VERSION="$(hatch version | sed 's/dev[0-9]*/dev/')$(date "+%s")"
    echo "Using synthetic version number $SYNTH_VERSION"
    #hatch version $(hatch version | sed 's/dev[0-9]*/dev/')$(date "+%s")
    hatch version $SYNTH_VERSION
    popd
fi

# Update pyproject.toml
pip install -r requirements.txt
mv "${SPACK_PKG_SRC}/spack/pyproject.toml" "${SPACK_PKG_SRC}/spack/pyproject.toml.bak"
python update-pyproject-toml.py -i "${SPACK_PKG_SRC}/spack/pyproject.toml.bak" -o "${SPACK_PKG_SRC}/pyproject.toml"

# Install site-admin config.yaml for external install
mkdir -p "${SPACK_PKG_SRC}/spack/etc/spack/site-admin"
cat <<EOF > "${SPACK_PKG_SRC}/spack/etc/spack/site-admin/config.yaml"
config:
  install_tree:
    root:
      \$spack_state_home/\$spack_instance_id/opt/spack
EOF

# Update defaults/config.yaml with a warning about site-admin/config.yaml
cp "${SPACK_PKG_SRC}/spack/etc/spack/defaults/config.yaml" config.yaml.bak
cat <<EOF > new.config.yaml
# Since this Spack is managed by pip, this configuration is overriden
# by the one in ../site-admin/config.yaml. Please refer to that one for
# current settings, particularly config: install_tree: root.
#
# This leverages the new site-admin configuration scope, which is
# described in the configuration section under scope precedence in the
# online documentation.
EOF
cat config.yaml.bak >> new.config.yaml
mv new.config.yaml "${SPACK_PKG_SRC}/spack/etc/spack/defaults/config.yaml"

pushd "${SPACK_PKG_SRC}"
python3 -m build
