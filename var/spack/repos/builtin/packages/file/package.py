##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class File(AutotoolsPackage):
    """a file type guesser"""

    homepage = "https://www.darwinsys.com/file"
    url      = "ftp://ftp.astron.com/pub/file/file-5.34.tar.gz"

    version('5.34', sha256='f15a50dbbfa83fec0bd1161e8e191b092ec832720e30cd14536e044ac623b20a')
