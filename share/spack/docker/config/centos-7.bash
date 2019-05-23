# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

unset DISTRO
unset DISTRO_VERSION
unset DOCKERFILE
unset DOCKER_BUILD_CONTEXT
unset BASE_IMAGE
unset BASE_NAME
unset BASE_TAG
unset NAME
unset TAG
unset EXTRA_TAGS

export BASE_IMAGE=centos
export BASE_TAG="7"
export NAME=spack
export TAG='${SPACK_VERSION}-centos-7'
export EXTRA_TAGS='${SPACK_VERSION} centos-7 latest'
