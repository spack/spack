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

export BASE_IMAGE=spack/spack
export BASE_TAG='${SPACK_VERSION}-centos-7'
export DISTRO=centos
export DISTRO_VERSION=7
export DOCKERFILE=ci/Dockerfile
export DOCKER_BUILD_CONTEXT=.
export NAME=ci
export TAG='centos-7'
