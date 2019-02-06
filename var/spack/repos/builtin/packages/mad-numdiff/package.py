# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class MadNumdiff(CMakePackage):
    """compare unformatted text files with numerical content"""

    homepage = "https://github.com/quinoacomputing/ndiff"
    url      = "https://github.com/quinoacomputing/ndiff/tarball/20150724"
    git      = "https://github.com/quinoacomputing/ndiff.git"

    version('develop', branch='master')
    version('20150724', '7723c0f2499aea8fd960377c5bed28d8')
