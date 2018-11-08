# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Typhon(CMakePackage):
    """
    Typhon is a distributed communications library for unstructured mesh
    applications.
    """

    homepage = "https://github.com/UK-MAC/Typhon"
    url      = "https://github.com/UK-MAC/Typhon/archive/v3.0.tar.gz"
    git      = "https://github.com/UK-MAC/Typhon.git"

    version('develop', branch='develop')

    version('3.0.2', sha256='28087eb07bf91d23792900214728b5eea61b5e81aa33df28c032dadd6d89b76e')
    version('3.0.1', '89045decfba5fd468ef05ad4c924df8c')
    version('3.0', 'ec67cd1aa585ce2410d4fa50514a916f')

    depends_on('mpi')
