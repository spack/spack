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


class PyFlake8(PythonPackage):
    """Flake8 is a wrapper around PyFlakes, pep8 and Ned Batchelder's
    McCabe script."""

    homepage = "https://github.com/PyCQA/flake8"
    url      = "https://github.com/PyCQA/flake8/archive/3.0.4.tar.gz"

    version('3.0.4', 'cf2a7d8c92070f7b62253404ffb54df7')
    version('2.5.4', '366dd1de6c300254c830b81e66979f06')

    extends('python', ignore='bin/(pyflakes|pycodestyle)')
    depends_on('python@2.7:2.8,3.4:')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-flake8 requires py-setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))

    # pyflakes >= 0.8.1, != 1.2.0, != 1.2.1, != 1.2.2, < 1.3.0
    depends_on('py-pyflakes@0.8.1:1.1.0,1.2.3:1.2.3', when='@3.0.4', type=('build', 'run'))
    # pyflakes >= 0.8.1, < 1.1
    depends_on('py-pyflakes@0.8.1:1.0.0', when='@2.5.4', type=('build', 'run'))

    # pycodestyle >= 2.0.0, < 2.1.0
    depends_on('py-pycodestyle@2.0.0:2.0.999', when='@3.0.4', type=('build', 'run'))
    # pep8 >= 1.5.7, != 1.6.0, != 1.6.1, != 1.6.2
    depends_on('py-pycodestyle@1.5.7,1.7.0:', when='@2.5.4', type=('build', 'run'))

    # mccabe >= 0.5.0, < 0.6.0
    depends_on('py-mccabe@0.5.0:0.5.999', when='@3.0.4', type=('build', 'run'))
    # mccabe >= 0.2.1, < 0.5
    depends_on('py-mccabe@0.2.1:0.4.0', when='@2.5.4', type=('build', 'run'))

    # These dependencies breaks concretization
    # See https://github.com/LLNL/spack/issues/2793
    # depends_on('py-configparser', when='^python@:3.3.999', type=('build', 'run'))  # noqa
    # depends_on('py-enum34', when='^python@:3.1.999', type=('build', 'run'))
    depends_on('py-configparser', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'))

    # TODO: Add test dependencies
    # depends_on('py-nose', type='test')
