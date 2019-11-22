# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GoMd2man(Package):
    """go-md2man converts markdown into roff (man pages)"""

    homepage = "https://github.com/cpuguy83/go-md2man"
    url      = "https://github.com/cpuguy83/go-md2man/archive/v1.0.10.tar.gz"

    version('1.0.10', sha256='76aa56849123b99b95fcea2b15502fd886dead9a5c35be7f78bdc2bad6be8d99')

    depends_on('go@1.11:')  # modules support

    def install(self, spec, prefix):
        env['GO111MODULE'] = 'on'  # not the default for go@1.11.x
        go = Executable("go")
        go("build")
        mkdir(prefix.bin)
        install('go-md2man', prefix.bin)
