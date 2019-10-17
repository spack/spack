#!/usr/bin/env bash
#
# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

script="$( basename "$0" )"
cd "$( dirname "$0" )"

export IMAGE="spack/packages.spack.io:latest"

if [ "$script" '=' 'push-image.sh' ] ; then
    docker push "${IMAGE}"
else
    docker build --no-cache --force-rm -t "${IMAGE}" .
fi
