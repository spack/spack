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


class PyNbconvert(Package):
    """Jupyter Notebook Conversion"""

    homepage = "https://github.com/jupyter/nbconvert"
    url      = "https://github.com/jupyter/nbconvert/archive/4.2.0.tar.gz"

    version('4.2.0' , '8bd88771cc00f575d5edcd0b5197f964')
    version('4.1.0' , '06655576713ba1ff7cece2b92760c187')
    version('4.0.0' , '9661620b1e10a7b46f314588d2d0932f')

    extends('python')

    depends_on('py-setuptools', type='build')
    depends_on('py-pycurl', type='build')
    depends_on('python@2.7:2.7.999,3.3:')
    depends_on('py-mistune')
    depends_on('py-jinja2')
    depends_on('py-pygments')
    depends_on('py-traitlets')
    depends_on('py-jupyter-core')
    depends_on('py-nbformat')
    depends_on('py-entrypoints')
    depends_on('py-tornado')
    depends_on('py-jupyter-client')

    def install(self, spec, prefix):
        setup_py('install', '--prefix={0}'.format(prefix))
