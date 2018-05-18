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


class Chlorop(Package):
    """Chlorop predicts the presence of chloroplast transit peptides
    in protein sequences and the location of potential cTP cleavage
    sites. You will need to obtain the tarball by visiting the
    URL and completing the form. You can then either run spack
    install with the tarball in the directory, or add it to a
    mirror. You will need to set the CHLOROTMP environment variable
    to the full path of the directory you want chlorop to use as
    a temporary directory."""

    homepage = "http://www.cbs.dtu.dk/services/ChloroP/"
    url      = "file://{0}/chlorop-1.1.Linux.tar.gz".format(os.getcwd())

    version('1.1', 'eb0ba6b28dfa735163ad5fc70e30139e46e33f6ae27f87666a7167a4ac5f71d9')

    depends_on('awk', type='run')
    patch('chlorop.patch')

    def install(self, spec, prefix):
        os.rename('chlorop', 'bin/chlorop')
        install_tree('.', prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.set('CHLOROP', self.prefix)
