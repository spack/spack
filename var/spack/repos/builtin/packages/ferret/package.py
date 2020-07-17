# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class Ferret(Package):
    """Ferret is an interactive computer visualization and analysis environment
       designed to meet the needs of oceanographers and meteorologists
       analyzing large and complex gridded data sets."""
    homepage = "http://ferret.pmel.noaa.gov/Ferret/home"
    url      = "ftp://ftp.pmel.noaa.gov/ferret/pub/source/fer_source.v696.tar.gz"

    version('7.2', sha256='21c339b1bafa6939fc869428d906451f130f7e77e828c532ab9488d51cf43095')
    version('6.96', sha256='7eb87156aa586cfe838ab83f08b2102598f9ab62062d540a5da8c9123816331a')

    depends_on("hdf5+hl")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("readline")
    depends_on("zlib")
    depends_on("libx11")

    def url_for_version(self, version):
        return "ftp://ftp.pmel.noaa.gov/ferret/pub/source/fer_source.v{0}.tar.gz".format(
            version.joined)

    def patch(self):
        hdf5_prefix = self.spec['hdf5'].prefix
        netcdff_prefix = self.spec['netcdf-fortran'].prefix
        readline_prefix = self.spec['readline'].prefix
        libz_prefix = self.spec['zlib'].prefix

        filter_file(r'^BUILDTYPE.+',
                    'BUILDTYPE = x86_64-linux',
                    'FERRET/site_specific.mk')
        filter_file(r'^INSTALL_FER_DIR.+',
                    'INSTALL_FER_DIR = %s' % self.spec.prefix,
                    'FERRET/site_specific.mk')
        filter_file(r'^HDF5_DIR.+',
                    'HDF5_DIR = %s' % hdf5_prefix,
                    'FERRET/site_specific.mk')
        filter_file(r'^NETCDF4_DIR.+',
                    'NETCDF4_DIR = %s' % netcdff_prefix,
                    'FERRET/site_specific.mk')
        filter_file(r'^READLINE_DIR.+',
                    'READLINE_DIR = %s' % readline_prefix,
                    'FERRET/site_specific.mk')
        filter_file(r'^LIBZ_DIR.+',
                    'LIBZ_DIR = %s' % libz_prefix,
                    'FERRET/site_specific.mk')
        filter_file(r'^JAVA_HOME.+',
                    ' ',
                    'FERRET/site_specific.mk')
        filter_file(r'-lm',
                    '-lgfortran -lm',
                    'FERRET/platform_specific.mk.x86_64-linux')
        filter_file(r'\$\(NETCDF4_DIR\)/lib64/libnetcdff.a',
                    "-L%s -lnetcdff" % self.spec['netcdf-fortran'].prefix.lib,
                    'FERRET/platform_specific.mk.x86_64-linux')
        filter_file(r'\$\(NETCDF4_DIR\)/lib64/libnetcdf.a',
                    "-L%s -lnetcdf" % self.spec['netcdf-c'].prefix.lib,
                    'FERRET/platform_specific.mk.x86_64-linux')
        filter_file(r'\$\(HDF5_DIR\)/lib64/libhdf5_hl.a',
                    "-L%s -lhdf5_hl" % self.spec['hdf5'].prefix.lib,
                    'FERRET/platform_specific.mk.x86_64-linux')
        filter_file(r'\$\(HDF5_DIR\)/lib64/libhdf5.a',
                    "-L%s -lhdf5" % self.spec['hdf5'].prefix.lib,
                    'FERRET/platform_specific.mk.x86_64-linux')

    def install(self, spec, prefix):
        if 'LDFLAGS' in env and env['LDFLAGS']:
            env['LDFLAGS'] += ' ' + '-lquadmath'
        else:
            env['LDFLAGS'] = '-lquadmath'

        with working_dir('FERRET', create=False):
            os.environ['LD_X11'] = '-L%s -lX11' % spec['libx11'].prefix.lib
            os.environ['HOSTTYPE'] = 'x86_64-linux'
            make(parallel=False)
            make("install")
