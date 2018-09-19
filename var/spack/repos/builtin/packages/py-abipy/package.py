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


class PyAbipy(PythonPackage):
    """Python package to automate ABINIT calculations and analyze
    the results."""

    homepage = "https://github.com/abinit/abipy"
    url      = "https://pypi.io/packages/source/a/abipy/abipy-0.2.0.tar.gz"

    version('0.2.0', 'af9bc5cf7d5ca1a56ff73e2a65c5bcbd')

    variant('gui',     default=False, description='Build the GUI')
    variant('ipython', default=False, description='Build IPython support')

    extends('python', ignore='bin/(feff_.*|gaussian_analyzer|get_environment|html2text|nc3tonc4|nc4tonc3|ncinfo|pmg|pydii|tabulate|tqdm)')

    depends_on('python@2.7:')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython',     type='build')

    depends_on('py-six',                 type=('build', 'run'))
    depends_on('py-prettytable',         type=('build', 'run'))
    depends_on('py-tabulate',            type=('build', 'run'))
    depends_on('py-apscheduler@2.1.0',   type=('build', 'run'))
    depends_on('py-pydispatcher@2.0.5:', type=('build', 'run'))
    depends_on('py-tqdm',                type=('build', 'run'))
    depends_on('py-html2text',           type=('build', 'run'))
    depends_on('py-pyyaml@3.11:',        type=('build', 'run'))
    depends_on('py-pandas',              type=('build', 'run'))
    depends_on('py-numpy@1.9:',          type=('build', 'run'))
    depends_on('py-scipy@0.14:',         type=('build', 'run'))
    depends_on('py-spglib',              type=('build', 'run'))
    depends_on('py-pymatgen@4.7.2:',     type=('build', 'run'))
    depends_on('py-netcdf4',             type=('build', 'run'))
    depends_on('py-matplotlib@1.5:',     type=('build', 'run'))
    depends_on('py-seaborn',             type=('build', 'run'))

    depends_on('py-wxpython', type=('build', 'run'), when='+gui')
    depends_on('py-wxmplot',  type=('build', 'run'), when='+gui')

    depends_on('py-ipython',  type=('build', 'run'), when='+ipython')
    depends_on('py-jupyter',  type=('build', 'run'), when='+ipython')
    depends_on('py-nbformat', type=('build', 'run'), when='+ipython')

    def build_args(self, spec, prefix):
        args = []

        if '+ipython' in spec:
            args.append('--with-ipython')

        return args
