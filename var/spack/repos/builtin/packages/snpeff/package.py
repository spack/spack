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

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "snpEff.sh")
        script = prefix.bin.snpEff
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec['java'].prefix.bin.java
        kwargs = {'backup': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('snpEff.jar', join_path(prefix.bin, 'snpEff.jar'),
                    script, **kwargs)
