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
import os


class Gapfiller(Package):
    """GapFiller is a stand-alone program for closing gaps within
       pre-assembled scaffolds.

       Note: A manual download is required for GapFiller.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.baseclear.com/genomics/bioinformatics/basetools/gapfiller"

    version('1.10', '54d5e2ada131a1305a66e41c0d380382')

    def url_for_version(self, version):
        return "file://{0}/39GapFiller_v{1}_linux-x86_64.tar.gz".format(
                os.getcwd(), version.dashed)

    depends_on('perl', type=('build', 'run'))

    def install(self, spec, prefix):
        install_tree('bowtie', prefix.bowtie)
        install_tree('bwa', prefix.bwa)
        install('GapFiller.pl', prefix)
