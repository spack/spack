##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Vmd(AutotoolsPackage):
    """VMD is a molecular visualization program
    for displaying, animating, and analyzing large biomolecular systems
    using 3-D graphics and built-in scripting."""

    homepage = "https://www.ks.uiuc.edu/Research/vmd/"
    url      = "http://www.ks.uiuc.edu/Research/vmd/vmd-1.9.3/files/final/vmd-1.9.3.src.tar.gz"

    version('1.9.3', '5706f88b9b77cc5fafda6fef3a82d6fa')

    depends_on('opengl')
    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    # depends_on('python@2.7:')
    # depends_on('perl')
    depends_on('tcl')
    depends_on('fltk')
    # depends_on('netcdf')
    # depends_on('tachyon')
    # depends_on('vrpn')

    # Intel compilers (icc,icpc) are hardcoded in massive vmd Makefiles
    # conflicts('%gcc')
    # conflicts('%pgi')

    configure_directory = 'vmd-1.9.3'

    parallel = False

    # def edit(self, spec, prefix):
        # configure = FileFilter('vmd-{0}/configure'.format(self.version))
        # configure.filter(r'^\$libtachyon_dir.*=.*',
        #                  r'$libtachyon_dir = "{0}";'
        #                  .format(spec['tachyon'].prefix))
        # makefile = FileFilter('vmd-{0}/src/Makefile'.format(self.version))
        # makefile.filter('-DVMDVRPN', '', )

    def configure_args(self):
        args = ["LINUXAMD64", "MESA"]
        return args

    def build(self, spec, prefix):
        # Build and distribute VMD plugins
        with working_dir('plugins'):
            make('LINUXAMD64')
            make('distrib',
                 'PLUGINDIR={0}/vmd-{1}/plugins'
                 .format(self.build_directory, self.version))
        # Configure VMD
        # with working_dir('vmd-{0}'.format(self.version)):
        #     make('linux.mesa')
        # Build VMD
        with working_dir('vmd-{0}/src'.format(self.version)):
            make()

    def install(self, spec, prefix):
        with working_dir('vmd-{0}/src'.format(self.version)):
            make('install')
