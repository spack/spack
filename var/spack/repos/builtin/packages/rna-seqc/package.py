# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class RnaSeqc(Package):
    """RNA-SeQC is a java program which computes a series of quality control
    metrics for RNA-seq data."""

    homepage = "http://archive.broadinstitute.org/cancer/cga/rna-seqc"
    url      = "http://www.broadinstitute.org/cancer/cga/tools/rnaseqc/RNA-SeQC_v1.1.8.jar"

    version('1.1.8', '71d7b5d3b3dcc1893cdc7f6819185d41', expand=False)
    version('1.1.7', '2d0b8ecac955af2f9bc1b185fdfb6b45', expand=False)
    version('1.1.6', 'fa9c9885081ae2e47f285c7c0f596a14', expand=False)
    version('1.1.5', '4b875671e906f708cbb8fd9bcf0e958d', expand=False)
    version('1.1.4', 'b04d06947c48cb2dc1b0ba29c8232db5', expand=False)

    depends_on('jdk@8:', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'RNA-SeQC_v{0}.jar'.format(self.version.dotted)
        install(jar_file, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "rna-seqc.sh")
        script = join_path(prefix.bin, "rna-seqc")
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec['jdk'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('RNA-SeQC_v{0}.jar', join_path(prefix.bin, jar_file),
                    script, **kwargs)
