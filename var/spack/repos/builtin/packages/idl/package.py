# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import shutil
import pathlib
import os


class Idl(Package):
    """IDL Software: Interactive Data Visulation.
    
    Note: IDL is a licensed software. You will also need an existing
    downloaded tarball of IDL in your current directory or in a 
    spack mirror in order to install."""

    homepage = "https://www.harrisgeospatial.com/Software-Technology/IDL"
    idl_mirror_path = 'idl/idl-8.7.tar.gz'
    manual_download = True
    url = "file://mirror.com/idl8.7-linux.tar.gz"

    maintainers = ['francinelapid']

    #version('8.7')

    license_required = True

    def install(self, spec, prefix):

        # replace default install dir to self.prefix by editing answer file
        filter_file('/usr/local/harris', self.prefix, 'silent/idl_answer_file')

        # execute install script
        install_script = Executable('./install.sh')
        install_script('-s', input='silent/idl_answer_file')

    def setup_run_environment(self, env):
        
        # set necessary environment variables
        env.prepend_path('EXELIS_DIR', self.prefix)
        env.prepend_path('IDL_DIR', self.prefix.idl)
        
        # add bin to path
        env.prepend_path('PATH', self.prefix.idl.bin)
