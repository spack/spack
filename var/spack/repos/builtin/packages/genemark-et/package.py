# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import glob


class GenemarkEt(Package):
    """Gene Prediction in Bacteria, archaea, Metagenomes and
       Metatranscriptomes."""

    homepage = "http://topaz.gatech.edu/GeneMark"

    version('4.33', '4ab7d7d3277a685dfb49e11bc5b493c3')

    depends_on('perl', type=('build', 'run'))

    def url_for_version(self, version):
        return "file://{0}/gm_et_linux_64.tar.gz".format(os.getcwd())

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('gmes_petap'):
            install_tree('lib', prefix.lib)
            files = glob.iglob('*')
            for file in files:
                if os.path.isfile(file):
                    install(file, prefix.bin)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PERL5LIB', prefix.lib)
