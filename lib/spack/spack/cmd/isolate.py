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
import sys
import time
import argparse
import cPickle as pickle
from socket import *

import llnl.util.tty as tty
import spack
import spack.cmd
from llnl.util.filesystem import join_path, mkdirp
from spack.util.chroot import build_chroot_environment,  \
                              remove_chroot_environment, \
                              isolate_environment,       \
                              run_command,               \
                              MountDaemon,               \
                              MountOperation

description = "starts an isolated bash session for spack"


def setup_parser(subparser):
    subparser.add_argument(
        '--build-environment', action='store_true', dest='build_enviroment',
        help="startup the isolation mode enviroment")
    subparser.add_argument(
        '--remove-environment', action='store_false', dest='build_enviroment',
        help="shutdown the isolation mode enviroment")
    subparser.add_argument(
        '--start-environment', action='store_true', dest='start_enviroment',
        help="start a local bash in the generated enviroment")
    subparser.add_argument(
        '--permanent', action='store_true', dest='permanent',
        help="""generate a permanent chroot environment to require
administrator rights when using spack as an user""")
    subparser.add_argument(
        '-f', '--force', action='store_true', dest='force',
        help="force the command (use this with caution!)")
    subparser.add_argument(
        '--cli', action='store_true', dest='cli',
        help="connect to a bash session in the generated environment"
    )
    #subparser.add_argument(
    #    '--install-daemon', action='store_true', dest='create_daemon',
    #    help="connect to a bash session in the generated environment"
    #)
    #subparser.add_argument(
    #    '--remove-daemon', action='store_false', dest='create_daemon',
    #    help="connect to a bash session in the generated environment"
    #)
    subparser.add_argument(
        '--start-daemon', action='store_true', dest='start_daemon',
        help="Start a daemon which handles the mount bind process"
    )
    subparser.add_argument(
        '--stop-daemon', action='store_true', dest='stop_daemon',
        help="Stops the daemon which handles the mount bind process"
    )

def construct_environment(force, permanent):
    lockFile = os.path.join(spack.spack_root, '.env')
    if not os.path.exists(lockFile) or force:
        tty.msg("Startup bootstraped enviroment")

        home = os.path.join(spack.spack_bootstrap_root, 'home')
        tmp = os.path.join(spack.spack_bootstrap_root, 'tmp')
        install_dir = os.path.join(home, 'spack')

        mkdirp(home)
        mkdirp(tmp)
        mkdirp(install_dir)

        build_chroot_environment(spack.spack_bootstrap_root, permanent)

        # update the config to set the isolation mode active
        config = spack.config.get_config("config", "site")
        config['isolate'] = True
        spack.config.update_config("config", config, "site")
        with open(lockFile, "w") as out:
            pass

def destroy_environment(force):
    lockFile = os.path.join(spack.spack_root, '.env')
    if os.path.exists(lockFile) or force:
        tty.msg("Shutdown bootstraped enviroment")

        config = spack.config.get_config("config", "site")
        config['isolate'] = False
        wasPermanent = config['permanent']
        config['permanent'] = False
        spack.config.update_config("config", config, "site")

        remove_chroot_environment(spack.spack_bootstrap_root, wasPermanent)
        os.remove(lockFile)

def start_daemon():
    if os.getuid() != 0:
        tty.die("Starting the daemon require root rights")
    daemon = MountDaemon(stdout='/tmp/spack-mount.out',
                         stderr='/tmp/spack-mount.err')
    daemon.start()

def stop_daemon():
    if os.getuid() != 0:
        tty.die("Stopping the daemon require root rights")
    daemon = MountDaemon()
    daemon.stop()

def isolate(parser, args):
    force = args.force
    build_enviroment = args.build_enviroment
    permanent = args.permanent
    cli = args.cli

    if build_enviroment:
        construct_environment(force, permanent)
    else:
        destroy_environment(force)

    if args.start_daemon:
        start_daemon()
    if args.stop_daemon:
        stop_daemon()

    if args.start_enviroment:
        isolate_environment()
    if cli:
        construct_environment(False, False)
        run_command('bash')
        destroy_environment(False)
