# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Grads(AutotoolsPackage):
    """The Grid Analysis and Display System (GrADS) is an interactive
    desktop tool that is used for easy access, manipulation, and visualization
    of earth science data. GrADS has two data models for handling gridded and
    station data. GrADS supports many data file formats, including
    binary (stream or sequential), GRIB (version 1 and 2), NetCDF,
    HDF (version 4 and 5), and BUFR (for station data)."""

    homepage = "http://cola.gmu.edu/grads/grads.php"
    url      = "ftp://cola.gmu.edu/grads/2.2/grads-2.2.1-src.tar.gz"

    version('2.2.2', sha256='5b28c2674c538342132f1a557be72287850ddaf10f51b7161c6837cf833f2c8f')
    version('2.2.1', sha256='695e2066d7d131720d598bac0beb61ac3ae5578240a5437401dc0ffbbe516206')

    variant('geotiff', default=True, description="Enable GeoTIFF support")
    variant('shapefile', default=True, description="Enable Shapefile support")
    variant('grib2', default=True, description='Enable GRIB2 support with the g2c library.')
    variant('netcdf', default=True, description='Enable NetCDF support')

    """
    # FIXME: Fails with undeclared functions (tdefi, tdef, ...) in gauser.c
    variant('hdf4', default=False, description="Enable HDF4 support")
    depends_on('hdf', when='+hdf4')
    """

    depends_on('libgeotiff', when='+geotiff')
    depends_on('shapelib', when='+shapefile')
    depends_on('g2c+pic', when='+grib2')
    depends_on('udunits')
    depends_on('libgd')
    depends_on('libxmu')
    depends_on('cairo +X +pdf +fc +ft')
    depends_on('readline')
    depends_on('pkgconfig', type='build')
    depends_on('netcdf-c', when='+netcdf')
    depends_on('hdf5', when='+netcdf')

    # Grads does not supply #include <stdint.h> which Intel complains about
    patch('stdint.patch')

    def setup_run_environment(self, env):
        env.set('GADDIR', self.prefix.data)

    # -lgrib2c is -lg2c
    # and no reason to hardcode PNG version
    def patch(self):
        filter_file('-lgrib2c', '-lg2c', 'configure')
        filter_file('-lpng15', '-lpng', 'configure')

    def setup_build_environment(self, env):
        spec = self.spec
        libs = []
        cppflags = []

        env.set('SUPPLIBS', '/')

        if '+grib2' in spec:
            cppflags.append('-I' + spec['g2c'].prefix.include)
            cppflags.append('-I' + spec['jasper'].prefix.include.jasper)

        # Grads is not compatible with HDF5 1.12.0
        # which had an API change in h5_getinfo
        if spec['hdf5'].satisfies('@1.12.0:'):
            cppflags.append('-DH5_USE_110_API')

        # Need to manually supply -ludunits2
        libs.append('-ludunits2')
        env.set('LIBS', ' '.join(libs))
        env.set('CPPFLAGS', ' '.join(cppflags))

    def configure_args(self):
        args = []

        args.extend(self.with_or_without('geotiff'))

        # GCC on macOS complained about these directories not existing
        mkdirp('bin')
        mkdirp('lib')

        return args

    @run_after('install')
    def copy_data(self):
        with working_dir(self.build_directory):
            install_tree('data', self.prefix.data)
        with working_dir(self.package_dir):
            install('udpt', self.prefix.data)
            filter_file(
                r'({lib})',
                self.prefix.lib,
                self.prefix.data.udpt
            )
