# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from os import symlink


class Recon(MakefilePackage):
    """RECON: a package for automated de novo identification of repeat families
       from genomic sequences

       NOTE: The 1.08 is a patched version from the RepeatModeler developers.
             The original versions can be found on the homepage."""

    homepage = "http://eddylab.org/software/recon/"
    url      = "http://www.repeatmasker.org/RepeatModeler/RECON-1.08.tar.gz"

    version('1.08', sha256='699765fa49d18dbfac9f7a82ecd054464b468cb7521abe9c2bd8caccf08ee7d8')

    build_directory = 'src'
    build_targets = ['install']

    depends_on('perl', type='run')

    def install(self, spec, prefix):
        filter_file('$path = ""', '$path = "%s"' % prefix.bin,
                    'scripts/recon.pl', string=True)

        install_tree('bin', prefix.bin)
        install_tree('scripts', prefix.scripts)

        symlink(join_path(prefix.scripts, 'recon.pl'),
                join_path(prefix.bin, 'recon'))
