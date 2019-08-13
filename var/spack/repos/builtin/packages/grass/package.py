# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Grass(AutotoolsPackage):
    """GRASS GIS (Geographic Resources Analysis Support System), is a free
       and open source Geographic Information System (GIS) software suite
       used for geospatial data management and analysis, image processing,
       graphics and maps production, spatial modeling, and visualization."""

    homepage = "http://grass.osgeo.org"

    version('7.6.1',    '9ca74f9010d013f735737a90c65d8a7f')
    version('7.4.4',    '98ae22f8a97a83a4d99a537236639e9c')
    version('7.4.3',    '4f4462af7a95fe84ee21f3dd585dcb05')
    version('7.4.2',    'bb3fc005e707f762c8fee36095e1df7f')
    version('7.4.1',    'bf7add62cbeb05a3ed5ad832344ba524')
    version('7.4.0',    '15b9eb019d6c132c1a65455b3283cf69')

    variant('cxx',       default=True,  description='Add c++ functionality')
    variant('tiff',      default=True,  description='Add TIFF functionality')
    variant('png',       default=True,  description='Add PNG functionality')
    variant('postgres',  default=False, description='Add PostgreSQL functionality')
    variant('mysql',     default=False, description='Add MySQL functionality')
    variant('sqlite',    default=True,  description='Add SQLite functionality')
    variant('opengl',    default=True,  description='Add OpenGL functionality')
    variant('fftw',      default=True,  description='Add FFTW functionality')
    variant('blas',      default=False, description='Add BLAS functionality')
    variant('lapack',    default=False, description='Add LAPACK functionality')
    variant('cairo',     default=True,  description='Add Cairo functionality')
    variant('freetype',  default=True,  description='Add FreeType functionality')
    variant('readline',  default=False, description='Add Readline functionality')
    variant('regex',     default=True,  description='Add regex functionality')
    variant('pthread',   default=False, description='Add POSIX threads functionality')
    variant('openmp',    default=False, description='Add OpenMP functionality')
    variant('opencl',    default=False, description='Add OpenCL functionality')
    variant('bzlib',     default=False, description='Add BZIP2 functionality')
    variant('netcdf',    default=False, description='Enable NetCDF support')
    variant('geos',      default=False, description='Geometry Engine for v.buffer')

    # required components
    depends_on('gmake@3.8.1:', type='build')
    depends_on('zlib')
    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('proj')
    depends_on('proj@:4', when='@:7.5')
    depends_on('proj@:5', when='@:7.7')
    depends_on('gdal')
    depends_on('python@2.7:2.9', type=('build', 'run'))
    depends_on('libx11')

    # optional pieces
    depends_on('libtiff', when='+tiff')
    depends_on('libpng', when='+png')
    depends_on('postgresql', when='+postgres')
    depends_on('mariadb', when='+mysql')
    depends_on('sqlite', when='+sqlite')
    depends_on('gl', when='+opengl')
    depends_on('fftw', when='+fftw')
    depends_on('blas', when='+blas')
    depends_on('lapack', when='+lapack')
    depends_on('cairo', when='+cairo')
    depends_on('freetype', when='+freetype')
    depends_on('readline', when='+readline')
    depends_on('opencl', when='+opencl')
    depends_on('bzip2', when='+bzlib')
    depends_on('netcdf', when='+netcdf')
    depends_on('geos', when='+geos')

    def url_for_version(self, version):
        base = 'https://grass.osgeo.org'
        return '{0}/grass{1}/source/grass-{2}.tar.gz'.format(
            base, version.up_to(2).joined, version.dotted
        )

    def configure_args(self):
        spec = self.spec

        args = [
            '--without-odbc',
            '--without-nls',
            '--without-opendwg',
            '--with-x',
            '--with-gdal={0}/bin/gdal-config'.format(
                spec['gdal'].prefix),
            '--with-proj-share={0}/share/proj'.format(
                spec['proj'].prefix),
        ]

        if '+cxx' in spec:
            args.append('--with-cxx')
        else:
            args.append('--without-cxx')

        if '+tiff' in spec:
            args.append('--with-tiff')
        else:
            args.append('--without-tiff')

        if '+png' in spec:
            args.append('--with-png')
        else:
            args.append('--without-png')

        if '+postgres' in spec:
            args.append('--with-postgres')
        else:
            args.append('--without-postgres')

        if '+mysql' in spec:
            args.append('--with-mysql')
        else:
            args.append('--without-mysql')

        if '+sqlite' in spec:
            args.append('--with-sqlite')
        else:
            args.append('--without-sqlite')

        if '+opengl' in spec:
            args.append('--with-opengl')
        else:
            args.append('--without-opengl')

        if '+fftw' in spec:
            args.append('--with-fftw')
        else:
            args.append('--without-fftw')

        if '+blas' in spec:
            args.append('--with-blas')
        else:
            args.append('--without-blas')

        if '+lapack' in spec:
            args.append('--with-lapack')
        else:
            args.append('--without-lapack')

        if '+cairo' in spec:
            args.append('--with-cairo')
        else:
            args.append('--without-cairo')

        if '+freetype' in spec:
            args.append('--with-freetype')
        else:
            args.append('--without-freetype')

        if '+readline' in spec:
            args.append('--with-readline')
        else:
            args.append('--without-readline')

        if '+regex' in spec:
            args.append('--with-regex')
        else:
            args.append('--without-regex')

        if '+pthread' in spec:
            args.append('--with-pthread')
        else:
            args.append('--without-pthread')

        if '+openmp' in spec:
            args.append('--with-openmp')
        else:
            args.append('--without-openmp')

        if '+opencl' in spec:
            args.append('--with-opencl')
        else:
            args.append('--without-opencl')

        if '+bzlib' in spec:
            args.append('--with-bzlib')
        else:
            args.append('--without-bzlib')

        if '+netcdf' in spec:
            args.append('--with-netcdf={0}/bin/nc-config'.format(
                spec['netcdf'].prefix))
        else:
            args.append('--without-netcdf')

        if '+geos' in spec:
            args.append('--with-geos={0}/bin/geos-config'.format(
                spec['geos'].prefix))
        else:
            args.append('--without-geos')

        return args

    # see issue: https://github.com/spack/spack/issues/11325
    # 'Platform.make' is created after configure step
    # hence invoke the following function afterwards
    @run_after('configure')
    def fix_iconv_linking(self):
        makefile = FileFilter('include/Make/Platform.make')
        makefile.filter(r'^ICONVLIB\s*=\s*', 'ICONVLIB = -liconv')
        return None
