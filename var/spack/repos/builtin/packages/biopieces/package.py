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


class Biopieces(Package):
    """The Biopieces are a collection of bioinformatics tools that can be
       pieced together in a very easy and flexible manner to perform both
       simple and complex tasks."""

    homepage = "http://maasha.github.io/biopieces/"
    git      = "https://github.com/maasha/biopieces.git"

    version('2016-04-12', commit='982f80f7c55e2cae67737d80fe35a4e784762856',
            submodules=True)

    depends_on('perl', type=('build', 'run'))
    depends_on('perl-module-build', type=('build', 'run'))
    depends_on('perl-bit-vector', type=('build', 'run'))
    depends_on('perl-svg', type=('build', 'run'))
    depends_on('perl-term-readkey', type=('build', 'run'))
    depends_on('perl-time-hires', type=('build', 'run'))
    depends_on('perl-dbi', type=('build', 'run'))
    depends_on('perl-xml-parser', type=('build', 'run'))
    depends_on('perl-carp-clan', type=('build', 'run'))
    depends_on('perl-class-inspector', type=('build', 'run'))
    depends_on('perl-html-parser', type=('build', 'run'))
    depends_on('perl-lwp', type=('build', 'run'))
    depends_on('perl-soap-lite', type=('build', 'run'))
    depends_on('perl-uri', type=('build', 'run'))
    depends_on('perl-inline', type=('build', 'run'))
    depends_on('perl-inline-c', type=('build', 'run'))
    depends_on('perl-parse-recdescent', type=('build', 'run'))
    depends_on('perl-version', type=('build', 'run'))
    depends_on('perl-dbfile', type=('build', 'run'))
    depends_on('perl-dbd-mysql', type=('build', 'run'))

    depends_on('ruby@1.9:')
    depends_on('ruby-gnuplot')
    depends_on('ruby-narray')
    depends_on('ruby-rubyinline')
    depends_on('ruby-terminal-table')

    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('blast-plus')
    depends_on('muscle')
    depends_on('mummer')
    depends_on('blat')
    depends_on('vmatch')
    depends_on('bowtie')
    depends_on('bwa')
    depends_on('usearch')
    depends_on('velvet')
    depends_on('idba')
    depends_on('ray')
    depends_on('scan-for-matches')

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def setup_environment(self, spack_env, run_env):
        # Note: user will need to set environment variables on their own,
        # dependent on where they will want data to be located:
        #    BP_DATA - Contains genomic data etc.
        #    BP_TMP - Required temporary directory
        #    BP_LOG - Required log directory
        run_env.prepend_path('BP_DIR', prefix)
