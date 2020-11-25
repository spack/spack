# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Prmon(CMakePackage):
    """Standalone monitor for process resource consumption."""

    homepage = "https://github.com/HSF/prmon/"
    url      = "https://github.com/HSF/prmon/archive/v1.1.1.tar.gz"
    git      = "https://github.com/HSF/prmon.git"

    maintainers = ['vvolkl']

    version("master", branch="master")
    version('1.1.1', sha256='5f074b05af2a12e2726c33f6a6e9e8e59ee0c4fb5fe056deb38abacd1bb6bf03')

    variant('plot', default=True,
            description='Make use of plotting scripts')

    depends_on('nlohmann-json')
    depends_on('cmake@3.3:', type="build")
    depends_on('py-matplotlib', type="run", when="+plot")
