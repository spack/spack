##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class PyMultiqc(PythonPackage):
    """MultiQC is a tool to aggregate bioinformatics results across many
    samples into a single report. It is written in Python and contains modules
    for a large number of common bioinformatics tools."""

    homepage = "https://multiqc.info"
    url      = "https://pypi.io/packages/source/m/multiqc/multiqc-1.0.tar.gz"

    version('1.5', 'c9fc5f54a75b1d0c3e119e0db7f5fe72')
    version('1.3', '78fef8a89c0bd40d559b10c1f736bbcd')
    version('1.0', '0b7310b3f75595e5be8099fbed2d2515')

    depends_on('python@2.7:')
    depends_on('py-setuptools', type='build')
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-jinja2@2.9:', type=('build', 'run'))
    depends_on('py-lzstring', type=('build', 'run'))
    depends_on('py-future@0.14.1:', type=('build', 'run'))
    depends_on('py-spectra', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-simplejson', type=('build', 'run'))
