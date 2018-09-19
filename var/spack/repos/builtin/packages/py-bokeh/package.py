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


class PyBokeh(PythonPackage):
    """Statistical and novel interactive HTML plots for Python"""

    homepage = "http://github.com/bokeh/bokeh"
    url      = "https://pypi.io/packages/source/b/bokeh/bokeh-0.12.2.tar.gz"

    version('0.12.2', '2d1621bffe6e2ab9d42efbf733861c4f')

    depends_on('python@2.6:')
    depends_on('py-six@1.5.2:',       type=('build', 'run'))
    depends_on('py-requests@1.2.3:',  type=('build', 'run'))
    depends_on('py-pyyaml@3.10:',     type=('build', 'run'))
    depends_on('py-dateutil@2.1:',    type=('build', 'run'))
    depends_on('py-jinja2@2.7:',      type=('build', 'run'))
    depends_on('py-numpy@1.7.1:',     type=('build', 'run'))
    depends_on('py-tornado@4.3:',     type=('build', 'run'))
    depends_on('py-futures@3.0.3:',   type=('build', 'run'),
        when='^python@2.7:2.8')
