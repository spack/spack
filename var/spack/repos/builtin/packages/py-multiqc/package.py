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


class PyMultiqc(PythonPackage):
    """MultiQC is a tool to aggregate bioinformatics results across many
    samples into a single report. It is written in Python and contains modules
    for a large number of common bioinformatics tools."""

    homepage = "https://multiqc.info"
    url      = "https://github.com/ewels/MultiQC/tarball/v1.0"

    version('1.0', '27afc19327105818e39b385211b27694')

    depends_on('py-setuptools', type='build')
    depends_on('py-click', type='run')
    depends_on('py-jinja2', type='run')
    depends_on('py-lzstring', type='run')
    depends_on('py-future', type='run')
    depends_on('py-spectra', type='run')
    depends_on('py-colormath', type='run')
