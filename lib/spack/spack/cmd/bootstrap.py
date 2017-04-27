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
<<<<<<< e10440220a549ef253fe200fa6d0a5fe52dd83fe
import spack.cmd
import spack.cmd.common.arguments as arguments
=======
from spack.util.executable import ProcessError, which
from spack.util.chroot import build_chroot_enviroment, remove_chroot_enviroment

>>>>>>> Created chroot enviroment for bootstrap if isolation mode is enabled

description = "Bootstrap packages needed for spack to run smoothly"
section = "admin"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-j', '--jobs', action='store', type=int,
        help="explicitly set number of make jobs. default is #cpus")
    subparser.add_argument(
        '--keep-prefix', action='store_true', dest='keep_prefix',
        help="don't remove the install prefix if installation fails")
    subparser.add_argument(
<<<<<<< e10440220a549ef253fe200fa6d0a5fe52dd83fe
        '--keep-stage', action='store_true', dest='keep_stage',
        help="don't remove the build stage if installation succeeds")
    subparser.add_argument(
        '-n', '--no-checksum', action='store_true', dest='no_checksum',
        help="do not check packages against checksum")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="display verbose build output while installing")

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])
=======
        '--isolate', action='store_true', dest='isolate',
        help="isolate the bootsraped enviroment from the system")


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


def bootstrap(parser, args):
    origin_url, branch = "https://github.com/TheTimmy/spack", "features/bootstrap" #get_origin_info(args.remote)
    prefix = args.prefix
    isolate = args.isolate

    tty.msg("Fetching spack from '%s': %s" % (args.remote, origin_url))

    if os.path.isfile(prefix):
        tty.die("There is already a file at %s" % prefix)

    mkdirp(prefix)

    if isolate:
        home = os.path.join(prefix, 'home')
        install_dir = os.path.join(home, 'spack')

        mkdirp(home)
        mkdirp(install_dir)

        build_chroot_enviroment(prefix)
    else:
        install_dir = prefix

    #remove_chroot_enviroment(prefix)

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
>>>>>>> Created chroot enviroment for bootstrap if isolation mode is enabled

    subparser.add_argument(
        '--run-tests', action='store_true', dest='run_tests',
        help="run package level tests during installation"
    )


def bootstrap(parser, args, **kwargs):
    kwargs.update({
        'keep_prefix': args.keep_prefix,
        'keep_stage': args.keep_stage,
        'install_deps': 'dependencies',
        'make_jobs': args.jobs,
        'run_tests': args.run_tests,
        'verbose': args.verbose,
        'dirty': args.dirty
    })

    # Define requirement dictionary defining general specs which need
    # to be satisfied, and the specs to install when the general spec
    # isn't satisfied.
    requirement_dict = {'environment-modules': 'environment-modules~X'}

    for requirement in requirement_dict:
        installed_specs = spack.store.db.query(requirement)
        if(len(installed_specs) > 0):
            tty.msg("Requirement %s is satisfied with installed "
                    "package %s" % (requirement, installed_specs[0]))
        else:
            # Install requirement
            spec_to_install = spack.Spec(requirement_dict[requirement])
            spec_to_install.concretize()
            tty.msg("Installing %s to satisfy requirement for %s" %
                    (spec_to_install, requirement))
            kwargs['explicit'] = True
            package = spack.repo.get(spec_to_install)
            package.do_install(**kwargs)
