##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class RubySvn2git(Package):
    """svn2git is a tiny utility for migrating projects from Subversion to Git
    while keeping the trunk, branches and tags where they should be. It uses
    git-svn to clone an svn repository and does some clean-up to make sure
    branches and tags are imported in a meaningful way, and that the code
    checked into master ends up being what's currently in your svn trunk rather
    than whichever svn branch your last commit was in."""

    homepage = "https://github.com/nirvdrum/svn2git/"
    url      = "https://github.com/nirvdrum/svn2git/archive/v2.4.0.tar.gz"

    version('2.4.0', 'f19ac6eb0634aa1fed31a1e40a2aeaa2')

    depends_on('git')
    depends_on('subversion+perl')

    extends('ruby')

    def install(self, spec, prefix):
        gem('build', 'svn2git.gemspec')
        gem('install', 'svn2git-{0}.gem'.format(self.version))
