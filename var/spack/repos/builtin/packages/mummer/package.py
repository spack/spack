# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mummer(Package):
    """MUMmer is a system for rapidly aligning entire genomes."""

    homepage = "http://mummer.sourceforge.net/"
    url      = "https://sourceforge.net/projects/mummer/files/mummer/3.23/MUMmer3.23.tar.gz/download"

    version('3.23', 'f2422b3d2638dba4baedb71b1acdffa2')

    depends_on('gnuplot')
    depends_on('perl', type=('build', 'run'))

    patch('Makefile.patch')
    patch('scripts-Makefile.patch')

    def patch(self):
        """Fix mummerplot's use of defined on hashes (deprecated
           since perl@5.10, made illegal in perl@5.20."""

        kwargs = {'string': True}
        filter_file('defined (%', '(%', 'scripts/mummerplot.pl',
                    **kwargs)

    def install(self, spec, prefix):
        if self.run_tests:
            make('check')
        make('INSTALL_TOP_DIR={0}'.format(prefix))
        bd = prefix.bin
        abd = join_path(prefix, 'aux_bin')
        sd = join_path(prefix, 'scripts')
        mkdirp(bd)
        mkdirp(abd)
        mkdirp(sd)

        bins = ["show-tiling", "show-snps", "show-coords", "show-aligns",
                "show-diff", "delta-filter", "combineMUMs", "mummer",
                "repeat-match", "annotate", "mgaps", "gaps", "dnadiff",
                "nucmer2xfig", "run-mummer3", "mummerplot", "promer",
                "run-mummer1", "nucmer", "mapview", "exact-tandems"]
        aux_bins = ["aux_bin/postnuc", "aux_bin/postpro",
                    "aux_bin/prenuc", "aux_bin/prepro"]
        scripts = ["scripts/Foundation.pm"]

        for f in bins:
            install(f, join_path(bd, f))
        for f in aux_bins:
            install(f, join_path(abd, f[8:]))
        for f in scripts:
            install(f, join_path(sd, f[8:]))
