# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    depends_on("boost")
    # depends_on("extrae")
    depends_on("wxwidgets")
    depends_on("wxpropgrid")

    def install(self, spec, prefix):
        distutils.dir_util.copy_tree(".", prefix)

        if platform.system() == 'Darwin':
            os.symlink(join_path(prefix,
                'wxparaver.app/Contents/MacOS/'), prefix.bin)
