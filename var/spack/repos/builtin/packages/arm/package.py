# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re
import os

from spack import *
import spack.platforms

_os_map = {
    'ubuntu18.04': 'Ubuntu-18.04',
    'ubuntu20.04': 'Ubuntu-20.04',
    'sles15': 'SLES-15',
    'rhel7': 'RHEL-7',
    'rhel8': 'RHEL-8',
    'centos7': 'RHEL-7',
    'centos8': 'RHEL-8',
    'amzn2': 'RHEL-7'
}

_armpl_versions = {
    '21.0' : '21.0.0'
}

_versions = {
    '21.0': {
        'RHEL-7': (
            'fa67a4b9c1e562ec73e270aa4ef7a969af99bdd792ce8916b69ee47f7906110b',
            'https://armkeil.blob.core.windows.net/developer/Files/downloads/hpc/arm-allinea-studio/21-0/ACfL/arm-compiler-for-linux_21.0_RHEL-7_aarch64.tar'
        ),
        'RHEL-8': (
            'a1bf517fc108100878233610ec5cc9538ee09cd114670bfacab0419bbdef0780',
            'https://armkeil.blob.core.windows.net/developer/Files/downloads/hpc/arm-allinea-studio/21-0/ACfL/arm-compiler-for-linux_21.0_RHEL-8_aarch64.tar'
        ),
        'SLES-15': (
            '0307c67425fcf6c2c171c16732353767f79a7dd45e77cd7e4d94675d769cce77',
            'https://armkeil.blob.core.windows.net/developer/Files/downloads/hpc/arm-allinea-studio/21-0/ACfL/arm-compiler-for-linux_21.0_SLES-15_aarch64.tar'
        ),
        'Ubuntu-18.04': (
            'f57bd4652ea87282705073ea81ca108fef8e0725eb4bc441240ec2fc51ff5980',
            'https://armkeil.blob.core.windows.net/developer/Files/downloads/hpc/arm-allinea-studio/21-0/ACfL/arm-compiler-for-linux_21.0_Ubuntu-18.04_aarch64.tar'
        ),
        'Ubuntu-20.04': (
            'dd93254b9fe9baa802baebb9da5d00e0076a639b47f3515a8645b06742900eea',
            'https://armkeil.blob.core.windows.net/developer/Files/downloads/hpc/arm-allinea-studio/21-0/ACfL/arm-compiler-for-linux_21.0_Ubuntu-20.04_aarch64.tar'
        )
    }
}


def get_os():
    spack_os = spack.platforms.host().default_os
    return _os_map.get(spack_os, 'RHEL-7')


def get_acfl_prefix(spec):
    acfl_prefix = spec.prefix
    return join_path(
        acfl_prefix,
        'arm-linux-compiler-{0}_Generic-AArch64_{1}_aarch64-linux'.format(
            spec.version,
            get_os()
        )
    )

def get_armpl_prefix(spec):

    acfl_prefix = spec.prefix

    # SVE
    if spec.satisfies('+sve'):
        sve_flag = '-SVE'
    else:
        sve_flag = ''

    if spec.satisfies('%gcc'):
        return os.path.join(
            acfl_prefix,
            'armpl-{0}_AArch64{1}_{2}_gcc_aarch64-linux'.format(
                _armpl_versions[str(spec.version)],
                sve_flag,
                get_os()
            )
        )
    else:
        return os.path.join(
            acfl_prefix,
            'armpl-{0}_AArch64{1}_{2}_arm-linux-compiler_aarch64-linux'.format(
                _armpl_versions[str(spec.version)],
                sve_flag,
                get_os()
            )
        )


