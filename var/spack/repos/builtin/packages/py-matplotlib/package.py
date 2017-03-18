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
import os


class PyMatplotlib(PythonPackage):
    """matplotlib is a python 2D plotting library which produces publication
    quality figures in a variety of hardcopy formats and interactive
    environments across platforms."""

    homepage = "https://pypi.python.org/pypi/matplotlib"
    url      = "https://pypi.io/packages/source/m/matplotlib/matplotlib-1.4.2.tar.gz"

    version('2.0.0', '7aa54b06327f0e1c4f3877fc2f7d6b17')
    version('1.5.3', 'ba993b06113040fee6628d74b80af0fd')
    version('1.5.1', 'f51847d8692cb63df64cd0bd0304fd20')
    version('1.4.3', '86af2e3e3c61849ac7576a6f5ca44267')
    version('1.4.2', '7d22efb6cce475025733c50487bd8898')

    # See: http://matplotlib.org/users/installing.html

    # Variants enabled by default for a standard configuration
    variant('tk', default=True, description='Enable Tk GUI')
    variant('image', default=True,
            description='Enable reading/saving JPEG, BMP and TIFF files')

    # Variants optionally available to user
    variant('ipython', default=False, description='Enable ipython support')
    variant('qt', default=False, description='Enable Qt GUI')
    variant('latex', default=False,
            description='Enable LaTeX text rendering support')
    variant('animation', default=False,
            description='Enable animation support')

    # Python 2.7, 3.4, or 3.5
    extends('python', ignore=r'bin/nosetests.*$|bin/pbr$')

    # ------ Required dependencies
    depends_on('py-setuptools', type='build')

    depends_on('libpng@1.2:')
    depends_on('freetype@2.3:')

    depends_on('py-numpy@1.6:', type=('build', 'run'))
    depends_on('py-dateutil@1.1:', type=('build', 'run'))
    depends_on('py-pyparsing', type=('build', 'run'))
    depends_on('py-pytz', type=('build', 'run'))
    depends_on('py-cycler@0.9:', type=('build', 'run'))

    # ------ Optional GUI frameworks
    depends_on('tk@8.3:', when='+tk')  # not 8.6.0 or 8.6.1
    depends_on('qt', when='+qt')
    depends_on('py-pyside', when='+qt', type=('build', 'run'))

    # --------- Optional external programs
    # ffmpeg/avconv or mencoder
    depends_on('image-magick', when='+animation')

    # --------- Optional dependencies
    depends_on('pkg-config', type='build')    # why not...
    depends_on('pil', when='+image', type=('build', 'run'))
    depends_on('py-ipython', when='+ipython', type=('build', 'run'))
    depends_on('ghostscript', when='+latex', type='run')
    depends_on('texlive', when='+latex', type='run')

    # Testing dependencies
    depends_on('py-nose')  # type='test'
    depends_on('py-mock')  # type='test'

    # Required libraries that ship with matplotlib
    # depends_on('agg@2.4:')
    depends_on('qhull@2012.1:')
    # depends_on('ttconv')
    depends_on('py-six@1.9.0:', type=('build', 'run'))

    @run_after('install')
    def set_backend(self):
        spec = self.spec
        prefix = self.prefix

        if '+qt' in spec or '+tk' in spec:
            # Set backend in matplotlib configuration file
            config_file = None
            for p, d, f in os.walk(prefix.lib):
                for file in f:
                    if file.find('matplotlibrc') != -1:
                        config_file = join_path(p, 'matplotlibrc')
            if not config_file:
                raise InstallError('Could not find matplotlibrc')

            kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
            rc = FileFilter(config_file)

            # Only make Qt4 be the default backend if Tk is turned off
            if '+qt' in spec and '+tk' not in spec:
                rc.filter('^backend.*', 'backend     : Qt4Agg', **kwargs)

            # Additional options in case user is doing Qt4:
            if '+qt' in spec:
                rc.filter('^#backend.qt4.*', 'backend.qt4 : PySide', **kwargs)
