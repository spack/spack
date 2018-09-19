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


class Prodigal(MakefilePackage):
    """Fast, reliable protein-coding gene prediction for prokaryotic
    genomes."""

    homepage = "https://github.com/hyattpd/Prodigal"
    url      = "https://github.com/hyattpd/Prodigal/archive/v2.6.3.tar.gz"

    version('2.6.3', '5181809fdb740e9a675cfdbb6c038466')

    def install(self, spec, prefix):
        make('INSTALLDIR={0}'.format(self.prefix), 'install')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', prefix)
