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

class Cbtf(Package):
    """CBTF project contains the base code for CBTF that supports creating components, 
       component networks and the support to connect these components and component 
       networks into sequential and distributed network tools."""
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home"

    # Mirror access template example
    #url      = "file:/g/g24/jeg/cbtf-1.5.tar.gz"
    #version('1.6', '1ca88a8834759c4c74452cb97fe7b70a')

    # Use when the git repository is available
    version('1.6', branch='master', git='http://git.code.sf.net/p/cbtf/cbtf')

    depends_on("cmake")
    #depends_on("boost@1.42.0:")
    depends_on("boost@1.50.0")
    depends_on("mrnet@4.1.0+lwthreads")
    depends_on("xerces-c@3.1.1:")
    depends_on("libxml2")

    parallel = False

    def install(self, spec, prefix):
      with working_dir('build', create=True):

          # Boost_NO_SYSTEM_PATHS  Set to TRUE to suppress searching   
          # in system paths (or other locations outside of BOOST_ROOT
          # or BOOST_INCLUDEDIR).  Useful when specifying BOOST_ROOT. 
          # Defaults to OFF.

          cmake('..',
                '--debug-output',
                '-DBoost_NO_SYSTEM_PATHS=TRUE',
                '-DXERCESC_DIR=%s'         % spec['xerces-c'].prefix,
                '-DBOOST_ROOT=%s'          % spec['boost'].prefix,
                '-DMRNET_DIR=%s'           % spec['mrnet'].prefix,
                '-DCMAKE_MODULE_PATH=%s'   % join_path(prefix.share,'KrellInstitute','cmake'),
                *std_cmake_args)

          make("clean")
          make()
          make("install")
