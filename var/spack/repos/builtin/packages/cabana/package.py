# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cabana(CMakePackage):
    """The Exascale Co-Design Center for Particle Applications Toolkit
    """
    homepage = "https://github.com/ECP-copa/Cabana"
    git      = "https://github.com/ECP-copa/Cabana.git"
    url      = "https://github.com/ECP-copa/Cabana/archive/0.1.0.tar.gz"

    version('develop', branch='master')
    version('0.1.0', sha256='3280712facf6932b9d1aff375b24c932abb9f60a8addb0c0a1950afd0cb9b9cf')
    version('0.1.0-rc0', sha256='73754d38aaa0c2a1e012be6959787108fec142294774c23f70292f59c1bdc6c5')

    variant('serial', default=True, description="enable Serial backend (default)")
    variant('openmp', default=False, description="enable OpenMP backend")
    variant('cuda', default=False, description="enable Cuda backend")

    depends_on("cmake@3.9:", type='build')
    depends_on("kokkos+serial", when="+serial")
    depends_on("kokkos+openmp", when="+openmp")
    depends_on("kokkos+cuda", when="+cuda")

    def cmake_args(self):
        options = [
            '-DCabana_ENABLE_TESTING=ON',
            '-DCabana_ENABLE_Serial=%s'  % (
                'On' if '+serial'  in self.spec else 'Off'),
            '-DCabana_ENABLE_OpenMP=%s'  % (
                'On' if '+openmp'  in self.spec else 'Off'),
            '-DCabana_ENABLE_Cuda=%s'  % (
                'On' if '+cuda'  in self.spec else 'Off')
        ]

        return options
