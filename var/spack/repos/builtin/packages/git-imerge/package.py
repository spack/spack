# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GitImerge(MakefilePackage):
    """git-imerge: Incremental merge & rebase for git

       Perform a merge between two branches incrementally. If
       conflicts are encountered, figure out exactly which pairs of
       commits conflict, and present the user with one pairwise
       conflict at a time for resolution.

       git-imerge has two primary design goals:

       * Reduce the pain of resolving merge conflicts to its
         unavoidable minimum, by finding and presenting the smallest
         possible conflicts: those between the changes introduced by
         one commit from each branch.

       * Allow a merge to be saved, tested, interrupted, published,
         and collaborated on while it is in progress."""

    homepage = "https://github.com/mhagger/git-imerge"
    url      = "https://github.com/mhagger/git-imerge/archive/v1.1.0.tar.gz"

    version('1.1.0', '94a44dcbe5e764d75770a24517572a76')
    version('1.0.0', 'e5e69a22610828cc33bf2cbd31685438')

    depends_on('python@2.6:')
    depends_on('py-argparse', when='^python@2.6')
    depends_on('git')

    # Package copies a Python script and bash-completion files, so
    # there's no need to "build" anything.
    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        make('DESTDIR={0}'.format(prefix), 'PREFIX=', 'install')