class Arm(Package):
    """Arm Compiler combines the optimized tools and libraries from Arm
    with a modern LLVM-based compiler framework.
    """

    homepage = "https://developer.arm.com/tools-and-software/server-and-hpc/arm-allinea-studio"
    url = "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/20-2-1/Ubuntu16.04/arm-compiler-for-linux_20.2.1_Ubuntu-16.04_aarch64.tar"

    maintainers = ['OliverPerks']

    # Build Versions: establish OS for URL
    acfl_os = get_os()

    # Build Versions
    for ver, packages in _versions.items():
        pkg = packages.get(acfl_os)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])
    
    variant('sve', default=False, description='SVE enabled Armpl library')
    variant('ilp64', default=False, description='use ilp64 specific Armpl library')
    variant('shared', default=True, description='enable shared libs')
    # Try to match the OpenBLAS threads variant format
    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('openmp', 'none'),
        multi=False
    )

    provides('blas')
    provides('lapack')
    provides('fftw-api@3')


    # Only install for Aarch64
    conflicts('target=x86_64:', msg='Only available on Aarch64')
    conflicts('target=ppc64:', msg='Only available on Aarch64')
    conflicts('target=ppc64le:', msg='Only available on Aarch64')

    executables = [r'armclang', r'armclang\+\+', r'armflang']

    # Set compiler dependency mapping
    conflicts('%gcc@:9.99.99', when='@21.0.0%gcc', msg='ArmPL 21.0 requires GCC@10')

    # Licensing
    license_required = True
    license_comment = "#"
    license_files = ["licences/Licence"]
    license_vars = ["ARM_LICENSE_DIR"]
    license_url = "https://developer.arm.com/tools-and-software/server-and-hpc/help/help-and-tutorials/system-administration/licensing/arm-licence-server"

    # Run the installer with the desired install directory
    def install(self, spec, prefix):
        exe = Executable('./arm-compiler-for-linux_{0}_{1}.sh'.format(
            spec.version, get_os())
        )
        exe("--accept", "--force", "--install-to", prefix)

    @classmethod
    def determine_version(cls, exe):
        regex_str = r'Arm C\/C\+\+\/Fortran Compiler version ([\d\.]+) '\
                    r'\(build number (\d+)\) '
        version_regex = re.compile(regex_str)
        try:
            output = spack.compiler.get_compiler_version_output(
                exe, '--version'
            )
            match = version_regex.search(output)
            if match:
                if match.group(1).count('.') == 1:
                    return match.group(1) + ".0." + match.group(2)
                return match.group(1) + "." + match.group(2)
        except spack.util.executable.ProcessError:
            pass
        except Exception as e:
            tty.debug(e)

    @classmethod
    def determine_variants(cls, exes, version_str):
        compilers = {}
        for exe in exes:
            if 'armclang' in exe:
                compilers['c'] = exe
            if 'armclang++' in exe:
                compilers['cxx'] = exe
            if 'armflang' in exe:
                compilers['fortran'] = exe
        return '', {'compilers': compilers}

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('c', None)
        return join_path(get_acfl_prefix(self.spec), 'bin', 'armclang')

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('cxx', None)
        return join_path(get_acfl_prefix(self.spec), 'bin', 'armclang++')

    @property
    def fortran(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('fortran', None)
        return join_path(get_acfl_prefix(self.spec), 'bin', 'armflang')
    
    @property
    def blas_libs(self):

        armpl_prefix = get_armpl_prefix(self.spec)

        shared = True if '+shared' in self.spec else False
        if '+ilp64' in self.spec and self.spec.satisfies('threads=openmp'):
            libname = 'libarmpl_ilp64_mp'
        elif '+ilp64' in self.spec:
            libname = 'libarmpl_ilp64'
        elif self.spec.satisfies('threads=openmp'):
            libname = 'libarmpl_mp'
        else:
            libname = 'libarmpl'

        # Get ArmPL Lib
        armpl_libs = find_libraries(
            [libname, 'libamath', 'libastring'],
            root=armpl_prefix,
            shared=shared,
            recursive=True)

        armpl_libs += find_system_libraries(['libm'])

        # Get additional libs
        # Find prefix of compiler
        arm_prefix = ancestor(self.compiler.cc, 2)
        # Search for libgfortran in this prefix
        arm_res = find_libraries(
            ['libflang', 'libflangrti'],
            root=arm_prefix,
            recursive=True
        )
        # Add to library path
        armpl_libs += arm_res

        return armpl_libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def fftw_libs(self):
        return self.blas_libs

    @property
    def libs(self):
        return self.blas_libs

    @property
    def headers(self):
        armpl_dir = get_armpl_prefix(self.spec)
        suffix = 'include'
        if self.spec.satisfies('+ilp64'):
            suffix += '_ilp64'
        if self.spec.satisfies('threads=openmp'):
            suffix += '_mp'
        incdir = join_path(armpl_dir, suffix)

        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    def setup_run_environment(self, env):
        arm_dir = get_acfl_prefix(self.spec)
        armpl_dir = get_armpl_prefix(self.spec)
        env.set("ARM_LINUX_COMPILER_DIR", arm_dir)
        env.set("ARM_LINUX_COMPILER_INCLUDES", join_path(arm_dir, 'includes'))
        env.set("ARMPL_DIR", armpl_dir)
        env.prepend_path("LD_LIBRARY_PATH", join_path(arm_dir, 'lib'))
        env.prepend_path("LD_LIBRARY_PATH", join_path(armpl_dir, 'lib'))
        env.prepend_path("PATH", join_path(arm_dir, 'bin'))
        env.prepend_path("CPATH", join_path(arm_dir, 'include'))
        env.prepend_path("MANPATH", join_path(arm_dir, 'share', 'man'))
        env.prepend_path("ARM_LICENSE_DIR", join_path(self.prefix, 'licences'))
