# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------

from spack import *


class SraTools(Package):
    """The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for
       using data in the INSDC Sequence Read Archives.
    """

    homepage = "https://github.com/ncbi/sra-tools/wiki"
    url      = "https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.10.7/sratoolkit.2.10.7-centos_linux64.tar.gz"

    maintainers = ['robqiao']

    version('2.10.7', sha256='b3f319974f0c7a318554d6383a13dd30f7d447533d92b6fd3bd057d3524e0140')

    def setup_run_environment(self, env):
        env.set('SRA-Toolkit', self.prefix)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('example', join_path(self.prefix, 'example'))
        install_tree('schema', join_path(self.prefix, 'schema'))
