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


class PyAse(PythonPackage):
    """The Atomic Simulation Environment (ASE) is a set of tools
    and Python modules for setting up, manipulating, running,
    visualizing and analyzing atomistic simulations."""

    homepage = "https://wiki.fysik.dtu.dk/ase/"
    url      = "https://pypi.io/packages/source/a/ase/ase-3.13.0.tar.gz"

    version('3.15.0', '65a0143753517c2df157e53bd29a18e3')
    version('3.13.0', 'e946a0addc5b61e5e2e75857e0f99b89')

    depends_on('python@2.6:')
    depends_on('py-numpy', type=('build', 'run'))
