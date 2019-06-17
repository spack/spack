# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import spack.architecture as architecture

description = "print architecture information about this machine"
section = "system"
level = "short"


def setup_parser(subparser):
    parts = subparser.add_mutually_exclusive_group()
    parts.add_argument(
        '-p', '--platform', action='store_true', default=False,
        help='print only the platform')
    parts.add_argument(
        '-o', '--operating-system', action='store_true', default=False,
        help='print only the operating system')
    parts.add_argument(
        '-t', '--target', action='store_true', default=False,
        help='print only the target')
    parts.add_argument(
        '-f', '--frontend', action='store_true', default=False,
        help='print frontend')
    parts.add_argument(
        '-b', '--backend', action='store_true', default=False,
        help='print backend')


def arch(parser, args):
    arch = architecture.Arch(
        architecture.platform(), 'default_os', 'default_target')

    if args.platform:
        print(arch.platform)
    elif args.operating_system:
        print(arch.os)
    elif args.target:
        print(arch.target)
    elif args.frontend:
        print(str(arch.platform) + "-" + arch.platform.front_os + "-"
              + arch.platform.front_end)
    elif args.backend:
        print(str(arch.platform) + "-" + arch.platform.back_os + "-"
              + arch.platform.back_end)
    else:
        print(arch)
