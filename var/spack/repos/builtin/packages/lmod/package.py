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
from glob import glob


class Lmod(AutotoolsPackage):
    """Lmod is a Lua based module system that easily handles the MODULEPATH
    Hierarchical problem. Environment Modules provide a convenient way to
    dynamically change the users' environment through modulefiles. This
    includes easily adding or removing directories to the PATH environment
    variable. Modulefiles for Library packages provide environment variables
    that specify where the library and header files can be found.
    """

    homepage = 'https://www.tacc.utexas.edu/research-development/tacc-projects/lmod'
    url = 'https://github.com/TACC/Lmod/archive/7.3.tar.gz'

    version('7.3',   '70180ec2ea1fae53aa83350523f6b2b3')
    version('6.4.5', '14f6c58dbc0a5a75574d795eac2c1e3c')
    version('6.4.1', '7978ba777c8aa41a4d8c05fec5f780f4')
    version('6.3.7', '0fa4d5a24c41cae03776f781aa2dedc1')
    version('6.0.1', '91abf52fe5033bd419ffe2842ebe7af9')

    depends_on('lua@5.2:')
    depends_on('lua-luaposix', type=('build', 'run'))
    depends_on('lua-luafilesystem', type=('build', 'run'))
    depends_on('tcl', type=('build', 'run'))

    parallel = False

    def setup_environment(self, spack_env, run_env):
        stage_lua_path = join_path(
            self.stage.path, 'Lmod-{version}', 'src', '?.lua')
        spack_env.append_path('LUA_PATH', stage_lua_path.format(
            version=self.version), separator=';')

    patch('fix_tclsh_paths.patch', when='@:6.4.3')

    def patch(self):
        """The tcl scripts should use the tclsh that was discovered
           by the configure script.  Touch up their #! lines so that the
           sed in the Makefile's install step has something to work on.
           Requires the change in the associated patch file.fg"""
        if self.spec.version <= Version('6.4.3'):
            for tclscript in glob('src/*.tcl'):
                filter_file(r'^#!.*tclsh', '#!@path_to_tclsh@', tclscript)
