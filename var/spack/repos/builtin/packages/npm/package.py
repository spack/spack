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
import os
from spack import *


class Npm(AutotoolsPackage):
    """npm: A package manager for javascript."""

    homepage = "https://github.com/npm/npm"
    # base http://www.npmjs.com/
    url      = "https://registry.npmjs.org/npm/-/npm-3.10.5.tgz"

    version('3.10.9', 'ec1eb22b466ce87cdd0b90182acce07f')
    version('3.10.5', '46002413f4a71de9b0da5b506bf1d992')

    depends_on('node-js')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        npm_config_cache_dir = "%s/npm-cache" % dependent_spec.prefix
        if not os.path.isdir(npm_config_cache_dir):
            mkdir(npm_config_cache_dir)
        run_env.set('npm_config_cache', npm_config_cache_dir)
        spack_env.set('npm_config_cache', npm_config_cache_dir)
