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


class Qorts(RPackage):
    """The QoRTs software package is a fast, efficient, and portable
    multifunction toolkit designed to assist in the analysis, quality
    control, and data management of RNA-Seq and DNA-Seq datasets. Its
    primary function is to aid in the detection and identification of
    errors, biases, and artifacts produced by high-throughput sequencing
    technology."""

    homepage = "https://github.com/hartleys/QoRTs"
    url      = "https://github.com/hartleys/QoRTs/releases/download/v1.2.42/QoRTs_1.2.42.tar.gz"

    version('1.2.42', '7d46162327b0da70bfe483fe2f2b7829')

    depends_on('java', type='run')

    resource(
        name='QoRTs.jar',
        url='https://github.com/hartleys/QoRTs/releases/download/v1.2.42/QoRTs.jar',
        md5='918df4291538218c12caa3ab98c535e9',
        placement='jarfile',
        expand=False
    )

    @run_after('install')
    def install_jar(self):
        install_tree(join_path(self.stage.source_path, 'jarfile'),
                     self.prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "QoRTs.sh")
        script = self.prefix.bin.QoRTs
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec['java'].prefix.bin.java
        kwargs = {'backup': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('QoRTs.jar', join_path(self.prefix.bin, 'QoRTs.jar'),
                    script, **kwargs)
