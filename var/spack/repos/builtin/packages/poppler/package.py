# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Poppler(CMakePackage):
    """Poppler is a PDF rendering library based on the xpdf-3.0 code base."""

    homepage = "https://poppler.freedesktop.org"
    url      = "https://poppler.freedesktop.org/poppler-0.72.0.tar.xz"
    list_url = "https://poppler.freedesktop.org/releases.html"

    version('0.72.0', sha256='c1747eb8f26e9e753c4001ed951db2896edc1021b6d0f547a0bd2a27c30ada51')
    version('0.65.0', 'b9a0af02e43deb26265f130343e90d78')
    version('0.64.0', 'f7f687ebb60004f8ad61994575018044')

    variant('cms',      default=False, description='Use color management system')
    variant('glib',     default=False, description='Compile poppler glib wrapper')
    variant('gobject',  default=False, description='Generate GObject introspection')
    variant('libcurl',  default=False, description='Build libcurl based HTTP support')
    variant('openjpeg', default=False, description='Use libopenjpeg for JPX streams')
    variant('qt5',      default=False, description='Compile poppler qt5 wrapper')
    variant('zlib',     default=False, description='Build with zlib')
    variant('cairo',    default=False, description='Search for Cairo package')
    variant('iconv',    default=False, description='Search for Iconv package')
    variant('jpeg',     default=False, description='Search for JPEG package')
    variant('png',      default=False, description='Search for PNG package')
    variant('tiff',     default=False, description='Search for TIFF package')

    depends_on('cmake@3.1.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('poppler-data', type=('build', 'run'))
    depends_on('fontconfig')
    depends_on('freetype')

    depends_on('lcms', when='+cms')
    depends_on('glib', when='+glib')
    depends_on('gobject-introspection', when='+gobject')
    depends_on('curl', when='+libcurl')
    depends_on('openjpeg', when='+openjpeg')
    depends_on('qt@5.0:5.999', when='+qt5')
    depends_on('zlib', when='+zlib')
    depends_on('cairo', when='+cairo')
    depends_on('libiconv', when='+iconv')
    depends_on('jpeg', when='+jpeg')
    depends_on('libpng', when='+png')
    depends_on('libtiff', when='+tiff')

    # Only needed to run `make test`
    resource(
        name='test',
        git='https://anongit.freedesktop.org/git/poppler/test.git',
        placement='testdata'
    )

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DTESTDATADIR={0}'.format(
                join_path(self.stage.source_path, 'testdata')),
            # TODO: Add packages for these missing dependencies
            '-DENABLE_SPLASH=OFF',
            '-DWITH_NSS3=OFF',
        ]

        if '+cms' in spec:
            args.append('-DENABLE_CMS=lcms2')
        else:
            args.append('-DENABLE_CMS=none')

        if '+glib' in spec:
            args.append('-DENABLE_GLIB=ON')
        else:
            args.append('-DENABLE_GLIB=OFF')

        if '+gobject' in spec:
            args.append('-DENABLE_GOBJECT_INTROSPECTION=ON')
        else:
            args.append('-DENABLE_GOBJECT_INTROSPECTION=OFF')

        if '+libcurl' in spec:
            args.append('-DENABLE_LIBCURL=ON')
        else:
            args.append('-DENABLE_LIBCURL=OFF')

        if '+openjpeg' in spec:
            args.append('-DENABLE_LIBOPENJPEG=openjpeg2')
        else:
            args.append('-DENABLE_LIBOPENJPEG=none')

        if '+qt5' in spec:
            args.append('-DENABLE_QT5=ON')
        else:
            args.append('-DENABLE_QT5=OFF')

        if '+zlib' in spec:
            args.append('-DENABLE_ZLIB=ON')
        else:
            args.append('-DENABLE_ZLIB=OFF')

        if '+cairo' in spec:
            args.append('-DWITH_Cairo=ON')
        else:
            args.append('-DWITH_Cairo=OFF')

        if '+iconv' in spec:
            args.append('-DWITH_Iconv=ON')
        else:
            args.append('-DWITH_Iconv=OFF')

        if '+jpeg' in spec:
            args.extend([
                '-DENABLE_DCTDECODER=libjpeg',
                '-DWITH_JPEG=ON'
            ])
        else:
            args.extend([
                '-DENABLE_DCTDECODER=none',
                '-DWITH_JPEG=OFF'
            ])

        if '+png' in spec:
            args.append('-DWITH_PNG=ON')
        else:
            args.append('-DWITH_PNG=OFF')

        if '+tiff' in spec:
            args.append('-DWITH_TIFF=ON')
        else:
            args.append('-DWITH_TIFF=OFF')

        return args
