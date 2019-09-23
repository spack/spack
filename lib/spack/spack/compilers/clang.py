# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import os
import sys
from shutil import copytree, ignore_patterns

import llnl.util.lang
import llnl.util.tty as tty

import spack.paths
import spack.stage
from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.util.executable import Executable
from spack.version import ver


#: compiler symlink mappings for mixed f77 compilers
f77_mapping = [
    ('gfortran', 'clang/gfortran'),
    ('xlf_r', 'xl_r/xlf_r'),
    ('xlf', 'xl/xlf'),
    ('pgfortran', 'pgi/pgfortran'),
    ('ifort', 'intel/ifort')
]

#: compiler symlink mappings for mixed f90/fc compilers
fc_mapping = [
    ('gfortran', 'clang/gfortran'),
    ('xlf90_r', 'xl_r/xlf90_r'),
    ('xlf90', 'xl/xlf90'),
    ('pgfortran', 'pgi/pgfortran'),
    ('ifort', 'intel/ifort')
]


class Clang(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['clang']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['clang++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['flang', 'gfortran', 'xlf_r']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['flang', 'gfortran', 'xlf90_r']

    # Clang has support for using different fortran compilers with the
    # clang executable.
    @property
    def link_paths(self):
        # clang links are always the same
        link_paths = {'cc': 'clang/clang',
                      'cxx': 'clang/clang++'}

        # fortran links need to look at the actual compiler names from
        # compilers.yaml to figure out which named symlink to use
        for compiler_name, link_path in f77_mapping:
            if self.f77 and compiler_name in self.f77:
                link_paths['f77'] = link_path
                break
        else:
            link_paths['f77'] = 'clang/flang'

        for compiler_name, link_path in fc_mapping:
            if self.fc and compiler_name in self.fc:
                link_paths['fc'] = link_path
                break
        else:
            link_paths['fc'] = 'clang/flang'

        return link_paths

    @property
    def is_apple(self):
        ver_string = str(self.version)
        return ver_string.endswith('-apple')

    @classmethod
    def verbose_flag(cls):
        return "-v"

    @property
    def openmp_flag(self):
        if self.is_apple:
            return "-Xpreprocessor -fopenmp"
        else:
            return "-fopenmp"

    @property
    def cxx11_flag(self):
        if self.is_apple:
            # Adapted from CMake's AppleClang-CXX rules
            # Spack's AppleClang detection only valid from Xcode >= 4.6
            if self.version < ver('4.0.0'):
                raise UnsupportedCompilerFlag(self,
                                              "the C++11 standard",
                                              "cxx11_flag",
                                              "Xcode < 4.0.0")
            else:
                return "-std=c++11"
        else:
            if self.version < ver('3.3'):
                raise UnsupportedCompilerFlag(self,
                                              "the C++11 standard",
                                              "cxx11_flag",
                                              "< 3.3")
            else:
                return "-std=c++11"

    @property
    def cxx14_flag(self):
        if self.is_apple:
            # Adapted from CMake's rules for AppleClang
            if self.version < ver('5.1.0'):
                raise UnsupportedCompilerFlag(self,
                                              "the C++14 standard",
                                              "cxx14_flag",
                                              "Xcode < 5.1.0")
            elif self.version < ver('6.1.0'):
                return "-std=c++1y"
            else:
                return "-std=c++14"
        else:
            if self.version < ver('3.4'):
                raise UnsupportedCompilerFlag(self,
                                              "the C++14 standard",
                                              "cxx14_flag",
                                              "< 3.5")
            elif self.version < ver('3.5'):
                return "-std=c++1y"
            else:
                return "-std=c++14"

    @property
    def cxx17_flag(self):
        if self.is_apple:
            # Adapted from CMake's rules for AppleClang
            if self.version < ver('6.1.0'):
                raise UnsupportedCompilerFlag(self,
                                              "the C++17 standard",
                                              "cxx17_flag",
                                              "Xcode < 6.1.0")
            else:
                return "-std=c++1z"
        else:
            if self.version < ver('3.5'):
                raise UnsupportedCompilerFlag(self,
                                              "the C++17 standard",
                                              "cxx17_flag",
                                              "< 3.5")
            elif self.version < ver('5.0'):
                return "-std=c++1z"
            else:
                return "-std=c++17"

    @property
    def c99_flag(self):
        return '-std=c99'

    @property
    def c11_flag(self):
        if self.version < ver('6.1.0'):
            raise UnsupportedCompilerFlag(self,
                                          "the C11 standard",
                                          "c11_flag",
                                          "< 6.1.0")
        else:
            return "-std=c11"

    @property
    def pic_flag(self):
        return "-fPIC"

    required_libs = ['libclang']

    @classmethod
    @llnl.util.lang.memoized
    def default_version(cls, comp):
        """The ``--version`` option works for clang compilers.
        On most platforms, output looks like this::

            clang version 3.1 (trunk 149096)
            Target: x86_64-unknown-linux-gnu
            Thread model: posix

        On macOS, it looks like this::

            Apple LLVM version 7.0.2 (clang-700.1.81)
            Target: x86_64-apple-darwin15.2.0
            Thread model: posix
        """
        compiler = Executable(comp)
        output = compiler('--version', output=str, error=str)
        return cls.extract_version_from_output(output)

    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        ver = 'unknown'
        match = re.search(
            # Apple's LLVM compiler has its own versions, so suffix them.
            r'^Apple (?:LLVM|clang) version ([^ )]+)|'
            # Normal clang compiler versions are left as-is
            r'clang version ([^ )]+)-svn[~.\w\d-]*|'
            r'clang version ([^ )]+)-[~.\w\d-]*|'
            r'clang version ([^ )]+)',
            output
        )
        if match:
            suffix = '-apple' if match.lastindex == 1 else ''
            ver = match.group(match.lastindex) + suffix
        return ver

    @classmethod
    def fc_version(cls, fc):
        # We could map from gcc/gfortran version to clang version, but on macOS
        # we normally mix any version of gfortran with any version of clang.
        if sys.platform == 'darwin':
            return cls.default_version('clang')
        else:
            return cls.default_version(fc)

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)

    def setup_custom_environment(self, pkg, env):
        """Set the DEVELOPER_DIR environment for the Xcode toolchain.

        On macOS, not all buildsystems support querying CC and CXX for the
        compilers to use and instead query the Xcode toolchain for what
        compiler to run. This side-steps the spack wrappers. In order to inject
        spack into this setup, we need to copy (a subset of) Xcode.app and
        replace the compiler executables with symlinks to the spack wrapper.
        Currently, the stage is used to store the Xcode.app copies. We then set
        the 'DEVELOPER_DIR' environment variables to cause the xcrun and
        related tools to use this Xcode.app.
        """
        super(Clang, self).setup_custom_environment(pkg, env)

        if not self.is_apple or not pkg.use_xcode:
            # if we do it for all packages, we get into big troubles with MPI:
            # filter_compilers(self) will use mockup XCode compilers on macOS
            # with Clang. Those point to Spack's compiler wrappers and
            # consequently render MPI non-functional outside of Spack.
            return

        # Use special XCode versions of compiler wrappers when using XCode
        # Overwrites build_environment's setting of SPACK_CC and SPACK_CXX
        xcrun = Executable('xcrun')
        xcode_clang = xcrun('-f', 'clang', output=str).strip()
        xcode_clangpp = xcrun('-f', 'clang++', output=str).strip()
        env.set('SPACK_CC', xcode_clang, force=True)
        env.set('SPACK_CXX', xcode_clangpp, force=True)

        xcode_select = Executable('xcode-select')

        # Get the path of the active developer directory
        real_root = xcode_select('--print-path', output=str).strip()

        # The path name can be used to determine whether the full Xcode suite
        # or just the command-line tools are installed
        if real_root.endswith('Developer'):
            # The full Xcode suite is installed
            pass
        else:
            if real_root.endswith('CommandLineTools'):
                # Only the command-line tools are installed
                msg  = 'It appears that you have the Xcode command-line tools '
                msg += 'but not the full Xcode suite installed.\n'

            else:
                # Xcode is not installed
                msg  = 'It appears that you do not have Xcode installed.\n'

            msg += 'In order to use Spack to build the requested application, '
            msg += 'you need the full Xcode suite. It can be installed '
            msg += 'through the App Store. Make sure you launch the '
            msg += 'application and accept the license agreement.\n'

            raise OSError(msg)

        real_root = os.path.dirname(os.path.dirname(real_root))
        developer_root = os.path.join(spack.stage.get_stage_root(),
                                      'xcode-select',
                                      self.name,
                                      str(self.version))
        xcode_link = os.path.join(developer_root, 'Xcode.app')

        if not os.path.exists(developer_root):
            tty.warn('Copying Xcode from %s to %s in order to add spack '
                     'wrappers to it. Please do not interrupt.'
                     % (real_root, developer_root))

            # We need to make a new Xcode.app instance, but with symlinks to
            # the spack wrappers for the compilers it ships. This is necessary
            # because some projects insist on just asking xcrun and related
            # tools where the compiler runs. These tools are very hard to trick
            # as they do realpath and end up ignoring the symlinks in a
            # "softer" tree of nothing but symlinks in the right places.
            copytree(real_root, developer_root, symlinks=True,
                     ignore=ignore_patterns('AppleTV*.platform',
                                            'Watch*.platform',
                                            'iPhone*.platform',
                                            'Documentation',
                                            'swift*'))

            real_dirs = [
                'Toolchains/XcodeDefault.xctoolchain/usr/bin',
                'usr/bin',
            ]

            bins = ['c++', 'c89', 'c99', 'cc', 'clang', 'clang++', 'cpp']

            for real_dir in real_dirs:
                dev_dir = os.path.join(developer_root,
                                       'Contents',
                                       'Developer',
                                       real_dir)
                for fname in os.listdir(dev_dir):
                    if fname in bins:
                        os.unlink(os.path.join(dev_dir, fname))
                        os.symlink(
                            os.path.join(spack.paths.build_env_path, 'cc'),
                            os.path.join(dev_dir, fname))

            os.symlink(developer_root, xcode_link)

        env.set('DEVELOPER_DIR', xcode_link)
