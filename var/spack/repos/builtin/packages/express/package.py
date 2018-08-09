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
import os.path
import glob


class Express(CMakePackage):
    """eXpress is a streaming tool for quantifying the abundances of a set of
       target sequences from sampled subsequences."""

    homepage = "http://bio.math.berkeley.edu/eXpress/"
    git      = "https://github.com/adarob/eXpress.git"

    version('2015-11-29', commit='f845cab2c7f2d9247b35143e4aa05869cfb10e79')

    depends_on('boost')
    depends_on('bamtools')
    depends_on('zlib')

    conflicts('%gcc@6.0.0:', when='@2015-11-29')

    def patch(self):
        with working_dir('src'):
            files = glob.iglob('*.*')
            for file in files:
                if os.path.isfile(file):
                    edit = FileFilter(file)
                    edit.filter('#include <api', '#include <%s' % self.spec[
                                'bamtools'].prefix.include.bamtools.api)
            edit = FileFilter('CMakeLists.txt')
            edit.filter('\${CMAKE_CURRENT_SOURCE_DIR}/../bamtools/lib/'
                        'libbamtools.a', '%s' % self.spec['bamtools'].libs)

    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path('CPATH', self.spec[
                               'bamtools'].prefix.include.bamtools)
