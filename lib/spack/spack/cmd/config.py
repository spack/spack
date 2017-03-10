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
import spack.config

description = "get and set configuration options"


def setup_parser(subparser):
    # User can only choose one
    subparser.add_argument('--scope', choices=spack.config.config_scopes,
                           help="configuration scope to read/modify")

    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='config_command')

    get_parser = sp.add_parser('get', help='print configuration values')
    get_parser.add_argument('section',
                            help="configuration section to print. "
                                 "options: %(choices)s",
                            metavar='SECTION',
                            choices=spack.config.section_schemas)

    edit_parser = sp.add_parser('edit', help='edit configuration file')
    edit_parser.add_argument('section',
                             help="configuration section to edit. "
                                  "options: %(choices)s",
                             metavar='SECTION',
                             choices=spack.config.section_schemas)


def config_get(args):
    spack.config.print_section(args.section)


def config_edit(args):
    if not args.scope:
        if args.section == 'compilers':
            args.scope = spack.cmd.default_modify_scope
        else:
            args.scope = 'user'
    if not args.section:
        args.section = None
    config_file = spack.config.get_config_filename(args.scope, args.section)
    spack.editor(config_file)


def config(parser, args):
    action = {'get': config_get,
              'edit': config_edit}
    action[args.config_command](args)
