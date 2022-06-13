# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class PyTensorboardDataServer(PythonPackage):
    """Fast data loading for TensorBoard"""

    homepage = "https://github.com/tensorflow/tensorboard/tree/master/tensorboard/data/server"
    git      = "https://github.com/tensorflow/tensorboard"

    version('0.6.1', commit='6acf0be88b5727e546dd64a8b9b12d790601d561')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('rust', type='build')

    def setup_build_environment(self, env):
        env.set('CARGO_HOME', self.stage.source_path)

    def install(self, spec, prefix):
        with working_dir(join_path('tensorboard', 'data', 'server')):
            cargo = which('cargo')
            cargo('build', '--release')

        with working_dir(join_path('tensorboard', 'data', 'server',
                                   'pip_package')):
            python('build.py',
                   '--out-dir={0}'.format(self.stage.source_path),
                   '--server-binary={0}'.format(join_path(self.stage.source_path,
                                                          'tensorboard',
                                                          'data',
                                                          'server',
                                                          'target',
                                                          'release',
                                                          'rustboard')))

        wheel = glob.glob('*.whl')[0]
        args = std_pip_args + ['--prefix=' + prefix, wheel]
        pip(*args)
