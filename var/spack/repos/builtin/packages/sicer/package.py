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


class Sicer(Package):
    """A clustering approach for identification of enriched domains
    from histone modification ChIP-Seq data."""

    homepage = "https://home.gwu.edu/~wpeng/Software.htm"
    url      = "https://home.gwu.edu/~wpeng/SICER_V1.1.tgz"

    version('1.1', '1c146ffc9cdd90716a5d025171cba33b')

    depends_on('python',   type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-scipy', type='run')

    def url_for_version(self, version):
        url = "https://home.gwu.edu/~wpeng/SICER_V{0}.tgz"
        return url.format(version.up_to(2))

    def install(self, spec, prefix):
        # everything must live under SICER
        install_tree('SICER', prefix.SICER)

        # replacing a placeholder path in all the scripts
        filter_file('/home/data/SICER1\.1', prefix,
                    *(find(prefix.SICER, '*.sh', recursive=True)),
                    backup=False)

        # one of the scripts is not executable by default
        set_executable(os.path.join(prefix.SICER, 'SICER.sh'))

        # link the main scripts from bin/ to avoid changing PATH
        mkdirp(prefix.bin)
        for f in find(prefix.SICER, '*.sh', recursive=False):
            os.symlink(f, os.path.join(prefix.bin, os.path.basename(f)))

        # utility/fragment-size-estimation.sh is broken (and left unlinked)
        # it could be patched and would introduce dependencies on
        # gnuplot and ghostscript
