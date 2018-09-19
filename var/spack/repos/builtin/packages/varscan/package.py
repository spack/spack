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


class Varscan(Package):
    """Variant calling and somatic mutation/CNV detection for next-generation
       sequencing data"""

    homepage = "http://dkoboldt.github.io/varscan/"
    url      = "https://github.com/dkoboldt/varscan/releases/download/2.4.2/VarScan.v2.4.2.jar"

    version('2.4.2', '4b810741505a8145a7f8f9f6791bbacf', expand=False)

    depends_on('java', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.jar)
        jar_file = 'VarScan.v{v}.jar'.format(v=self.version.dotted)
        install(jar_file, prefix.jar)

        script_sh = join_path(os.path.dirname(__file__), "varscan.sh")
        script = prefix.bin.varscan
        install(script_sh, script)
        set_executable(script)

        java = join_path(self.spec['java'].prefix, 'bin', 'java')
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('varscan.jar', join_path(prefix.jar, jar_file),
                    script, **kwargs)

    def setup_environment(self, spack_env, run_env):
        run_env.set('VARSCAN_HOME', self.prefix)
        run_env.set('CLASSPATH', self.prefix.jar)
