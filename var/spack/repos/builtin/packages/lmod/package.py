# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    url      = 'https://github.com/TACC/Lmod/archive/7.4.11.tar.gz'

    version('8.1.5', sha256='3e5846d3d8e593cbcdfa0aed1474569bf5b5cfd19fd288de22051823d449d344')
    version('8.0.9', sha256='9813c22ae4dd21eb3dc480f6ce307156512092b4bca954bf8aacc15944f23673')
    version('7.8.15', sha256='00a257f5073d656adc73045997c28f323b7a4f6d901f1c57b7db2b0cd6bee6e6')
    version('7.8', sha256='40388380a36a00c3ce929a9f88c8fffc93deeabf87a7c3f8864a82acad38c3ba')
    version('7.7.29', 'bd3f171995e6863505e8a958d158ced1')
    version('7.7.13', 'e1d222fa04148707dceb08c82d7e9fa5')
    version('7.7',    '8ac594401716c6d1b40cac22bc1030ca')
    version('7.6.14', '60726c991038b6337fbb27b6a333a2d4')
    version('7.4.11', '70c55ba0ba3877b6d8df536ee7ea6d49')
    version('7.4.10', 'a13e36d6196747fded7987ef3dcfb605')
    version('7.4.9',  'd8ffab81ddca2491fe13e2ac0a4fd320')
    version('7.4.8',  '3b22932437cc29ce546ec887885355e7')
    version('7.4.5',  'fc34029c60dd9782c3d011c2b93fd266')
    version('7.4.1',  '59b2558ee50877f2cf49ed37d7b09fea')
    version('7.3',    '70180ec2ea1fae53aa83350523f6b2b3')
    version('6.4.5',  '14f6c58dbc0a5a75574d795eac2c1e3c')
    version('6.4.1',  '7978ba777c8aa41a4d8c05fec5f780f4')
    version('6.3.7',  '0fa4d5a24c41cae03776f781aa2dedc1')
    version('6.0.1',  '91abf52fe5033bd419ffe2842ebe7af9')

    depends_on('lua@5.1:')
    depends_on('lua-luaposix', type=('build', 'run'))
    depends_on('lua-luafilesystem', type=('build', 'run'))
    depends_on('tcl', type=('build', 'link', 'run'))

    patch('fix_tclsh_paths.patch', when='@:6.4.3')
    patch('0001-fix-problem-with-MODULESHOME-and-issue-271.patch', when='@7.3.28:7.4.10')

    parallel = False

    def setup_environment(self, spack_env, run_env):
        stage_lua_path = join_path(
            self.stage.source_path, 'src', '?.lua')
        spack_env.append_path('LUA_PATH', stage_lua_path.format(
            version=self.version), separator=';')

    def patch(self):
        """The tcl scripts should use the tclsh that was discovered
           by the configure script.  Touch up their #! lines so that the
           sed in the Makefile's install step has something to work on.
           Requires the change in the associated patch file.fg"""
        if self.spec.version <= Version('6.4.3'):
            for tclscript in glob('src/*.tcl'):
                filter_file(r'^#!.*tclsh', '#!@path_to_tclsh@', tclscript)
