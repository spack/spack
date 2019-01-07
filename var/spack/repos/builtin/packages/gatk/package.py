# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Gatk(Package):
    """Genome Analysis Toolkit
       Variant Discovery in High-Throughput Sequencing Data
    """
    homepage = "https://software.broadinstitute.org/gatk/"
    url      = "https://github.com/broadinstitute/gatk/releases/download/4.0.4.0/gatk-4.0.4.0.zip"

    version('4.0.11.0', sha256='5ee23159be7c65051335ac155444c6a49c4d8e3515d4227646c0686819934536')
    version('4.0.8.1', sha256='6d47463dfd8c16ffae82fd29e4e73503e5b7cd0fcc6fea2ed50ee3760dd9acd9',
            url='https://github.com/broadinstitute/gatk/archive/4.0.8.1.tar.gz')
    version('4.0.4.0', '083d655883fb251e837eb2458141fc2b',
            url="https://github.com/broadinstitute/gatk/releases/download/4.0.4.0/gatk-4.0.4.0.zip")
    version('3.8-1', 'a0829534d2d0ca3ebfbd3b524a9b50427ff238e0db400d6e9e479242d98cbe5c', extension='tar.bz2',
            url="https://software.broadinstitute.org/gatk/download/auth?package=GATK-archive&version=3.8-1-0-gf15c1c3ef")
    version('3.8-0', '0581308d2a25f10d11d3dfd0d6e4d28e', extension='tar.gz',
            url="https://software.broadinstitute.org/gatk/download/auth?package=GATK")

    depends_on('java@8:', type='run')
    depends_on('python@2.6:2.8,3.6:', type='run', when='@4.0:')
    depends_on('r@3.2:', type='run', when='@4.0:')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        # Install all executable non-script files to prefix bin
        jar_file = 'GenomeAnalysisTK.jar'
        install(jar_file, prefix.bin)

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
