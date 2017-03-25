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


class PyMccabe(PythonPackage):
    """Ned's script to check McCabe complexity."""

    homepage = "https://github.com/PyCQA/mccabe"
    url      = "https://github.com/PyCQA/mccabe/archive/0.5.2.tar.gz"

    version('0.5.2', '3cdf2d7faa1464b18905fe9a7063a632')
    version('0.5.1', '864b364829156701bec797712be8ece0')
    version('0.5.0', '71c0ce5e5c4676753525154f6c5d3af8')
    version('0.4.0', '9cf5712e5f1785aaa27273a4328babe4')
    version('0.3.1', '45c48c0978e6fc1f31fedcb918178abb')
    version('0.3',   'c583f58ea28be12842c001473d77504d')
    version('0.2.1', 'fcba311ebd999f48359a8ab28da94b30')
    version('0.2',   '36d4808c37e187dbb1fe2373a0ac6645')
    version('0.1',   '3c9e8e72612a9c01d865630cc569150a')

    depends_on('python@2.7:2.8,3.3:')

    depends_on('py-setuptools', type='build')

    # TODO: Add test dependencies
    # depends_on('py-pytest', type='test')
