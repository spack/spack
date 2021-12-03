# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack import *
from spack.error import SpackError
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

_versions = {
    '21.1.0_10.2': {
        'RHEL-7': ('41597c67ff2cd6281961111964e5065a49d32f2550b3290be1e2378aa05df74a',
                   'https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries/21-1-0/RHEL7/arm-performance-libraries_21.1_RHEL-7_gcc-10.2.tar'),
        'RHEL-8': ('fdc9d0a394e58f6a5575862bf9cc375cc1a8b36cb3bbb0ef1dcdeee1873e6959',
                   'https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries/21-1-0/RHEL8/arm-performance-libraries_21.1_RHEL-8_gcc-10.2.tar')
    },
    '21.1.0_9.3': {
        'RHEL-7': ('5dbe9e738b6b41df8459417cbca70df924395b8b70825ed793159feb0bdc74da',
                   'https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries/21-1-0/RHEL7/arm-performance-libraries_21.1_RHEL-7_gcc-9.3.tar'),
        'RHEL-8': ('626f91f1facede437d7ebee3bb511f3845b029862298001274685b282200747d',
                   'https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries/21-1-0/RHEL8/arm-performance-libraries_21.1_RHEL-8_gcc-9.3.tar')
    },
    '21.1.0_8.2': {
        'RHEL-7': ('2994fce82a7d5b5a72eccbd7281f88d5cd4439a2bad832628d5cabbb8d960135',
                   'https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries/21-1-0/RHEL7/arm-performance-libraries_21.1_RHEL-7_gcc-8.2.tar'),
        'RHEL-8': ('5633768b892db3d959b1d3fc1e435dc022666a5ec8567f9394adbd4edf7972dc',
                   'https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries/21-1-0/RHEL8/arm-performance-libraries_21.1_RHEL-8_gcc-8.2.tar')
    }
}


def get_os():
    spack_os = spack.platforms.host().default_os
    return _os_map.get(spack_os, 'RHEL-7')


def get_armpl_prefix(spec, compiler):

    acfl_prefix = spec.prefix

    return os.path.join(
        acfl_prefix,
        'armpl_{0}_gcc-{1}'.format(
            spec.version.up_to(2),
            compiler.version.up_to(2)
        )
    )


class Armpl(Package):
    """Arm performance Libraries provide advanced math functions
    tuned for Arm processors. """

    homepage = "https://developer.arm.com/tools-and-software/server-and-hpc/downloads/arm-performance-libraries"
    url = "https://developer.arm.com/tools-and-software/server-and-hpc/downloads/arm-performance-libraries"

    maintainers = ['OliverPerks', 'annwon']

    for ver, packages in _versions.items():
        key = "{0}".format(get_os())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    conflicts('target=x86:', msg='Only available on Aarch64')
    conflicts('target=ppc64:', msg='Only available on Aarch64')
    conflicts('target=ppc64le:', msg='Only available on Aarch64')
    conflicts('%gcc@:10.1.999,10.3:', when='@21.1.0_10.2')
    conflicts('%gcc@:9.2.999,9.4:', when='@21.1.0_9.3')
    conflicts('%gcc@:8.1.999,8.3:', when='@21.1.0_8.2')

    # Set compiler dependency mapping

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

    # Run the installer with the desired install directory
    def install(self, spec, prefix):
        if self.compiler.name != 'gcc':
            raise SpackError(('Only compatible with GCC.\n'))

        exe = Executable('./arm-performance-libraries_{0}_{1}.sh'.format(
            spec.version.up_to(2), get_os())
        )
        exe("--accept", "--force", "--install-to", prefix)

    @property
    def blas_libs(self):

        armpl_prefix = get_armpl_prefix(self.spec, self.compiler)

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

        # Find prefix of compiler
        gcc_prefix = ancestor(self.compiler.cc, 2)
        # Search for libgfortran in this prefix
        gcc_res = find_libraries(
            ['libgfortran'],
            root=gcc_prefix,
            recursive=True
        )
        # Add to library path
        armpl_libs += gcc_res

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
        armpl_dir = get_armpl_prefix(self.spec, self.compiler)
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
        armpl_dir = get_armpl_prefix(self.spec, self.compiler)
        env.set("ARMPL_DIR", armpl_dir)
        env.prepend_path("LD_LIBRARY_PATH", join_path(armpl_dir, "lib"))
