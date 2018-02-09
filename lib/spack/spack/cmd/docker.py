##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import argparse
import contextlib
import os
import os.path
import tempfile

import llnl.util.filesystem
import llnl.util.tty as tty
import spack.tengine
import spack.util.executable

description = "use docker to build and serve mirrors and binary caches"
section = "build"
level = "long"

#: Wrapper to the 'docker' command
docker_cmd = spack.util.executable.Executable('docker')

#: Name of the mirror volume
mirror_volume = 'spack-mirror'
#: Destination of the mirror volume
mirror_destination = '/share/spack/mirror'

#: Name of the opt volume
opt_volume = 'spack-opt'
#: destination of the opt volume
opt_destination = '/home/spack/opt'


@contextlib.contextmanager
def docker_volume(name, remove_on_exit=False):
    """Ensure that a docker volume exists within the context manager, and
    optionally deletes it on exit.

    Args:
        name (str): name of the volume
        remove_on_exit (bool): if True the volume is deleted on exit

    Return:
        a format string to be used with ``--mount`` that accepts the
        destination of the mount in a container
    """
    verbosity = _verbosity_kwargs(activate=False)
    # Check if the volume exists...
    docker_cmd('volume', 'inspect', name, fail_on_error=False, **verbosity)
    # ... and, if not, creates it
    if docker_cmd.returncode:
        docker_cmd('volume', 'create', name, **verbosity)

    yield

    if remove_on_exit:
        docker_cmd('volume', 'rm', name, **verbosity)


def create_dockerfile(image, branch, repo):
    """Creates a dockerfile for the build image, starting from a template.

    Args:
        image (str): base image for the build
        branch (str): branch of the Spack repository to checkout
        repo (str): Spack repository to checkout

    Returns:
        directory where the Dockerfile resides
    """
    # Dictionaries with the system dependencies needed in
    # various distributions
    system_dependencies = {
        'centos': """yum -y update && \\
    yum -y upgrade && \\
    yum -y install git gcc gcc-c++ gcc-gfortran make bzip2 patch file
    """,
        'ubuntu': """apt-get update && \\
    apt-get upgrade -y && \\
    apt-get install -y git gcc g++ gfortran make bzip2 && \\
    apt-get install -y patch file curl python gnupg2 xz-utils && \\
    rm -rf /var/lib/apt/lists/*
    """
    }

    # Create a temporary working directory
    working_directory = tempfile.mkdtemp()
    dockerfile = os.path.join(working_directory, 'Dockerfile')

    # Dockerfile for our build image
    template_dockerfile = os.path.join('docker', 'builder', 'Dockerfile')
    t = spack.tengine.make_environment().get_template(template_dockerfile)

    # Stamp the template Dockerfile
    dependencies = next(
        v for k, v in system_dependencies.items() if k in image
    )
    with open(dockerfile, 'w') as f:
        f.write(t.render({
            'image': image,
            'dependencies': dependencies,
            'branch': branch,
            'repo': repo
        }))

    return working_directory


def _verbosity_kwargs(activate):
    if not activate:
        return {
            'output': os.devnull,
            'error': os.devnull
        }
    return {}


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='subparser_name')

    # 'start' sub-command
    start = sp.add_parser('start', help='start docker related services')
    start_sp = start.add_subparsers(metavar='SERVICES', dest='service_name')

    # 'start mirror'
    mirror = start_sp.add_parser(
        'mirror', help='docker daemon that serves a spack mirror via http'
    )
    mirror.add_argument(
        '--ip', help='ip address of the exposed volume', default='0.0.0.0'
    )
    mirror.add_argument(
        '--port', help='port to expose on host', default='32679'
    )

    # 'build'
    build = sp.add_parser(
        'build', help='populate the mirror with sources and binary artifacts'
    )
    build.add_argument(
        '--repo', help='git repository used for the build', default='spack'
    )
    build.add_argument(
        '--branch', help='git branch used for the build', default='develop'
    )
    build.add_argument(
        '--image', help='base image for the build', default='centos:7'
    )
    build.add_argument(
        '--no-cache',
        help='avoid building a binary cache of the specs',
        action='store_false', dest='binary_cache'
    )
    build.add_argument(
        '--net', choices=('none', 'bridge'), default='none',
        help='network setting to be used at install time',
    )
    build.add_argument(
        'spec', nargs=argparse.REMAINDER, help='spec to be built'
    )


