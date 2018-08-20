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
import os.path


class Pilon(Package):
    """Pilon is an automated genome assembly improvement and variant
    detection tool."""

    homepage = "https://github.com/broadinstitute/pilon"
    url      = "https://github.com/broadinstitute/pilon/releases/download/v1.22/pilon-1.22.jar"

    version('1.22', '3c45568dc1b878a9a0316410ec62ab04', expand=False)
    version('1.13', '9e96b4cf4ea595b1996c7e9ca76498b5', expand=False)

    depends_on('java@1.7:', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'pilon-{0}.jar'.format(self.version.dotted)
        install(jar_file, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "pilon.sh")
        script = prefix.bin.pilon
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec['java'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('pilon-{0}.jar', join_path(prefix.bin, jar_file),
                    script, **kwargs)
