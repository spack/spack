# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cdo(AutotoolsPackage):
    """CDO is a collection of command line Operators to manipulate and analyse
       Climate and NWP model Data.
    """

    homepage = 'https://code.mpimet.mpg.de/projects/cdo'
    url = 'https://code.mpimet.mpg.de/attachments/download/12760/cdo-1.7.2.tar.gz'
    list_url = 'https://code.mpimet.mpg.de/projects/cdo/files'

    maintainers = ['skosukhin']

    version('1.9.7.1', sha256='3771952e065bcf935d43e492707370ed2a0ecb59a06bea24f9ab69d77943962c',
            url='https://code.mpimet.mpg.de/attachments/download/20124/cdo-1.9.7.1.tar.gz')
    version('1.9.6', '322f56c5e13f525c585ee5318d4435db', url='https://code.mpimet.mpg.de/attachments/download/19299/cdo-1.9.6.tar.gz')
    version('1.9.5', '0c60f2c94dc5c76421ecf363153a5043', url='https://code.mpimet.mpg.de/attachments/download/18264/cdo-1.9.5.tar.gz')
    version('1.9.4', '377c9e5aa7d8cbcb4a6c558abb2eb053', url='https://code.mpimet.mpg.de/attachments/download/17374/cdo-1.9.4.tar.gz')
    version('1.9.3', '13ae222164413dbd53532b03b072def5', url='https://code.mpimet.mpg.de/attachments/download/16435/cdo-1.9.3.tar.gz')
    version('1.9.2', '38e68d34f0b5b44a52c3241be6831423', url='https://code.mpimet.mpg.de/attachments/download/16035/cdo-1.9.2.tar.gz')
    version('1.9.1', 'e60a89f268ba24cee5c461f2c217829e', url='https://code.mpimet.mpg.de/attachments/download/15653/cdo-1.9.1.tar.gz')
    version('1.9.0', '2d88561b3b4a880df0422a62e5027e40', url='https://code.mpimet.mpg.de/attachments/download/15187/cdo-1.9.0.tar.gz')
    version('1.8.2', '6a2e2f99b7c67ee9a512c40a8d4a7121', url='https://code.mpimet.mpg.de/attachments/download/14686/cdo-1.8.2.tar.gz')
    version('1.7.2', 'f08e4ce8739a4f2b63fc81a24db3ee31', url='https://code.mpimet.mpg.de/attachments/download/12760/cdo-1.7.2.tar.gz')

    variant('netcdf', default=True, description='Enable NetCDF support')
    variant('grib2', default='eccodes', values=('eccodes', 'grib-api', 'none'),
            description='Specify GRIB2 backend')
    variant('external-grib1', default=False,
            description='Ignore the built-in support and use the external '
                        'GRIB2 backend for GRIB1 files')
    variant('szip', default=True,
            description='Enable szip compression for GRIB1')
    variant('hdf5', default=True, description='Enable HDF5 support')

    variant('udunits2', default=True, description='Enable UDUNITS2 support')
    variant('libxml2', default=True, description='Enable libxml2 support')
    variant('proj', default=True,
            description='Enable PROJ library for cartographic projections')
    variant('curl', default=False, description='Enable curl support')
    variant('fftw3', default=True, description='Enable support for fftw3')
    variant('magics', default=False,
            description='Enable Magics library support')
    variant('openmp', default=True, description='Enable OpenMP support')

    depends_on('pkgconfig', type='build')

    depends_on('netcdf', when='+netcdf')
    # In this case CDO does not depend on hdf5 directly but we need the backend
    # of netcdf to be thread safe.
    depends_on('hdf5+threadsafe', when='+netcdf')

    depends_on('grib-api', when='grib2=grib-api')
    depends_on('eccodes', when='grib2=eccodes')

    depends_on('szip', when='+szip')

    depends_on('hdf5+threadsafe', when='+hdf5')

    depends_on('udunits2', when='+udunits2')
    depends_on('libxml2', when='+libxml2')
    depends_on('proj@:5', when='+proj')
    depends_on('curl', when='+curl')
    depends_on('fftw@3:', when='+fftw3')
    depends_on('magics', when='+magics')
    depends_on('libuuid')

    conflicts('grib2=eccodes', when='@:1.8',
              msg='Eccodes is supported starting version 1.9.0')
    conflicts('+szip', when='+external-grib1 grib2=none',
              msg='The configuration does not support GRIB1')
    conflicts('%gcc@9:', when='@:1.9.6',
              msg='GCC 9 changed OpenMP data sharing behavior')

    def configure_args(self):
        config_args = self.with_or_without('netcdf', activation_value='prefix')

        if self.spec.variants['grib2'].value == 'eccodes':
            config_args.append('--with-eccodes=' +
                               self.spec['eccodes'].prefix)
            config_args.append('--without-grib_api')
        elif self.spec.variants['grib2'].value == 'grib-api':
            config_args.append('--with-grib_api=' +
                               self.spec['grib-api'].prefix)
            if self.spec.satisfies('@1.9:'):
                config_args.append('--without-eccodes')
        else:
            config_args.append('--without-grib_api')
            if self.spec.satisfies('@1.9:'):
                config_args.append('--without-eccodes')

        if '+external-grib1' in self.spec:
            config_args.append('--disable-cgribex')
        else:
            config_args.append('--enable-cgribex')

        if '+szip' in self.spec:
            config_args.append('--with-szlib=' + self.spec['szip'].prefix)
        else:
            config_args.append('--without-szlib')

        config_args += self.with_or_without('hdf5',
                                            activation_value='prefix')

        config_args += self.with_or_without('udunits2',
                                            activation_value='prefix')

        config_args += self.with_or_without('libxml2',
                                            activation_value='prefix')

        config_args += self.with_or_without('proj',
                                            activation_value='prefix')

        config_args += self.with_or_without('curl',
                                            activation_value='prefix')

        config_args += self.with_or_without('magics',
                                            activation_value='prefix')

        config_args += self.with_or_without('fftw3')

        config_args += self.enable_or_disable('openmp')

        # Starting version 1.9.0 CDO is a C++ program but it uses the C
        # interface of HDF5 without the parallel features. To avoid
        # unnecessary dependencies on mpi's cxx library, we need to set the
        # following flags. This works for OpenMPI, MPICH, MVAPICH, Intel MPI,
        # IBM Spectrum MPI, bullx MPI, and Cray MPI.
        if self.spec.satisfies('@1.9:+hdf5^hdf5+mpi'):
            config_args.append(
                'CPPFLAGS=-DOMPI_SKIP_MPICXX -DMPICH_SKIP_MPICXX')

        return config_args
