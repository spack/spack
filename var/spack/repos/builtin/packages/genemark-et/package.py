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
import glob


class GenemarkEt(Package):
    """Gene Prediction in Bacteria, archaea, Metagenomes and
       Metatranscriptomes."""

    homepage = "http://topaz.gatech.edu/GeneMark"

    version('4.33', '4ab7d7d3277a685dfb49e11bc5b493c3')

    depends_on('perl', type=('build', 'run'))

    def url_for_version(self, version):
        return "file://{0}/gm_et_linux_64.tar.gz".format(os.getcwd())

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('gmes_petap'):
            install_tree('lib', prefix.lib)
            files = glob.iglob('*')
            for file in files:
                if os.path.isfile(file):
                    install(file, prefix.bin)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PERL5LIB', prefix.lib)
