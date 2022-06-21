# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import shutil
import sys

from spack.package import *


class VtkM(CMakePackage, CudaPackage, ROCmPackage):
    """VTK-m is a toolkit of scientific visualization algorithms for emerging
    processor architectures. VTK-m supports the fine-grained concurrency for
    data analysis and visualization algorithms required to drive extreme scale
    computing by providing abstract models for data and execution that can be
    applied to a variety of algorithms across many different processor
    architectures."""

    homepage = "https://m.vtk.org/"
    maintainers = ['kmorel', 'vicentebolea']

    url      = "https://gitlab.kitware.com/vtk/vtk-m/-/archive/v1.5.1/vtk-m-v1.5.1.tar.gz"
    git      = "https://gitlab.kitware.com/vtk/vtk-m.git"
    tags     = ['e4s']

    version('master', branch='master')
    version('release', branch='release')
    version('1.8.0-rc1', sha256="99e344c89ecb84b04cc0f0b9fdf042b9a4ae3144bb4deeca8e90f098ab8a569b")
    version('1.7.1', sha256="7ea3e945110b837a8c2ba49b41e45e1a1d8d0029bb472b291f7674871dbbbb63", preferred=True)
    version('1.7.0', sha256="a86667ac22057462fc14495363cfdcc486da125b366cb568ec23c86946439be4")
    version('1.6.0', sha256="14e62d306dd33f82eb9ddb1d5cee987b7a0b91bf08a7a02ca3bce3968c95fd76")
    version('1.5.5', commit="d2d1c854adc8c0518802f153b48afd17646b6252")
    version('1.5.4', commit="bbba2a1967b271cc393abd043716d957bca97972")
    version('1.5.3', commit="a3b8525ef97d94996ae843db0dd4f675c38e8b1e")
    version('1.5.2', commit="c49390f2537c5ba8cf25bd39aa5c212d6eafcf61")
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

    variant("doubleprecision", default=True,
            description='enable double precision')
    variant("logging", default=False, description="build logging support")
    variant("ascent_types", default=True, description="build support for ascent types")
    variant("virtuals", default=False, description="enable support for deprecated virtual functions")
    variant("mpi", default=False, description="build mpi support")
    variant("rendering", default=True, description="build rendering support")
    variant("64bitids", default=False,
            description="enable 64 bits ids")
    variant("testlib", default=False, description="build test library")
    variant("fpic", default=False, description="build fpic support")

    # Device variants
    # CudaPackage provides cuda variant
    # ROCmPackage provides rocm variant
    variant("kokkos", default=False, when='@1.6:', description="build using Kokkos backend")
    variant("cuda_native", default=True, description="build using native cuda backend", when="+cuda")
    variant("openmp", default=(sys.platform != 'darwin'), description="build openmp support")
    variant("tbb", default=(sys.platform == 'darwin'), description="build TBB support")

    depends_on("cmake@3.12:", type="build")               # CMake >= 3.12
    depends_on("cmake@3.18:", when="+rocm", type="build")  # CMake >= 3.18

    conflicts('%gcc@:4.10',
              msg='vtk-m requires gcc >= 5. Please install a newer version')

    depends_on('cuda@10.1.0:', when='+cuda_native')
    depends_on("tbb", when="+tbb")
    depends_on("mpi", when="+mpi")

    # VTK-m uses the default Kokkos backend
    depends_on('kokkos', when='+kokkos')
    # VTK-m native CUDA and Kokkos CUDA backends are not compatible
    depends_on('kokkos ~cuda', when='+kokkos +cuda +cuda_native')
    depends_on('kokkos +cuda', when='+kokkos +cuda ~cuda_native')
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on("kokkos cuda_arch=%s" % cuda_arch, when="+kokkos +cuda ~cuda_native cuda_arch=%s" % cuda_arch)
    # VTK-m uses the Kokkos HIP backend.
    # If Kokkos provides multiple backends, the HIP backend may or
    # may not be used for VTK-m depending on the default selected by Kokkos
    depends_on('kokkos +rocm', when='+kokkos +rocm')
    # Propagate AMD GPU target to kokkos for +rocm
    for amdgpu_value in ROCmPackage.amdgpu_targets:
        depends_on("kokkos amdgpu_target=%s" % amdgpu_value, when="+kokkos +rocm amdgpu_target=%s" % amdgpu_value)

    depends_on("hip@3.7:", when="+rocm")

    # The rocm variant is only valid options for >= 1.7. It would be better if
    # this could be expressed as a when clause to disable the rocm variant,
    # but that is not currently possible since when clauses are stacked,
    # not overwritten.
    conflicts('+rocm', when='@:1.6')
    conflicts("+rocm", when="+cuda")
    conflicts("+rocm", when="~kokkos", msg="VTK-m does not support HIP without Kokkos")

    # Can build +shared+cuda after @1.7:
    conflicts("+shared", when="@:1.6 +cuda_native")
    conflicts("+cuda~cuda_native~kokkos", msg="Cannot have +cuda without a cuda device")
    conflicts("+cuda~cuda_native", when="@:1.5", msg="Cannot have +cuda without a cuda device")

    conflicts("+cuda", when="cuda_arch=none",
              msg="vtk-m +cuda requires that cuda_arch be set")

    def cmake_args(self):
        spec = self.spec
        options = []
        gpu_name_table = {'30': 'kepler',  '32': 'kepler',  '35': 'kepler',
                          '50': 'maxwell', '52': 'maxwell', '53': 'maxwell',
                          '60': 'pascal',  '61': 'pascal',  '62': 'pascal',
                          '70': 'volta',   '72': 'turing',  '75': 'turing',
                          '80': 'ampere',  '86': 'ampere'}
        with working_dir('spack-build', create=True):
            options = ["-DVTKm_ENABLE_TESTING:BOOL=OFF"]
            # shared vs static libs logic
            # force building statically with cuda
            if "+shared" in spec:
                options.append('-DBUILD_SHARED_LIBS=ON')
            else:
                options.append('-DBUILD_SHARED_LIBS=OFF')

            # double precision
            if "+doubleprecision" in spec:
                options.append("-DVTKm_USE_DOUBLE_PRECISION:BOOL=ON")
            else:
                options.append("-DVTKm_USE_DOUBLE_PRECISION:BOOL=OFF")

            # logging support
            if "+logging" in spec:
                if not spec.satisfies('@1.3.0:'):
                    raise InstallError('logging is not supported for\
                            vtkm version lower than 1.3')
                options.append("-DVTKm_ENABLE_LOGGING:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_LOGGING:BOOL=OFF")

            # mpi support
            if "+mpi" in spec:
                if not spec.satisfies('@1.3.0:'):
                    raise InstallError('mpi is not supported for\
                            vtkm version lower than 1.3')
                options.append("-DVTKm_ENABLE_MPI:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_MPI:BOOL=OFF")

            # rendering support
            if "+rendering" in spec:
                options.append("-DVTKm_ENABLE_RENDERING:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_RENDERING:BOOL=OFF")

            # Support for ascent types
            if "+ascent_types" in spec:
                options.append("-DVTKm_USE_DEFAULT_TYPES_FOR_ASCENT:BOOL=ON")
            else:
                options.append("-DVTKm_USE_DEFAULT_TYPES_FOR_ASCENT:BOOL=OFF")

            # Support for deprecated virtual functions
            if "+virtuals" in spec:
                options.append("-DVTKm_NO_DEPRECATED_VIRTUAL:BOOL=OFF")
            else:
                options.append("-DVTKm_NO_DEPRECATED_VIRTUAL:BOOL=ON")

            # 64 bit ids
            if "+64bitids" in spec:
                options.append("-DVTKm_USE_64BIT_IDS:BOOL=ON")
                print("64 bit ids enabled")
            else:
                options.append("-DVTKm_USE_64BIT_IDS:BOOL=OFF")

            # Support for the testing header files
            if "+testlib" in spec and spec.satisfies('@1.7.0:'):
                options.append("-DVTKm_ENABLE_TESTING_LIBRARY:BOOL=ON")

            if spec.variants["build_type"].value != 'Release':
                options.append("-DVTKm_NO_ASSERT:BOOL=ON")

            # Support for relocatable code
            if "~shared" in spec and "+fpic" in spec:
                options.append("-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON")

            # cuda support
            if "+cuda_native" in spec:
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
                    # no devices (this is common for front end nodes on hpc
                    # clusters). We choose volta as a lowest common denominator
                    options.append("-DVTKm_CUDA_Architecture=volta")
            else:
                options.append("-DVTKm_ENABLE_CUDA:BOOL=OFF")

            # hip support
            if "+rocm" in spec:
                options.append("-DVTKm_NO_DEPRECATED_VIRTUAL:BOOL=ON")

                archs = ",".join(self.spec.variants['amdgpu_target'].value)
                options.append(
                    "-DCMAKE_HIP_ARCHITECTURES:STRING={0}".format(archs))

            # openmp support
            if "+openmp" in spec:
                # openmp is added since version 1.3.0
                if not spec.satisfies('@1.3.0:'):
                    raise InstallError('OpenMP is not supported for\
                            vtkm version lower than 1.3')
                options.append("-DVTKm_ENABLE_OPENMP:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_OPENMP:BOOL=OFF")

            if "+kokkos" in spec:
                options.append("-DVTKm_ENABLE_KOKKOS:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_KOKKOS:BOOL=OFF")

            # tbb support
            if "+tbb" in spec:
                # vtk-m detectes tbb via TBB_ROOT env var
                os.environ["TBB_ROOT"] = spec["tbb"].prefix
                options.append("-DVTKm_ENABLE_TBB:BOOL=ON")
            else:
                options.append("-DVTKm_ENABLE_TBB:BOOL=OFF")

            return options

    def smoke_test(self):
        print("Checking VTK-m installation...")
        spec = self.spec
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            source = r"""
#include <vtkm/cont/Algorithm.h>
#include <vtkm/cont/ArrayHandle.h>
#include <vtkm/cont/Initialize.h>

#include <iostream>
#include <vector>

struct NoArgKernel {
    VTKM_EXEC void operator()(vtkm::Id) const {}

    void SetErrorMessageBuffer(
        const vtkm::exec::internal::ErrorMessageBuffer &errorMessage) {
      this->ErrorMessage = errorMessage;
    }

    vtkm::exec::internal::ErrorMessageBuffer ErrorMessage;
};

template <typename PortalType> struct FillArrayKernel {
    using ValueType = typename PortalType::ValueType;

    FillArrayKernel(const PortalType &array, ValueType fill)
        : Array(array), FillValue(fill) {}

    VTKM_EXEC void operator()(vtkm::Id index) const {
      this->Array.Set(index, this->FillValue);
    }
    void SetErrorMessageBuffer(
        const vtkm::exec::internal::ErrorMessageBuffer &) {
    }

    PortalType Array;
    ValueType FillValue;
};


int main() {
    vtkm::cont::Initialize();

    constexpr vtkm::Id size = 1000000;
#if defined(VTKM_ENABLE_KOKKOS)
    constexpr vtkm::cont::DeviceAdapterTagKokkos desired_device;
#elif defined(VTKM_ENABLE_CUDA)
    constexpr vtkm::cont::DeviceAdapterTagCuda desired_device;
#elif defined(VTKM_ENABLE_TBB)
    constexpr vtkm::cont::DeviceAdapterTagTBB desired_device;
#elif defined(VTKM_ENABLE_OPENMP)
    constexpr vtkm::cont::DeviceAdapterTagOpenMP desired_device;
#else
    #error "No VTK-m Device Adapter enabled"
#endif

    std::cout << "-------------------------------------------\n";
    std::cout << "Testing No Argument Kernel" << std::endl;
    vtkm::cont::Algorithm::Schedule(desired_device, NoArgKernel(), size);

    vtkm::cont::ArrayHandle<vtkm::Id> handle;
    {
    std::cout << "-------------------------------------------\n";
    std::cout << "Testing Kernel + ArrayHandle PrepareForOutput" << std::endl;
    vtkm::cont::Token token;
    auto portal = handle.PrepareForOutput(size, desired_device, token);
    vtkm::cont::Algorithm::Schedule(desired_device,
        FillArrayKernel<decltype(portal)>{portal, 1}, size);
    }

    {
    std::cout << "-------------------------------------------\n";
    std::cout << "Testing Kernel + ArrayHandle PrepareForInPlace" << std::endl;
    vtkm::cont::Token token;
    auto portal = handle.PrepareForInPlace(desired_device, token);
    vtkm::cont::Algorithm::Schedule(desired_device,
        FillArrayKernel<decltype(portal)>{portal, 2}, size);
    }

    std::cout << "-------------------------------------------\n";
    std::cout << "Ran tests on: " << desired_device.GetName() << std::endl;

    return 0;
}
"""

            cmakelists = r"""
##============================================================================
##  Copyright (c) Kitware, Inc.
##  All rights reserved.
##  See LICENSE.txt for details.
##
##  This software is distributed WITHOUT ANY WARRANTY; without even
##  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
##  PURPOSE.  See the above copyright notice for more information.
##============================================================================
cmake_minimum_required(VERSION 3.12...3.18 FATAL_ERROR)
project(VTKmSmokeTest CXX)

#Find the VTK-m package
find_package(VTKm REQUIRED QUIET)

add_executable(VTKmSmokeTest main.cxx)
target_link_libraries(VTKmSmokeTest PRIVATE vtkm_cont)
vtkm_add_target_information(VTKmSmokeTest
                            DROP_UNUSED_SYMBOLS MODIFY_CUDA_FLAGS
                            DEVICE_SOURCES main.cxx)
"""

            with open("main.cxx", 'w') as f:
                f.write(source)
            with open("CMakeLists.txt", 'w') as f:
                f.write(cmakelists)
            builddir = "build"
            with working_dir(builddir, create=True):
                cmake = Executable(spec['cmake'].prefix.bin + "/cmake")
                cmakefiledir = spec['vtk-m'].prefix.lib + "/cmake"
                cmakefiledir = cmakefiledir + "/" + os.listdir(cmakefiledir)[0]
                cmake(*(["..", "-DVTKm_DIR=" + cmakefiledir]))
                cmake(*(["--build", "."]))
                try:
                    test = Executable('./VTKmSmokeTest')
                    output = test(output=str)
                except ProcessError:
                    output = ""
                print(output)
                if "+cuda_native" in spec:
                    expected_device = 'Cuda'
                elif "+kokkos" in spec:
                    expected_device = 'Kokkos'
                elif "+tbb" in spec:
                    expected_device = 'TBB'
                elif "+openmp" in spec:
                    expected_device = 'OpenMP'
                expected = """\
-------------------------------------------
Testing No Argument Kernel
-------------------------------------------
Testing Kernel + ArrayHandle PrepareForOutput
-------------------------------------------
Testing Kernel + ArrayHandle PrepareForInPlace
-------------------------------------------
Ran tests on: """ + expected_device + "\n"
                success = output == expected
                if success:
                    print("Test success")
                if not success:
                    print("Produced output does not match expected output.")
                    print("Expected output:")
                    print('-' * 80)
                    print(expected)
                    print('-' * 80)
                    print("Produced output:")
                    print('-' * 80)
                    print(output)
                    print('-' * 80)
                    raise RuntimeError("VTK-m install check failed")
        shutil.rmtree(checkdir)

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        spec = self.spec
        if "@master" in spec:
            self.smoke_test()
