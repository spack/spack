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
from socket import *

import llnl.util.tty as tty
import spack
import spack.cmd
from spack.util.executable import ProcessError, which
from llnl.util.filesystem import join_path, mkdirp
from spack.util.chroot import build_chroot_environment
from spack.util.chroot import remove_chroot_environment
from spack.util.chroot import run_command
from spack.util.chroot import MountDaemon

description = "manages the isolation of spack by a jail"
section = "admin"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '--build-environment', action='store', dest='build_environment',
        help="create a environment to jail spack")
    subparser.add_argument(
        '--remove-environment', action='store_true', dest='remove_environment',
        help="shutdown the local spack jailed enviroment")
    subparser.add_argument(
        '--permanent', action='store_true', dest='permanent',
        help="""generate a permanent chroot environment to require
administrator rights when using spack as an user""")
    subparser.add_argument(
        '-f', '--force', action='store_true', dest='force',
        help="force the command (use this with caution!)")
    subparser.add_argument(
        '--cli', action='store_true', dest='cli',
        help="connect to a bash session in the generated environment")
    subparser.add_argument(
        '-r', '--remote', action='store', dest='remote',
        help="name of the remote to bootstrap from",
        default='origin')
    subparser.add_argument(
        '--tarball',
        help="name of the tar file which contains the operating system")
    # subparser.add_argument(
    # '--install-daemon', action='store_true', dest='create_daemon',
    # help="connect to a bash session in the generated environment"
    # )
    # subparser.add_argument(
    # '--remove-daemon', action='store_false', dest='create_daemon',
    # help="connect to a bash session in the generated environment"
    # )
    subparser.add_argument(
        '--start-daemon', action='store_true', dest='start_daemon',
        help="Start a daemon which handles the mount bind process"
    )
    subparser.add_argument(
        '--stop-daemon', action='store_true', dest='stop_daemon',
        help="Stops the daemon which handles the mount bind process"
    )


def get_origin_info(remote):
    git_dir = join_path(spack.prefix, '.git')
    git = which('git', required=True)
    try:
        branch = git('symbolic-ref', '--short', 'HEAD', output=str)
    except ProcessError:
        branch = 'develop'
        tty.warn('No branch found; using default branch: %s' % branch)
    if remote == 'origin' and \
       branch not in ('master', 'develop'):
        branch = 'develop'
        tty.warn('Unknown branch found; using default branch: %s' % branch)
    try:
        origin_url = git(
            '--git-dir=%s' % git_dir,
            'config', '--get', 'remote.%s.url' % remote,
            output=str)
    except ProcessError:
        origin_url = _SPACK_UPSTREAM
        tty.warn('No git repository found; '
                 'using default upstream URL: %s' % origin_url)
    return (origin_url.strip(), branch.strip())


def adapt_config(install_dir, permanent):
    """
    Rewrite the configuration file in the bootstrapped environment to inform
    the local spack that it is running in a isolated environment.
    """
    etc_path = join_path(install_dir, "etc")
    config_path = join_path(etc_path, "spack")

    # Add the boostrap file to the config list
    spack.config.ConfigScope('bootstrap', config_path)
    config = spack.config.get_config('config', 'bootstrap')

    # write to the config
    config['isolate'] = True
    config['permanent'] = permanent
    spack.config.update_config('config', config, 'bootstrap')


def check_file_owner(prefix):
    if os.geteuid() == 0:
        who = which('who', required=True)
        chown = which('chown', required=True)

        username = who(output=str).split(' ')[0]
        group = get_group(username)
        chown('-R', '%s:%s' % (username, group), '%s' % (prefix))


def unpack_environment(path, tarball):
    tar = which('tar', required=True)
    tar('-xzf', tarball, '-C', path, '--strip-components=1')


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
            out.write('please do not remove this file')


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
    build_enviroment = args.build_environment
    permanent = args.permanent
    if build_enviroment:
        # origin_url, branch = get_origin_info(args.remote)
        origin_url = "https://github.com/TheTimmy/spack.git"
        branch = "features/bootstrap-systemimages"

        prefix = args.build_environment
        tarball = args.tarball
        permanent = args.permanent

        tty.msg("Fetching spack from '%s': %s" % (args.remote, origin_url))
        if not tarball:
            tty.die("Require a tarball with the target system")

        if os.path.isfile(prefix):
            tty.die("There is already a file at %s" % prefix)
        mkdirp(prefix)

        # TODO remove environment if an error ocurred
        unpack_environment(prefix, tarball)
        home = os.path.join(prefix, 'home')
        install_dir = os.path.join(home, 'spack')

        mkdirp(home)
        mkdirp(install_dir)

        # generate and remove enviroment
        build_chroot_environment(prefix, permanent)
        if not permanent:
            remove_chroot_environment(prefix, False)

        if os.path.exists(join_path(install_dir, '.git')):
            tty.die("There already seems to be a git repository in %s" %
                    prefix)

        files_in_the_way = os.listdir(install_dir)
        if files_in_the_way:
            tty.die("There are already files there! "
                    "Delete these files before boostrapping spack.",
                    *files_in_the_way)

        tty.msg("Installing:",
                "%s/bin/spack" % install_dir,
                "%s/lib/spack/..." % install_dir)

        os.chdir(install_dir)
        git = which('git', required=True)
        git('init', '--shared', '-q')
        git('remote', 'add', 'origin', origin_url)
        git('fetch', 'origin', '%s:refs/remotes/origin/%s' % (branch, branch),
                               '-n', '-q')
        git('reset', '--hard', 'origin/%s' % branch, '-q')
        git('checkout', '-B', branch, 'origin/%s' % branch, '-q')

        tty.msg("Successfully created a new spack in %s" % prefix,
                "Run %s/home/spack/bin/spack to use this installation." %
                prefix)

        adapt_config(install_dir, permanent)
        check_file_owner(prefix)

    if args.remove_environment:
        destroy_environment(force)
    if args.start_daemon:
        start_daemon()
    if args.stop_daemon:
        stop_daemon()
    if args.cli:
        construct_environment(False, False)
        run_command('bash')
        destroy_environment(False)
