# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Haploview(Package):
    """Haploview is designed to simplify and expedite the process of haplotype
       analysis."""

    homepage = "http://www.broadinstitute.org/haploview/haploview"
    url      = "https://downloads.sourceforge.net/project/haploview/release/Haploview4.1.jar"

    version('4.1', 'f7aa4accda5fad1be74c9c1969c6ee7d', expand=False)

    depends_on('java', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'Haploview{v}.jar'.format(v=self.version)
        install(jar_file, prefix.bin)

        script_sh = join_path(os.path.dirname(__file__), "haploview.sh")
        script = prefix.bin.haploview
        install(script_sh, script)
        set_executable(script)

        java = self.spec['java'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('haploview.jar', join_path(prefix.bin, jar_file),
                    script, **kwargs)
