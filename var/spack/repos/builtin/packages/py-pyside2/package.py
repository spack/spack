# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyPyside2(PythonPackage):
    """Python bindings for Qt."""

    homepage = "https://www.pyside.org/"
    git      = "https://code.qt.io/pyside/pyside-setup.git"

    # More recent versions of PySide2 (for Qt5) have been taken under
    # the offical Qt umbrella.  For more information, see:
    # https://wiki.qt.io/Qt_for_Python_Development_Getting_Started

    version('develop', tag='dev')
    version('5.15.2.1', tag='v5.15.2.1', submodules=True)
    version('5.14.2.1', tag='v5.14.2.1', submodules=True)
    version('5.13.2', tag='v5.13.2', submodules=True)
    version('5.13.1', tag='v5.13.1', submodules=True)
    version('5.13.0', tag='v5.13.0', submodules=True)
    version('5.12.5', tag='v5.12.5', submodules=True)

    variant('doc', default=False, description='Enables the generation of html and man page documentation')

    depends_on('python@2.7.0:2.7,3.5.0:3.5,3.6.1:', type=('build', 'run'))
    depends_on('python@2.7.0:2.7,3.5.0:3.5,3.6.1:3.8', when='@:5.14', type=('build', 'run'))

    depends_on('cmake@3.1:', type='build')
    depends_on('llvm@6:', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-packaging', type='build')
    depends_on('py-wheel', type='build')
    # https://bugreports.qt.io/browse/PYSIDE-1385
    depends_on('py-wheel@:0.34', when='@:5.14', type='build')
    depends_on('qt@5.11:+opengl')

    depends_on('graphviz', when='+doc', type='build')
    depends_on('libxml2@2.6.32:', when='+doc', type='build')
    depends_on('libxslt@1.1.19:', when='+doc', type='build')
    depends_on('py-sphinx', when='+doc', type='build')

    def install_options(self, spec, prefix):
        args = [
            '--parallel={0}'.format(make_jobs),
            '--ignore-git',
            '--qmake={0}'.format(spec['qt'].prefix.bin.qmake)
        ]
        if self.run_tests:
            args.append('--build-tests')
        return args

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=' + prefix,
               *self.install_options(spec, prefix))

    @run_after('install')
    def install_docs(self):
        if '+doc' in self.spec:
            make('apidoc')
