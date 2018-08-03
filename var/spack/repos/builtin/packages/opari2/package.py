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


class Opari2(AutotoolsPackage):
    """OPARI2 is a source-to-source instrumentation tool for OpenMP and hybrid
    codes. It surrounds OpenMP directives and runtime library calls with calls
    to the POMP2 measurement interface. OPARI2 will provide you with a new
    initialization method that allows for multi-directory and parallel builds
    as well as the usage of pre-instrumented libraries. Furthermore, an
    efficient way of tracking parent-child relationships was added.
    Additionally, we extended OPARI2 to support instrumentation of OpenMP 3.0
    tied tasks.
    """

    homepage = "http://www.vi-hps.org/projects/score-p"
    url      = "http://www.vi-hps.org/upload/packages/opari2/opari2-1.1.2.tar.gz"

    version('2.0.3', 'f34674718ffdb098a48732a1eb9c1aa2')
    version('2.0.1', '74af78f1f27b8caaa4271e0b97fb0fba')
    version('2.0',   '72350dbdb6139f2e68a5055a4f0ba16c')
    version('1.1.4', '245d3d11147a06de77909b0805f530c0')
    version('1.1.2', '9a262c7ca05ff0ab5f7775ae96f3539e')

    def configure_args(self):
        return ["--enable-shared"]
