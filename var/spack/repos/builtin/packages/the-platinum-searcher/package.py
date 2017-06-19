##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
from spack import *
import os
import shutil


class ThePlatinumSearcher(Package):
    """Fast parallel recursive grep alternative"""
    homepage = "https://github.com/monochromegane/the_platinum_searcher"
    url = "https://github.com/monochromegane/the_platinum_searcher"

    package = 'github.com/monochromegane/the_platinum_searcher/...'

    version('head', go=package)

    extends("go", deptypes='build')

    def install(self, spec, prefix):
        env = os.environ
        env['GOPATH'] = self.stage.source_path + ':' + env['GOPATH']
        go('install', self.package, env=env)
        shutil.copytree('bin', os.path.join(prefix, 'bin'))
