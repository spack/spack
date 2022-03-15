# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

is_windows = str(spack.platforms.host()) == 'windows'


class Nasm(Package):
    """NASM (Netwide Assembler) is an 80x86 assembler designed for
    portability and modularity. It includes a disassembler as well."""

    homepage = "https://www.nasm.us"
    url      = "https://www.nasm.us/pub/nasm/releasebuilds/2.14.02/nasm-2.14.02.tar.gz"
    list_url = "https://www.nasm.us/pub/nasm/releasebuilds"
    list_depth = 1
    a = '3caf6729c1073bf96629b57cee31eeb54f4f8129b01902c73428836550b30a3f'

    version('2.15.05', sha256='9182a118244b058651c576baa9d0366ee05983c4d4ae1d9ddd3236a9f2304997')
    version('2.14.02', sha256='e24ade3e928f7253aa8c14aa44726d1edf3f98643f87c9d72ec1df44b26be8f5')
    version('2.13.03', sha256='812ecfb0dcbc5bd409aaa8f61c7de94c5b8752a7b00c632883d15b2ed6452573')
    version('2.11.06', sha256='90f60d95a15b8a54bf34d87b9be53da89ee3d6213ea739fb2305846f4585868a')

    # Fix compilation with GCC 8
    # https://bugzilla.nasm.us/show_bug.cgi?id=3392461
    patch('https://src.fedoraproject.org/rpms/nasm/raw/0cc3eb244bd971df81a7f02bc12c5ec259e1a5d6/f/0001-Remove-invalid-pure_func-qualifiers.patch', level=1, sha256='ac9f315d204afa6b99ceefa1fe46d4eed2b8a23c7315d32d33c0f378d930e950', when='@2.13.03 %gcc@8:')

    patch('msvc.mak.patch', when='platform=windows')

    conflicts('%intel@:14', when='@2.14:',
              msg="Intel 14 has immature C11 support")

    phases = ['configure', 'build', 'install']

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies('%nvhpc@:20.11'):
            filter_file(r'CFLAGS="\$pa_add_cflags__old_cflags -Werror=.*"',
                        'CFLAGS="$pa_add_cflags__old_cflags"', 'configure')
            filter_file(r'CFLAGS="\$pa_add_flags__old_flags -Werror=.*"',
                        'CFLAGS="$pa_add_flags__old_flags"', 'configure')

    def configure(self, spec, prefix):
        with working_dir(self.stage.source_path, create=True):
            if not is_windows:
                configure(*['--prefix={0}'.format(self.prefix)])

    def build(self, spec, prefix):
        with working_dir(self.stage.source_path):
            if is_windows:
                touch('asm\\warnings.time')
                nmake('/f', 'Mkfiles\\msvc.mak')
            else:
                make(*['V=1'])

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            if is_windows:
                pass
            else:
                make(*['install'])
