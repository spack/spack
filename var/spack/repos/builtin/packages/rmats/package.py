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
from os import symlink


class Rmats(Package):
    """MATS is a computational tool to detect differential alternative
       splicing events from RNA-Seq data."""

    homepage = "https://rnaseq-mats.sourceforge.net/index.html"
    url      = "https://downloads.sourceforge.net/project/rnaseq-mats/MATS/rMATS.4.0.2.tgz"

    version('4.0.2', sha256='afab002a9ae836d396909aede96318f6dab6e5818078246419dd563624bf26d1')

    depends_on('python@2.7:', type='run')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('openblas')

    def install(self, spec, prefix):
        # since the tool is a python script we install it to /usr/lib
        install_tree('rMATS-turbo-Linux-UCS4', join_path(prefix.lib, 'rmats'))

        # the script has an appropriate shebang so a quick symlink will do
        set_executable(join_path(prefix.lib, 'rmats/rmats.py'))
        mkdirp(prefix.bin)
        symlink(join_path(prefix.lib, 'rmats/rmats.py'),
                join_path(prefix.bin, 'rmats'))
