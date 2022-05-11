# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package_defs import *


class Alpaka(CMakePackage, CudaPackage):
    """Abstraction Library for Parallel Kernel Acceleration."""

    homepage = "https://alpaka.readthedocs.io"
    url      = "https://github.com/alpaka-group/alpaka/archive/refs/tags/0.6.0.tar.gz"
    git      = "https://github.com/alpaka-group/alpaka.git"

    maintainers = ['vvolkl']

    version('develop', branch='develop')
    version('0.8.0', sha256='e01bc377a7657d9a3e0c5f8d3f83dffbd7d0b830283c59efcbc1fb98cf88de43')
    version('0.7.0', sha256='4b61119a7b3b073f281ba15b63430db98b77dbd9420bc290a114f80121fbdd97')
    version('0.6.0', sha256='7424ecaee3af15e587b327e983998410fa379c61d987bfe923c7e95d65db11a3')
    version('0.5.0', sha256='0ba08ea19961dd986160219ba00d6162fe7758980d88a606eff6494d7b3a6cd1')
    version('0.4.0', sha256='ad7905b13c22abcee4344ba225a65078e3f452ad45a9eda907e7d27c08315e46')

    variant("backend", multi=True, values=('serial', 'threads', 'fiber', 'tbb', 'omp2_gridblock', 'omp2_blockthread', 'omp5', 'oacc', 'cuda', 'cuda_only', 'hip', 'hip_only'), description="Backends to enable", default='serial')

    variant("examples", default=False, description="Build alpaka examples")

    depends_on('boost')
    depends_on('boost+fiber', when="backend=fiber")
    depends_on('cmake@3.18:', when='@0.7.0:')

    # make sure no other backend is enabled if using cuda_only or hip_only
    for v in ('serial', 'threads', 'fiber', 'tbb', 'oacc',
              'omp2_gridblock', 'omp2_blockthread', 'omp5', 'cuda', 'hip'):
        conflicts('backend=cuda_only,%s' % v)
        conflicts('backend=hip_only,%s' % v)
    conflicts('backend=cuda_only,hip_only')
    for v in ('omp2_blockthread', 'omp2_blockthread', 'omp5'):
        conflicts('backend=oacc,%s' % v)

    # todo: add conflict between cuda 11.3 and gcc 10.3.0
    # see https://github.com/alpaka-group/alpaka/issues/1297

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
        args.append(self.define("BUILD_TESTING", self.run_tests))
        return args
