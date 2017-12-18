##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install gatk
#
# You can edit this file again by typing:
#
#     spack edit gatk
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
from shutil import copyfile
import glob
import os.path
import re


class Gatk(Package):
    """Genome Analysis Toolkit
       Variant Discovery in High-Throughput Sequencing Data
    """
    homepage = "http://broadinstitute.github.io/gatk/"
    url      = "https://software.broadinstitute.org/gatk/download/auth?package=GATK"
    _urlfmt  = "https://github.com/broadgsa/gatk-protected/archive/{0}.tar.gz"

    version('3.8-0', '0581308d2a25f10d11d3dfd0d6e4d28e', extension='tar.gz',
            url="https://software.broadinstitute.org/gatk/download/auth?package=GATK")

    depends_on('java@8:', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        # The list of files to install varies with release...
        # ... but skip the spack-{build.env}.out files.
        files = [x for x in glob.glob("*") if not re.match("^spack-", x)]
        for f in files:
            install(f, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "gatk.sh")
        script = join_path(prefix.bin, "gatk")
        copyfile(script_sh, script)
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
