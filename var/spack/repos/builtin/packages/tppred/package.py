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


class Tppred(Package):
    """TPPRED is a software package for the prediction of mitochondrial
       targeting peptides from protein primary sequence."""

    homepage = "https://tppred2.biocomp.unibo.it/tppred2/default/software"
    url      = "http://biocomp.unibo.it/savojard/tppred2.tar.gz"

    version('2.0', 'cd848569f6a8aa51d18fbe55fe45d624')

    depends_on('python@2.7:2.999', type='run')
    depends_on('py-scikit-learn@0.13.1', type='run')
    depends_on('emboss')

    def url_for_version(self, version):
        url = 'http://biocomp.unibo.it/savojard/tppred{0}.tar.gz'
        return url.format(version.up_to(1))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('bin'):
            install('tppred2.py', prefix.bin)
        install_tree('data', prefix.data)
        install_tree('example', prefix.example)
        install_tree('tppred2modules', prefix.modules)

    def setup_environment(self, spack_env, run_env):
        run_env.set('TPPRED_ROOT', prefix)
