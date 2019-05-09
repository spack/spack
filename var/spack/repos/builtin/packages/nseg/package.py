# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Nseg(MakefilePackage):
    """NSEG - Low complexity sequence identification

       This package is hosted as an FTP directory. To install it, you will
       need to download all of the files from the 'homepage' and tar them."""

    homepage = "ftp://ftp.ncbi.nih.gov/pub/seg/nseg/"
    url      = "file://{0}/nseg.tar.gz".format(os.getcwd())

    version('1.0', sha256='6fd0fc77f54a061615931a5de4fe203eef7cdbc35b791efee5407bb2df7f20b2')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('nseg', prefix.bin)
        install('nmerge', prefix.bin)
