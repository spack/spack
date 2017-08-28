##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import os
import platform
import distutils.dir_util


class Paraver(Package):
    """"A very powerful performance visualization and analysis tool
        based on traces that can be used to analyse any information that
        is expressed on its input trace format.  Traces for parallel MPI,
        OpenMP and other programs can be genereated with Extrae."""
    homepage = "https://tools.bsc.es/paraver"
    url = "https://ftp.tools.bsc.es/paraver/wxparaver-4.6.3-src.tar.bz2"

    system = platform.system()
    machine = platform.machine()

    # TODO: changed source to binary distribution
    # see discussion in https://github.com/LLNL/spack/issues/4860

    if system == 'Linux' and machine == 'x86_64':
        version('4.6.3', 'f26555ce22fd83bfdcbf90648491026c')
    elif system == 'Linux' and machine == 'i686':
        version('4.6.3', 'ee13df1b9b8a86dd28e9332d4cb8b9bd')
    elif system == 'Darwin':
        version('4.6.3', '922d7f531751278fcc05da57b6a771fd')
    elif system == 'Windows':
        version('4.6.3', '943388e760d91e95ef5287aeb460a8b6')

    def url_for_version(self, version):
        base_url = "https://ftp.tools.bsc.es/wxparaver/wxparaver"
        package_ext = ''

        system = platform.system()
        machine = platform.machine()

        if system == 'Linux' and machine == 'x86_64':
            package_ext = 'linux_x86_64.tar.bz2'
        elif system == 'Linux' and machine == 'i686':
            package_ext = 'linux_x86_32.tar.bz2'
        elif system == 'Darwin':
            package_ext = 'mac.zip'
        elif system == 'Windows':
            package_ext = 'win.zip'

        return "{0}-{1}-{2}".format(base_url, version, package_ext)

    def install(self, spec, prefix):
        distutils.dir_util.copy_tree(".", prefix)

        if platform.system() == 'Darwin':
            os.symlink(join_path(prefix,
                'wxparaver.app/Contents/MacOS/'), prefix.bin)
