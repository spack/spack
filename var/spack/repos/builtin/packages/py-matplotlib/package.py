# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.pkgkit import *


class PyMatplotlib(PythonPackage):
    """Matplotlib is a comprehensive library for creating static, animated,
    and interactive visualizations in Python."""

    homepage = "https://matplotlib.org/"
    pypi = "matplotlib/matplotlib-3.3.2.tar.gz"

    maintainers = ['adamjstewart']
    import_modules = [
        'mpl_toolkits.axes_grid1', 'mpl_toolkits.axes_grid',
        'mpl_toolkits.mplot3d', 'mpl_toolkits.axisartist', 'matplotlib',
        'matplotlib.compat', 'matplotlib.tri', 'matplotlib.axes',
        'matplotlib.sphinxext', 'matplotlib.cbook', 'matplotlib.backends',
        'matplotlib.backends.qt_editor', 'matplotlib.style',
        'matplotlib.projections', 'matplotlib.testing',
        'matplotlib.testing.jpl_units', 'pylab'
    ]

    version('3.5.1', sha256='b2e9810e09c3a47b73ce9cab5a72243a1258f61e7900969097a817232246ce1c')
    version('3.5.0', sha256='38892a254420d95594285077276162a5e9e9c30b6da08bdc2a4d53331ad9a6fa')
    version('3.4.3', sha256='fc4f526dfdb31c9bd6b8ca06bf9fab663ca12f3ec9cdf4496fb44bc680140318')
    version('3.4.2', sha256='d8d994cefdff9aaba45166eb3de4f5211adb4accac85cbf97137e98f26ea0219')
    version('3.4.1', sha256='84d4c4f650f356678a5d658a43ca21a41fca13f9b8b00169c0b76e6a6a948908')
    version('3.4.0', sha256='424ddb3422c65b284a38a97eb48f5cb64b66a44a773e0c71281a347f1738f146')
    version('3.3.4', sha256='3e477db76c22929e4c6876c44f88d790aacdf3c3f8f3a90cb1975c0bf37825b0')
    version('3.3.3', sha256='b1b60c6476c4cfe9e5cf8ab0d3127476fd3d5f05de0f343a452badaad0e4bdec')
    version('3.3.2', sha256='3d2edbf59367f03cd9daf42939ca06383a7d7803e3993eb5ff1bee8e8a3fbb6b')
    version('3.3.1', sha256='87f53bcce90772f942c2db56736788b39332d552461a5cb13f05ff45c1680f0e')
    version('3.3.0', sha256='24e8db94948019d531ce0bcd637ac24b1c8f6744ac86d2aa0eb6dbaeb1386f82')
    version('3.2.2', sha256='3d77a6630d093d74cbbfebaa0571d00790966be1ed204e4a8239f5cbd6835c5d')
    version('3.2.1', sha256='ffe2f9cdcea1086fc414e82f42271ecf1976700b8edd16ca9d376189c6d93aee')
    version('3.2.0', sha256='651d76daf9168250370d4befb09f79875daa2224a9096d97dfc3ed764c842be4')
    version('3.1.3', sha256='db3121f12fb9b99f105d1413aebaeb3d943f269f3d262b45586d12765866f0c6')
    version('3.1.2', sha256='8e8e2c2fe3d873108735c6ee9884e6f36f467df4a143136209cff303b183bada')
    version('3.1.1', sha256='1febd22afe1489b13c6749ea059d392c03261b2950d1d45c17e3aed812080c93')
    version('3.1.0', sha256='1e0213f87cc0076f7b0c4c251d7e23601e2419cd98691df79edb95517ba06f0c')
    version('3.0.2', sha256='c94b792af431f6adb6859eb218137acd9a35f4f7442cea57e4a59c54751c36af')
    version('3.0.0', sha256='b4e2333c98a7c2c1ff6eb930cd2b57d4b818de5437c5048802096b32f66e65f9')
    version('2.2.5', sha256='a3037a840cd9dfdc2df9fee8af8f76ca82bfab173c0f9468193ca7a89a2b60ea')
    version('2.2.4', sha256='029620799e581802961ac1dcff5cb5d3ee2f602e0db9c0f202a90495b37d2126')
    version('2.2.3', sha256='7355bf757ecacd5f0ac9dd9523c8e1a1103faadf8d33c22664178e17533f8ce5')
    version('2.2.2', sha256='4dc7ef528aad21f22be85e95725234c5178c0f938e2228ca76640e5e84d8cde8')
    version('2.0.2', sha256='0ffbc44faa34a8b1704bc108c451ecf87988f900ef7ce757b8e2e84383121ff1')
    version('2.0.0', sha256='36cf0985829c1ab2b8b1dae5e2272e53ae681bf33ab8bedceed4f0565af5f813')

    # https://matplotlib.org/tutorials/introductory/usage.html#backends
    # From `lib/matplotlib/rcsetup.py`:
    interactive_bk = [
        'gtk3agg', 'gtk3cairo', 'macosx', 'nbagg', 'qt4agg', 'qt4cairo',
        'qt5agg', 'qt5cairo', 'tkagg', 'tkcairo', 'webagg', 'wx', 'wxagg',
        'wxcairo'
    ]
    non_interactive_bk = [
        'agg', 'cairo', 'pdf', 'pgf', 'ps', 'svg', 'template'
    ]
    all_backends = interactive_bk + non_interactive_bk

    default_backend = 'agg'
    if sys.platform == 'darwin':
        default_backend = 'macosx'

    variant('backend', default=default_backend,
            description='Default backend. All backends are installed and ' +
            'functional as long as dependencies are found at run-time',
            values=all_backends, multi=False)
    variant('movies', default=False,
            description='Enable support for saving movies')
    variant('animation', default=False,
            description='Enable animation support')
    variant('image', default=True,
            description='Enable reading/saving JPEG, BMP and TIFF files')
    variant('latex', default=False,
            description='Enable LaTeX text rendering support')
    variant('fonts', default=False,
            description='Enable support for system font detection')

    # https://matplotlib.org/stable/devel/dependencies.html
    # Required dependencies
    extends('python', ignore=r'bin/nosetests.*$|bin/pbr$')
    depends_on('python@2.7:2.8,3.4:', when='@:2', type=('build', 'link', 'run'))
    depends_on('python@3.5:', when='@3:', type=('build', 'link', 'run'))
    depends_on('python@3.6:', when='@3.1:', type=('build', 'link', 'run'))
    depends_on('python@3.7:', when='@3.4:', type=('build', 'link', 'run'))
    depends_on('freetype@2.3:')  # freetype 2.6.1 needed for tests to pass
    depends_on('qhull@2020.2:', when='@3.4:')
    # starting from qhull 2020.2 libqhull.so on which py-matplotlib@3.3 versions
    # rely on does not exist anymore, only libqhull_r.so
    depends_on('qhull@2015.2:2020.1', when='@3.3.0:3.3')
    depends_on('libpng@1.2:')
    depends_on('py-setuptools', type=('build', 'run'))  # See #3813
    depends_on('py-certifi@2020.6.20:', when='@3.3.1:', type='build')
    depends_on('py-setuptools-scm@4:', when='@3.5:', type='build')
    depends_on('py-setuptools-scm-git-archive', when='@3.5:', type='build')
    depends_on('py-cycler@0.10:', type=('build', 'run'))
    depends_on('py-fonttools@4.22:', when='@3.5:', type=('build', 'run'))
    depends_on('py-kiwisolver@1.0.1:', type=('build', 'run'), when='@2.2.0:')
    depends_on('py-numpy@1.11:', type=('build', 'run'))
    depends_on('py-numpy@1.15:', when='@3.3:', type=('build', 'run'))
    depends_on('py-numpy@1.16:', when='@3.4:', type=('build', 'run'))
    depends_on('py-numpy@1.17:', when='@3.5:', type=('build', 'run'))
    depends_on('py-packaging', when='@3.5:', type=('build', 'run'))
    depends_on('pil@6.2:', when='@3.3:', type=('build', 'run'))
    depends_on('py-pyparsing@2.0.3,2.0.5:2.1.1,2.1.3:2.1.5,2.1.7:', type=('build', 'run'))
    depends_on('py-pyparsing@2.2.1:', when='@3.4:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.1:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.7:', when='@3.4:', type=('build', 'run'))
    depends_on('py-pytz', type=('build', 'run'), when='@:2')
    depends_on('py-subprocess32', type=('build', 'run'), when='^python@:2.7')
    depends_on('py-functools32', type=('build', 'run'), when='@:2.0 ^python@:2.7')
    depends_on('py-backports-functools-lru-cache', type=('build', 'run'),
               when='@2.1.0:2 ^python@:2')
    depends_on('py-six@1.10.0:', type=('build', 'run'), when='@2.0:2')
    depends_on('py-six@1.9.0:',  type=('build', 'run'), when='@:1')

    # Optional backend dependencies
    depends_on('tk@8.3:8.5,8.6.2:', when='backend=tkagg', type='run')
    depends_on('tk@8.3:8.5,8.6.2:', when='backend=tkcairo', type='run')
    depends_on('python+tkinter', when='backend=tkagg', type='run')
    depends_on('python+tkinter', when='backend=tkcairo', type='run')
    depends_on('py-pyqt4@4.6:', when='backend=qt4agg', type='run')    # or py-pyside@1.0.3:
    depends_on('py-pyqt4@4.6:', when='backend=qt4cairo', type='run')  # or py-pyside@1.0.3:
    depends_on('py-pyqt5', when='backend=qt5agg', type='run')
    depends_on('py-pyqt5', when='backend=qt5cairo', type='run')
    depends_on('py-pygobject', when='backend=gtk3agg', type='run')
    depends_on('py-pygobject', when='backend=gtk3cairo', type='run')
    depends_on('py-wxpython@4:', when='backend=wx', type='run')
    depends_on('py-wxpython@4:', when='backend=wxagg', type='run')
    depends_on('py-wxpython@4:', when='backend=wxcairo', type='run')
    depends_on('py-cairocffi@0.8:', when='backend=gtk3cairo', type='run')
    depends_on('py-cairocffi@0.8:', when='backend=qt4cairo', type='run')
    depends_on('py-cairocffi@0.8:', when='backend=qt5cairo', type='run')
    depends_on('py-cairocffi@0.8:', when='backend=tkcairo', type='run')
    depends_on('py-cairocffi@0.8:', when='backend=wxcairo', type='run')
    depends_on('py-cairocffi@0.8:', when='backend=cairo', type='run')
    depends_on('py-tornado', when='backend=webagg', type='run')

    # Optional dependencies
    depends_on('ffmpeg', when='+movies')
    depends_on('imagemagick', when='+animation')
    depends_on('pil@3.4:', when='+image', type=('build', 'run'))
    depends_on('texlive', when='+latex', type='run')
    depends_on('ghostscript@9.0:', when='+latex', type='run')
    depends_on('fontconfig@2.7:', when='+fonts')
    depends_on('pkgconfig', type='build')

    # Testing dependencies
    # https://matplotlib.org/stable/devel/development_setup.html#additional-dependencies-for-testing
    depends_on('py-pytest@3.6:', type='test')
    depends_on('ghostscript@9.0:', type='test')
    # depends_on('inkscape@:0', type='test')

    msg = 'MacOSX backend requires the Cocoa headers included with XCode'
    conflicts('platform=linux', when='backend=macosx', msg=msg)
    conflicts('platform=cray',  when='backend=macosx', msg=msg)

    conflicts('~image', when='@3.3:', msg='Pillow is no longer an optional dependency')

    # https://github.com/matplotlib/matplotlib/pull/21662
    patch('matplotlibrc.patch', when='@3.5.0')
    # Patch to pick up correct freetype headers
    patch('freetype-include-path.patch', when='@2.2.2:2.9.9')

    @property
    def config_file(self):
        # https://github.com/matplotlib/matplotlib/pull/20871
        return 'mplsetup.cfg' if self.spec.satisfies('@3.5:') else 'setup.cfg'

    @property
    def archive_files(self):
        return [os.path.join(self.build_directory, self.config_file)]

    def setup_build_environment(self, env):
        include = []
        library = []
        for dep in self.spec.dependencies(deptype='link'):
            query = self.spec[dep.name]
            include.extend(query.headers.directories)
            library.extend(query.libs.directories)

        # Build uses a mix of Spack's compiler wrapper and the actual compiler,
        # so this is needed to get parts of the build working.
        # See https://github.com/spack/spack/issues/19843
        env.set('CPATH', ':'.join(include))
        env.set('LIBRARY_PATH', ':'.join(library))

    @run_before('install')
    def configure(self):
        """Set build options with regards to backend GUI libraries."""

        backend = self.spec.variants['backend'].value

        with open(self.config_file, 'w') as config:
            # Default backend
            config.write('[rc_options]\n')
            config.write('backend = ' + backend + '\n')

            # Starting with version 3.3.0, freetype is downloaded by default
            # Force matplotlib to use Spack installations of freetype and qhull
            if self.spec.satisfies('@3.3:'):
                config.write('[libs]\n')
                config.write('system_freetype = True\n')
                config.write('system_qhull = True\n')
                # avoids error where link time opt is used for compile but not link
                if self.spec.satisfies('%clang') or self.spec.satisfies('%oneapi'):
                    config.write('enable_lto = False\n')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def build_test(self):
        pytest = which('pytest')
        pytest()
