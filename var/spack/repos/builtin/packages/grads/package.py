# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install grads
#
# You can edit this file again by typing:
#
#     spack edit grads
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

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

    version('2.2.1', sha256='695e2066d7d131720d598bac0beb61ac3ae5578240a5437401dc0ffbbe516206')

    variant('hdf5', default=False, description="Enable HDF5 support")
    variant('netcdf', default=False, description="Enable NetCDF support")
    variant('geotiff', default=False, description="Enable GeoTIFF support")
    variant('shapefile', default=False, description="Enable Shapefile support")

    depends_on('hdf5', when='+hdf5')
    depends_on('netcdf-c', when='+netcdf')
    depends_on('libgeotiff', when='+geotiff')
    depends_on('shapelib', when='+shapefile')
    depends_on('libgd')
    depends_on('libxmu')
    depends_on('cairo +X +pdf +fc +ft')
    depends_on('pkgconfig')
    depends_on('readline')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('SUPPLIBS', '/')
        run_env.set('GADDIR', join_path(self.prefix, 'data'))

    @run_after('install')
    def copy_data(self):
        with working_dir(self.build_directory):
            install_tree('data', join_path(self.prefix, 'data'))
        with working_dir(self.package_dir):
            copy('udpt', join_path(self.prefix, 'data'))
            filter_file(
                r'({lib})',
                join_path(self.prefix, 'lib'),
                join_path(self.prefix, 'data/udpt')
            )
