# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Brayns(CMakePackage):
    """Interactive visualizer for large-scale scientific data
    """

    homepage = "https://github.com/BlueBrain/Brayns"
    git = "https://github.com/BlueBrain/Brayns.git"
    generator = 'Ninja'
    submodules = False

    version('develop', branch='develop')
    version('3.0.0', tag='3.0.0')

    variant('blueconfig', default=True, description='BlueConfig support')

    depends_on('cmake@3.15:', type='build')
    depends_on('ispc@1.18.0:', type='build')
    depends_on('ninja', type='build')
    depends_on('git', type='build')

    depends_on('brion@3.3.9:', when='+blueconfig')
    depends_on('libsonata@0.1.16:')
    depends_on('morphio@3.3.3:')
    depends_on('mvdtool@2.4.2:')
    depends_on('ospray@2.10.0')
    depends_on('rkcommon@1.10.0')
    depends_on('spdlog@1.9.2')
    depends_on('poco@1.11.1')
    depends_on('glm')
    depends_on('zlib')
    depends_on('bzip2')

    patch(
        "https://patch-diff.githubusercontent.com/raw/BlueBrain/Brayns/pull/1133.patch",
        sha256="a698a881dc2353dcf60a165f283017612d728c87a1b0abf8c24ec76a60bb8e6b",
        when="@3.0.0%gcc@12:",
    )

    def cmake_args(self):
        return [
            '-DBRAYNS_CIRCUITEXPLORER_ENABLED=ON',
            '-DBRAYNS_DTI_ENABLED=ON',
            '-DBRAYNS_ATLASEXPLORER_ENABLED=ON',
            '-DBRAYNS_CYLINDRICCAMERA_ENABLED=ON',
            '-DBRAYNS_MOLECULEEXPLORER_ENABLED=ON'
        ]

    def check(self):
        with working_dir(self.build_directory):
            ninja('tests')
