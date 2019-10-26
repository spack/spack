# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class PyPillow(PythonPackage):
    """Pillow is a fork of the Python Imaging Library (PIL). It adds image
    processing capabilities to your Python interpreter. This library supports
    many file formats, and provides powerful image processing and graphics
    capabilities."""

    homepage = "https://python-pillow.org/"
    url = "https://pypi.io/packages/source/P/Pillow/Pillow-6.2.0.tar.gz"

    version('6.2.0', sha256='4548236844327a718ce3bb182ab32a16fa2050c61e334e959f554cac052fb0df')
    version('5.4.1', sha256='5233664eadfa342c639b9b9977190d64ad7aca4edc51a966394d7e08e7f38a9f')
    version('5.1.0', sha256='cee9bc75bff455d317b6947081df0824a8f118de2786dc3d74a3503fd631f4ef')
    version('3.2.0', sha256='64b0a057210c480aea99406c9391180cd866fc0fd8f0b53367e3af21b195784a')
    version('3.0.0', sha256='ad50bef540fe5518a4653c3820452a881b6a042cb0f8bb7657c491c6bd3654bb')

    provides('pil')

    # These defaults correspond to Pillow defaults
    variant('tiff',     default=False, description='Access to TIFF files')
    variant('freetype', default=False, description='Font related services')
    variant('lcms',     default=False, description='Color management')
    variant('jpeg2000', default=False, description='Provide JPEG 2000 functionality')

    # Spack does not (yet) support these modes of building
    # variant('webp', default=False, description='Provide the WebP format')
    # variant('webpmux', default=False,
    #         description='WebP metadata, relies on WebP support')
    # variant('imagequant', default=False,
    #         description='Provide improved color quantization')

    # Required dependencies
    depends_on('binutils', type='build', when=sys.platform != 'darwin')
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('jpeg')
    depends_on('zlib')

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

        setup.filter('JPEG_ROOT = None',
                     'JPEG_ROOT=("{0}","{1}")'.format(
                         spec['jpeg'].libs.directories[0],
                         spec['jpeg'].prefix.include))
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
        args = list(map(variant_to_flag, variants))
        args.extend(['--rpath=%s' % ":".join(self.rpath)])
        return args
