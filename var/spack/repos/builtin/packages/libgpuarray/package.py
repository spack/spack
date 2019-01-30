# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libgpuarray(CMakePackage):
    """Make a common GPU ndarray(n dimensions array) that can be reused by all
    projects that is as future proof as possible, while keeping it easy to use
    for simple need/quick test."""

    homepage = "http://deeplearning.net/software/libgpuarray/"
    url      = "https://github.com/Theano/libgpuarray/archive/v0.6.1.tar.gz"

    version('0.7.5', '2534011464555c3e99d14231db965c20')
    version('0.7.4', '19f57cd381175162048c8154f5251546')
    version('0.7.3', 'cb44aeb8482330974abdb36b0a477e5d')
    version('0.7.2', '0f9d7748501bc5c71bf04aae2285ac4e')
    version('0.7.1', '7eb5bb6689ddbc386a9d498f5c0027fb')
    version('0.7.0', 'f71b066f21ef7666f3a851e96c26f52e')
    version('0.6.9', '7f75c39f1436c920ed9c5ffde5631fc0')
    version('0.6.2', '7f163bd5f48f399cd6e608ee3d528ee4')
    version('0.6.1', 'cfcd1b54447f9d55b05514df62c70ae2')
    version('0.6.0', '98a4ec1b4c8f225f0b89c18b899a000b')

    depends_on('cuda')
    depends_on('cmake@3:', type='build')
    depends_on('libcheck')
