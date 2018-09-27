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


class PyScipy(PythonPackage):
    """SciPy (pronounced "Sigh Pie") is a Scientific Library for Python.
    It provides many user-friendly and efficient numerical routines such
    as routines for numerical integration and optimization."""

    homepage = "http://www.scipy.org/"
    url = "https://pypi.io/packages/source/s/scipy/scipy-0.19.1.tar.gz"

    install_time_test_callbacks = ['install_test', 'import_module_test']

    import_modules = [
        'scipy', 'scipy._build_utils', 'scipy._lib', 'scipy.cluster',
        'scipy.constants', 'scipy.fftpack', 'scipy.integrate',
        'scipy.interpolate', 'scipy.io', 'scipy.linalg', 'scipy.misc',
        'scipy.ndimage', 'scipy.odr', 'scipy.optimize', 'scipy.signal',
        'scipy.sparse', 'scipy.spatial', 'scipy.special', 'scipy.stats',
        'scipy.weave', 'scipy.io.arff', 'scipy.io.harwell_boeing',
        'scipy.io.matlab', 'scipy.optimize._lsq', 'scipy.sparse.csgraph',
        'scipy.sparse.linalg', 'scipy.sparse.linalg.dsolve',
        'scipy.sparse.linalg.eigen', 'scipy.sparse.linalg.isolve',
        'scipy.sparse.linalg.eigen.arpack', 'scipy.sparse.linalg.eigen.lobpcg',
        'scipy.special._precompute'
    ]

    version('1.1.0', 'aa6bcc85276b6f25e17bcfc4dede8718')
    version('1.0.0', '53fa34bd3733a9a4216842b6000f7316')
    version('0.19.1', '6b4d91b62f1926282b127194a06b72b3')
    version('0.19.0', '91b8396231eec780222a57703d3ec550',
            url="https://pypi.io/packages/source/s/scipy/scipy-0.19.0.zip")
    version('0.18.1', '5fb5fb7ccb113ab3a039702b6c2f3327')
    version('0.17.0', '5ff2971e1ce90e762c59d2cd84837224')
    version('0.15.1', 'be56cd8e60591d6332aac792a5880110')
    version('0.15.0', '639112f077f0aeb6d80718dc5019dc7a')

    depends_on('python@2.6:2.8,3.2:')
    depends_on('py-setuptools', type='build')
    depends_on('py-nose', type='test')
    depends_on('py-numpy@1.7.1:+blas+lapack', type=('build', 'run'))

    # NOTE: scipy picks up Blas/Lapack from numpy, see
    # http://www.scipy.org/scipylib/building/linux.html#step-4-build-numpy-1-5-0
    depends_on('blas')
    depends_on('lapack')

    def build_args(self, spec, prefix):
        args = []

        # Build in parallel
        # Known problems with Python 3.5+
        # https://github.com/spack/spack/issues/7927
        # https://github.com/scipy/scipy/issues/7112
        if not spec.satisfies('^python@3.5:'):
            args.extend(['-j', str(make_jobs)])

        return args

    def test(self):
        # `setup.py test` is not supported.  Use one of the following
        # instead:
        #
        # - `python runtests.py`              (to build and test)
        # - `python runtests.py --no-build`   (to test installed scipy)
        # - `>>> scipy.test()`           (run tests for installed scipy
        #                                 from within an interpreter)
        pass

    def install_test(self):
        # Change directories due to the following error:
        #
        # ImportError: Error importing scipy: you should not try to import
        #       scipy from its source directory; please exit the scipy
        #       source tree, and relaunch your python interpreter from there.
        with working_dir('spack-test', create=True):
            python('-c', 'import scipy; scipy.test("full", verbose=2)')
