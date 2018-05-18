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


class RnaSeqc(Package):
    """RNA-SeQC is a java program which computes a series of quality control
    metrics for RNA-seq data."""

    homepage = "http://archive.broadinstitute.org/cancer/cga/rna-seqc"
    url      = "http://www.broadinstitute.org/cancer/cga/tools/rnaseqc/RNA-SeQC_v1.1.8.jar"

    version('1.1.8', '71d7b5d3b3dcc1893cdc7f6819185d41', expand=False)
    version('1.1.7', '2d0b8ecac955af2f9bc1b185fdfb6b45', expand=False)
    version('1.1.6', 'fa9c9885081ae2e47f285c7c0f596a14', expand=False)
    version('1.1.5', '4b875671e906f708cbb8fd9bcf0e958d', expand=False)
    version('1.1.4', 'b04d06947c48cb2dc1b0ba29c8232db5', expand=False)

    depends_on('jdk@8:', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'RNA-SeQC_v{0}.jar'.format(self.version.dotted)
        install(jar_file, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "rna-seqc.sh")
        script = join_path(prefix.bin, "rna-seqc")
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec['jdk'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('RNA-SeQC_v{0}.jar', join_path(prefix.bin, jar_file),
                    script, **kwargs)
