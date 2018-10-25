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


class PyBluepyopt(PythonPackage):
    """Bluebrain Python Optimisation Library"""

    homepage = "https://github.com/BlueBrain/BluePyOpt"
    url = "https://pypi.io/packages/source/b/bluepyopt/bluepyopt-1.6.56.tar.gz"

    version('1.6.56', sha256='1c57c91465ca4b947fe157692e7004a3e6df02e4151e3dc77a8831382a8f1ab9')
    
    variant('neuron', default=True, description="Use BluePyOpt together with NEURON")

    depends_on('py-setuptools', type='build')
    depends_on('py-pandas', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-efel', type='run')
    depends_on('py-deap', type='run')
    depends_on('py-ipyparallel', type='run')
    depends_on('py-pickleshare', type='run')
    depends_on('py-future', type='run')
    depends_on('py-jinja2', type='run')
    depends_on('neuron', type='run', when='+neuron')
