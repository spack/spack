# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rocgdb(AutotoolsPackage):
    """This is ROCgdb, the ROCm source-level debugger for Linux, based on GDB, the GNU source-level debugger."""

    homepage = "https://github.com/ROCm-Developer-Tools/ROCgdb/"
    url      = "https://github.com/ROCm-Developer-Tools/ROCgdb/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='cf36d956e84c7a5711b71f281a44b0a9708e13e941d8fca0247d01567e7ee7d1')
    depends_on('cmake@3.5.2', type='build')
    depends_on('texinfo')
    depends_on('bison')
    depends_on('flex')
    depends_on('libunwind')
    depends_on('expat')
    depends_on('python')
    depends_on('rocm-dbgapi@3.5:', type='link', when='@3.5:')
    depends_on('comgr@3.5:', type='link', when='@3.5:')
    build_directory = 'spack-build'
 
    def configure_args(self):
        spec = self.spec

        # Generic options to compile GCC
        options = [
            # Distributor options
            '--program-prefix=roc',
            '--enable-64-bit-bfd',
            '--with-bugurl=https://github.com/ROCm-Developer-Tools/ROCgdb/issues',
            '--with-pkgversion=-ROCm',
            '--enable-targets=x86_64-linux-gnu,amdgcn-amd-amdhsa',
            '--disable-ld',
            '--disable-gas',
            '--disable-gdbserver',
            '--disable-sim',
            '--enable-tui',  
            '--disable-gdbtk',
            '--disable-shared',
            '--with-expat',
            '--with-system-zlib'
            '--without-guile',
            '--with-babeltrace',
            '--with-lzma',
            '--with-python'
        ]
        return options
