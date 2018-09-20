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


class Picard(Package):
    """Picard is a set of command line tools for manipulating high-throughput
       sequencing (HTS) data and formats such as SAM/BAM/CRAM and VCF.
    """

    homepage = "http://broadinstitute.github.io/picard/"
    url      = "https://github.com/broadinstitute/picard/releases/download/2.9.2/picard.jar"
    _urlfmt  = "https://github.com/broadinstitute/picard/releases/download/{0}/picard.jar"
    _oldurlfmt = 'https://github.com/broadinstitute/picard/releases/download/{0}/picard-tools-{0}.zip'

    # They started distributing a single jar file at v2.6.0, prior to
    # that it was a .zip file with multiple .jar and .so files
    version('2.18.3', '181b1b0731fd35f0d8bd44677d8787e9', expand=False)
    version('2.18.0', '20045ff141e4a67512365f0b6bbd8229', expand=False)
    version('2.17.0', '72cc527f1e4ca6a799ae0117af60b54e', expand=False)
    version('2.16.0', 'fed8928b03bb36e355656f349e579083', expand=False)
    version('2.15.0', '3f5751630b1a3449edda47a0712a64e4', expand=False)
    version('2.13.2', '3d7b33fd1f43ad2129e6ec7883af56f5', expand=False)
    version('2.10.0', '96f3c11b1c9be9fc8088bc1b7b9f7538', expand=False)
    version('2.9.4', '5ce72af4d5efd02fba7084dcfbb3c7b3', expand=False)
    version('2.9.3', '3a33c231bcf3a61870c3d44b3b183924', expand=False)
    version('2.9.2', '0449279a6a89830917e8bcef3a976ef7', expand=False)
    version('2.9.0', 'b711d492f16dfe0084d33e684dca2202', expand=False)
    version('2.8.3', '4a181f55d378cd61d0b127a40dfd5016', expand=False)
    version('2.6.0', '91f35f22977d9692ce2718270077dc50', expand=False)
    version('1.140', '308f95516d94c1f3273a4e7e2b315ec2')

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
        script = prefix.bin.picard
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec['java'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('picard.jar', join_path(prefix.bin, 'picard.jar'),
                    script, **kwargs)

    def setup_environment(self, spack_env, run_env):
        """The Picard docs suggest setting this as a convenience."""
        run_env.prepend_path('PICARD',
                             join_path(self.prefix, 'bin', 'picard.jar'))

    def url_for_version(self, version):
        if version < Version('2.6.0'):
            return self._oldurlfmt.format(version)
        else:
            return self._urlfmt.format(version)
