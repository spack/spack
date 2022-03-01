# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyqt5(SIPPackage):
    """PyQt is a set of Python v2 and v3 bindings for The Qt Company's Qt
    application framework and runs on all platforms supported by Qt including
    Windows, OS X, Linux, iOS and Android. PyQt5 supports Qt v5."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/intro"
    url = "https://files.pythonhosted.org/packages/source/P/PyQt5/PyQt5-5.15.2.tar.gz"
    list_url = "https://pypi.org/simple/PyQt5/"

    sip_module = 'PyQt5.sip'

    version('5.15.6', sha256='80343bcab95ffba619f2ed2467fd828ffeb0a251ad7225be5fc06dcc333af452')
    version('5.13.1', sha256='54b7f456341b89eeb3930e786837762ea67f235e886512496c4152ebe106d4af')
    version('5.13.0', sha256='0cdbffe5135926527b61cc3692dd301cd0328dd87eeaf1313e610787c46faff9')
    version('5.12.3', sha256='0db0fa37debab147450f9e052286f7a530404e2aaddc438e97a7dcdf56292110')

    # API files can be installed regardless if Qscintilla is installed or not
    variant('qsci_api', default=False, description='Install PyQt API file for QScintilla')

    # Without opengl support, I got the following error:
    # sip: QOpenGLFramebufferObject is undefined
    depends_on('qt@5:+opengl')
    depends_on('python@2.6:', type=('build', 'run'))
    # contraints according to PKG-INFO
    depends_on('python@3.6:', when='@5.15.2:', type=('build', 'run'))
    depends_on('python@3.5:', when='@5.14:', type=('build', 'run'))
    depends_on('py-pyqt5-sip@12.8:12', when='@5.15.0,5.15.1', type=('build', 'run'))
    depends_on('py-pyqt5-sip@12.7:12', when='@5.14', type=('build', 'run'))
    # contraints according to pyproject.toml
    depends_on('py-sip@6.4:6', when='@5.15.6:', type=('build', 'run'))
    depends_on('py-sip@5.3:6', when='@5.15.0:5.15.5', type=('build', 'run'))
    depends_on('py-sip@5.0.1:5', when='@5.14', type=('build', 'run'))
    depends_on('py-pyqt-builder@1.9:1', when='@5.15.3:', type=('build', 'run'))
    depends_on('py-pyqt-builder@1.6:1', when='@5.15.2', type=('build', 'run'))
    depends_on('py-pyqt-builder@1.1:1', when='@5.14:5.15.1', type=('build', 'run'))
    # contraints according to configure.py
    depends_on('py-sip@4.19.19:4 module=PyQt5.sip', when='@5.13', type=('build', 'run'))
    depends_on('py-sip@4.19.14:4 module=PyQt5.sip', when='@5.12.3', type=('build', 'run'))
    depends_on('py-enum34', when='^python@:3.3', type=('build', 'run'))

    depends_on('py-sip@:4.19.18 module=PyQt5.sip', type=('build', 'run'), when='@:5.13.0')

    @when('@5.14:')
    def configure(self, spec, prefix):
        pass

    @when('@:5.13')
    def configure_args(self):
        args = [
            '--pyuic5-interpreter', self.spec['python'].command.path,
            '--sipdir', self.prefix.share.sip.PyQt5,
            '--designer-plugindir', self.prefix.plugins.designer,
            '--qml-plugindir', self.prefix.plugins.PyQt5,
            '--stubsdir', join_path(python_platlib, 'PyQt5'),
        ]
        if '+qsci_api' in self.spec:
            args.extend(['--qsci-api',
                         '--qsci-api-destdir', self.prefix.share.qsci])
        return args

    @when('@5.14:')
    def build(self, spec, prefix):
        with working_dir(self.stage.source_path):
            sip = Executable(join_path(spec['py-sip'].prefix.bin, 'sip-install'))
            sip(*self.build_args())

    @when('@5.14:')
    def build_args(self):
        args = [
            '--verbose',
            '--confirm-license',
            '--qmake', self.spec['qt'].prefix.bin.qmake,
            '--target-dir', join_path(python_platlib, 'PyQt5'),
            '--jobs', str(make_jobs),
        ]
        if '+qsci_api' in self.spec:
            args.extend(['--api-dir', self.prefix.share.qsci])

        return args

    @when('@5.14:')
    def install(self, spec, prefix):
        pass

    @run_after('install')
    def extend_path_setup(self):
        if self.spec.satisfies('@:5.13'):
            SIPPackage.extend_path_setup(self)

    def setup_run_environment(self, env):
        if self.spec.satisfies('@:5.13'):
            env.prepend_path('QT_PLUGIN_PATH', self.prefix.plugins)
