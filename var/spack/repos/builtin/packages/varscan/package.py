# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Varscan(Package):
    """Variant calling and somatic mutation/CNV detection for next-generation
       sequencing data"""

    homepage = "http://dkoboldt.github.io/varscan/"
    url      = "https://github.com/dkoboldt/varscan/releases/download/2.4.2/VarScan.v2.4.2.jar"

    version('2.4.2', '4b810741505a8145a7f8f9f6791bbacf', expand=False)

    depends_on('java', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.jar)
        jar_file = 'VarScan.v{v}.jar'.format(v=self.version.dotted)
        install(jar_file, prefix.jar)

        script_sh = join_path(os.path.dirname(__file__), "varscan.sh")
        script = prefix.bin.varscan
        install(script_sh, script)
        set_executable(script)

        java = join_path(self.spec['java'].prefix, 'bin', 'java')
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('varscan.jar', join_path(prefix.jar, jar_file),
                    script, **kwargs)

    def setup_environment(self, spack_env, run_env):
        run_env.set('VARSCAN_HOME', self.prefix)
        run_env.set('CLASSPATH', self.prefix.jar)
