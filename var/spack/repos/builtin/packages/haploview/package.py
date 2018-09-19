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


class Haploview(Package):
    """Haploview is designed to simplify and expedite the process of haplotype
       analysis."""

    homepage = "http://www.broadinstitute.org/haploview/haploview"
    url      = "https://downloads.sourceforge.net/project/haploview/release/Haploview4.1.jar"

    version('4.1', 'f7aa4accda5fad1be74c9c1969c6ee7d', expand=False)

    depends_on('java', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'Haploview{v}.jar'.format(v=self.version)
        install(jar_file, prefix.bin)

        script_sh = join_path(os.path.dirname(__file__), "haploview.sh")
        script = prefix.bin.haploview
        install(script_sh, script)
        set_executable(script)

        java = self.spec['java'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('haploview.jar', join_path(prefix.bin, jar_file),
                    script, **kwargs)
