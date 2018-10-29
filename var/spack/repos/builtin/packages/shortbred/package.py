# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Shortbred(Package):
    """ShortBRED is a system for profiling protein families of interest at
    very high specificity in shotgun meta'omic sequencing data."""

    homepage = "https://huttenhower.sph.harvard.edu/shortbred"
    url      = "https://bitbucket.org/biobakery/shortbred/get/0.9.4.tar.gz"

    version('0.9.4', 'ad3dff344cbea3713e78b384afad28fd')

    depends_on('blast-plus@2.2.28:')
    depends_on('cdhit@4.6:')
    depends_on('muscle@3.8.31:')
    depends_on('python@2.7.9:')
    depends_on('py-biopython')
    depends_on('usearch@6.0.307:')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('shortbred_identify.py', prefix.bin)
        install('shortbred_quantify.py', prefix.bin)
        install_tree('src', prefix.src)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PYTHONPATH', self.prefix)
