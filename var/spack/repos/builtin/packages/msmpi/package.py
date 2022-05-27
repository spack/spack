# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Msmpi(Package):
    """A Windows-specced build of MPICH provided directly by
    Microsoft Support Team
    """
    homepage = 'https://www.microsoft.com/en-us/download/default.aspx'
    maintainers = ['jpopelar']

    version('10.0', sha256='7dae13797627726f67fab9c1d251aec2df9ecd25939984645ec05748bdffd396', extension='exe')

    provides('mpi')

    conflicts('platform=linux')
    conflicts('platform=darwin')
    conflicts('platform=cray')

    def url_for_version(self, version):
        return 'https://download.microsoft.com/download/A/E/0/AE002626-9D9D-448D-8197-1EA510E297CE/msmpisetup.exe'

    def install(self):
        installer = Executable('msmpisetup.exe')
        installer()
