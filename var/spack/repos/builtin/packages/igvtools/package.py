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
import os


class Igvtools(Package):
    """IGVTools suite of command-line utilities for preprocessing data
    files"""

    homepage = "https://software.broadinstitute.org/software/igv/home"
    url      = "http://data.broadinstitute.org/igv/projects/downloads/2.3/igvtools_2.3.98.zip"

    version('2.3.98', '17ed12a213cd9cdaeb2f2a5c56d84bc4')

    depends_on('java@8:')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'igvtools.jar'
        install(jar_file, prefix.bin)
        install_tree('genomes', prefix.genomes)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "igvtools.sh")
        script = prefix.bin.igvtools
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = spec['jdk'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file(jar_file, join_path(prefix.bin, jar_file),
                    script, **kwargs)
