##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Libgpuarray(CMakePackage):
    """Make a common GPU ndarray(n dimensions array) that can be reused by all
    projects that is as future proof as possible, while keeping it easy to use
    for simple need/quick test."""

    homepage = "http://deeplearning.net/software/libgpuarray/"
    url      = "https://github.com/Theano/libgpuarray/archive/v0.6.1.tar.gz"

    version('0.6.2', '7f163bd5f48f399cd6e608ee3d528ee4')
    version('0.6.1', 'cfcd1b54447f9d55b05514df62c70ae2')
    version('0.6.0', '98a4ec1b4c8f225f0b89c18b899a000b')

    depends_on('cuda')

    extends('python')
