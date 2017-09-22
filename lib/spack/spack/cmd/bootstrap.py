##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import llnl.util.tty as tty
import spack
from spack.util.executable import ProcessError, which
from spack.util.chroot import get_username_and_group, get_group, \
                                build_chroot_environment, \
                                remove_chroot_environment


_SPACK_UPSTREAM = 'https://github.com/llnl/spack'

description = "Bootstrap packages needed for spack to run smoothly"
section = "admin"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-j', '--jobs', action='store', type=int,
        help="explicitly set number of make jobs. default is #cpus")
    subparser.add_argument(
        'prefix',
        help="names of prefix where we should install spack")
    subparser.add_argument(
        '--isolate', action='store_true', dest='isolate',
        help="isolate the bootstraped enviroment from the system")
    subparser.add_argument(
        '--permanent', action='store_true', dest='permanent',
        help="""generate a permanent chroot environment to require
administrator rights when using spack as an user""")
    subparser.add_argument(
        '--tarball',
        help="name of the tar file which contains the operating system"
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

# Rewrite the configuration file in the bootstrapped environment to inform
# the local spack that it is running in a isolated environment.
def adapt_config(install_dir, permanent):
    etc_path = join_path(install_dir, "etc")
    config_path = join_path(etc_path, "spack")

    # Add the boostrap file to the config list
    spack.config.ConfigScope('bootstrap', config_path)
    config = spack.config.get_config("config", "bootstrap")

    #write to the config
    config['isolate'] = True
    config['permanent'] = permanent
    spack.config.update_config("config", config, "bootstrap")

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

def bootstrap(parser, args):
    origin_url, branch = "file:///home/spack/Documents/Projects/spack", "features/bootstrap-systemimages" #get_origin_info(args.remote)
    prefix = args.prefix
    isolate = args.isolate
    tarball = args.tarball
    permanent = args.permanent

    tty.msg("Fetching spack from '%s': %s" % (args.remote, origin_url))

    if os.path.isfile(prefix):
        tty.die("There is already a file at %s" % prefix)

    mkdirp(prefix)

    if isolate:
        if not tarball:
            tty.die("Require a tarball with the target system")

        # TODO remove environment if an error ocurred
        unpack_environment(prefix, tarball)
        home = os.path.join(prefix, 'home')
        install_dir = os.path.join(home, 'spack')

        mkdirp(home)
        mkdirp(install_dir)

        #generate and remove enviroment
        build_chroot_environment(prefix, permanent)
        if not permanent:
            remove_chroot_environment(prefix, False)
    else:
        install_dir = prefix

    if os.path.exists(join_path(install_dir, '.git')):
        tty.die("There already seems to be a git repository in %s" % prefix)

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

    if not isolate:
        tty.msg("Successfully created a new spack in %s" % prefix,
                "Run %s/bin/spack to use this installation." % prefix)
    else:
        tty.msg("Successfully created a new spack in %s" % prefix,
                "Run %s/home/spack/bin/spack to use this installation." % prefix)

    # at last change the config
    if isolate:
        adapt_config(install_dir, permanent)

    check_file_owner(prefix)
