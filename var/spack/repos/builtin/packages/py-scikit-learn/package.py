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


class PyScikitLearn(PythonPackage):
    """A set of python modules for machine learning and data mining."""

    homepage = "https://pypi.python.org/pypi/scikit-learn"
    url      = "https://pypi.io/packages/source/s/scikit-learn/scikit-learn-0.18.1.tar.gz"

    version('0.19.1', 'b67143988c108862735a96cf2b1e827a')
    version('0.18.1', '6b0ff1eaa5010043895dd63d1e3c60c9')
    version('0.15.2', 'd9822ad0238e17b382a3c756ea94fe0d')
    version('0.16.1', '363ddda501e3b6b61726aa40b8dbdb7e')
    version('0.17.1', 'a2f8b877e6d99b1ed737144f5a478dfc')
    version('0.13.1', 'acba398e1d46274b8470f40d0926e6a4')

    depends_on('python@2.6:2.8,3.3:')
    depends_on('py-numpy@1.6.1:', type=('build', 'run'))
    depends_on('py-scipy@0.9:',   type=('build', 'run'))
