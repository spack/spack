# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gmt(Package):
    """GMT (Generic Mapping Tools) is an open source collection of about 80
    command-line tools for manipulating geographic and Cartesian data sets
    (including filtering, trend fitting, gridding, projecting, etc.) and
    producing PostScript illustrations ranging from simple x–y plots via
    contour maps to artificially illuminated surfaces and 3D perspective views.
    """

    homepage = "http://gmt.soest.hawaii.edu/"
    url      = "https://github.com/GenericMappingTools/gmt/archive/5.4.4.tar.gz"

    version('5.4.4', sha256='b593dfb101e6507c467619f3d2190a9f78b09d49fe2c27799750b8c4c0cd2da0')
    version('4.5.9', sha256='9b13be96ccf4bbd38c14359c05dfa7eeeb4b5f06d6f4be9c33d6c3ea276afc86',
            url='ftp://ftp.soest.hawaii.edu/gmt/legacy/gmt-4.5.9.tar.bz2')

    variant('pcre', default=False, description='Enable the PCRE interface')
    variant('gdal', default=False, description='Enable the GDAL interface')
    variant('fftw', default=True, description='Fast FFTs')
    variant('lapack', default=True, description='Fast matrix inversion')
    variant('blas', default=True, description='Fast matrix multiplications')

    # http://gmt.soest.hawaii.edu/projects/gmt/wiki/BuildingGMT

    # Required dependencies
    depends_on('ghostscript')
    depends_on('subversion')
    depends_on('cmake@2.8.5:', type='build', when='@5:')
    depends_on('netcdf@4:')
    depends_on('curl', when='@5.4:')

    # Optional dependencies
    depends_on('pcre2', when='@5.4.4:+pcre')
    depends_on('pcre', when='@:5.4.3+pcre')
    depends_on('gdal', when='+gdal')
    depends_on('fftw', when='+fftw')
    depends_on('lapack', when='+lapack')
    depends_on('blas', when='+blas')
    depends_on('graphicsmagick', type='test')

    @when('@5:')
    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            if self.run_tests:
                make('test')
            make('install')

    @when('@:4')
    def install(self, spec, prefix):
        args = [
            '--prefix={0}'.format(prefix),
            '--enable-netcdf={0}'.format(spec['netcdf'].prefix),
            '--enable-shared'
        ]

        if '+gdal' in spec:
            args.append('--enable-gdal')
        else:
            args.append('--disable-gdal')

        configure(*args)
        make()
        if self.run_tests:
            make('check')
        make('install')
