# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os
import sys


class Vtkm(CMakePackage, CudaPackage):
    """VTK-m is a toolkit of scientific visualization algorithms for emerging
    processor architectures. VTK-m supports the fine-grained concurrency for
    data analysis and visualization algorithms required to drive extreme scale
    computing by providing abstract models for data and execution that can be
    applied to a variety of algorithms across many different processor
    architectures."""

    homepage = "https://m.vtk.org/"
    url      = "https://gitlab.kitware.com/api/v4/projects/vtk%2Fvtk-m/repository/archive.tar.gz?sha=v1.3.0"
    git      = "https://gitlab.kitware.com/vtk/vtk-m.git"

    version('master', branch='master')
    version('1.4.0', sha256="60e1ce73a8c6beda8aed5f2d3ae670b6b0c78c068c6eff4ece769e6d719d5065")
    version('1.3.0', sha256="72c2c8525a77a456fe0b6a1af0328dad6b9a688f402a3d3ebfa8942e0b5dba1a")
    version('1.2.0', sha256="9103d954284661f6f03e5b18be6d7bc94254603e6abc8fce67f617f4ad325a0e")
    version('1.1.0', sha256="a1746b1547d6fb901ea7d7ed50834e8832d6d41ddd497c84d02e1481100d43bc")

    # use release, instead of release with debug symbols b/c vtkm libs
    # can overwhelm compilers with too many symbols
    variant('build_type', default='Release', description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant("shared", default=False, description="build shared libs")
    variant("cuda", default=False, description="build cuda support")
    variant("doubleprecision", default=True,
            description='enable double precision')
    variant("logging", default=True, description="build logging support")
    variant("mpi", default=False, description="build mpi support")
    variant("openmp", default=(sys.platform != 'darwin'), description="build openmp support")
    variant("rendering", default=True, description="build rendering support")
    variant("tbb", default=(sys.platform == 'darwin'), description="build TBB support")
    variant("64bitids", default=False,
            description="enable 64 bits ids")

    depends_on("cmake")
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
                          '70': 'turing',  '72': 'turing',  '75': 'turing'}
        with working_dir('spack-build', create=True):
            options = ["-DVTKm_ENABLE_TESTING:BOOL=OFF"]
            # shared vs static libs
            if "+shared" in spec:
                options.append('-DBUILD_SHARED_LIBS=ON')
            else:
                options.append('-DBUILD_SHARED_LIBS=OFF')
            # cuda support
            if "+cuda" in spec:
                options.append("-DVTKm_ENABLE_CUDA:BOOL=ON")
                if 'cuda_arch' in spec.variants:
                    cuda_value = spec.variants['cuda_arch'].value
                    name = gpu_name_table[cuda_value[0]]
                    options.append(
                        '-DVTKm_CUDA_Architecture={0}'.format(name))
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
                if spec.satisfies('@:1.2.0') and \
                        spec['vtkm'].version.string != 'master':
                    raise InstallError('logging is not supported for\
                            vtkm version lower than 1.3')
                options.append("-DVTKm_ENABLE_LOGGING:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_LOGGING:BOOL=OFF")

            # mpi support
            if "+mpi" in spec:
                if spec.satisfies('@:1.2.0') and \
                        spec['vtkm'].version.string != 'master':
                    raise InstallError('mpi is not supported for\
                            vtkm version lower than 1.3')
                options.append("-DVTKm_ENABLE_MPI:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_MPI:BOOL=OFF")

            # openmp support
            if "+openmp" in spec:
                # openmp is added since version 1.3.0
                if spec.satisfies('@:1.2.0') and \
                        spec['vtkm'].version.string != 'master':
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
            return options
