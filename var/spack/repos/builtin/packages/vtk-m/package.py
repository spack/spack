# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os
import sys


class VtkM(CMakePackage, CudaPackage):
    """VTK-m is a toolkit of scientific visualization algorithms for emerging
    processor architectures. VTK-m supports the fine-grained concurrency for
    data analysis and visualization algorithms required to drive extreme scale
    computing by providing abstract models for data and execution that can be
    applied to a variety of algorithms across many different processor
    architectures."""

    homepage = "https://m.vtk.org/"
    maintainers = ['robertmaynard', 'kmorel', 'vicentebolea']

    url      = "https://gitlab.kitware.com/vtk/vtk-m/-/archive/v1.5.1/vtk-m-v1.5.1.tar.gz"
    git      = "https://gitlab.kitware.com/vtk/vtk-m.git"

    version('master', branch='master')
    version('1.5.1', sha256="64c19e66c0d579cfb21bb0df10d649b523b470b0c9a6c2ea5fd979dfeda2c25e")
    version('1.5.0', sha256="b1b13715c7fcc8d17f5c7166ff5b3e9025f6865dc33eb9b06a63471c21349aa8")
    version('1.4.0', sha256="8d83cca7cd5e204d10da151ce4f1846c1f7414c7c1e579173d15c5ea0631555a")
    version('1.3.0', sha256="f88c1b0a1980f695240eeed9bcccfa420cc089e631dc2917c9728a2eb906df2e")
    version('1.2.0', sha256="607272992e05f8398d196f0acdcb4af025a4a96cd4f66614c6341f31d4561763")
    version('1.1.0', sha256="78618c81ca741b1fbba0853cb5d7af12c51973b514c268fc96dfb36b853cdb18")

    # use release, instead of release with debug symbols b/c vtkm libs
    # can overwhelm compilers with too many symbols
    variant('build_type', default='Release', description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant("shared", default=False, description="build shared libs")
    variant("cuda", default=False, description="build cuda support")
    variant("doubleprecision", default=True,
            description='enable double precision')
    variant("logging", default=False, description="build logging support")
    variant("mpi", default=False, description="build mpi support")
    variant("openmp", default=(sys.platform != 'darwin'), description="build openmp support")
    variant("rendering", default=True, description="build rendering support")
    variant("tbb", default=(sys.platform == 'darwin'), description="build TBB support")
    variant("64bitids", default=False,
            description="enable 64 bits ids")

    depends_on("cmake@3.12:", type="build")         # CMake >= 3.12
    depends_on("tbb", when="+tbb")
    depends_on("cuda", when="+cuda")
    depends_on("mpi", when="+mpi")

    conflicts("~shared", when="~pic")

    def cmake_args(self):
        spec = self.spec
        options = []
        gpu_name_table = {'20': 'fermi',
                          '30': 'kepler',  '32': 'kepler',  '35': 'kepler',
                          '50': 'maxwell', '52': 'maxwell', '53': 'maxwell',
                          '60': 'pascal',  '61': 'pascal',  '62': 'pascal',
                          '70': 'volta',   '72': 'turing',  '75': 'turing'}
        with working_dir('spack-build', create=True):
            options = ["-DVTKm_ENABLE_TESTING:BOOL=OFF"]
            # shared vs static libs logic
            # force building statically with cuda
            if "+cuda" in spec:
                options.append('-DBUILD_SHARED_LIBS=OFF')
            else:
                if "+shared" in spec:
                    options.append('-DBUILD_SHARED_LIBS=ON')
                else:
                    options.append('-DBUILD_SHARED_LIBS=OFF')
            # cuda support
            if "+cuda" in spec:
                options.append("-DVTKm_ENABLE_CUDA:BOOL=ON")
                options.append("-DCMAKE_CUDA_HOST_COMPILER={0}".format(
                               env["SPACK_CXX"]))
                if 'cuda_arch' in spec.variants:
                    cuda_value = spec.variants['cuda_arch'].value
                    cuda_arch = cuda_value[0]
                    if cuda_arch in gpu_name_table:
                        vtkm_cuda_arch = gpu_name_table[cuda_arch]
                        options.append('-DVTKm_CUDA_Architecture={0}'.format(
                                       vtkm_cuda_arch))
                else:
                    # this fix is necessary if compiling platform has cuda, but
                    # no devices (this's common for front end nodes on hpc clus
                    # ters)
                    # we choose kepler as a lowest common denominator
                    options.append("-DVTKm_CUDA_Architecture=kepler")
            else:
                options.append("-DVTKm_ENABLE_CUDA:BOOL=OFF")

            # double precision
            if "+doubleprecision" in spec:
                options.append("-DVTKm_USE_DOUBLE_PRECISION:BOOL=ON")
            else:
                options.append("-DVTKm_USE_DOUBLE_PRECISION:BOOL=OFF")

            # logging support
            if "+logging" in spec:
                if spec.satisfies('@:1.2.0'):
                    raise InstallError('logging is not supported for\
                            vtkm version lower than 1.3')
                options.append("-DVTKm_ENABLE_LOGGING:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_LOGGING:BOOL=OFF")

            # mpi support
            if "+mpi" in spec:
                if spec.satisfies('@:1.2.0'):
                    raise InstallError('mpi is not supported for\
                            vtkm version lower than 1.3')
                options.append("-DVTKm_ENABLE_MPI:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_MPI:BOOL=OFF")

            # openmp support
            if "+openmp" in spec:
                # openmp is added since version 1.3.0
                if spec.satisfies('@:1.2.0'):
                    raise InstallError('OpenMP is not supported for\
                            vtkm version lower than 1.3')
                options.append("-DVTKm_ENABLE_OPENMP:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_OPENMP:BOOL=OFF")

            # rendering support
            if "+rendering" in spec:
                options.append("-DVTKm_ENABLE_RENDERING:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_RENDERING:BOOL=OFF")

            # tbb support
            if "+tbb" in spec:
                # vtk-m detectes tbb via TBB_ROOT env var
                os.environ["TBB_ROOT"] = spec["tbb"].prefix
                options.append("-DVTKm_ENABLE_TBB:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_TBB:BOOL=OFF")

            # 64 bit ids
            if "+64bitids" in spec:
                options.append("-DVTKm_USE_64BIT_IDS:BOOL=ON")
                print("64 bit ids enabled")
            else:
                options.append("-DVTKm_USE_64BIT_IDS:BOOL=OFF")

            if spec.variants["build_type"].value != 'Release':
                options.append("-DVTKm_NO_ASSERT:BOOL=ON")

            return options
