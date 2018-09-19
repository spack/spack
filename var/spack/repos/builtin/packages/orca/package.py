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


class Orca(Package):
    """An ab initio, DFT and semiempirical SCF-MO package

       Downloading orca requires accepting a license agreement,
       so spack wil search the working directory for the package"""

    homepage = "https://cec.mpg.de"
    url      = "file://{0}/orca_4_0_1_2_linux_x86-64_openmpi202.tar.zst".format(os.getcwd())

    # required for extracting tar.zst archives
    depends_on('zstd', type='build')

    version('4.0.1.2', sha256='cea442aa99ec0d7ffde65014932196b62343f7a6191b4bfc438bfb38c03942f7',
            expand=False)

    def url_for_version(self, version):
        out = "file://{0}/orca_{1}_linux_x86-64_openmpi202.tar.zst"
        return out.format(os.getcwd(), version.underscored)

    def install(self, spec, prefix):
        # we have to extract the archive ourself
        # fortunately it's just full of a bunch of binaries

        vername = os.path.basename(self.stage.archive_file).split('.')[0]

        zstd = which('zstd')
        zstd('-d', self.stage.archive_file, '-o', vername + '.tar')

        tar = which('tar')
        tar('-xvf', vername + '.tar')

        # there are READMEs in there but they don't hurt anyone
        mkdirp(prefix.bin)
        install_tree(vername, prefix.bin)
