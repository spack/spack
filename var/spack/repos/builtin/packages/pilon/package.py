# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Pilon(Package):
    """Pilon is an automated genome assembly improvement and variant
    detection tool."""

    homepage = "https://github.com/broadinstitute/pilon"
    url      = "https://github.com/broadinstitute/pilon/releases/download/v1.22/pilon-1.22.jar"

    version('1.24', sha256='ea8e7ca8669887ebe1c376bef440ba487377d4802a45c5937ed37c49cafb8df6')
    version('1.23', sha256='bde1d3c8da5537abbc80627f0b2a4165c2b68551690e5733a6adf62413b87185')
    version('1.22', sha256='ff738f3bbb964237f6b2cf69243ebf9a21cb7f4edf10bbdcc66fa4ebaad5d13d', expand=False)
    version('1.13', sha256='c6195a054acbc76afc457e6a7615f75c91adc28faeb7b8738ee2b65309b0bbe3', expand=False)

    depends_on('java@1.7:', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'pilon-{0}.jar'.format(self.version.dotted)
        install(jar_file, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "pilon.sh")
        script = prefix.bin.pilon
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec['java'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('pilon-{0}.jar', join_path(prefix.bin, jar_file),
                    script, **kwargs)
