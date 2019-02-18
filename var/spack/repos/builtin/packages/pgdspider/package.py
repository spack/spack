# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Pgdspider(Package):
    """"PGDSpider is a powerful automated data conversion tool for population
        genetic and genomics programs"""

    homepage = "http://www.cmpg.unibe.ch/software/PGDSpider"
    url      = "http://www.cmpg.unibe.ch/software/PGDSpider/PGDSpider_2.1.1.2.zip"

    version('2.1.1.2', '170e5b4a002277ff66866486da920693')

    depends_on('java', type=('build', 'run'))
    depends_on('bcftools')
    depends_on('bwa')
    depends_on('samtools')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'PGDSpider{0}-cli.jar'.format(self.version.up_to(1))
        install(jar_file, prefix.bin)

        script_sh = join_path(os.path.dirname(__file__), "pgdspider.sh")
        script = prefix.bin.pgdspider
        install(script_sh, script)
        set_executable(script)

        java = self.spec['java'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('pgdspider.jar', join_path(prefix.bin, jar_file),
                    script, **kwargs)
