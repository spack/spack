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
import sys


class PyPillow(PythonPackage):
    """Pillow is a fork of the Python Imaging Library (PIL). It adds image
    processing capabilities to your Python interpreter. This library supports
    many file formats, and provides powerful image processing and graphics
    capabilities."""

    homepage = "https://python-pillow.org/"
    url = "https://pypi.python.org/packages/source/P/Pillow/Pillow-3.0.0.tar.gz"

    # TODO: This version should be deleted once the next release comes out.
    # TODO: It fixes a bug that prevented us from linking to Tk/Tcl.
    # TODO: Tk/Tcl support is necessary for tkinter bitmap and photo images.
    # TODO: If you require this support, run the following command:
    # TODO:     `spack install py-pillow@3.3.0.dev0 ^python+tk`
    version('3.3.0.dev0', git='https://github.com/python-pillow/Pillow.git',
            commit='30eced62868141a6c859a4370efd40b9434a7c3f')

    version('3.2.0', '7cfd093c11205d9e2ebe3c51dfcad510', preferred=True)
    version('3.0.0', 'fc8ac44e93da09678eac7e30c9b7377d')

    provides('pil')

    # These defaults correspond to Pillow defaults
    variant('jpeg', default=True, description='Provide JPEG functionality')
    variant('zlib', default=True, description='Access to compressed PNGs')
    variant('tiff', default=False, description='Access to TIFF files')
    variant('freetype', default=False, description='Font related services')
    variant('lcms', default=False, description='Color management')
    variant('jpeg2000', default=False,
            description='Provide JPEG 2000 functionality')

    # Spack does not (yet) support these modes of building
    # variant('webp', default=False, description='Provide the WebP format')
    # variant('webpmux', default=False,
    #         description='WebP metadata, relies on WebP support')
    # variant('imagequant', default=False,
    #         description='Provide improved color quantization')

    # Required dependencies
    depends_on('binutils', type='build', when=sys.platform != 'darwin')
    depends_on('py-setuptools', type='build')

    # Recommended dependencies
    depends_on('jpeg', when='+jpeg')
    depends_on('zlib', when='+zlib')

    # Optional dependencies
    depends_on('libtiff', when='+tiff')
    depends_on('freetype', when='+freetype')
    depends_on('lcms', when='+lcms')
    depends_on('openjpeg', when='+jpeg2000')

    # Spack does not (yet) support these modes of building
    # depends_on('webp', when='+webp')
    # depends_on('webpmux', when='+webpmux')
    # depends_on('imagequant', when='+imagequant')

    phases = ['build_ext', 'install']

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
        if '+jpeg2000' in spec:
            setup.filter('JPEG2K_ROOT = None',
                         'JPEG2K_ROOT = ("{0}", "{1}")'.format(
                             spec['openjpeg'].prefix.lib,
                             spec['openjpeg'].prefix.include))

    def build_ext_args(self, spec, prefix):
        def variant_to_flag(variant):
            able = 'enable' if '+{0}'.format(variant) in spec else 'disable'
            return '--{0}-{1}'.format(able, variant)

        variants = ['jpeg', 'zlib', 'tiff', 'freetype', 'lcms', 'jpeg2000']
        return list(map(variant_to_flag, variants))
