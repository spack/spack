##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PyPygpu(PythonPackage):
    """Python packge for the libgpuarray C library."""

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

    depends_on('libgpuarray')
    # not just build-time, requires pkg_resources
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython@0.25:', type=('build', 'run'))
    depends_on('py-nose', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-mako', type=('build', 'run'))
    depends_on('libcheck')
