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


class AperturePhotometry(Package):
    """Aperture Photometry Tool APT is software for astronomical research"""

    homepage = "http://www.aperturephotometry.org/aptool/"
    url      = "http://www.aperturephotometry.org/aptool/wp-content/plugins/download-monitor/download.php?id=1"

    version('2.7.2', '2beca6aac14c5e0a94d115f81edf0caa9ec83dc9d32893ea00ee376c9360deb0', extension='tar.gz')

    depends_on('java')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'APT.jar'
        install(jar_file, prefix.bin)
        java = join_path(self.spec['java'].prefix, 'bin', 'java')
        script_sh = join_path(os.path.dirname(__file__), "APT.sh")
        script = join_path(prefix.bin, "apt")
        install(script_sh, script)
        set_executable(script)
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('APT.jar', join_path(prefix.bin, 'APT.jar'),
                    script, **kwargs)
