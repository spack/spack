##############################################################################
# Copyright (c) 2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Elizabeth Fischer
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import argparse
import os
import string
import sys

import llnl.util.tty as tty
import spack
import spack.cmd
from spack import which
from spack.cmd.edit import edit_package
from spack.stage import DIYStage
from llnl.util.filesystem import set_executable

description = "Create a configuration script and module, but don't build."


def setup_parser(subparser):
    subparser.add_argument(
        '-i', '--ignore-dependencies', action='store_true', dest='ignore_deps',
        help="Do not try to install dependencies of requested packages.")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="Display verbose build output while installing.")
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="specs to use for install.  Must contain package AND version.")
    subparser.add_argument(
        '--dirty', action='store_true', dest='dirty',
        help="Install a package *without* cleaning the environment.")


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

        fout.write("env['CMAKE_TRANSITIVE_INCLUDE_PATH'] = env['SPACK_TRANSITIVE_INCLUDE_PATH']   # Deprecated\n")  # NOQA: ignore=E501
        fout.write('\ncmd = cmdlist("""\n')
        fout.write('%s\n' % cmd[0])
        for arg in cmd[1:]:
            fout.write('    %s\n' % arg)
        fout.write('""") + sys.argv[1:]\n')
        fout.write('\nproc = subprocess.Popen(cmd, env=env)\nproc.wait()\n')
        set_executable(setup_fname)


def setup(self, args):
    if not args.spec:
        tty.die("spack setup requires a package spec argument.")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack setup only takes one spec.")

    # Take a write lock before checking for existence.
    with spack.installed_db.write_transaction():
        spec = specs[0]
        if not spack.repo.exists(spec.name):
            tty.warn("No such package: %s" % spec.name)
            create = tty.get_yes_or_no("Create this package?", default=False)
            if not create:
                tty.msg("Exiting without creating.")
                sys.exit(1)
            else:
                tty.msg("Running 'spack edit -f %s'" % spec.name)
                edit_package(spec.name, spack.repo.first_repo(), None, True)
                return

        if not spec.versions.concrete:
            tty.die(
                "spack setup spec must have a single, concrete version. "
                "Did you forget a package version number?")

        spec.concretize()
        package = spack.repo.get(spec)

        # It's OK if the package is already installed.

        # Forces the build to run out of the current directory.
        package.stage = DIYStage(os.getcwd())

        # TODO: make this an argument, not a global.
        spack.do_checksum = False

        if not isinstance(package, spack.CMakePackage):
            raise RuntimeError(
                'Support for {0} not yet implemented'.format(type(package)))

        write_spconfig(package)
