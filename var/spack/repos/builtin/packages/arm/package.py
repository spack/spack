# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

import llnl.util.tty as tty
import spack.compiler
import spack.util.executable


class Arm(Package):
    """Arm Compiler combines the optimized tools and libraries from Arm
    with a modern LLVM-based compiler framework.
    """

    homepage = "https://developer.arm.com/tools-and-software/embedded/arm-compiler"
    url = "https://developer.arm.com/-/media/Files/downloads/compiler/DS500-BN-00026-r5p0-16rel0.tgz"

    version('6.14', sha256='0f72db76d9315550423593eecb60105914222d3dbc17f61a094c3a1ad2c23865',
            url='https://developer.arm.com/-/media/Files/downloads/compiler/DS500-BN-00026-r5p0-16rel0.tgz')

    def install(self, spec, prefix):
        raise InstallError(
            'No install method available yet, only system detection.'
        )

    executables = [r'armclang', r'armclang\+\+', r'armflang']

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
