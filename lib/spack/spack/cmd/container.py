# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse

import llnl.util.tty as tty

try:
    import hpccm
    from hpccm.building_blocks.base import bb_base
    from hpccm.primitives import baseimage, comment, copy, environment, shell
except ImportError:
    # The HPCCM module is not present, but do not error out here.
    # HPCCM is optional unless using 'spack container'.  Check again
    # inside the container() function and error there.
    pass

import spack
import spack.cmd
import spack.spec

description = "generate a container specification file"
section = "build"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="specs of packages")

    subparser.add_argument(
        '--baseimage', action='store', type=str, default='centos:7',
        help='container base image (default: centos:7)')
    subparser.add_argument(
        '--depth', action='store', type=int, default=2,
        help='spack DAG depth to use (default: 2)')
    subparser.add_argument(
        '--distro', action='store', type=str, default='',
        choices=['centos', 'rhel', 'ubuntu', 'ubuntu16', 'ubuntu18'],
        help='Linux distribution type of the base image '
        '(default: try to determine automatically from the base image name)')
    subparser.add_argument(
        '--extra-package', action='append', type=str, default=[],
        help='extra OS package to install')
    subparser.add_argument(
        '--format', action='store', type=str, default='docker',
        choices=['docker', 'singularity'],
        help='container specification format (default: docker)')
    subparser.add_argument(
        '--multi-stage', action='store_true', default=False,
        help='generate a multi-stage Dockerfile (Docker specific)')
    subparser.add_argument(
        '--no-checksum', action='store_true', default=False,
        help='do not use checksums to verify downloaded files (unsafe)')
    subparser.add_argument(
        '--show-log-on-error', action='store_true', default=False,
        help='print full build log if build fails')
    subparser.add_argument(
        '--spack-branch', '--branch', action='store', type=str,
        default='develop',
        help='branch of Spack to deploy (default: develop)')


def container(parser, args):
    if not args.specs:
        tty.die("spack container requires at least one spec")

    # Verify that HPCCM is installed
    try:
        recipe = hpccm.Stage()
    except NameError:
        tty.die('The HPCCM Python module must be installed to use '
                'spack container')

    recipe += baseimage(image=args.baseimage, _distro=args.distro)

    # Base OS dependencies
    recipe += hpccm.building_blocks.packages(
        apt=['autoconf', 'build-essential', 'bzip2', 'ca-certificates',
             'coreutils', 'cpio', 'curl', 'environment-modules', 'git',
             'gzip', 'libssl-dev', 'make', 'openssh-client', 'patch',
             'pkg-config', 'subversion', 'tar', 'tcl', 'unzip', 'zlib1g'],
        yum=['autoconf', 'bzip2', 'ca-certificates', 'coreutils', 'cpio',
             'curl', 'environment-modules', 'git', 'gzip', 'make',
             'openssh-clients', 'openssl-devel', 'patch', 'pkg-config',
             'svn', 'tar', 'tcl', 'unzip', 'zlib-devel'])

    # Extra OS dependencies
    if args.extra_package:
        recipe += hpccm.building_blocks.packages(
            ospackages=args.extra_package)

    # Python
    recipe += hpccm.building_blocks.python()

    # GNU compilers
    recipe += hpccm.building_blocks.gnu()

    # Spack itself
    spack_bb = bb_base()
    spack_bb += comment('Spack')
    spack_bb += shell(commands=[
        'mkdir -p /opt && cd /opt',
        'git clone --depth=1 --branch %s https://github.com/spack/spack' % args.spack_branch,
        '/opt/spack/bin/spack bootstrap',
        'ln -s /opt/spack/share/spack/setup-env.sh /etc/profile.d/spack.sh',
        'ln -s /opt/spack/share/spack/spack-completion.bash /etc/profile.d'])
    spack_bb += environment(variables={'PATH': '/opt/spack/bin:$PATH',
                                       'FORCE_UNSAFE_CONFIGURE': '1'})
    recipe += spack_bb

    # spack install command line arguments
    install_args = ['-y']
    if args.no_checksum:
        install_args.append('--no-checksum')
    if args.show_log_on_error:
        install_args.append('--show-log-on-error')
    install_args_str = ' '.join(install_args)

    # Process each spec
    for spec in spack.cmd.parse_specs(args.specs):
        spec.concretize()

        bb = bb_base()
        bb += comment('%s %s' % (spec.name, spec.version))

        # Process each dependency.  Use a selectable depth to balance
        # the build cache vs. container spec file complexity
        for depth, dspec in spec.traverse_edges(order='post', depth=True):
            if depth <= args.depth:
                node = dspec.spec
                # Compilers and arch are omitted from the format
                # string because they reflect the host, not the
                # container.
                cmd = 'spack install %s %s' % (
                    install_args_str,
                    node.format(format_string='$_$@$+'))
                bb += shell(chdir=False, commands=[cmd, 'spack clean --all'])

        recipe += bb

    hpccm.config.set_container_format(args.format)
    print(recipe)

    # Really basic implementation of a multi-stage container
    # specification.  Assume the same base image should be used and
    # just copy /opt/spack.  If more advanced runtime capabilities
    # become available, this should become more selective in what
    # files are copied for a much bigger reduction in container size
    # (e.g., build vs. link dependencies).  Multi-stage containers are
    # Docker specific.
    if args.multi_stage and args.format == 'docker':
        runtime = hpccm.Stage()
        runtime += baseimage(image=args.baseimage, _distro=args.distro)
        runtime += recipe.runtime()

        spack_rt = bb_base()
        spack_rt += comment('Spack')
        spack_rt += copy(_from='0', src='/opt/spack', dest='/opt/spack')
        spack_rt += shell(commands=[
            'ln -s /opt/spack/share/spack/setup-env.sh'
            ' /etc/profile.d/spack.sh',
            'ln -s /opt/spack/share/spack/spack-completion.bash'
            ' /etc/profile.d'])
        spack_rt += environment(variables={'PATH': '/opt/spack/bin:$PATH'})
        runtime += spack_rt

        # Prepend newline to clearly separate stages
        print('\n' + str(runtime))
