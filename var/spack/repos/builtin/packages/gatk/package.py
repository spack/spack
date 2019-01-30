# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os.path
import re


class Gatk(Package):
    """Genome Analysis Toolkit
       Variant Discovery in High-Throughput Sequencing Data
    """
    homepage = "https://software.broadinstitute.org/gatk/"
    url      = "https://github.com/broadinstitute/gatk/releases/download/4.0.4.0/gatk-4.0.4.0.zip"

    version('4.0.8.1', sha256='6d47463dfd8c16ffae82fd29e4e73503e5b7cd0fcc6fea2ed50ee3760dd9acd9',
            url='https://github.com/broadinstitute/gatk/archive/4.0.8.1.tar.gz')
    version('4.0.4.0', '083d655883fb251e837eb2458141fc2b',
            url="https://github.com/broadinstitute/gatk/releases/download/4.0.4.0/gatk-4.0.4.0.zip")
    version('3.8-0', '0581308d2a25f10d11d3dfd0d6e4d28e', extension='tar.gz',
            url="https://software.broadinstitute.org/gatk/download/auth?package=GATK")

    depends_on('java@8:', type='run')
    depends_on('python@2.6:2.8,3.6:', type='run', when='@4.0:')
    depends_on('r@3.2:', type='run', when='@4.0:')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        # Install all executable non-script files to prefix bin
        files = [x for x in glob.glob("*")
                 if not re.match("^.*\.sh$", x) and is_exe(x)]
        for f in files:
            install(f, prefix.bin)

        # Skip helper script settings
        if spec.satisfies('@:4.0'):
            return

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "gatk.sh")
        script = join_path(prefix.bin, "gatk")
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = join_path(self.spec['java'].prefix, 'bin', 'java')
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('GenomeAnalysisTK.jar', join_path(prefix.bin,
                    'GenomeAnalysisTK.jar'),
                    script, **kwargs)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('GATK',
                             join_path(self.prefix, 'bin',
                                                    'GenomeAnalysisTK.jar'))
