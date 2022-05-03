# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re
import sys

from spack import *


class Msmpi(Package):
    """MPICH is a high performance and widely portable implementation of
    the Message Passing Interface (MPI) standard."""

    homepage = "https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi"
    url      = "https://github.com/microsoft/Microsoft-MPI/archive/refs/tags/v10.1.1.tar.gz"
    git      = "https://github.com/microsoft/Microsoft-MPI.git"

    version("10.1.1", sha256="63c7da941fc4ffb05a0f97bd54a67968c71f63389a0d162d3182eabba1beab3d")
    version("10.0.0", sha256="cfb53cf53c3cf0d4935ab58be13f013a0f7ccb1189109a5b8eea0fcfdcaef8c1")


    def is_64bit(self):
        return platform.machine().endswith('64')

    def build_command_line(self):
        arch = 'intel64' if self.is_64() else 'ia32'
        args = []
        ver_str = os.environ['VCToolsInstallDir']
        ver = re.search(r'[1-9][1-9].[1-9][1-9].[1-9][1-9][1-9][1-9][1-9]', ver_str)
        ver = '' if not ver else ver.group()
        args.append('/p:GFORTRAN_BIN=%sbin\%s' % (os.environ['IFORT_COMPILER21'], arch))
        args.append('/p:VCToolsVersion=%s' % ver)
        args.append('/p:WindowsTargetPlatformVersion=%s' % '')

    def install(self):
        with working_dir(self.stage.build_directory, create=True):
            msbuild()
