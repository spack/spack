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

    version('4.0.12.0', sha256='733134303f4961dec589247ff006612b7a94171fab8913c5d44c836aa086865f')
    version('4.0.11.0', sha256='5ee23159be7c65051335ac155444c6a49c4d8e3515d4227646c0686819934536')
    version('4.0.8.1', sha256='e4bb082d8c8826d4f8bc8c2f83811d0e81e5088b99099d3396d284f82fbf28c9')
    version('4.0.4.0', '083d655883fb251e837eb2458141fc2b')
    version('3.8-1', 'a0829534d2d0ca3ebfbd3b524a9b50427ff238e0db400d6e9e479242d98cbe5c', extension='tar.bz2',
            url="https://software.broadinstitute.org/gatk/download/auth?package=GATK-archive&version=3.8-1-0-gf15c1c3ef")
    version('3.8-0', '0581308d2a25f10d11d3dfd0d6e4d28e', extension='tar.gz',
            url="https://software.broadinstitute.org/gatk/download/auth?package=GATK")

    depends_on('java@8:', type='run')
    depends_on('python@2.6:2.8,3.6:', type='run', when='@4.0:')
    depends_on('r@3.2:', type='run', when='@4.0:')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        # The list of files to install varies with release...
        # ... but skip the spack-{build.env}.out files and gatkdoc directory.
        files = [x for x in glob.glob("*")
                 if not re.match("^spack-", x) and not re.match("^gatkdoc", x)]
        for f in files:
            if os.path.isdir(f):
                install_tree(f, join_path(prefix.bin, f))
            else:
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
