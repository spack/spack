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


class Pgdspider(Package):
    """"PGDSpider is a powerful automated data conversion tool for population
        genetic and genomics programs"""

    homepage = "http://www.cmpg.unibe.ch/software/PGDSpider"
    url      = "http://www.cmpg.unibe.ch/software/PGDSpider/PGDSpider_2.1.1.2.zip"

    version('2.1.1.2', '170e5b4a002277ff66866486da920693')

    depends_on('java', type=('build', 'run'))
    depends_on('bcftools')
    depends_on('bwa')
    depends_on('samtools')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'PGDSpider{0}-cli.jar'.format(self.version.up_to(1))
        install(jar_file, prefix.bin)

        script_sh = join_path(os.path.dirname(__file__), "pgdspider.sh")
        script = prefix.bin.pgdspider
        install(script_sh, script)
        set_executable(script)

        java = self.spec['java'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('pgdspider.jar', join_path(prefix.bin, jar_file),
                    script, **kwargs)
