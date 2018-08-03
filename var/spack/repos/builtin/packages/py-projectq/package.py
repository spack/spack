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


class PyProjectq(PythonPackage):
    """
    ProjectQ is an open-source software framework for quantum computing started
    at ETH Zurich. It allows users to implement their quantum programs in
    Python using a powerful and intuitive syntax. ProjectQ can then translate
    these programs to any type of back-end, be it a simulator run on a
    classical computer of an actual quantum chip.
    """

    # Homepage and git repository
    homepage = "https://projectq.ch"
    git      = "https://github.com/projectq-framework/projectq.git"

    # Provided python modules
    import_modules = ['projectq', 'projectq.backends', 'projectq.cengines',
                      'projectq.libs', 'projectq.meta', 'projectq.ops',
                      'projectq.setups', 'projectq.types']

    # Versions
    version('develop', branch='develop')
    version('0.3.6', commit='fa484fe037a3a1772127bbd00fe4628ddba34611')

    # Dependencies
    depends_on('py-setuptools', type=('build'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))
    depends_on('py-pytest@3.1.0:', type=('test'))
    depends_on('py-requests', type=('build', 'run'))
    # conflict with pybind11@2.2.0 -> see requirements.txt
    depends_on('py-pybind11@1.7:2.1,2.2.1:', type=('build', 'run'))
