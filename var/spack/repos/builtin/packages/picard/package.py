##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
from shutil import copyfile
import glob
import os.path
import re


class Picard(Package):
    """Picard is a set of command line tools for manipulating high-throughput
       sequencing (HTS) data and formats such as SAM/BAM/CRAM and VCF.
    """

    homepage = "http://broadinstitute.github.io/picard/"
    url      = "https://github.com/broadinstitute/picard/releases/download/2.9.2/picard.jar"

    # They started distributing a single jar file at v2.6.0, prior to
    # that it was a .zip file with multiple .jar and .so files
    version('2.9.2', '0449279a6a89830917e8bcef3a976ef7', expand=False,
            url="https://github.com/broadinstitute/picard/releases/download/2.9.2/picard.jar")
    version('1.140', '308f95516d94c1f3273a4e7e2b315ec2',
            url='https://github.com/broadinstitute/picard/releases/download/1.140/picard-tools-1.140.zip')

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
        script_sh = join_path(os.path.dirname(__file__), "picard.sh")
        script = join_path(prefix.bin, "picard")
        copyfile(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = join_path(self.spec['java'].prefix, 'bin', 'java')
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('picard.jar', join_path(prefix.bin, 'picard.jar'),
                    script, **kwargs)

    def setup_environment(self, spack_env, run_env):
        """The Picard docs suggest setting this as a convenience."""
        run_env.prepend_path('PICARD',
                             join_path(self.prefix, 'bin', 'picard.jar'))
