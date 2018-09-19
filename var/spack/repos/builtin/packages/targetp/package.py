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


class Targetp(Package):
    """TargetP predicts the subcellular location of eukaryotic protein sequences.

       Note: A manual download is required for TargetP.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://www.cbs.dtu.dk/services/TargetP/"
    url      = "file://{0}/targetp-1.1b.Linux.tar.gz".format(os.getcwd())

    version('1.1b', '80233d0056e11abfd22a4ce73d1808c6')

    depends_on('perl', type='run')
    depends_on('awk', type='run')
    depends_on('chlorop')
    depends_on('signalp')

    def patch(self):
        targetp = FileFilter('targetp')
        targetp.filter('TARGETP=', '#TARGETP=')
        targetp.filter('CHLOROP=/usr/cbs/bio/bin/chlorop',
                       self.spec['chlorop'].prefix.bin.chlorop)
        targetp.filter('SIGNALP=/usr/cbs/bio/bin/signalp',
                       self.spec['signalp'].prefix.signalp)
        targetp.filter('TMP=/scratch', 'TMP=/tmp')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('etc', prefix.etc)
        install_tree('how', prefix.how)
        install_tree('test', prefix.test)
        install_tree('tmp', prefix.tmp)
        install('targetp', prefix.targetp)

    def setup_environment(self, spack_env, run_env):
        run_env.set('TARGETP', self.prefix)
        run_env.prepend_path('PATH', self.prefix)
