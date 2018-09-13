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
##############################################################################
# Copyright (c) 2015-2017 Krell Institute. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
##############################################################################
from spack import *
import os


class Qtgraph(QMakePackage):
    """The baseline library used in the CUDA-centric Open|SpeedShop Graphical
       User Interface (GUI) which allows Graphviz DOT formatted data to be
       imported into a Qt application by wrapping the Graphviz libcgraph and
       libgvc within the Qt Graphics View Framework."""

    homepage = "https://github.com/OpenSpeedShop/QtGraph"
    git      = "https://github.com/OpenSpeedShop/QtGraph.git"

    version('develop', branch='master')
    version('1.0.0.0', branch='1.0.0.0')

    # qtgraph depends on these packages
    depends_on('qt@4.8.6:', when='@develop')
    depends_on('qt@5.10.0', when='@1.0.0.0:')

    depends_on("graphviz@2.40.1:", when='@develop')
    depends_on("graphviz@2.40.1", when='@1.0.0.0:')

    def setup_environment(self, spack_env, run_env):
        """Set up the compile and runtime environments for a package."""
        spack_env.set('GRAPHVIZ_ROOT', self.spec['graphviz'].prefix)
        spack_env.set('INSTALL_ROOT', self.prefix)

        # What library suffix should be used based on library existence
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        # The implementor has set up the library and include paths in
        # a non-conventional way.  We reflect that here.
        run_env.prepend_path(
            'LD_LIBRARY_PATH', join_path(
                lib_dir,
                '{0}'.format(self.spec['qt'].version.up_to(3))))

        run_env.prepend_path('CPATH', self.prefix.include.QtGraph)
