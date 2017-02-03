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

description = "create a configuration script and module, but don't build"


def setup_parser(subparser):
    subparser.add_argument(
        '-i', '--ignore-dependencies', action='store_true', dest='ignore_deps',
        help="do not try to install dependencies of requested packages")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="display verbose build output while installing")
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="specs to use for install. must contain package AND version")

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])


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


def setup(self, args):
    if not args.spec:
        tty.die("spack setup requires a package spec argument.")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack setup only takes one spec.")

    # Take a write lock before checking for existence.
    with spack.store.db.write_transaction():
        spec = specs[0]
        if not spack.repo.exists(spec.name):
            tty.die("No package for '{0}' was found.".format(spec.name),
                    "  Use `spack create` to create a new package")
        if not spec.versions.concrete:
            tty.die(
                "spack setup spec must have a single, concrete version. "
                "Did you forget a package version number?")

        spec.concretize()
        package = spack.repo.get(spec)
        if not isinstance(package, spack.CMakePackage):
            tty.die(
                'Support for {0} derived packages not yet implemented'.format(
                    package.build_system_class
                )
            )

        # It's OK if the package is already installed.

        # Forces the build to run out of the current directory.
        package.stage = DIYStage(os.getcwd())

        # TODO: make this an argument, not a global.
        spack.do_checksum = False

        # Install dependencies if requested to do so
        if not args.ignore_deps:
            parser = argparse.ArgumentParser()
            install.setup_parser(parser)
            inst_args = copy.deepcopy(args)
            inst_args = parser.parse_args(
                ['--only=dependencies'] + args.spec,
                namespace=inst_args
            )
            install.install(parser, inst_args)
        # Generate spconfig.py
        tty.msg(
            'Generating spconfig.py [{0}]'.format(package.spec.cshort_spec)
        )
        write_spconfig(package)
        # Install this package to register it in the DB and permit
        # module file regeneration
        inst_args = copy.deepcopy(args)
        inst_args = parser.parse_args(
            ['--only=package', '--fake'] + args.spec,
            namespace=inst_args
        )
        install.install(parser, inst_args)
