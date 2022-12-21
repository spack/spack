# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess

from spack import *


class Shumlib(MakefilePackage):
    """A set of libraries which are used by the UK Met Office's Unified Model,
    that may be of use to external tools or applications where
    identical functionality is desired"""

    homepage = "https://github.com/metomi/shumlib"
    # git = "https://github.com/metomi/shumlib.git"
    git = "https://github.com/climbfuji/shumlib.git"
    url = "https://github.com/metomi/shumlib/archive/refs/tags/2021.10.1.zip"

    maintainers = ['matthewrmshin', 'climbfuji']

    version('macos_clang_linux_intel_port', commit='84770606669463a54b51f9b8ed65a1d31f105fe9')
    version('macos_clang_port', commit='e5e5c9f23ce2656aacd75a884c26b01a5380752e')
    # version('2021.10.1', commit='545874fba961deadf4b2758926be7c26f4c8dcb9')
    # version('2021.07.1', commit='a4ea525ad3bf04684ef39b0241991a350e2b7241')
    # version('2021.03.1', commit='58f599ce9cfb4bd47197125548a44039695fa7f1')
    # version('2020.11.1', commit='58f599ce9cfb4bd47197125548a44039695fa7f1')

    depends_on("patchelf", type="build", when="platform=linux")

    def edit(self, spec, prefix):
        env['LIBDIR_OUT'] = os.path.join(self.build_directory, 'spack-build')
        # env['LIBDIR_ROOT'] = self.build_directory

    def build(self, spec, prefix):
        if spec.satisfies('%clang') or spec.satisfies('%apple-clang'):
            os.system('make -f make/vm-x86-gfortran-clang.mk')
        elif spec.satisfies('%gcc'):
            os.system('make -f make/vm-x86-gfortran-gcc.mk')
        elif spec.satisfies('%intel'):
            os.system('make -f make/vm-x86-ifort-icc.mk')
        else:
            raise InstallError('No shumlib make config for this compiler')

    def install(self, spec, prefix):
        install_tree(os.path.join(os.getenv('LIBDIR_OUT'), 'include'), prefix.include)
        install_tree(os.path.join(os.getenv('LIBDIR_OUT'), 'lib'), prefix.lib)

    @run_after("install")
    def lib_path_fix(self):
        # The shared libraries are not installed correctly. shumlib
        # build expects the build location being the final location.
        # Fix by replacing the hard-coded build path with RPATH. On
        # macOS, this problem doesn't exist, the libraries are linked
        # without path, LD_LIBRARY_PATH needs to be set to find them.
        if self.spec.satisfies("platform=linux"):
            patchelf = which("patchelf")
            libdirs = ['lib', 'lib64']
            for libdir in libdirs:
                libpath = os.path.join(self.prefix, libdir)
                if not os.path.isdir(libpath):
                    continue
                allfiles = os.listdir(libpath)
                for filename in allfiles:
                    if filename.startswith("lib") and filename.endswith('.so'):
                        filepath = os.path.join(libpath, filename)
                        ldd_output = subprocess.check_output(['ldd', filepath])
                        ldd_output = ldd_output.decode("utf-8").split('\n')
                        for line in ldd_output:
                            if self.build_directory in line:
                                so_name_old = line.strip().split()[0]
                                # Sanity check that we really got the correct
                                # part of the string, at this stage (post install)
                                # the original build path still exists.
                                if not os.path.isfile(so_name_old):
                                    raise Exception("{} does not exist!".format(
                                        so_name_old))
                                so_name_new = os.path.join(self.prefix, libdir,
                                    os.path.basename(so_name_old))
                                patchelf_output = patchelf(
                                    "--replace-needed",
                                    so_name_old,
                                    so_name_new,
                                    filepath)
