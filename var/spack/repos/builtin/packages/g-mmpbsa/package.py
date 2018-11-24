# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class GMmpbsa(CMakePackage):
    "g_mmpbsa is a gromacs tool for high-throughput MM-PBSA calculations."

    homepage = "http://rashmikumari.github.io/g_mmpbsa/"
    url      = "https://github.com/RashmiKumari/g_mmpbsa/archive/v1.1.0.tar.gz"

    version('master', git='https://github.com/RashmiKumari/g_mmpbsa.git', tag='master')

    depends_on('gromacs@:5.1.3')

    # def patch(self):
    #     # Replace lib/pkgconfig with lib64/pkgconfig in search path
    #     findgromacs = FileFilter('cmake/FindGROMACS.cmake')
    #     findgromacs.filter('lib/pkgconfig', 'lib64/pkgconfig', string=True)

    def cmake_args(self):
        spec = self.spec
        return ["-DGMX_PATH=%s" % spec['gromacs'].prefix]
