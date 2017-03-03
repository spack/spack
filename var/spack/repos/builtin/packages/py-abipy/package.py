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


class PyAbipy(PythonPackage):
    """Set of python modules and scripts to analyze the results of
    ABINIT computations."""

    homepage = "https://github.com/gmatteo/abipy"

    version('master', git="https://github.com/gmatteo/abipy.git", branch='master')

    variant('gui',     default=False, description='Build the GUI')
    variant('ipython', default=False, description='Build IPython support')

    # Python 2.7 required (Python 3.0+ not supported)
    depends_on('python@2.7:2.8')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython',     type='build')

    depends_on('py-six',                 type=('build', 'run'))
    depends_on('py-prettytable',         type=('build', 'run'))
    depends_on('py-tabulate',            type=('build', 'run'))
    depends_on('py-apscheduler@2.1.0',   type=('build', 'run'))
    depends_on('py-pydispatcher@2.0.3:', type=('build', 'run'))
    depends_on('py-tqdm',                type=('build', 'run'))
    depends_on('py-html2text',           type=('build', 'run'))
    depends_on('py-pyyaml@3.11:',        type=('build', 'run'))
    depends_on('py-pandas',              type=('build', 'run'))
    depends_on('py-numpy@1.8:',          type=('build', 'run'))
    depends_on('py-scipy@0.10:',         type=('build', 'run'))
    depends_on('py-pymatgen@3.0.8:',     type=('build', 'run'))
    depends_on('py-netcdf4',             type=('build', 'run'))

    depends_on('py-wxpython', type=('build', 'run'), when='+gui')
    depends_on('py-wxmplot',  type=('build', 'run'), when='+gui')

    depends_on('py-ipython',  type=('build', 'run'), when='+ipython')
    depends_on('py-jupyter',  type=('build', 'run'), when='+ipython')
    depends_on('py-nbformat', type=('build', 'run'), when='+ipython')

    def patch(self):
        # As of 2017-03-03, the call to the `cleanup()` method
        # causes the build to fail. Add additional exception.
        # TODO: Once a release is added on PyPI, older versions can be
        # removed as well as this patch.
        filter_file('except IOError', 'except (IOError, OSError)', 'setup.py')

    def build_args(self, spec, prefix):
        args = []

        if '+ipython' in spec:
            args.append('--with-ipython')

        return args
