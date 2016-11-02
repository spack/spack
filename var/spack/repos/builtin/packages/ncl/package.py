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
import os
import shutil
import tempfile


class Ncl(Package):
    """NCL is an interpreted language designed specifically for
       scientific data analysis and visualization. Supports NetCDF 3/4,
       GRIB 1/2, HDF 4/5, HDF-EOD 2/5, shapefile, ASCII, binary.
       Numerous analysis functions are built-in."""

    homepage = "https://www.ncl.ucar.edu"

    version('6.3.0', '4834df63d3b56778441246303ab921c4',
            url='https://www.earthsystemgrid.org/download/fileDownload.html?'
                'logicalFileId=bec58cb3-cd9b-11e4-bb80-00c0f03d5b7c',
            extension='tar.gz')
    patch('spack_ncl.patch')

    # This installation script is implemented according to this manual:
    # http://www.ncl.ucar.edu/Download/build_from_src.shtml

    variant('hdf4', default=False, description='Enable HDF4 support.')
    variant('gdal', default=False, description='Enable GDAL support.')
    variant('triangle', default=True, description='Enable Triangle support.')
    variant('udunits2', default=True, description='Enable UDUNITS-2 support.')
    variant('openmp', default=True, description='Enable OpenMP support.')

    # Non-optional dependencies according to the manual:
    depends_on('jpeg')
    depends_on('netcdf')
    depends_on('cairo')

    # Also, the manual says that ncl requires zlib, but that comes as a
    # mandatory dependency of libpng, which is a mandatory dependency of cairo.

    # In Spack, we do not have an option to compile netcdf without netcdf-4
    # support, so we will tell the ncl configuration script that we want
    # support for netcdf-4, but the script assumes that hdf5 is compiled with
    # szip support. We introduce this restriction with the following dependency
    # statement.
    depends_on('hdf5@:1.8+szip')

    # In Spack, we also do not have an option to compile netcdf without DAP
    # support, so we will tell the ncl configuration script that we have it.

    # Some of the optional dependencies according to the manual:
    depends_on('hdf', when='+hdf4')
    depends_on('gdal', when='+gdal')
    depends_on('udunits2', when='+udunits2')

    # We need src files of triangle to appear in ncl's src tree if we want
    # triangle's features.
    resource(
        name='triangle',
        url='http://www.netlib.org/voronoi/triangle.zip',
        md5='10aff8d7950f5e0e2fb6dd2e340be2c9',
        placement='triangle_src',
        when='+triangle')

    def install(self, spec, prefix):

        if (self.compiler.fc is None) or (self.compiler.cc is None):
            raise InstallError('NCL package requires both '
                               'C and Fortran compilers.')

        self.prepare_site_config()
        self.prepare_install_config()
        self.prepare_src_tree()
        make('Everything', parallel=False)

    def setup_environment(self, spack_env, run_env):
        run_env.set('NCARG_ROOT', self.spec.prefix)

    def prepare_site_config(self):
        fc_flags = []
        cc_flags = []
        c2f_flags = []

        if '+openmp' in self.spec:
            fc_flags.append(self.compiler.openmp_flag)
            cc_flags.append(self.compiler.openmp_flag)

        if self.compiler.name == 'gcc':
            fc_flags.append('-fno-range-check')
            c2f_flags.extend(['-lgfortran'])
        elif self.compiler.name == 'intel':
            fc_flags.append('-fp-model precise')
            cc_flags.append('-fp-model precise')
            c2f_flags.extend(['-lifcore', '-lifport'])

        with open('./config/Spack', 'w') as f:
            f.writelines([
                '#define HdfDefines\n',
                '#define CppCommand \'/usr/bin/env cpp -traditional\'\n',
                '#define CCompiler cc\n',
                '#define FCompiler fc\n',
                ('#define CtoFLibraries ' + ' '.join(c2f_flags) + '\n'
                 if len(c2f_flags) > 0
                 else ''),
                ('#define CtoFLibrariesUser ' + ' '.join(c2f_flags) + '\n'
                 if len(c2f_flags) > 0
                 else ''),
                ('#define CcOptions ' + ' '.join(cc_flags) + '\n'
                 if len(cc_flags) > 0
                 else ''),
                ('#define FcOptions ' + ' '.join(fc_flags) + '\n'
                 if len(fc_flags) > 0
                 else ''),
                '#define BuildShared NO'
            ])

    def prepare_install_config(self):
        # Remove the results of the previous configuration attempts.
        self.delete_files('./Makefile', './config/Site.local')

        # Generate an array of answers that will be passed to the interactive
        # configuration script.
        config_answers = [
            # Enter Return to continue
            '\n',
            # Build NCL?
            'y\n',
            # Parent installation directory :
            '\'' + self.spec.prefix + '\'\n',
            # System temp space directory   :
            '\'' + tempfile.mkdtemp(prefix='ncl_ncar_') + '\'\n',
            # Build NetCDF4 feature support (optional)?
            'y\n'
        ]

        if '+hdf4' in self.spec:
            config_answers.extend([
                # Build HDF4 support (optional) into NCL?
                'y\n',
                # Also build HDF4 support (optional) into raster library?
                'y\n',
                # Did you build HDF4 with szip support?
                'y\n' if self.spec.satisfies('^hdf+szip') else 'n\n'
            ])
        else:
            config_answers.extend([
                # Build HDF4 support (optional) into NCL?
                'n\n',
                # Also build HDF4 support (optional) into raster library?
                'n\n'
            ])

        config_answers.extend([
            # Build Triangle support (optional) into NCL
            'y\n' if '+triangle' in self.spec else 'n\n',
            # If you are using NetCDF V4.x, did you enable NetCDF-4 support?
            'y\n',
            # Did you build NetCDF with OPeNDAP support?
            'y\n',
            # Build GDAL support (optional) into NCL?
            'y\n' if '+gdal' in self.spec else 'n\n',
            # Build Udunits-2 support (optional) into NCL?
            'y\n' if '+uduints2' in self.spec else 'n\n',
            # Build Vis5d+ support (optional) into NCL?
            'n\n',
            # Build HDF-EOS2 support (optional) into NCL?
            'n\n',
            # Build HDF5 support (optional) into NCL?
            'y\n',
            # Build HDF-EOS5 support (optional) into NCL?
            'n\n',
            # Build GRIB2 support (optional) into NCL?
            'n\n',
            # Enter local library search path(s) :
            # The paths will be passed by the Spack wrapper.
            ' \n',
            # Enter local include search path(s) :
            # All other paths will be passed by the Spack wrapper.
            '\'' + join_path(self.spec['freetype'].prefix.include,
                             'freetype2') + '\'\n',
            # Go back and make more changes or review?
            'n\n',
            # Save current configuration?
            'y\n'
        ])

        config_answers_filename = 'spack-config.in'
        config_script = Executable('./Configure')

        with open(config_answers_filename, 'w') as f:
            f.writelines(config_answers)

        with open(config_answers_filename, 'r') as f:
            config_script(input=f)

    def prepare_src_tree(self):
        if '+triangle' in self.spec:
            triangle_src = join_path(self.stage.source_path, 'triangle_src')
            triangle_dst = join_path(self.stage.source_path, 'ni', 'src',
                                     'lib', 'hlu')
            shutil.copy(join_path(triangle_src, 'triangle.h'), triangle_dst)
            shutil.copy(join_path(triangle_src, 'triangle.c'), triangle_dst)

    @staticmethod
    def delete_files(*filenames):
        for filename in filenames:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except OSError, e:
                    raise InstallError('Failed to delete file %s: %s' % (
                        e.filename, e.strerror))
