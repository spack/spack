# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package_defs import *


class AutoconfArchive(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Autoconf Archive is a collection of more than 500 macros for
    GNU Autoconf."""

    homepage = "https://www.gnu.org/software/autoconf-archive/"
    gnu_mirror_path = "autoconf-archive/autoconf-archive-2019.01.06.tar.xz"

    version('2022.02.11', sha256='78a61b611e2eeb55a89e0398e0ce387bcaf57fe2dd53c6fe427130f777ad1e8c')
    version('2019.01.06', sha256='17195c833098da79de5778ee90948f4c5d90ed1a0cf8391b4ab348e2ec511e3f')
