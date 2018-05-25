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
import os.path


class Astral(Package):
    """ASTRAL is a tool for estimating an unrooted species tree given a set of
       unrooted gene trees."""

    homepage = "https://github.com/smirarab/ASTRAL"
    url      = "https://github.com/smirarab/ASTRAL/archive/v4.10.7.tar.gz"

    version('4.10.7', '38c81020570254e3f5c75d6c3c27fc6d')

    depends_on('java', type=('build', 'run'))
    depends_on('zip', type='build')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        make = Executable('./make.sh')
        make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree('lib', prefix.tools.lib)
        jar_file = 'astral.{v}.jar'.format(v=self.version)
        install(jar_file, prefix.tools)

        script_sh = join_path(os.path.dirname(__file__), "astral.sh")
        script = prefix.bin.astral
        install(script_sh, script)
        set_executable(script)

        java = self.spec['java'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('astral.jar', join_path(prefix.tools, jar_file),
                    script, **kwargs)

    def setup_environment(self, spack_env, run_env):
        run_env.set('ASTRAL_HOME', self.prefix.tools)
