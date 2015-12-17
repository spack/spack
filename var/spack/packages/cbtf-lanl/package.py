################################################################################
# Copyright (c) 2015 Krell Institute. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
################################################################################

from spack import *

class CbtfLanl(Package):
    """CBTF LANL project contains a memory tool and data center type system command monitoring tool."""
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home/"


    # Mirror access template example
    #url      = "file:/g/g24/jeg/cbtf-lanl-1.5.tar.gz"
    #version('1.5', 'c3f78f967b0a42c6734ce4be0e602426')

    version('1.6', branch='master', git='http://git.code.sf.net/p/cbtf-lanl/cbtf-lanl')


    # Dependencies for cbtf-krell
    depends_on("boost@1.50")
    depends_on("mrnet@4.1.0:+lwthreads")
    depends_on("xerces-c@3.1.1:")
    depends_on("cbtf")
    depends_on("cbtf-krell")

    parallel = False

    def install(self, spec, prefix):

     # Add in paths for finding package config files that tell us where to find these packages
     cmake_prefix_path = join_path(spec['cbtf'].prefix) + ':' + join_path(spec['cbtf-krell'].prefix)

     with working_dir('build', create=True):
          cmake('..',
                '-DCBTF_DIR=%s'            % spec['cbtf'].prefix,
                '-DCBTF_KRELL_DIR=%s'      % spec['cbtf-krell'].prefix,
                '-DMRNET_DIR=%s'           % spec['mrnet'].prefix,
                '-DXERCESC_DIR=%s'         % spec['xerces-c'].prefix,
                '-DCMAKE_PREFIX_PATH=%s'   % cmake_prefix_path,
                '-DCMAKE_MODULE_PATH=%s'   % join_path(prefix.share,'KrellInstitute','cmake'),
                *std_cmake_args)

          make("clean")
          make()
          make("install")

