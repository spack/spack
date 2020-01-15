# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Vecgeom(CMakePackage, CudaPackage):
    """The vectorized geometry library for particle-detector simulation
    (toolkits)."""

    homepage = "https://gitlab.cern.ch/VecGeom/VecGeom"
    url = "https://gitlab.cern.ch/VecGeom/VecGeom/-/archive/v1.1.5/VecGeom-v1.1.5.tar.gz"
    git = "https://gitlab.cern.ch/VecGeom/VecGeom.git"

    maintainers = ['sethrj']

    version('1.1.5', sha256='da674f3bbc75c30f56c1a2d251fa8930c899f27fa64b03a36569924030d87b95')
    version('1.1.3', tag='v01.01.03')
    version('1.0.1', sha256='1eae7ac9014c608e8d8db5568058b8c0fea1a1dc7a8f54157a3a1c997b6fd9eb')
    version('0.5.2', tag='v00.05.02',
            commit='a7e0828c915ff936a79e672d1dd84b087a323b51')
    version('0.3.rc', sha256='a87a9ea4ab126b59ff9c79182bc0911ead3d76dd197194742e2a35ccd341299d')

    _cxxstd_values = ('11', '14', '17')
    variant('cxxstd', default='14', values=_cxxstd_values, multi=False,
            description='Use the specified C++ standard when building')
    variant('gdml', default=True,
            description='Support Geant XML geometry descriptions')
    variant('shared', default=True,
            description='Build shared libraries')
    variant('root', default=True,
            description='Support ROOT geometry descriptions')

    depends_on('veccore@0.5.2', type=('build', 'link'), when='@1.1.0:')
    depends_on('veccore@0.4.2', type=('build', 'link'), when='@:1.0')
    depends_on('veccore+cuda', type=('build', 'link'), when='+cuda')

    for std in _cxxstd_values:
        depends_on('xerces-c cxxstd=' + std, when='+gdml cxxstd=' + std)
        depends_on('veccore cxxstd=' + std, when='cxxstd=' + std)
        depends_on('root cxxstd=' + std, when='+root cxxstd=' + std)

    def cmake_args(self):
        # Possible target options are from the main CMakeLists.txt, assuming
        # "best" is last
        target = self.spec.target
        vecgeom_arch = "sse2 sse3 ssse3 sse4.1 sse4.2 avx avx2".split()
        for feature in reversed(vecgeom_arch):
            if feature.replace('.', '_') in target:
                target_instructions = feature
                break
        else:
            # No features available (could be 'generic' arch)
            target_instructions = 'empty'

        define = CMakePackage.define
        options = [
            define('BACKEND', 'Scalar'),
            define('BUILD_TESTING', False),
            define('BUILTIN_VECCORE', False),
            define('CTEST', False),
            define('GEANT4', False),
            define('NO_SPECIALIZATION', True),
            define('VECGEOM_VECTOR', target_instructions),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('GDML'),
            self.define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
            self.define_from_variant('CUDA'),
            self.define_from_variant('CUDA_ARCH'),
            self.define_from_variant('ROOT'),
        ]

        if self.spec.satisfies("@:0.5.2"):
            options.extend([
                define('USOLIDS', True),
                define('USOLIDS_VECGEOM', True),
            ])

        return options
