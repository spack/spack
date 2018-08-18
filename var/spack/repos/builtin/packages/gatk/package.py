##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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

    version('4.0.4.0', '083d655883fb251e837eb2458141fc2b',
            url="https://github.com/broadinstitute/gatk/releases/download/4.0.4.0/gatk-4.0.4.0.zip")
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
