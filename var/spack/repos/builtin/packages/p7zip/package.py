# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkgkit import *


class P7zip(MakefilePackage):
    """A Unix port of the 7z file archiver"""

    maintainers = ['vmiheer']
    homepage = "http://p7zip.sourceforge.net"
    url      = "https://downloads.sourceforge.net/project/p7zip/p7zip/16.02/p7zip_16.02_src_all.tar.bz2"

    version('16.02', sha256='5eb20ac0e2944f6cb9c2d51dd6c4518941c185347d4089ea89087ffdd6e2341f')

    patch('gcc10.patch', when='%gcc@10:', sha256='96914025b9f431fdd75ae69768162d57751413634622f9df1a4bc4960e7e8fe1')

    # Replace boolean increments with assignments of true (which is
    # semantically equivalent). Use of increment operators on booleans is
    # forbidden by C++17, the default standard targeted by GCC 11.
    patch('gcc11.patch', when='%gcc@11:', sha256='39dd15f2dfc86eeee8c3a13ffde65c2ca919433cfe97ea126fbdc016afc587d1')

    # all3 includes 7z, 7za, and 7zr
    build_targets = ['all3']

    def edit(self, spec, prefix):
        if 'platform=darwin' in self.spec:
            if '%gcc' in self.spec:
                copy('makefile.macosx_gcc_64bits', 'makefile.machine')
            elif '%apple-clang' in self.spec or '%clang' in self.spec:
                copy('makefile.macosx_llvm_64bits', 'makefile.machine')

    @property
    def install_targets(self):
        return ['DEST_HOME={0}'.format(self.prefix), 'install']
