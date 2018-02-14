##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
##########################################################################
# Copyright (c) 2015-2017 Krell Institute. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
##########################################################################

from spack import *


class CbtfArgonavisGui(QMakePackage):
    """CBTF Argo Navis GUI project contains the GUI that views OpenSpeedShop
       performance information by loading in the Sqlite database files.
    """
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home/"

    version('0.8.1', branch='master',
            git='https://github.com/OpenSpeedShop/cbtf-argonavis-gui.git')

    depends_on("cmake@3.0.2", type='build')
    depends_on("openspeedshop+cuda gui='qt4'")
    depends_on('qt@4.8.6:')
    depends_on("boost@1.50.0:1.59.0")
    depends_on("cbtf")
    depends_on("cbtf-krell")
    depends_on("cbtf-argonavis")
    depends_on("cuda")
    depends_on("mrnet@5.0.1:+lwthreads")
    depends_on("xerces-c@3.1.1:")
    depends_on("graphviz")
    depends_on("qtgraph")

    parallel = False

    def setup_environment(self, spack_env, run_env):
        """Set up the compile and runtime environments for a package."""
        spack_env.set('BOOSTROOT', self.spec['boost'].prefix)
        spack_env.set('CBTF_ROOT', self.spec['cbtf'].prefix)
        spack_env.set('CBTF_KRELL_ROOT', self.spec['cbtf-krell'].prefix)
        spack_env.set('CBTF_ARGONAVIS_ROOT',
                      self.spec['cbtf-argonavis'].prefix)
        spack_env.set('OSS_CBTF_ROOT', self.spec['openspeedshop'].prefix)
        spack_env.set('GRAPHVIZ_ROOT', self.spec['graphviz'].prefix)
        spack_env.set('QTGRAPHLIB_ROOT', self.spec['qtgraph'].prefix)
        spack_env.set('KRELL_ROOT_MRNET', self.spec['mrnet'].prefix)
        spack_env.set('KRELL_ROOT_XERCES', self.spec['xerces-c'].prefix)
        spack_env.set('INSTALL_ROOT', self.spec.prefix)

        # The implementor of qtgraph has set up the library and include
        # paths in a non-conventional way.  We reflect that here.
        run_env.prepend_path(
            'LD_LIBRARY_PATH', join_path(
                self.spec['qtgraph'].prefix.lib64,
                '{0}'.format(self.spec['qt'].version.up_to(3))))
        # The openspeedshop libraries are needed to actually load the
        # performance information into the GUI.
        run_env.prepend_path(
            'LD_LIBRARY_PATH', self.spec['openspeedshop'].prefix.lib64)

    def qmake_args(self):
        options = ['-o', 'Makefile', 'openss-gui.pro']
        return options
