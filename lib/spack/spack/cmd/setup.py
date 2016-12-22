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
import argparse
import copy
import os
import string
import sys

import llnl.util.tty as tty
import spack
import spack.store
import spack.cmd
import spack.cmd.install as install
import spack.cmd.common.arguments as arguments
from llnl.util.filesystem import set_executable
from spack import which
from spack.stage import DIYStage

description = "Create a configuration script and module, but don't build."

# Same cmd line arguments as `spack install`
setup_parser = install.setup_parser

def spack_transitive_include_path():
    return ';'.join(
        os.path.join(dep, 'include')
        for dep in os.environ['SPACK_DEPENDENCIES'].split(os.pathsep)
    )


def write_spconfig(package):
    # Set-up the environment
    spack.build_environment.setup_package(package)

    cmd = [str(which('cmake'))] + package.std_cmake_args + package.cmake_args()

    env = dict()

    paths = os.environ['PATH'].split(':')
    paths = [item for item in paths if 'spack/env' not in item]
    env['PATH'] = ':'.join(paths)
    env['SPACK_TRANSITIVE_INCLUDE_PATH'] = spack_transitive_include_path()
    env['CMAKE_PREFIX_PATH'] = os.environ['CMAKE_PREFIX_PATH']
    env['CC'] = os.environ['SPACK_CC']
    env['CXX'] = os.environ['SPACK_CXX']
    env['FC'] = os.environ['SPACK_FC']

    setup_fname = 'spconfig.py'
    with open(setup_fname, 'w') as fout:
        fout.write(
            r"""#!%s
#

import sys
import os
import subprocess

def cmdlist(str):
    return list(x.strip().replace("'",'') for x in str.split('\n') if x)
env = dict(os.environ)
""" % sys.executable)

        env_vars = sorted(list(env.keys()))
        for name in env_vars:
            val = env[name]
            if string.find(name, 'PATH') < 0:
                fout.write('env[%s] = %s\n' % (repr(name), repr(val)))
            else:
                if name == 'SPACK_TRANSITIVE_INCLUDE_PATH':
                    sep = ';'
                else:
                    sep = ':'

                fout.write(
                    'env[%s] = "%s".join(cmdlist("""\n' % (repr(name), sep))
                for part in string.split(val, sep):
                    fout.write('    %s\n' % part)
                fout.write('"""))\n')

        fout.write('\ncmd = cmdlist("""\n')
        fout.write('%s\n' % cmd[0])
        for arg in cmd[1:]:
            fout.write('    %s\n' % arg)
        fout.write('""") + sys.argv[1:]\n')
        fout.write('\nproc = subprocess.Popen(cmd, env=env)\nproc.wait()\n')
        set_executable(setup_fname)


def top_install(spec, install_package=True, install_dependencies=True, **kwargs):
    """Top-level install method for spack setup."""
    if install_dependencies:
        # Install dependencies as-if they were installed
        # for root (explicit=False in the DB)
        for s in spec.dependencies():
            package = spack.repo.get(s)
            package.do_install(install_dependencies=True, explicit=False, **kwargs)

    if install_package:
        package = spack.repo.get(spec)
        package.stage = DIYStage(os.getcwd())    # Force build in cwd

        # --- Generate spconfig.py
        tty.msg(
            'Generating spconfig.py [{0}]'.format(package.spec.cshort_spec)
        )
        write_spconfig(package)

        # --- Install this package to register it in the DB
        # --- and permit module file regeneration
        del kwargs['fake']
        package.do_install(
            install_dependencies=False, explicit=True, fake=True,
            **kwargs)


def setup(self, args):
    # Further parsing of arguments
    kwargs = install.validate_args(args)
    spec = spack.cmd.parse_specs(args.package, concretize=False, allow_multi=False)

    # Log if command line args call for it
    with install.setup_logging(spec, args):
        # Take a write lock before checking for existence.
        with spack.store.db.write_transaction():

            if not spack.repo.exists(spec.name):
                tty.die("No such package: %s" % spec.name)

            if not spec.versions.concrete:
                tty.die(
                    "spack setup spec must have a single, concrete version. "
                    "Did you forget a package version number?")

            spec.concretize()
            install.show_spec(spec, args)

            package = spack.repo.get(spec)
            if not isinstance(package, spack.CMakePackage):
                tty.die(
                    'Support for packages derived from {0} '
                    'is not yet implemented'.format(
                        package.build_system_class
                    )
                )

            top_install(spec, **kwargs)
