# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pindel(MakefilePackage):
    """Pindel can detect breakpoints from next-gen sequence data."""

    homepage = "http://gmt.genome.wustl.edu/packages/pindel/"
    url      = "https://github.com/genome/pindel/archive/v0.2.5.tar.gz"

    version('0.2.5b8', 'e6de2ffb38ba1cb89351cdccabe78cde')
    version('0.2.5b6', 'dc2febb18c203f0ef1ba02b7b882e94b')
    version('0.2.5b5', '73e964bc19de9ab9e6e8a316353e3184')
    version('0.2.5b4', 'b4aefd538d9f62578f46440c4bce497e')
    version('0.2.5b1', 'a8e53e8919aa29093db13fad5ede93a5')
    version('0.2.5a7', '5fb2bac6108547b5d60c38fc66abdfc4')
    version('0.2.5',   'd4568cbb83ec25ef9f9f6f058b30053e')

    depends_on('htslib@1.7:')
    #
    # This Makefile2 stuff is due to the original installer,
    # The author wants to run make twice, the first
    # time generates a Makefile.local then returns "false"
    # User is then suppose to run make again and the
    # package will compile. This is an attempt to
    # stay as close to the original installer as possible
    #

    def edit(self, spec, prefix):
        copy('Makefile', 'Makefile2')
        myedit = FileFilter('Makefile2')
        myedit.filter('-include Makefile.local', '#removed include')
        myedit.filter('@false', '#removed autofailure')

    def build(self, spec, prefix):
        make("Makefile.local", "-f",
             "Makefile2",
             "HTSLIB=%s" % spec['htslib'].prefix)
        make("HTSLIB=%s" % spec['htslib'].prefix)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('src/pindel', prefix.bin)
        install('src/pindel2vcf', prefix.bin)
        install('src/sam2pindel', prefix.bin)
        install('src/pindel2vcf4tcga', prefix.bin)
        install_tree('demo', prefix.doc)
