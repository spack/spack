# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Trf(Package):
    """Tandem Repeats Finder is a program to locate and display tandem repeats
       in DNA sequences.

       Note: A manual download is required for TRF.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://tandem.bu.edu/trf/trf.html"

    version('4.09', '0c594fe666e0332db1df9d160d7fabc8', expand=False,
            url='file://{0}/trf409.linux64'.format(os.getcwd()))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('trf409.linux64', prefix.bin.trf)
        chmod = which('chmod')
        chmod('+x', prefix.bin.trf)
