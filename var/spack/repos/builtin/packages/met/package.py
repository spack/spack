# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Met(AutotoolsPackage):
    """
    Statistical tool that matches up grids with either gridded analyses or point observations and applies configurable methods to compute statistics and diagnostics
    """

    homepage = "https://dtcenter.org/community-code/model-evaluation-tools-met"
    url      = "https://github.com/dtcenter/MET/releases/download/v10.1.0/met-10.1.0.20220314.tar.gz"

    maintainers = ['kgerheiser']

    version('10.1.0', sha256='8d4c1fb2311d8481ffd24e30e407a1b1bc72a6add9658d76b9c323f1733db336')
    version('10.0.1', sha256='8e965bb0eb8353229a730af511c5fa62bad9744606ab6a218d741d29eb5f3acd')
    version('10.0.0', sha256='92f37c8bd83c951d86026cce294a16e4d3aa6dd41905629d0a729fa1bebe668a')
    version('9.1.3', sha256='7356a5ad79ca961fd965cadd93a7bf6c73b3aa5fb1a01a932580b94e66d0d0c8')    

    variant('openmp', default=True, description='Use OpenMP multithreading')
    variant('grib2', default=False,
            description='Enable compilation of utilities using GRIB2')
    variant('python', default=False, description='Enable python embedding')
    variant('lidar2nc', default=False,
            description='Enable compilation of lidar2nc')
    variant('modis', default=False, description='Enable compilation of modis')
    variant('graphics', default=False,
            description='Enable compilation of mode_graphics')
    
    depends_on('gsl')
    depends_on('bufr')
    depends_on('zlib')
    depends_on('netcdf-c')
    depends_on('netcdf-cxx4')
    depends_on('g2c', when='+grib2')

    depends_on('hdf-eos2', when='+modis')
    depends_on('hdf-eos2', when='+lidar2nc')
    depends_on('hdf', when='+modis')
    depends_on('hdf', when='+lidar2nc')

    depends_on('cairo', when='+graphics')
    depends_on('freetype', when='+graphics')

    depends_on('python@3.6.3:', when='+python', type=('build', 'run'))
    depends_on('py-netcdf4', when='+python', type=('run'))
    depends_on('py-numpy', when='+python', type=('run'))
    depends_on('py-xarray', when='+python', type=('run'))
    depends_on('py-pandas', when='+python', type=('run'))
    depends_on('py-cartopy', when='+python', type=('run'))
    depends_on('py-matplotlib', when='+python', type=('run'))
    depends_on('py-python-dateutil', when='+python', type=('run'))
    
    patch('openmp_shape_patch.patch', when='@10.1.0')

    def url_for_version(self, version):
        release_date = {
            '10.1.0': '20220314',
            '10.0.1': '20211201',
            '10.0.0': '20210510',
            '9.1.3':  '20210319'
        }
        url = "https://github.com/dtcenter/MET/releases/download/v{0}/met-{0}.{1}.tar.gz"
        return url.format(version, release_date[str(version)])

    def setup_build_environment(self, env):
        spec = self.spec
        cppflags = []
        ldflags = []
        libs = []

        gsl = spec['gsl']
        env.set('MET_GSL', gsl.prefix)

        netcdfc = spec['netcdf-c']
        netcdfcxx = spec['netcdf-cxx4']
        zlib = spec['zlib']

        cppflags.append('-I' + netcdfc.prefix.include)
        cppflags.append('-I' + netcdfcxx.prefix.include)
        cppflags.append('-D__64BIT__')

        ldflags.append('-L' + netcdfc.prefix.lib)
        ldflags.append('-L' + netcdfcxx.prefix.lib)
        ldflags.append('-L' + zlib.prefix.lib)

        libs.append('-lnetcdf')
        libs.append('-lnetcdf_c++4')
        libs.append('-lz')

        bufr = spec['bufr']
        bufr_libdir = find_libraries('libbufr_4', root=bufr.prefix, 
            shared=False, recursive=True).directories[0]
        env.set('BUFRLIB_NAME', '-lbufr_4')
        env.set('MET_BUFRLIB', bufr_libdir)
        
        if '+grib2' in spec:
            g2c = spec['g2c']
            g2c_libdir = find_libraries('libg2c', root=g2c.prefix,
                                        shared=False, recursive=True).directories[0]
            env.set('MET_GRIB2CLIB', g2c_libdir)
            env.set('GRIB2CLIB_NAME', '-lg2c')

        if '+python' in spec:
            python = spec['python']
            env.set('MET_PYTHON', python.command.path)
            env.set('MET_PYTHON_CC', '-I' + python.headers.directories[0])
            env.set('MET_PYTHON_LD', python.libs.ld_flags)

        if '+lidar2nc' in spec or '+modis' in spec:
            hdf = spec['hdf']
            hdfeos = spec['hdf-eos2']
            env.set('MET_HDF5', hdf.prefix)
            env.set('MET_HDFEOS', hdfeos.prefix)

        if '+graphics' in spec:
            cairo = spec['cairo']
            freetype = spec['freetype']
            env.set('MET_CAIRO', cairo.prefix)
            cppflags.append('-I' + cairo.prefix.include.cairo)
            env.set('MET_FREETYPE', freetype.prefix)

        env.set('CPPFLAGS', ' '.join(cppflags))
        env.set('LIBS', ' '.join(libs))
        env.set('LDFLAGS', ' '.join(ldflags))

    def configure_args(self):
        args = []
        spec = self.spec

        if '+grib2' in spec:
            args.append('--enable-grib2')

        if '+python' in spec:
            args.append('--enable-python')

        if '~openmp' in spec:
            args.append('--disable-openmp')

        if '+lidar2nc' in spec:
            args.append('--enable-lidar2nc')

        if '+modis' in spec:
            args.append('--enable-modis')
        
        if '+graphics' in spec:
            args.append('--enable-mode_graphics')

        return args

    def setup_run_environment(self, env):
        env.set('MET_BASE', self.prefix)
