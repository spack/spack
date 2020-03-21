# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class PyMatplotlib(PythonPackage):
    """Matplotlib is a comprehensive library for creating static, animated,
    and interactive visualizations in Python."""

    homepage = "https://matplotlib.org/"
    url      = "https://pypi.io/packages/source/m/matplotlib/matplotlib-3.2.1.tar.gz"

    maintainers = ['adamjstewart']

    import_modules = [
        'mpl_toolkits', 'matplotlib', 'mpl_toolkits.axes_grid1',
        'mpl_toolkits.axes_grid', 'mpl_toolkits.mplot3d',
        'mpl_toolkits.axisartist', 'matplotlib.compat', 'matplotlib.tri',
        'matplotlib.axes', 'matplotlib.sphinxext', 'matplotlib.cbook',
        'matplotlib.backends', 'matplotlib.style', 'matplotlib.projections',
        'matplotlib.testing', 'matplotlib.backends.qt_editor',
        'matplotlib.testing.jpl_units'
    ]

    version('3.2.1', sha256='ffe2f9cdcea1086fc414e82f42271ecf1976700b8edd16ca9d376189c6d93aee')
    version('3.2.0', sha256='651d76daf9168250370d4befb09f79875daa2224a9096d97dfc3ed764c842be4')
    version('3.1.3', sha256='db3121f12fb9b99f105d1413aebaeb3d943f269f3d262b45586d12765866f0c6')
    version('3.1.2', sha256='8e8e2c2fe3d873108735c6ee9884e6f36f467df4a143136209cff303b183bada')
    version('3.1.1', sha256='1febd22afe1489b13c6749ea059d392c03261b2950d1d45c17e3aed812080c93')
    version('3.0.2', sha256='c94b792af431f6adb6859eb218137acd9a35f4f7442cea57e4a59c54751c36af')
    version('3.0.0', sha256='b4e2333c98a7c2c1ff6eb930cd2b57d4b818de5437c5048802096b32f66e65f9')
    version('2.2.5', sha256='a3037a840cd9dfdc2df9fee8af8f76ca82bfab173c0f9468193ca7a89a2b60ea')
    version('2.2.4', sha256='029620799e581802961ac1dcff5cb5d3ee2f602e0db9c0f202a90495b37d2126')
    version('2.2.3', sha256='7355bf757ecacd5f0ac9dd9523c8e1a1103faadf8d33c22664178e17533f8ce5')
    version('2.2.2', sha256='4dc7ef528aad21f22be85e95725234c5178c0f938e2228ca76640e5e84d8cde8')
    version('2.0.2', sha256='0ffbc44faa34a8b1704bc108c451ecf87988f900ef7ce757b8e2e84383121ff1')
    version('2.0.0', sha256='36cf0985829c1ab2b8b1dae5e2272e53ae681bf33ab8bedceed4f0565af5f813')
    version('1.5.3', sha256='a0a5dc39f785014f2088fed2c6d2d129f0444f71afbb9c44f7bdf1b14d86ebbc')
    version('1.5.1', sha256='3ab8d968eac602145642d0db63dd8d67c85e9a5444ce0e2ecb2a8fedc7224d40')
    version('1.4.3', sha256='61f201c6a82e89e4d9e324266203fad44f95fd8f36d8eec0d8690273e1182f75')
    version('1.4.2', sha256='17a3c7154f152d8dfed1f37517c0a8c5db6ade4f6334f684989c36dab84ddb54')

    # https://matplotlib.org/tutorials/introductory/usage.html#backends
    # From `matplotlib.rcsetup`:
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

    variant('backend', default=default_backend, description='Default backend',
            values=all_backends, multi=False)
    variant('movies', default=False,
            description='Enable support for saving movies')
    variant('animation', default=False,
            description='Enable animation support')
    variant('image', default=True,
            description='Enable reading/saving JPEG, BMP and TIFF files')
    variant('latex', default=False,
            description='Enable LaTeX text rendering support')

    # https://matplotlib.org/users/installing.html#dependencies
    # Required dependencies
    extends('python', ignore=r'bin/nosetests.*$|bin/pbr$')
    depends_on('python@2.7:2.8,3.4:', when='@:2')
    depends_on('python@3.5:', when='@3:')
    depends_on('python@3.6:', when='@3.1:')
    depends_on('freetype@2.3:')
    depends_on('libpng@1.2:')
    depends_on('py-numpy@1.11:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))  # See #3813
    depends_on('py-cycler@0.10:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.1:', type=('build', 'run'))
    depends_on('py-kiwisolver@1.0.1:', type=('build', 'run'), when='@2.2.0:')
    depends_on('py-pyparsing@2.0.3,2.0.5:2.1.1,2.1.3:2.1.5,2.1.7:', type=('build', 'run'))
    depends_on('py-pytz', type=('build', 'run'), when='@:2')
    depends_on('py-subprocess32', type=('build', 'run'), when='^python@:2.7')
    depends_on('py-functools32', type=('build', 'run'), when='@:2.0.999 ^python@2.7')
    depends_on('py-backports-functools-lru-cache', type=('build', 'run'),
               when='@2.1.0:2.999.999 ^python@:2')
    depends_on('py-six@1.10.0:', type=('build', 'run'), when='@2.0:2.999')
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
    # depends_on('libav', when='+movies')
    depends_on('imagemagick', when='+animation')
    depends_on('py-pillow@3.4:', when='+image', type=('build', 'run'))
    depends_on('texlive', when='+latex', type='run')
    depends_on('ghostscript@0.9:', when='+latex', type='run')
    depends_on('pkgconfig', type='build')

    # Testing dependencies
    depends_on('py-pytest', type='test')

    msg = 'MacOSX backend requires the Cocoa headers included with XCode'
    conflicts('platform=linux', when='backend=macosx', msg=msg)
    conflicts('platform=bgq',   when='backend=macosx', msg=msg)
    conflicts('platform=cray',  when='backend=macosx', msg=msg)

    # Patch to pick up correct freetype headers
    patch('freetype-include-path.patch', when='@2.2.2:2.9.9')

    @run_before('build')
    def set_backend(self):
        """Set build options with regards to backend GUI libraries."""

        backend = self.spec.variants['backend'].value

        with open('setup.cfg', 'w') as setup:
            # Default backend
            setup.write('[rc_options]\n')
            setup.write('backend = ' + backend + '\n')

    def test(self):
        pytest = which('pytest')
        pytest()
