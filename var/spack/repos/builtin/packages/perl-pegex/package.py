# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlPegex(PerlPackage):
    """Acmeist PEG Parser Framework"""

    homepage = "http://search.cpan.org/~ingy/Pegex-0.64/lib/Pegex.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/I/IN/INGY/Pegex-0.64.tar.gz"

    version('0.64', 'db86d4f1ddc36c4c7860ce060e77976f')

    depends_on('perl-file-sharedir-install', type=('build', 'run'))
    depends_on('perl-yaml-libyaml', type=('build', 'run'))
