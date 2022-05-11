# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

from spack.util.package import *

_os_map = {
    'ubuntu18.04': 'Ubuntu-18.04',
    'ubuntu20.04': 'Ubuntu-20.04',
    'sles15': 'SLES-15',
    'centos7': 'RHEL-7',
    'centos8': 'RHEL-8',
    'amzn2': 'RHEL-7'
}


_versions = {
    '22.0.1': {
        'RHEL-7': (
            '6b0ab76dce3fd44aab1e679baef01367c86f6bbd3544e04f9642b6685482cd76',
            'https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_RHEL-7_aarch64.tar'
        ),
        'RHEL-8': (
            '41e5bffc52701b1e8a606f8db09c3c02e35ae39eae0ebeed5fbb41a13e61f057',
            'https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_RHEL-8_aarch64.tar'
        ),
        'SLES-15': (
            'b578ff517dec7fa23c4b7353a1a7c958f28cc9c9447f71f7c4e83de2e2c5538f',
            'https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_SLES-15_aarch64.tar'
        ),
        'Ubuntu-18.04': (
            'becc6826ce0f6e696092e79a40f758d7cd0302227f6cfc7c2215f6483ade9748',
            'https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_Ubuntu-18.04_aarch64.tar'
        ),
        'Ubuntu-20.04': (
            'dea136238fc2855c41b8a8154bf279b7df5df8dba48d8f29121fa26f343e7cdb',
            'https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_Ubuntu-20.04_aarch64.tar'
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

    # Only install for Aarch64
    conflicts('target=x86_64:', msg='Only available on Aarch64')
    conflicts('target=ppc64:', msg='Only available on Aarch64')
    conflicts('target=ppc64le:', msg='Only available on Aarch64')

    executables = [r'armclang', r'armclang\+\+', r'armflang']

    # Licensing - Not required from 22.0.1 on.

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

    def setup_run_environment(self, env):
        arm_dir = get_acfl_prefix(self.spec)
        env.set("ARM_LINUX_COMPILER_DIR", arm_dir)
        env.set("ARM_LINUX_COMPILER_INCLUDES", join_path(arm_dir, 'includes'))
        env.prepend_path("LD_LIBRARY_PATH", join_path(arm_dir, 'lib'))
        env.prepend_path("PATH", join_path(arm_dir, 'bin'))
        env.prepend_path("CPATH", join_path(arm_dir, 'include'))
        env.prepend_path("MANPATH", join_path(arm_dir, 'share', 'man'))
        env.prepend_path("ARM_LICENSE_DIR", join_path(self.prefix, 'licences'))