def start_mirror(args):
    # Check if the mirror exists already
    output = docker_cmd(
        'ps', '-q',
        '--filter', 'name=spack-mirror',
        '--filter', 'status=running',
        fail_on_error=False, output=str, error=os.devnull
    )
    if output:
        msg = 'Docker mirror already up '
        msg += '[docker ps --filter "name=spack-mirror"]'
        tty.msg(msg)
        return

    verbosity = _verbosity_kwargs(activate=args.verbose or args.debug)

    with docker_volume(mirror_volume):
        # Build the docker image for the server
        dockerfile_directory = os.path.join(
            spack.share_path, 'docker', 'mirror-server'
        )
        with llnl.util.filesystem.working_dir(dockerfile_directory):
            docker_cmd('build', '-t', 'mirror-server-image', '.', **verbosity)

        # Start the server
        docker_cmd(
            'run', '-d', '--rm',
            '--mount',
            'source={0},target={1}'.format(mirror_volume, mirror_destination),
            '-p', '{0.ip}:{0.port}:8000'.format(args),
            '--name', 'spack-mirror', 'mirror-server-image',
            **verbosity
        )
        tty.msg('Docker mirror started [{0.ip}:{0.port}]'.format(args))


def build(args):
    verbosity = _verbosity_kwargs(activate=args.verbose or args.debug)
    specs = ' '.join(args.spec)

    # Create the dockerfile
    tmp_dir = create_dockerfile(args.image, args.branch, args.repo)

    # Build the image
    with llnl.util.filesystem.working_dir(tmp_dir):
        tty.msg('Building image for "{0.image}"'.format(args))
        docker_cmd('build', '-t', 'spack-builder', '.', **verbosity)

    with docker_volume(mirror_volume):
        # Fetch the sources into the mirror
        tty.msg('Fetching source files')
        docker_cmd(
            'run', '--rm',
            '--mount', 'source={0},target={1}'.format(
                mirror_volume, mirror_destination
            ),
            'spack-builder',
            'mirror', 'create', '-D', '-d', mirror_destination, specs,
            **verbosity
        )

        # These two containers communicate through the opt volume
        # that is deleted on exit
        with docker_volume(opt_volume, remove_on_exit=True):

            common_setup = [
                'run', '--rm',
                '--mount', 'source={0},target={1}'.format(
                    mirror_volume, mirror_destination
                ),
                '--mount', 'source={0},target={1}'.format(
                    opt_volume, opt_destination
                ),
                '-v', '{0}:{1}'.format(
                    os.path.join(spack.opt_path, 'spack', 'gpg'),
                    '/home/spack/opt/spack/gpg'
                )
            ]

            install_run = [
                '--net', args.net, 'spack-builder', 'install', specs
            ]

            buildcache_run = [
                'spack-builder', 'buildcache',
                'create', '-r', '-d', mirror_destination, '-f', specs
            ]

            # Install the spec
            tty.msg('Installing specs [--net={0.net}]'.format(args))
            docker_cmd(*(common_setup + install_run), **verbosity)

            # Build the binary cache
            if args.binary_cache:
                tty.msg('Creating binary caches')
                docker_cmd(*(common_setup + buildcache_run), **verbosity)


def docker(parser, args):

    def start(args):
        start_callbacks = {
            'mirror': start_mirror
        }
        start_callbacks[args.service_name](args)

    callbacks = {
        'start': start,
        'build': build
    }
    callbacks[args.subparser_name](args)
