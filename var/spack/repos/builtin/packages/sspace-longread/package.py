##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class SspaceLongread(Package):
    """SSPACE-LongRead is a stand-alone program for scaffolding pre-assembled
       contigs using long reads

       Note: A manual download is required for SSPACE-LongRead.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.baseclear.com/genomics/bioinformatics/basetools/SSPACE-longread"

    version('1.1', '0bb5d8603d7ead4ff1596135a520cc26')

    def url_for_version(self, version):
        return "file://{0}/40SSPACE-LongRead_v{1}.tar.gz".format(
                os.getcwd(), version.dashed)

    depends_on('perl', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('blasr', prefix.bin)
        install('SSPACE-LongRead.pl', prefix.bin)
