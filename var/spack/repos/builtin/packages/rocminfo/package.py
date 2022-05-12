# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rocminfo(CMakePackage):
    """Radeon Open Compute (ROCm) Runtime rocminfo tool"""

    homepage = "https://github.com/RadeonOpenCompute/rocminfo"
    git      = "https://github.com/RadeonOpenCompute/rocminfo.git"
    url      = "https://github.com/RadeonOpenCompute/rocminfo/archive/rocm-5.0.2.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    version('master', branch='master')

    version('5.1.0', sha256='76f6cc9e69d9fc7e692e5c7db35e89079d3b1d2d47632e4742d612e743c396d3')
    version('5.0.2', sha256='5fd970f08c5d6591efe7379ece564ce5580cba87fb6237531dabbd5adcb6a899')
    version('5.0.0', sha256='43e025de31bffa335d9cb682649add886afdd02c92090ee63e9bf77b3aaaa75b')
    version('4.5.2', sha256='5ea839cd1f317cbc72ea1e3634a75f33a458ba0cb5bf48377f08bb329c29222d')
    version('4.5.0', sha256='421ed55192780eb478f0341fd1ce47a0dd3ffafbec9d7a02109a411878a58ee5')
    version('4.3.1', sha256='d042947d3f29e943a2e3294a2a2d759ca436cebe31151ce048e49bc4f02d6993')
    version('4.3.0', sha256='2cc1f251c0ed9c3ea413cc15cb5ce11559e4497540eebbf5e8dcfd52b03e53d1')
    version('4.2.0', sha256='6952b6e28128ab9f93641f5ccb66201339bb4177bb575b135b27b69e2e241996')
    version('4.1.0', sha256='5b994ad02b6d250160770f6f7730835f3a52127193ac9a8dee40c53aec911f4f', deprecated=True)
    version('4.0.0', sha256='0b3d692959dd4bc2d1665ab3a838592fcd08d2b5e373593b9192ca369e2c4aa7', deprecated=True)
    version('3.10.0', sha256='ed02375be3be518b83aea7309ef5ca62dc9b6dbad0aae33e92995102d6d660be', deprecated=True)
    version('3.9.0', sha256='9592781e0c62b910c4adc5c7f4c27c7a0cddbed13111a19dd91a2ff43720e43d', deprecated=True)
    version('3.8.0', sha256='c135dc98ecb5f420e22a6efd2f461ba9ed90be3f42e2ac29356e05c6a0706f8f', deprecated=True)
    version('3.7.0', sha256='86a8e3ce7d91fb2d79688a22a2805757c83922d9f17ea7ea1cb41bf9516197ea', deprecated=True)
    version('3.5.0', sha256='1d113f06b7c9b60d0e92b2c12c0c704a565696867496fe7038e5dddd510567b7', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2',
                '5.1.0', 'master']:
        depends_on('hsakmt-roct@' + ver, when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, when='@' + ver)

    def cmake_args(self):
        return [self.define('ROCM_DIR', self.spec['hsa-rocr-dev'].prefix)]
