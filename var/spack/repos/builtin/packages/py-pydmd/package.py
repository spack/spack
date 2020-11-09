# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPydmd(PythonPackage):
    """PyDMD is a Python package that uses Dynamic Mode Decomposition
    for a data-driven model simplification based on spatiotemporal
    coherent structures."""

    homepage = "https://mathlab.github.io/PyDMD/"
    url      = "https://github.com/mathLab/PyDMD/archive/v0.3.tar.gz"

    import_modules = ['pydmd']

    version('0.3', sha256='f490fc139677e4d9fc1240636a2c5992d22879517c9574d13164dc5179b0f785')

    variant('docs', default=False, description='Build HTML documentation')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))

    depends_on('py-nose', type=('build', 'test'))
    depends_on('py-sphinx@1.4.5', type=('build', 'run'), when='+docs')
    depends_on('py-sphinx-rtd-theme', type=('build', 'run'), when='+docs')

    # https://github.com/mathLab/PyDMD/pull/133
    patch('isuue-133.patch', when='@0.3')

    conflicts(
        '^py-sphinx-rtd-theme@0.5.0',
        msg='py-sphinx-rtd-theme@0.5.0 fails to build (see https://github.com/spack/spack/issues/19310); '
        'specify an older version, e.g., py-sphinx-rtd-theme@0.4.3',
    )

    phases = ['build', 'install']

    def build(self, spec, prefix):
        self.setup_py('build')

        if '+docs' in spec:
            with working_dir('docs'):
                make('html')

    def install(self, spec, prefix):
        self.setup_py('install')

        if '+docs' in spec:
            install_tree('docs', prefix.docs)

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        python('test.py')
