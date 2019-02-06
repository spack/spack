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


class Wordnet(AutotoolsPackage):
    """WordNet is a large lexical database of English. Nouns, verbs, adjectives
    and adverbs are grouped into sets of cognitive synonyms (synsets), each
    expressing a distinct concept. """

    homepage = "https://wordnet.princeton.edu/"
    url      = "http://wordnetcode.princeton.edu/3.0/WordNet-3.0.tar.gz"

    version('3.0', sha256='640db279c949a88f61f851dd54ebbb22d003f8b90b85267042ef85a3781d3a52')

    depends_on('tk')
    depends_on('tcl')

    def configure_args(self):
        args = []
        args.append('--with-tk=%s' % self.spec['tk'].prefix.lib)
        args.append('--with-tcl=%s' % self.spec['tcl'].prefix.lib)
        if self.spec.satisfies('^tcl@8.6:'):
            args.append('CPPFLAGS=-DUSE_INTERP_RESULT')

        return args

    def setup_environment(self, spack_env, run_env):
        run_env.set('WNHOME', self.prefix)
        run_env.set('WNSEARCHDIR', self.prefix.dict)
