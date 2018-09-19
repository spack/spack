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


class Soapindel(MakefilePackage):
    """SOAPindel is focusing on calling indels from the next-generation
       paired-end sequencing data."""

    homepage = "http://soap.genomics.org.cn/soapindel.html"

    version('2.1.7.17', '317ef494173969cdc6a8244dd87d06bd',
            url='http://soap.genomics.org.cn/down/SOAPindel_20130918_2.1.7.17.zip')

    depends_on('perl', type=('build', 'run'))

    build_directory = 'indel_detection.release'

    def install(self, spec, prefix):
        with working_dir('indel_detection.release'):
            install_tree('tools', prefix.tools)
            mkdirp(prefix.lib)
            install('affine_align.pm', prefix.lib)
            install('indel_lib.pm', prefix.lib)
            mkdirp(prefix.bin)
            install('assemble_align', prefix.bin)
            install('cluster_reads', prefix.bin)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PERL5LIB', self.prefix.lib)
        run_env.prepend_path('PATH', self.prefix.tools)
