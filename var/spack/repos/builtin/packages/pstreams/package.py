# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Pstreams(Package):
    """C++ wrapper for the POSIX.2 functions popen(3) and pclose(3)"""

    homepage = "http://pstreams.sourceforge.net/"
    url      = "https://superb-sea2.dl.sourceforge.net/project/pstreams/pstreams/Release%201.0/pstreams-1.0.1.tar.gz"

    version('1.0.1', '23199e3d12a644a2a0c66ec889d4c064')

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install('pstream.h', prefix.include)
