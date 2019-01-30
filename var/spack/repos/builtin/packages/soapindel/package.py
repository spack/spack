# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
