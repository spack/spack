#!/usr/bin/env bash
#
# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
set -e

# Use the same spack version as used in the build cache container to make sure the compiler version is available and installs without issues.
version_tag="v0.22.0"

set_pcluster_defaults() {
    # Set versions of pre-installed software in packages.yaml
    [ -z "${SLURM_ROOT}" ] && ls /etc/systemd/system/slurm* &>/dev/null && \
        SLURM_ROOT=$(dirname $(dirname "$(awk '/ExecStart=/ {print $1}' /etc/systemd/system/slurm* | sed -e 's?^.*=??1' | head -n1)"))
    # Fallback to default location if SLURM not in systemd
    [ -z "${SLURM_ROOT}" ] && [ -d "/opt/slurm" ] && SLURM_ROOT=/opt/slurm
    [ -z "${SLURM_VERSION}" ] && SLURM_VERSION=$(strings "${SLURM_ROOT}"/lib/libslurm.so | grep -e '^VERSION' | awk '{print $2}' | sed -e 's?"??g')
    [ -z "${LIBFABRIC_VERSION}" ] && LIBFABRIC_VERSION=$(awk '/Version:/{print $2}' "$(find /opt/amazon/efa/ -name libfabric.pc | head -n1)" | sed -e 's?~??g' -e 's?amzn.*??g')
    export SLURM_ROOT SLURM_VERSION LIBFABRIC_VERSION

    envsubst < "${SPACK_ROOT}/share/spack/gitlab/cloud_pipelines/stacks/${SPACK_CI_STACK_NAME}/packages.yaml" > "${SPACK_ROOT}"/etc/spack/packages.yaml
}

patch_compilers_yaml() {
    # Graceful exit if package not found by spack
    set -o pipefail
    compilers_yaml="${SPACK_ROOT}/etc/spack/compilers.yaml"
    [ -f "${compilers_yaml}" ] || {
        echo "Cannot find ${compilers_yaml}, compiler setup might now be optimal."
        return
    }

    # System ld is too old for amzn linux2
    spack_gcc_version=$(spack find --format '{version}' gcc)
    binutils_path=$(spack find -p binutils | awk '/binutils/ {print $2}' | head -n1)
    if [ -d "${binutils_path}" ] && [ -n "${spack_gcc_version}" ]; then python3 <<EOF
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
    fi
    # Oneapi needs extra_rpath to gcc libstdc++.so.6
    if [ "x86_64" == "$(arch)" ] && oneapi_gcc_version=$(spack find --format '{compiler}' intel-oneapi-compilers | sed -e 's/=//g') && \
            [ -n "${oneapi_gcc_version}" ] && oneapi_gcc_path=$(spack find -p "${oneapi_gcc_version}" | grep "${oneapi_gcc_version}" | awk '{print $2}' | head -n1) && \
            [ -d "${oneapi_gcc_path}" ]; then python3 <<EOF
import yaml

with open("${compilers_yaml}",'r') as f:
    compilers=yaml.safe_load(f)

for c in compilers["compilers"]:
    if "oneapi" in c["compiler"]["spec"]:
        compilers["compilers"][compilers["compilers"].index(c)]["compiler"]["extra_rpaths"] = ["${oneapi_gcc_path}/lib64"]

with open("${compilers_yaml}",'w') as f:
    yaml.dump(compilers, f)
EOF
    fi
}

install_compilers() {
    # Install Intel compilers through a static spack version such that the compiler's hash does not change.
    # The compilers needs to be in the same install tree as the rest of the software such that the path
    # relocation works correctly. This holds the danger that this part will fail when the current spack gets
    # incompatible with the one in $spack_intel_compiler_commit. Therefore, we make intel installations optional
    # in packages.yaml files and add a fallback `%gcc` version for each application.
    if [ -f "/bootstrap-compilers/spack/etc/spack/compilers.yaml" ]; then
        # Running inside a gitlab CI container
        # Intel and gcc@12 compiler are pre-installed and their location is known in 
        cp /bootstrap-compilers/spack/etc/spack/compilers.yaml "${SPACK_ROOT}"/etc/spack/
    else
        spack compiler add --scope site
        # We need to treat compilers as essentially external, i.e. their installation location
        # (including hash) must not change when any changes are pushed to spack. The reason is that
        # changes in the compilers are not reflected in the package hashes built in the CI. Hence, those
        # packages will reference a wrong compiler path once the path changes.

        # `gcc@12.3.0%gcc@7.3.1` is created as part of building the pipeline containers.
        # `ghcr.io/spack/pcluster-amazonlinux-2:pr-52@sha256:27a2e9cc8ddbe25504caeac3d78ef556d913a2ff1bab0a7e713e98e35578bc36` produced the following hashes.
        if [ "x86_64" == "$(arch)" ]; then
            gcc_hash="vxlibl3ubl5ptwzb3zydgksfa5osdea6"
        else
            gcc_hash="bikooik6f3fyrkroarulsadbii43ggz5"
        fi

        spack install /${gcc_hash}
        (
            spack load gcc
            spack compiler add --scope site
        )

        if [ "x86_64" == "$(arch)" ]; then
            (
                # Running on a system consuming the binary cache
                CURRENT_SPACK_ROOT=${SPACK_ROOT}
                DIR="$(mktemp -d)"
                cd "${DIR}"
                # oneapi@2024.1.0 is the last compiler which works with AL2 glibc
                git clone --depth=1 -b ${version_tag} https://github.com/spack/spack.git \
                    && cd spack \
                    && cp "${CURRENT_SPACK_ROOT}/etc/spack/{config,compilers,packages}.yaml" etc/spack/ \
                    && . share/spack/setup-env.sh \
                    && spack install intel-oneapi-compilers@2024.1.0
                rm -rf "${DIR}"
            )
            bash -c ". \"$(spack location -i intel-oneapi-compilers)\"/setvars.sh; spack compiler add --scope site" \
                || true
            spack clean -m
        fi
    fi
}

set_pcluster_defaults
install_compilers
patch_compilers_yaml
