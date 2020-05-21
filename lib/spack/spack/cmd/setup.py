# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import copy
import os
import sys

import llnl.util.tty as tty
from llnl.util.filesystem import set_executable

import spack.repo
import spack.store
import spack.build_systems.cmake
import spack.cmd
import spack.cmd.install as install
import spack.cmd.common.arguments as arguments
from spack.util.executable import which

from spack.stage import DIYStage

description = "create a configuration script and module, but don't build"
section = "build"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-i', '--ignore-dependencies', action='store_true', dest='ignore_deps',
        help="do not try to install dependencies of requested packages")
    arguments.add_common_arguments(subparser, ['no_checksum', 'spec'])
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="display verbose build output while installing")

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])


def spack_transitive_include_path():
    return ';'.join(
        os.path.join(dep, 'include')
        for dep in os.environ['SPACK_DEPENDENCIES'].split(os.pathsep)
    )


def write_spconfig(package, dirty):
    # Set-up the environment
    spack.build_environment.setup_package(package, dirty)

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
            if name.find('PATH') < 0:
                fout.write('env[%s] = %s\n' % (repr(name), repr(val)))
            else:
                if name == 'SPACK_TRANSITIVE_INCLUDE_PATH':
                    sep = ';'
                else:
                    sep = ':'

                fout.write(
                    'env[%s] = "%s".join(cmdlist("""\n' % (repr(name), sep))
                for part in val.split(sep):
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
        if not spack.repo.path.exists(spec.name):
            tty.die("No package for '{0}' was found.".format(spec.name),
                    "  Use `spack create` to create a new package")
        if not spec.versions.concrete:
            tty.die(
                "spack setup spec must have a single, concrete version. "
                "Did you forget a package version number?")

        spec.concretize()
        package = spack.repo.get(spec)
        if not isinstance(package, spack.build_systems.cmake.CMakePackage):
            tty.die(
                'Support for {0} derived packages not yet implemented'.format(
                    package.build_system_class))

        # It's OK if the package is already installed.

        # Forces the build to run out of the current directory.
        package.stage = DIYStage(os.getcwd())

        # disable checksumming if requested
        if args.no_checksum:
            spack.config.set('config:checksum', False, scope='command_line')

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
        dirty = args.dirty
        write_spconfig(package, dirty)

        # Install this package to register it in the DB and permit
        # module file regeneration
        inst_args = copy.deepcopy(args)
        inst_args = parser.parse_args(
            ['--only=package', '--fake'] + args.spec,
            namespace=inst_args
        )
        install.install(parser, inst_args)
