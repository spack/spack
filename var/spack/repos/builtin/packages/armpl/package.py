# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import llnl.util.tty as tty
import os

_os_map = {
    'ubuntu18.04': 'Ubuntu-18.04',
    'ubuntu20.04': 'Ubuntu-20.04',
    'sles15': 'SLES-15',
    'centos7': 'RHEL-7',
    'centos8': 'RHEL-8',
    'amzn2': 'RHEL-7'
}


def get_os():
    spack_os = spack.architecture.platform().default_os
    if spack_os in _os_map:
        return _os_map[spack_os]
    else:
        return 'RHEL-7'


def get_armpl_prefix(spec):

    acfl_prefix = spec['acfl'].prefix

    # SVE
    if spec.satisfies('+sve'):
        sve_flag = '-SVE'
    else:
        sve_flag = ''

    if spec.satisfies('%gcc'):
        return os.path.join(
            acfl_prefix,
            'armpl-{0}_AArch64{1}_{2}_gcc_aarch64-linux'.format(
                spec.version, sve_flag, get_os()
            )
        )
    else:
        return os.path.join(
            acfl_prefix,
            'armpl-{0}_AArch64{1}_{2}_arm-linux-compiler_aarch64-linux'.format(
                spec.version, sve_flag, get_os()
            )
        )


class Armpl(Package):
    """Arm performance Libraries tuned maths libraries for Arm processors."""

    homepage = "https://developer.arm.com/tools-and-software/server-and-hpc/downloads/arm-performance-libraries"
    url = "https://developer.arm.com/tools-and-software/server-and-hpc/downloads/arm-performance-libraries"
    has_code = False

    maintainers = ['OliverPerks', 'srinathv']

    conflicts('target=x86:', msg='Only available on Aarch64')
    conflicts('target=ppc64:', msg='Only available on Aarch64')

    version("21.0.0")
    version("20.2.0")

    depends_on('acfl@21.0', when='@21.0.0')
    depends_on('acfl@20.2', when='@20.2.0')

    variant('sve', default=False, description='SVE enabled Armpl library')
    variant('ilp64', default=False, description='use ilp64 specific Armpl library')
    variant('shared', default=True, description='enable shared libs')
    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('openmp', 'none'),
        multi=False
    )

    provides('blas')
    provides('lapack')
    provides('fftw-api@3')

    # No install phase
    phases = []

    @property
    def blas_libs(self):

        armpl_prefix = get_armpl_prefix(self.spec)

        tty.warn("Looking in: " + armpl_prefix)

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
        if self.spec.satisfies('%gcc'):
            # Find prefix of compiler
            gcc_prefix = ancestor(self.compiler.cc, 2)
            # Search for libgfortran in this prefix
            gcc_res = find_libraries(
                ['libgfortran'], root=gcc_prefix, recursive=True
            )
            # Add to library path
            armpl_libs += gcc_res

        if self.spec.satisfies('%arm'):
            # Find prefix of compiler
            arm_prefix = ancestor(self.compiler.cc, 2)
            # Search for libgfortran in this prefix
            arm_res = find_libraries(
                ['libflang', 'libflangrti'], root=arm_prefix, recursive=True
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
        incdir = os.path.join(armpl_dir, suffix)

        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    def setup_run_environment(self, env):
        armpl_dir = get_armpl_prefix(self.spec)
        env.prepend_path("LD_LIBRARY_PATH", join_path(armpl_dir, "lib"))
