# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Snpeff(Package):
    """SnpEff is a variant annotation and effect prediction tool. It
    annotates and predicts the effects of genetic variants (such as
    amino acid changes)."""

    homepage = "http://snpeff.sourceforge.net/"
    url      = "https://kent.dl.sourceforge.net/project/snpeff/snpEff_latest_core.zip"

    version('2017-11-24', '1fa84a703580a423e27f1e14a945901c')

    depends_on('jdk', type=('build', 'run'))

    def install(self, spec, prefix):
        install_tree('snpEff', prefix.bin)

        # Set up a helper script to call java on the jar files,
        # explicitly codes the path for java and the jar files.
        scripts = ['snpEff', 'SnpSift']

        for script in scripts:
            script_sh = join_path(os.path.dirname(__file__), script + ".sh")
            script_path = join_path(prefix.bin, script)
            install(script_sh, script_path)
            set_executable(script_path)

            # Munge the helper script to explicitly point to java and the
            # jar file.
            java = self.spec['java'].prefix.bin.java
            kwargs = {'backup': False}
            filter_file('^java', java, script_path, **kwargs)
            filter_file(script + '.jar',
                        join_path(prefix.bin, script + '.jar'),
                        script_path, **kwargs)
