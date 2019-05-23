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

export BASE_IMAGE=ubuntu
export BASE_TAG="16.04"
export NAME=spack
export TAG='${SPACK_VERSION}-ubuntu-16.04'
export EXTRA_TAGS='${SPACK_VERSION}-ubuntu-xenial ubuntu-16.04 ubuntu-xenial'
