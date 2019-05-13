# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Recon(MakefilePackage):
    """RECON: a package for automated de novo identification of repeat families
       from genomic sequences.

       NOTE: The 1.08 is a patched version from the RepeatModeler developers.
             The original versions can be found on the homepage."""

    homepage = "http://eddylab.org/software/recon/"
    url      = "http://www.repeatmasker.org/RepeatModeler/RECON-1.08.tar.gz"

    version('1.08', sha256='699765fa49d18dbfac9f7a82ecd054464b468cb7521abe9c2bd8caccf08ee7d8')

    build_directory = 'src'

    depends_on('perl', type='run')

    @property
    def install_targets(self):
        return [
            'install',
            'BINDIR=%s' % self.prefix.bin
        ]

    # edit the recon.pl script with the prefix as mentioned in the README
    def edit(self, spec, prefix):
        filter_file('$path = ""', '$path = "%s"' % prefix.bin,
                    'scripts/recon.pl', string=True)

    # recon's makefile is very basic -- the target directory must
    # already exist to properly install
    @run_before('install')
    def prepare_bin(self):
        mkdirp(prefix.bin)

    # finally, install the scripts dir as well
    # and link the recon command into bin.
    @run_after('install')
    def finalize(self):
        install_tree('scripts', prefix.scripts)
        symlink(join_path(prefix.scripts, 'recon.pl'),
                join_path(prefix.bin, 'recon'))
