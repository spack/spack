# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import re

import llnl.util.tty as tty
import spack.compilers


class AppleClang(Package):
    """Apple's Clang compiler"""

    homepage = "https://developer.apple.com/videos/developer-tools/compiler-and-llvm"

    def install(self, spec, prefix):
        raise InstallError(
            "Apple's Clang cannot be installed, only detected on "
            "Apple's platform."
        )

    executables = ['clang', 'ld.lld', 'lldb']

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        result = []
        for exe in exes_in_prefix:
            # Executables like lldb-vscode-X are daemon listening
            # on some port and would hang Spack during detection.
            # clang-cl and clang-cpp are dev tools that we don't
            # need to test
            if any(x in exe for x in ('vscode', 'cpp', '-cl')):
                continue
            result.append(exe)
        return result

    @classmethod
    def determine_version(cls, exe):
        version_regex = re.compile(
            # Apple's LLVM compiler has its own versions, which are
            # different from vanilla LLVM
            r'^Apple (?:LLVM|clang) version ([^ )]+)',
            # Multi-line, since 'Apple clang' may not be on the first line
            # in particular, when run as gcc, it seems to output
            # "Configured with: --prefix=..." as the first line
            re.M
        )
        try:
            compiler = Executable(exe)
            output = compiler('--version', output=str, error=str)
            match = version_regex.search(output)
            if match:
                return match.group(match.lastindex)
        except spack.util.executable.ProcessError:
            pass
        except Exception as e:
            tty.debug(e)

        return None

    @classmethod
    def determine_variants(cls, exes, version_str):
        compilers = {}
        for exe in exes:
            if 'clang++' in exe:
                compilers['cxx'] = exe
            elif 'clang' in exe:
                compilers['c'] = exe
            elif 'ld.lld' in exe:
                compilers['ld'] = exe
            elif 'lldb' in exe:
                compilers['lldb'] = exe

        return '', {'compilers': compilers}

    @classmethod
    def validate_detected_spec(cls, spec, extra_attributes):
        # For GCC 'compilers' is a mandatory attribute
        msg = ('the extra attribute "compilers" must be set for '
               'the detected spec "{0}"'.format(spec))
        assert 'compilers' in extra_attributes, msg
        compilers = extra_attributes['compilers']
        for key in ('c', 'cxx'):
            msg = '{0} compiler not found for {1}'
            assert key in compilers, msg.format(key, spec)

    @property
    def cc(self):
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('c', None)
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        return self.spec.prefix.bin.clang if '+clang' in self.spec else None

    @property
    def cxx(self):
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('cxx', None)
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        result = None
        if '+clang' in self.spec:
            result = os.path.join(self.spec.prefix.bin, 'g++')
        return result
