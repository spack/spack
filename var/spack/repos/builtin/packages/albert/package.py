# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Albert(MakefilePackage):
    """Albert is an interactive program to assist the
    specialist in the study of nonassociative algebra."""

    homepage = "https://people.cs.clemson.edu/~dpj/albertstuff/albert.html"
    url      = "https://github.com/kentavv/Albert/archive/v4.0a_opt4.tar.gz"

    version('4.0a_opt4', '79e3d9623602f2ca5db7d84c81d4eb8c')

    depends_on('readline')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('albert', join_path(prefix.bin))
