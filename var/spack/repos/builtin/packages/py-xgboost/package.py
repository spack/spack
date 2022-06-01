# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyXgboost(PythonPackage):
    """XGBoost is an optimized distributed gradient boosting library designed to be
    highly efficient, flexible and portable."""

    homepage  = 'https://xgboost.ai/'
    pypi = 'xgboost/xgboost-1.3.3.tar.gz'

    maintainers = ['adamjstewart']
    import_modules = ['xgboost']

    version('1.5.2', sha256='404dc09dca887ef5a9bc0268f882c54b33bfc16ac365a859a11e7b24d49da387')
    version('1.3.3', sha256='397051647bb837915f3ff24afc7d49f7fca57630ffd00fb5ef66ae2a0881fb43')

    variant('pandas',       default=False, description='Enable Pandas extensions for training.')
    variant('scikit-learn', default=False, description='Enable scikit-learn extensions for training.')
    variant('dask',         default=False, description='Enables Dask extensions for distributed training.')
    variant('plotting',     default=False, description='Enables tree and importance plotting.')

    for ver in ['1.3.3', '1.5.2']:
        depends_on('xgboost@' + ver, when='@' + ver)

    depends_on('python@3.6:',   type=('build', 'run'))
    depends_on('py-setuptools', type=('build'))
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-scipy',      type=('build', 'run'))

    depends_on('py-pandas', when='+pandas', type=('build', 'run'))

    depends_on('py-scikit-learn', when='+scikit-learn', type=('build', 'run'))

    depends_on('py-dask',        when='+dask', type=('build', 'run'))
    depends_on('py-pandas',      when='+dask', type=('build', 'run'))
    depends_on('py-distributed', when='+dask', type=('build', 'run'))

    depends_on('py-graphviz',   when='+plotting', type=('build', 'run'))
    depends_on('py-matplotlib', when='+plotting', type=('build', 'run'))

    def patch(self):
        # https://github.com/dmlc/xgboost/issues/6706
        # 'setup.py' is hard-coded to search in Python installation prefix
        filter_file("lib_path = os.path.join(sys.prefix, 'lib')",
                    "lib_path = '{0}'".format(self.spec['xgboost'].libs.directories[0]),
                    "setup.py", string=True)

        # Same for run-time search
        filter_file("os.path.join(curr_path, 'lib'),",
                    "'{0}',".format(self.spec['xgboost'].libs.directories[0]),
                    os.path.join('xgboost', 'libpath.py'), string=True)

    def install_options(self, spec, prefix):
        return ['--use-system-libxgboost']
