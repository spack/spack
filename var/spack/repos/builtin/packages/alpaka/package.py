# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Alpaka(CMakePackage, CudaPackage):
    """Abstraction Library for Parallel Kernel Acceleration."""

    homepage = "https://alpaka.readthedocs.io"
    url      = "https://github.com/alpaka-group/alpaka/archive/refs/tags/0.6.0.tar.gz"
    git      = "https://github.com/alpaka-group/alpaka.git"

    maintainers = ['vvolkl']

    version('develop', branch='develop')
    version('0.6.0', sha256='7424ecaee3af15e587b327e983998410fa379c61d987bfe923c7e95d65db11a3')

    variant("backend", multi=True, values=('serial', 'threads', 'fibers', 'tbb', 'omp2_gridblock', 'omp2_blockthread', 'cuda', 'cuda_only', 'hip', 'hip_only'), description="Backends to enable", default='serial')

    variant("examples", default=False, description="Build alpaka examples")

    depends_on('boost')

    # make sure no other backend is enabled if using cuda_only or hip_only
    for v in ('serial', 'threads', 'fibers', 'tbb',
              'omp2_gridblock', 'omp2_blockthread',):
        conflicts('backend=cuda_only backend=%s' % v)
    conflicts('backend=cuda_only backend=hip_only')

    def cmake_args(self):
        spec = self.spec
        args = []
        if 'backend=serial' in spec:
            args.append(self.define("ALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLE", True))
        if 'backend=threads' in self.spec:
            args.append(self.define("ALPAKA_ACC_CPU_B_SEQ_T_THREADS_ENABLE", True))
        if 'backend=fiber' in spec:
            args.append(self.define("ALPAKA_ACC_CPU_B_SEQ_T_FIBERS_ENABLE", True))
        if 'backend=tbb' in spec:
            args.append(self.define("ALPAKA_ACC_CPU_B_TBB_T_SEQ_ENABLE", True))
        if 'backend=omp2_gridblock' in spec:
            args.append(self.define("ALPAKA_ACC_CPU_B_OMP2_T_SEQ_ENABLE", True))
        if 'backend=omp2_blockthread' in spec:
            args.append(self.define("ALPAKA_ACC_CPU_B_SEQ_T_OMP2_ENABLE", True))
        if 'backend=omp5' in spec:
            args.append(self.define("ALPAKA_ACC_ANY_BT_OMP5_ENABLE", True))
        if 'backend=oacc' in spec:
            args.append(self.define("ALPAKA_ACC_ANY_BT_OACC_ENABLE", True))
        if 'backend=cuda' in spec:
            args.append(self.define("ALPAKA_ACC_GPU_CUDA_ENABLE", True))
        if 'backend=cuda_only' in spec:
            args.append(self.define("ALPAKA_ACC_GPU_CUDA_ENABLE", True))
            args.append(self.define("ALPAKA_ACC_GPU_CUDA_ONLY_MODE", True))
        if 'backend=hip' in spec:
            args.append(self.define("ALPAKA_ACC_GPU_HIP_ENABLE", True))
        if 'backend=hip_only' in spec:
            args.append(self.define("ALPAKA_ACC_GPU_HIP_ENABLE", True))
            args.append(self.define("ALPAKA_ACC_GPU_HIP_ONLY_MODE", True))

        args.append(self.define_from_variant("alpaka_BUILD_EXAMPLES",
                                             "examples"))
        # need to define, as it is explicitly declared as an option by alpaka:
        ags.append(self.define("BUILD_TESTING", self.run_tests))
        return args
