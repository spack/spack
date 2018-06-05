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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-projectq
#
# You can edit this file again by typing:
#
#     spack edit py-projectq
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class PyProjectq(PythonPackage):
    """ProjectQ is an open-source software framework for quantum computing started at ETH Zurich. It allows users to implement their quantum programs in Python using a powerful and intuitive syntax. Proj    ectQ can then translate these programs to any type of back-end, be it a simulator run on a classical computer of an actual quantum chip."""
    
    ## URL and HOMEPAGE
    homepage = "https://projectq.ch"
    url      = "https://github.com/projectq-framework"
    
    ## Provided python modules
    import_modules = ['projectq', 'projectq.backends', 'projectq.cengines', 'projectq.libs', 'projectq.meta', 'projectq.ops', 'projectq.setups', 'projectq.types']

    ## Versions
    version('develop', branch = 'develop', git = 'https://github.com/projectq-framework/projectq.git')
    version('master', branch = 'master', git = 'https://github.com/projectq-framework/projectq.git')

    ## Dependencies
    extends('python')
    
    # always
    depends_on('python', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type=('build', 'link'))
    depends_on('py-numpy', type=('build', 'link', 'run'))
    depends_on('py-scipy',type=('build', 'link', 'run'))
    depends_on('py-future',type=('build', 'link'))
    depends_on('py-pytest@3.1.0:', type=('build', 'link'))
    depends_on('py-requests',type=('build', 'link', 'run'))
    # only when with cppsim - conflict with pybind11@2.2.0
    depends_on('py-pybind11@1.7:2.1,2.2.1:', type=('build', 'link', 'run'))

