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


class PyPycairo(PythonPackage):
    """Pycairo is a set of Python bindings for the cairo graphics library."""

    homepage = "https://www.cairographics.org/pycairo/"
    url      = "https://github.com/pygobject/pycairo/releases/download/v1.17.1/pycairo-1.17.1.tar.gz"
    url      = "https://files.pythonhosted.org/packages/68/76/340ff847897296b2c8174dfa5a5ec3406e3ed783a2abac918cf326abad86/pycairo-1.17.1.tar.gz"

    version('1.17.1', '34c1ee106655b450c4bd57e29371a4a7')

    depends_on('cairo@1.2.0:')
    depends_on('pkgconfig', type='build')
    depends_on('py-setuptools', type='build')

    @run_after('install')
    def post_install(self):
        src = self.prefix.lib + '/pkgconfig/py3cairo.pc'
        dst = self.prefix.lib + '/pkgconfig/pycairo.pc'
        if os.path.exists(src) and not os.path.exists(dst):
            copy(src, dst)
