##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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


def arch(parser, args):
    arch = architecture.Arch(
        architecture.platform(), 'default_os', 'default_target')

    if args.platform:
        print(arch.platform)
    elif args.operating_system:
        print(arch.platform_os)
    elif args.target:
        print(arch.target)
    else:
        print(arch)
