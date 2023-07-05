#!/usr/bin/env bash
#
# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
set -e

# TODO: Remove debugging output
set -xv
set_pcluster_defaults() {
    # Set versions of pre-installed software in packages.yaml
    [ -z "${SLURM_VERSION}" ] && SLURM_VERSION=$(strings /opt/slurm/lib/libslurm.so | grep  -e '^VERSION'  | awk '{print $2}'  | sed -e 's?"??g')
    [ -z "${LIBFABRIC_MODULE_VERSION}" ] && LIBFABRIC_MODULE_VERSION=$(grep 'Version:' /opt/amazon/efa/lib64/pkgconfig/libfabric.pc | awk '{print $2}')
    [ -z "${LIBFABRIC_MODULE}" ] && LIBFABRIC_MODULE="libfabric-aws/${LIBFABRIC_MODULE_VERSION}"
    [ -z "${LIBFABRIC_VERSION}" ] && LIBFABRIC_VERSION=${LIBFABRIC_MODULE_VERSION//amzn*}
    [ -z "${GCC_VERSION}" ] && GCC_VERSION=$(gcc -v 2>&1 |tail -n 1| awk '{print $3}' )

    cp "${SPACK_ROOT}"/share/spack/gitlab/cloud_pipelines/stacks/aws-pcluster-"${SPACK_TARGET_ARCH}"/packages.yaml /tmp/packages.yaml
    eval "echo \"$(cat /tmp/packages.yaml)\"" > "${SPACK_ROOT}"/etc/spack/packages.yaml
}

setup_spack() {
    spack compiler add --scope site
    spack external find --scope site
    # Remove all autotools/buildtools packages. These versions need to be managed by spack or it will
    # eventually end up in a version mismatch (e.g. when compiling gmp).
    spack tags build-tools | xargs -I {} spack config --scope site rm packages:{}
}

patch_compilers_yaml() {
    # Graceful exit if package not found by spack
    set +e
    set -o pipefail
    compilers_yaml="${SPACK_ROOT}/etc/spack/compilers.yaml"
    [ -f "${compilers_yaml}" ] || {
        echo "Cannot find ${compilers_yaml}, compiler setup might now be optimal."
        return
    }

    # System ld is too old for amzn linux2
    spack_gcc_version=$(spack find --format '{version}' gcc)
    binutils_path=$(spack find -p binutils | awk '/binutils/ {print $2}')
    [ -d "${binutils_path}" ] && [ -n "${spack_gcc_version}" ] && python3 <<EOF
import yaml

with open("${compilers_yaml}",'r') as f:
    compilers=yaml.safe_load(f)

for c in compilers["compilers"]:
    if "arm" in c["compiler"]["spec"] or "intel" in c["compiler"]["spec"] or "oneapi" in c["compiler"]["spec"] \
       or "${spack_gcc_version}" in c["compiler"]["spec"]:
        compilers["compilers"][compilers["compilers"].index(c)]["compiler"]["environment"] = {"prepend_path":{"PATH":"${binutils_path}/bin"}}

with open("${compilers_yaml}",'w') as f:
    yaml.dump(compilers, f)
EOF

    # Oneapi needs extra_rpath to gcc libstdc++.so.6
    oneapi_gcc_version=$(spack find --format '{compiler}' intel-oneapi-compilers | sed -e 's/=//g') && \
        [ -n "${oneapi_gcc_version}" ] && oneapi_gcc_path=$(spack find -p "${oneapi_gcc_version}" | grep "${oneapi_gcc_version}" | awk '{print $2}') && \
        [ -d "${oneapi_gcc_path}" ] && python3 <<EOF
import yaml

with open("${compilers_yaml}",'r') as f:
    compilers=yaml.safe_load(f)

for c in compilers["compilers"]:
    if "oneapi" in c["compiler"]["spec"]:
        compilers["compilers"][compilers["compilers"].index(c)]["compiler"]["extra_rpaths"] = ["${oneapi_gcc_path}/lib64"]

with open("${compilers_yaml}",'w') as f:
    yaml.dump(compilers, f)
EOF
}

install_packages() {
    # Get gcc from buildcache
    if echo "${SPACK_TARGET_ARCH}" | grep -q neoverse; then
        gcc_hash="jttj24nibqy5jsqf34as5m63umywfa3d"
    else
        gcc_hash="yyvkvlgimaaxjhy32oa5x5eexqekrevc"
    fi

    spack install --no-check-signature /${gcc_hash}
    (
        spack load gcc
        spack compiler add --scope site
    )

    if ! echo "${SPACK_TARGET_ARCH}" | grep -q neoverse; then
        # Add oneapi@latest & intel@latest
        spack install intel-oneapi-compilers-classic
        bash -c ". "$(spack location -i intel-oneapi-compilers)/setvars.sh"; spack compiler add --scope site"
    fi
}

set_pcluster_defaults
setup_spack
install_packages
patch_compilers_yaml
