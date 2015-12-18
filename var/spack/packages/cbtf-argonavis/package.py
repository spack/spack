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

class CbtfArgonavis(Package):
    """CBTF Argo Navis project contains the CUDA collector and supporting 
       libraries that was done as a result of a DOE SBIR grant."""
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home/"

    # Mirror access template example
    #url      = "file:/g/g24/jeg/cbtf-argonavis-1.5.tar.gz"
    #version('1.5', '1f7f6512f55409ed2135cfceabe26b82')

    version('1.6', branch='master', git='http://git.code.sf.net/p/cbtf-argonavis/cbtf-argonavis')

    depends_on("cmake@3.0.2:")
    depends_on("papi")
    depends_on("cbtf")
    depends_on("cbtf-krell")
    depends_on("cuda")

    parallel = False

    def install(self, spec, prefix):

       # Look for package installation information in the cbtf and cbtf-krell prefixes
       cmake_prefix_path = join_path(spec['cbtf'].prefix) + ':' + join_path(spec['cbtf-krell'].prefix)

       # FIXME, hard coded for testing purposes, we will alter when the external package feature is available
       cuda_prefix_path = "/usr/local/cudatoolkit-6.0"
       cupti_prefix_path = "/usr/local/cudatoolkit-6.0/extras/CUPTI"


       with working_dir('CUDA'):
         with working_dir('build', create=True):
           cmake('..',
                 '-DCMAKE_INSTALL_PREFIX=%s'	% prefix,
                 '-DCMAKE_LIBRARY_PATH=%s'	% prefix.lib64,
                 '-DCMAKE_PREFIX_PATH=%s'	% cmake_prefix_path,
                 '-DCUDA_INSTALL_PATH=%s'	% cuda_prefix_path,
                 '-DCUDA_ROOT=%s'		% cuda_prefix_path,
                 '-DCUPTI_ROOT=%s'		% cupti_prefix_path,
                 '-DCUDA_DIR=%s'                % cuda_prefix_path,
                 '-DPAPI_ROOT=%s'		% spec['papi'].prefix,
                 '-DCBTF_PREFIX=%s'		% spec['cbtf'].prefix,
                 *std_cmake_args)
           make("clean")
           make()
           make("install")

