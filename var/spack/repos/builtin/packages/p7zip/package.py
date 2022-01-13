# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class P7zip(MakefilePackage):
    """A Unix port of the 7z file archiver"""

    maintainers = ['vmiheer']
    homepage = "http://p7zip.sourceforge.net"
    url      = "https://downloads.sourceforge.net/project/p7zip/p7zip/16.02/p7zip_16.02_src_all.tar.bz2"

    version('16.02', sha256='5eb20ac0e2944f6cb9c2d51dd6c4518941c185347d4089ea89087ffdd6e2341f')

    patch('gcc10.patch', when='%gcc@10:', sha256='96914025b9f431fdd75ae69768162d57751413634622f9df1a4bc4960e7e8fe1')
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
