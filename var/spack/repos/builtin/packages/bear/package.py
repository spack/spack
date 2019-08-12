# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bear(CMakePackage):
    """Bear is a tool that generates a compilation database for clang tooling
    from non-cmake build systems."""
    homepage = "https://github.com/rizsotto/Bear"
    url      = "https://github.com/rizsotto/Bear/archive/2.0.4.tar.gz"

    version('2.2.0', '87250cc3a9a697e7d1e8972253a35259')
    version('2.0.4', 'fd8afb5e8e18f8737ba06f90bd77d011')

    depends_on('python')
    depends_on('cmake@2.8:', type='build')
