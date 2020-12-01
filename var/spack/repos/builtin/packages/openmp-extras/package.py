# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

tools_url = 'https://github.com/ROCm-Developer-Tools'
compute_url = 'https://github.com/RadeonOpenCompute'

# 3.9 SHA Keys
openmp_extras39 = dict()
openmp_extras39 = {
    "aomp":
        "377ab59b685a73b3f95fba95f5e028678ec5aafabc4177b7f0ffb78da095d679",
    "devlib":
        "c99f45dacf5967aef9a31e3731011b9c142446d4a12bac69774998976f2576d7",
    "llvm":
        "1ff14b56d10c2c44d36c3c412b190d3d8cd1bb12cfc7cd58af004c16fd9987d1",
    "flang":
        "5d113f44fb173bd0d5704b282c5cebbb2aa642c7c29f188764bfa1daa58374c9",
    "extras":
        "830a37cf1c6700f81fc00749206a37e7cda4d2867bbdf489e9e2d81f52d06b3d"

}


class OpenmpExtras(Package):
    """OpenMP support for ROCm LLVM."""

    homepage = tools_url + "/aomp"
    url = tools_url + "/aomp/archive/rocm-uc-3.9.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'estewart08']
    version('3.9.0', sha256=openmp_extras39['aomp'])

    depends_on('cmake@3.5.2:3.13.4', type='build')
    depends_on('mesa18~llvm@18.3:', type=('build', 'link'))
    depends_on('py-setuptools@44.1.0', type='build')
    depends_on('python@3.8.6', type='build', when='@3.9.0')
    depends_on('perl-data-dumper', type='build')
    depends_on('awk', type='build')
    depends_on('elfutils', type=('build', 'link'))
    depends_on('libffi', type=('build', 'link'))

    for ver in ['3.9.0']:
        depends_on('hsakmt-roct@' + ver, type=('build', 'run'), when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type=('build', 'run'),
                   when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type=('build', 'run'),
                   when='@' + ver)

        if ver == '3.9.0':
            resource(
                name='rocm-device-libs',
                url=compute_url +
                '/ROCm-Device-Libs/archive/rocm-uc-3.9.0.tar.gz',
                sha256=openmp_extras39['devlib'],
                expand=True,
                destination='openmp-extras',
                placement='rocm-device-libs',
                when='@3.9.0')

            resource(
                name='flang',
                url=tools_url + '/flang/archive/rocm-uc-3.9.0.tar.gz',
                sha256=openmp_extras39['flang'],
                expand=True,
                destination='openmp-extras',
                placement='flang',
                when='@3.9.0')

            resource(
                name='aomp-extras',
                url=tools_url + '/aomp-extras/archive/rocm-uc-3.9.0.tar.gz',
                sha256=openmp_extras39['extras'],
                expand=True,
                destination='openmp-extras',
                placement='aomp-extras',
                when='@3.9.0')

            resource(
                name='llvm-project',
                url=compute_url + '/llvm-project/archive/rocm-3.9.0.tar.gz',
                sha256=openmp_extras39['llvm'],
                expand=True,
                destination='openmp-extras',
                placement='llvm-project',
                when='@3.9.0')

    def setup_run_environment(self, env):
        devlibs_prefix = self.spec['rocm-device-libs'].prefix
        openmp_extras_prefix = self.spec['openmp-extras'].prefix
        env.set('HIP_DEVICE_LIB_PATH',
                '{0}/amdgcn/bitcode'.format(format(devlibs_prefix)))
        env.set('AOMP', '{0}'.format(format(openmp_extras_prefix)))
        env.set('AOMP_GPU',
                '`{0}/rocm-bin/mygpu`'.format(format(openmp_extras_prefix)))

    def setup_build_environment(self, env):
        openmp_extras_prefix = self.spec['openmp-extras'].prefix
        env.set('AOMP', '{0}'.format(format(openmp_extras_prefix)))
        env.set('FC', '{0}/bin/flang'.format(format(openmp_extras_prefix)))
        env.set(
            'GFXLIST',
            'gfx700 gfx701 gfx801 gfx803 gfx900 gfx902 gfx906 gfx908')

    # This fix has not been applied to the llvm compiler as of 3.9.0.
    patch('fix-missing-arguments-assertion.patch',
          working_dir='openmp-extras/llvm-project', when='@3.9.0:')

    def patch(self):
        src = self.stage.source_path
        aomp_extras = '{0}/openmp-extras/aomp-extras/aomp-device-libs'
        libomptarget = '{0}/openmp-extras/llvm-project/openmp/libomptarget'
        flang = '{0}/openmp-extras/flang/'

        filter_file(
            '{ROCM_DIR}/amdgcn/bitcode', '{DEVICE_LIBS_DIR}',
            aomp_extras.format(src) + '/aompextras/CMakeLists.txt',
            aomp_extras.format(src) + '/libm/CMakeLists.txt',
            libomptarget.format(src) + '/deviceRTLs/amdgcn/CMakeLists.txt')

        # Openmp adjustments
        filter_file(
            '-nogpulib', '-nogpulib -nogpuinc',
            libomptarget.format(src) + '/deviceRTLs/amdgcn/CMakeLists.txt')

        filter_file(
            '-x hip', '-x hip -nogpulib -nogpuinc',
            libomptarget.format(src) + '/deviceRTLs/amdgcn/CMakeLists.txt')

        filter_file(
            '-c ', '-c -nogpulib -nogpuinc -I{LIMIT}',
            libomptarget.format(src) + '/hostrpc/CMakeLists.txt')

        filter_file(
            r'\${ROCM_DIR}/hsa/include \${ROCM_DIR}/hsa/include/hsa',
            '${HSA_INCLUDE}/hsa/include ${HSA_INCLUDE}/hsa/include/hsa',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '{ROCM_DIR}/hsa/lib', '{HSA_LIB}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            r'{ROCM_DIR}/lib\)',
            '{HSAKMT_LIB})\nset(HSAKMT_LIB64 ${HSAKMT_LIB64})',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            r'-L\${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}',
            '-L${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS} -L${HSAKMT_LIB64}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            r'-rpath,\${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}',
            '-rpath,${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}' +
            ',-rpath,${HSAKMT_LIB64}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '{ROCM_DIR}/include', '{COMGR_INCLUDE}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '{ROCM_DIR}/include', '{COMGR_INCLUDE}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            r'-L\${LLVM_LIBDIR}\${OPENMP_LIBDIR_SUFFIX}',
            '-L${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX} -L${COMGR_LIB}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            r'rpath,\${LLVM_LIBDIR}\${OPENMP_LIBDIR_SUFFIX}',
            'rpath,${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}' +
            '-Wl,-rpath,${COMGR_LIB}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            'ADDITIONAL_VERSIONS 2.7', 'ADDITIONAL_VERSIONS 3',
            flang.format(src) + 'CMakeLists.txt')

    def install(self, spec, prefix):
        src = self.stage.source_path
        gfx_list = "gfx700;gfx701;gfx801;gfx803;gfx900;gfx902;gfx906;gfx908"
        openmp_extras_prefix = self.spec['openmp-extras'].prefix
        devlibs_prefix = self.spec['rocm-device-libs'].prefix
        hsa_prefix = self.spec['hsa-rocr-dev'].prefix
        hsakmt_prefix = self.spec['hsakmt-roct'].prefix
        comgr_prefix = self.spec['comgr'].prefix
        llvm_inc = '/openmp-extras/llvm-project/llvm/include'
        bin_dir = '{0}/bin'.format(openmp_extras_prefix)
        components = dict()

        components['llvm'] = [
            '../openmp-extras/llvm-project/llvm',
            '-DLLVM_ENABLE_PROJECTS=clang;lld;clang-tools-extra;compiler-rt',
            '-DCMAKE_C_COMPILER={0}'.format(self.compiler.cc),
            '-DCMAKE_CXX_COMPILER={0}'.format(self.compiler.cxx),
            '-DCMAKE_ASM_COMPILER={0}'.format(self.compiler.cc),
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;X86',
            '-DLLVM_ENABLE_ASSERTIONS=1'
        ]

        components['aomp-extras'] = [
            '../openmp-extras/aomp-extras',
            '-DLLVM_DIR={0}'.format(openmp_extras_prefix),
            '-DDEVICE_LIBS_DIR={0}/amdgcn/bitcode'.format(devlibs_prefix),
            '-DAOMP_STANDALONE_BUILD=0',
            '-DDEVICELIBS_ROOT={0}/openmp-extras/rocm-device-libs'.format(src),
            '-DNEW_BC_PATH=1',
            '-DAOMP={0}'.format(openmp_extras_prefix),
            '-DCMAKE_VERBOSE_MAKEFILE=1'
        ]

        components['openmp'] = [
            '../openmp-extras/llvm-project/openmp',
            '-DROCM_DIR={0}'.format(hsa_prefix),
            '-DDEVICE_LIBS_DIR={0}/amdgcn/bitcode'.format(devlibs_prefix),
            '-DAOMP_STANDALONE_BUILD=0',
            '-DDEVICELIBS_ROOT={0}/openmp-extras/rocm-device-libs'.format(src),
            '-DOPENMP_TEST_C_COMPILER=$AOMP/bin/clang',
            '-DOPENMP_TEST_CXX_COMPILER=$AOMP/bin/clang++',
            '-DLIBOMPTARGET_AMDGCN_GFXLIST={0}'.format(gfx_list),
            '-DLIBOMP_COPY_EXPORTS=OFF',
            '-DHSA_INCLUDE={0}'.format(hsa_prefix),
            '-DHSA_LIB={0}/lib'.format(hsa_prefix),
            '-DHSAKMT_LIB={0}/lib'.format(hsakmt_prefix),
            '-DHSAKMT_LIB64={0}/lib64'.format(hsakmt_prefix),
            '-DCOMGR_INCLUDE={0}/include'.format(comgr_prefix),
            '-DCOMGR_LIB={0}/lib'.format(comgr_prefix),
            '-DOPENMP_ENABLE_LIBOMPTARGET=1',
            '-DOPENMP_ENABLE_LIBOMPTARGET_HSA=1',
            '-DLLVM_MAIN_INCLUDE_DIR={0}{1}'.format(src, llvm_inc),
            '-DLLVM_INSTALL_PREFIX={0}'.format(openmp_extras_prefix)
        ]

        components['openmp-debug'] = [
            '../openmp-extras/llvm-project/openmp',
            '-DROCM_DIR={0}'.format(hsa_prefix),
            '-DDEVICE_LIBS_DIR={0}/amdgcn/bitcode'.format(devlibs_prefix),
            '-DAOMP_STANDALONE_BUILD=0',
            '-DDEVICELIBS_ROOT={0}/openmp-extras/rocm-device-libs'.format(src),
            '-DOPENMP_TEST_C_COMPILER=$AOMP/bin/clang',
            '-DOPENMP_TEST_CXX_COMPILER=$AOMP/bin/clang++',
            '-DLIBOMPTARGET_AMDGCN_GFXLIST={0}'.format(gfx_list),
            '-DLIBOMP_COPY_EXPORTS=OFF',
            '-DHSA_INCLUDE={0}'.format(hsa_prefix),
            '-DHSA_LIB={0}/lib'.format(hsa_prefix),
            '-DHSAKMT_LIB={0}/lib'.format(hsakmt_prefix),
            '-DHSAKMT_LIB64={0}/lib64'.format(hsakmt_prefix),
            '-DCOMGR_INCLUDE={0}/include'.format(comgr_prefix),
            '-DCOMGR_LIB={0}/lib'.format(comgr_prefix),
            '-DLIBOMPTARGET_NVPTX_DEBUG=ON',
            '-DOPENMP_ENABLE_LIBOMPTARGET=1',
            '-DOPENMP_ENABLE_LIBOMPTARGET_HSA=1',
            '-DLLVM_MAIN_INCLUDE_DIR={0}{1}'.format(src, llvm_inc),
            '-DLLVM_INSTALL_PREFIX={0}'.format(openmp_extras_prefix),
            '-DCMAKE_CXX_FLAGS=-g',
            '-DCMAKE_C_FLAGS=-g'
        ]

        components['pgmath'] = [
            '../openmp-extras/flang/runtime/libpgmath',
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_CONFIG={0}/llvm-config'.format(bin_dir),
            '-DCMAKE_CXX_COMPILER={0}/clang++'.format(bin_dir),
            '-DCMAKE_C_COMPILER={0}/clang'.format(bin_dir),
            '-DCMAKE_Fortran_COMPILER={0}/flang'.format(bin_dir),
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86'
        ]

        components['flang'] = [
            '../openmp-extras/flang',
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_CONFIG={0}/llvm-config'.format(bin_dir),
            '-DCMAKE_CXX_COMPILER={0}/clang++'.format(bin_dir),
            '-DCMAKE_C_COMPILER={0}/clang'.format(bin_dir),
            '-DCMAKE_Fortran_COMPILER={0}/flang'.format(bin_dir),
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86',
            '-DFLANG_OPENMP_GPU_AMD=ON',
            '-DFLANG_OPENMP_GPU_NVIDIA=ON'
        ]

        components['flang-runtime'] = [
            '../openmp-extras/flang',
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_CONFIG={0}/llvm-config'.format(bin_dir),
            '-DCMAKE_CXX_COMPILER={0}/clang++'.format(bin_dir),
            '-DCMAKE_C_COMPILER={0}/clang'.format(bin_dir),
            '-DCMAKE_Fortran_COMPILER={0}/flang'.format(bin_dir),
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86',
            '-DLLVM_INSTALL_RUNTIME=ON',
            '-DFLANG_BUILD_RUNTIME=ON',
            '-DOPENMP_BUILD_DIR={0}/spack-build-openmp/runtime/src'.format(src)
        ]

        build_order = [
            "llvm", "aomp-extras", "openmp", "openmp-debug", "pgmath",
            "flang", "flang-runtime"
        ]

        # Override standard CMAKE_BUILD_TYPE
        std_cmake_args.remove("-DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo")
        for component in build_order:
            with working_dir('spack-build-{0}'.format(component), create=True):
                cmake_args = components[component]
                cmake_args.extend(std_cmake_args)
                # OpenMP build needs to be run twice(Release, Debug)
                if component == "openmp-debug":
                    cmake_args.append("-DCMAKE_BUILD_TYPE=Debug")
                else:
                    cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
                cmake(*cmake_args)
                make()
                make("install")
