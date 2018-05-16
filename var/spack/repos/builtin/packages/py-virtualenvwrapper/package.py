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


class PyVirtualenvwrapper(PythonPackage):
    """virtualenvwrapper is a set of extensions to Ian Bicking's
    virtualenv tool. The extensions include wrappers for creating and
    deleting virtual environments and otherwise managing your development
    workflow, making it easier to work on more than one project at a time
    without introducing conflicts in their dependencies."""

    homepage = "https://bitbucket.org/virtualenvwrapper/virtualenvwrapper.git"
    url      = "https://pypi.io/packages/source/v/virtualenvwrapper/virtualenvwrapper-4.8.2.tar.gz"

    version('4.8.2', '8e3af0e0d42733f15c5e36df484a952e')

    depends_on('python@2.6:')
    depends_on('py-virtualenv', type=('build', 'run'))
    depends_on('py-virtualenv-clone', type=('build', 'run'))
    depends_on('py-stevedore', type=('build', 'run'))
    # not just build-time, requires pkg_resources
    depends_on('py-setuptools', type=('build', 'run'))
