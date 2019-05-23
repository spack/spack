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
export BASE_TAG='${SPACK_VERSION}-ubuntu-18.04'
export DISTRO=ubuntu
export DISTRO_VERSION=18.04
export DOCKERFILE=ci/Dockerfile
export DOCKER_BUILD_CONTEXT=.
export NAME=ci
export TAG='ubuntu-18.04'
