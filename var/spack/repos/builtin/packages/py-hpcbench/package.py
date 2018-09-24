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
from spack import *

class PyHpcbench(PythonPackage):
    """Define and run your benchmarks"""

    homepage = "https://github.com/BlueBrain/hpcbench"

    url      = "https://pypi.io/packages/source/h/hpcbench/hpcbench-0.8.tar.gz"
    git      = "https://github.com/BlueBrain/hpcbench.git"

    version('develop', branch='master')
    version('0.8', sha256='120f5b1e6ff05a944b34a910f3099b4b0f50e96c60cf550b8fc6c42f64194697')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-cached-property')
    depends_on('py-clustershell')
    depends_on('py-cookiecutter')
    depends_on('py-docopt')
    depends_on('py-elasticsearch')
    depends_on('py-jinja2')
    depends_on('py-mock', type='test')
    depends_on('py-numpy')
    depends_on('py-pyyaml')
    depends_on('py-magic')
    depends_on('py-six')
