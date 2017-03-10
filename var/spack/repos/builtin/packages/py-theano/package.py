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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-theano
#
# You can edit this file again by typing:
#
#     spack edit py-theano
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class PyTheano(PythonPackage):
    """Theano is a Python library that allows you to define, optimize,
    and evaluate mathematical expressions involving multi-dimensional
    arrays efficiently. Theano features: tight integration with NumPy
    transparent use of a GPU, transparent use of a GPU, efficient
    symbolic differentiation, speed and stability optimizations,
    dynamic C code generation, extensive unit-testing and
    self-verification.

    Theano has been powering large-scale computationally intensive
    scientific investigations since 2007. But it is also approachable
    enough to be used in the classroom (University of Montreal's deep
    learning/machine learning classes)."""

    homepage = "http://deeplearning.net/software/theano/index.html"
    url      = "https://github.com/Theano/Theano/archive/rel-0.9.0rc2.tar.gz"

    version('rel-0.9.0rc2', '18109046d68f3e7f9211885a98ff6357')
    version('rel-0.7rc2',   '8bff0d24e692fd4f0a917a6af99775c6')

    variant('gpu', default=False, 
            description='Builds with support for GPUs via CUDA and cuDNN')

    depends_on('python@2.6:,3.3:')
    depends_on('py-setuptools',   type='build')
    depends_on('py-numpy@1.7.1:', type='run')
    depends_on('py-scipy@0.11:',  type='run')

    depends_on('blas')

    depends_on('cuda', when='+gpu')
    depends_on('libgpuarray', when='+gpu')

    extends('python')
