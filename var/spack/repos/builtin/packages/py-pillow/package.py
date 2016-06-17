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


class PyPillow(Package):
    """Pillow is a fork of the Python Imaging Library (PIL). It adds image
    processing capabilities to your Python interpreter. This library supports
    many file formats, and provides powerful image processing and graphics
    capabilities."""

    homepage = "https://python-pillow.org/"
    url      = "https://pypi.python.org/packages/source/P/Pillow/Pillow-3.0.0.tar.gz"

    version('3.2.0', '7cfd093c11205d9e2ebe3c51dfcad510')
    version('3.0.0', 'fc8ac44e93da09678eac7e30c9b7377d')

    # These defaults correspond to Pillow defaults
    variant('jpeg',     default=True,  description='Provide JPEG functionality')
    variant('zlib',     default=True,  description='Access to compressed PNGs')
    variant('tiff',     default=False, description='Access to TIFF files')
    variant('freetype', default=False, description='Font related services')
    variant('lcms',     default=False, description='Color management')
    variant('tk',       default=False, description='Support for tkinter bitmap and photo images')
    variant('jpeg2000', default=False, description='Provide JPEG 2000 functionality')

    # Spack does not (yet) support these modes of building
    # variant('webp',       default=False, description='Provide the WebP format')
    # variant('webpmux',    default=False, description='WebP metadata, relies on WebP support')
    # variant('imagequant', default=False, description='Provide improved color quantization')

    provides('PIL')

    # Required dependencies
    extends('python')
    depends_on('py-setuptools')

    # Recommended dependencies
    depends_on('jpeg', when='+jpeg')
    depends_on('zlib', when='+zlib')

    # Optional dependencies
    depends_on('libtiff',  when='+tiff')
    depends_on('freetype', when='+freetype')
    depends_on('lcms',     when='+lcms')
    depends_on('tcl',      when='+tk')
    depends_on('tk',       when='+tk')
    depends_on('openjpeg', when='+jpeg2000')

    # Spack does not (yet) support these modes of building
    # depends_on('webp',       when='+webp')
    # depends_on('webpmux',    when='+webpmux')
    # depends_on('imagequant', when='+imagequant')

    def patch(self):
        """Patch setup.py to provide lib and include directories
        for dependencies."""

        spec = self.spec
        setup = FileFilter('setup.py')

        if '+jpeg' in spec:
            setup.filter('JPEG_ROOT = None',
                         'JPEG_ROOT = ("{0}", "{1}")'.format(
                            spec['jpeg'].prefix.lib,
                            spec['jpeg'].prefix.include))
        if '+zlib' in spec:
            setup.filter('ZLIB_ROOT = None',
                         'ZLIB_ROOT = ("{0}", "{1}")'.format(
                            spec['zlib'].prefix.lib,
                            spec['zlib'].prefix.include))
        if '+tiff' in spec:
            setup.filter('TIFF_ROOT = None',
                         'TIFF_ROOT = ("{0}", "{1}")'.format(
                            spec['libtiff'].prefix.lib,
                            spec['libtiff'].prefix.include))
        if '+freetype' in spec:
            setup.filter('FREETYPE_ROOT = None',
                         'FREETYPE_ROOT = ("{0}", "{1}")'.format(
                            spec['freetype'].prefix.lib,
                            spec['freetype'].prefix.include))
        if '+lcms' in spec:
            setup.filter('LCMS_ROOT = None',
                         'LCMS_ROOT = ("{0}", "{1}")'.format(
                            spec['lcms'].prefix.lib,
                            spec['lcms'].prefix.include))
        if '+tk' in spec:
            setup.filter('TCL_ROOT = None',
                         'TCL_ROOT = ("{0}", "{1}")'.format(
                            spec['tcl'].prefix.lib,
                            spec['tcl'].prefix.include))
        if '+jpeg2000' in spec:
            setup.filter('JPEG2K_ROOT = None',
                         'JPEG2K_ROOT = ("{0}", "{1}")'.format(
                            spec['openjpeg'].prefix.lib,
                            spec['openjpeg'].prefix.include))

    def install(self, spec, prefix):
        build_args = [
            '--{0}-jpeg'.format('enable' if '+jpeg' in spec else 'disable'),
            '--{0}-zlib'.format('enable' if '+zlib' in spec else 'disable'),
            '--{0}-tiff'.format('enable' if '+tiff' in spec else 'disable'),
            '--{0}-freetype'.format(
                'enable' if '+freetype' in spec else 'disable'),
            '--{0}-lcms'.format('enable' if '+lcms' in spec else 'disable'),
            '--{0}-tk'.format('enable' if '+tk' in spec else 'disable'),
            '--{0}-tcl'.format('enable' if '+tk' in spec else 'disable'),
            '--{0}-jpeg2000'.format(
                'enable' if '+jpeg2000' in spec else 'disable')
        ]

        python('setup.py', 'build_ext', *build_args)
        python('setup.py', 'install', '--prefix={0}'.format(prefix))
