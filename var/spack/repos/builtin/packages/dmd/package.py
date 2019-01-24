# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Dmd(MakefilePackage):
    """DMD is the reference compiler for the D programming language."""

    homepage = "https://github.com/dlang/dmd"
    url      = "https://github.com/dlang/dmd/archive/v2.081.1.tar.gz"

    version('2.081.1', sha256='14f3aafe1c93c86646aaeb3ed7361a5fc5a24374cf25c8848c81942bfd9fae1a')

    depends_on('openssl')
    depends_on('curl')

    # https://wiki.dlang.org/Building_under_Posix
    resource(name='druntime',
             url='https://github.com/dlang/druntime/archive/v2.081.1.tar.gz',
             md5='49c8ba48fcb1e53d553a52d8ed7f9164',
             placement='druntime')
    resource(name='phobos',
             url='https://github.com/dlang/phobos/archive/v2.081.1.tar.gz',
             md5='ccf4787275b490eb2ddfc6713f9e9882',
             placement='phobos')
    resource(name='tools',
             url='https://github.com/dlang/tools/archive/v2.081.1.tar.gz',
             md5='a3bc7ed3d60b39712ef011bf19b3d427',
             placement='tools')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.linux.bin64)
        run_env.prepend_path('LIBRARY_PATH', self.prefix.linux.lib64)
        run_env.prepend_path('LD_LIBRARY_PATH', self.prefix.linux.lib64)

    def edit(self, spec, prefix):
        # Move contents to dmd/
        mkdir = which('mkdir')
        mkdir('dmd')
        mv = which('mv')
        dmd_files = [f for f in os.listdir('.')
                     if not f.startswith(('dmd',
                                          'druntime',
                                          'phobos',
                                          'tools',
                                          'spack-build'))]
        for f in dmd_files:
            mv(f, 'dmd')
        # Edit
        dmd_mak = FileFilter('dmd/posix.mak')
        dmd_mak.filter('$(PWD)/../install', prefix, string=True)
        dr_mak = FileFilter('druntime/posix.mak')
        dr_mak.filter('INSTALL_DIR=.*', 'INSTALL_DIR={0}'.format(prefix))
        pb_mak = FileFilter('phobos/posix.mak')
        pb_mak.filter('INSTALL_DIR = .*', 'INSTALL_DIR = {0}'.format(prefix))
        tl_mak = FileFilter('tools/posix.mak')
        tl_mak.filter('INSTALL_DIR = .*', 'INSTALL_DIR = {0}'.format(prefix))

    def build(self, spec, prefix):
        with working_dir('dmd'):
            make('-f', 'posix.mak', 'AUTO_BOOTSTRAP=1')
        with working_dir('phobos'):
            make('-f', 'posix.mak')

    def install(self, spec, prefix):
        with working_dir('dmd'):
            make('-f', 'posix.mak', 'install', 'AUTO_BOOTSTRAP=1')
        with working_dir('phobos'):
            make('-f', 'posix.mak', 'install')
        with working_dir('tools'):
            make('-f', 'posix.mak', 'install')
        with working_dir('druntime'):
            make('-f', 'posix.mak', 'install')
