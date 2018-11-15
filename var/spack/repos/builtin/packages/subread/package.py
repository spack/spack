# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Subread(MakefilePackage):
    """The Subread software package is a tool kit for processing next-gen
       sequencing data."""

    homepage = "http://subread.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/subread/subread-1.5.2/subread-1.5.2-source.tar.gz"

    version('1.6.2', '70125531737fe9ba2be83622ca236e5e')
    version('1.6.0', 'ed7e32c56bda1e769703e0a4db5a89a7')
    version('1.5.2', '817d2a46d87fcef885c8832475b8b247')

    depends_on('zlib')

    def build(self, spec, prefix):
        plat = sys.platform
        with working_dir('src'):
            if plat.startswith('linux'):
                filter_file(
                    'CC_EXEC = gcc',
                    'CC_EXEC = {0}'.format(spack_cc),
                    'Makefile.Linux'
                )
                make('-f', 'Makefile.Linux')
            elif plat.startswith('darwin'):
                make('-f', 'Makefile.MacOS')
            else:
                raise InstallError("The communication mechanism %s is not"
                                   "supported" % plat)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
