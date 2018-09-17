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
"""Implementation details of the ``spack module`` command."""

import collections
import os.path
import shutil

from llnl.util import filesystem, tty

import spack.cmd
import spack.modules
import spack.repo

import spack.cmd.common.arguments as arguments

description = "manipulate module files"
section = "environment"
level = "short"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='subparser_name')

    refresh_parser = sp.add_parser('refresh', help='regenerate module files')
    refresh_parser.add_argument(
        '--delete-tree',
        help='delete the module file tree before refresh',
        action='store_true'
    )
    arguments.add_common_arguments(
        refresh_parser, ['constraint', 'yes_to_all']
    )

    find_parser = sp.add_parser('find', help='find module files for packages')
    find_parser.add_argument(
        '--full-path',
        help='display full path to module file',
        action='store_true'
    )
    arguments.add_common_arguments(
        find_parser, ['constraint', 'recurse_dependencies']
    )

    rm_parser = sp.add_parser('rm', help='remove module files')
    arguments.add_common_arguments(
        rm_parser, ['constraint', 'yes_to_all']
    )

    loads_parser = sp.add_parser(
        'loads',
        help='prompt the list of modules associated with a constraint'
    )
    loads_parser.add_argument(
        '--input-only', action='store_false', dest='shell',
        help='generate input for module command (instead of a shell script)'
    )
    loads_parser.add_argument(
        '-p', '--prefix', dest='prefix', default='',
        help='prepend to module names when issuing module load commands'
    )
    loads_parser.add_argument(
        '-x', '--exclude', dest='exclude', action='append', default=[],
        help="exclude package from output; may be specified multiple times"
    )
    arguments.add_common_arguments(
        loads_parser, ['constraint', 'recurse_dependencies']
    )
    return sp


class MultipleSpecsMatch(Exception):
    """Raised when multiple specs match a constraint, in a context where
    this is not allowed.
    """


class NoSpecMatches(Exception):
    """Raised when no spec matches a constraint, in a context where
    this is not allowed.
    """


def one_spec_or_raise(specs):
    """Ensures exactly one spec has been selected, or raises the appropriate
    exception.
    """
    # Ensure a single spec matches the constraint
    if len(specs) == 0:
        raise NoSpecMatches()
    if len(specs) > 1:
        raise MultipleSpecsMatch()

    # Get the spec and module type
    return specs[0]


def loads(module_type, specs, args):
    """Prompt the list of modules associated with a list of specs"""

    # Get a comprehensive list of specs
    if args.recurse_dependencies:
        specs_from_user_constraint = specs[:]
        specs = []
        # FIXME : during module file creation nodes seem to be visited
        # FIXME : multiple times even if cover='nodes' is given. This
        # FIXME : work around permits to get a unique list of spec anyhow.
        # FIXME : (same problem as in spack/modules.py)
        seen = set()
        seen_add = seen.add
        for spec in specs_from_user_constraint:
            specs.extend(
                [item for item in spec.traverse(order='post', cover='nodes')
                 if not (item in seen or seen_add(item))]
            )

    module_cls = spack.modules.module_types[module_type]
    modules = [
        (spec, module_cls(spec).layout.use_name)
        for spec in specs if os.path.exists(module_cls(spec).layout.filename)
    ]

    module_commands = {
        'tcl': 'module load ',
        'lmod': 'module load ',
        'dotkit': 'use '
    }

    d = {
        'command': '' if not args.shell else module_commands[module_type],
        'prefix': args.prefix
    }

    exclude_set = set(args.exclude)
    prompt_template = '{comment}{exclude}{command}{prefix}{name}'
    for spec, mod in modules:
        d['exclude'] = '## ' if spec.name in exclude_set else ''
        d['comment'] = '' if not args.shell else '# {0}\n'.format(
            spec.format())
        d['name'] = mod
        print(prompt_template.format(**d))


def find(module_type, specs, args):
    """Returns the module file "use" name if there's a single match. Raises
    error messages otherwise.
    """

    spec = one_spec_or_raise(specs)

    # Check if the module file is present
    def module_exists(spec):
        writer = spack.modules.module_types[module_type](spec)
        return os.path.isfile(writer.layout.filename)

    if not module_exists(spec):
        msg = 'Even though {1} is installed, '
        msg += 'no {0} module has been generated for it.'
        tty.die(msg.format(module_type, spec))

    # Check if we want to recurse and load all dependencies. In that case
    # modify the list of specs adding all the dependencies in post order
    if args.recurse_dependencies:
        specs = [
            item for item in spec.traverse(order='post', cover='nodes')
            if module_exists(item)
        ]

    # ... and if it is print its use name or full-path if requested
    def module_str(specs):
        modules = []
        for x in specs:
            writer = spack.modules.module_types[module_type](x)
            if args.full_path:
                modules.append(writer.layout.filename)
            else:
                modules.append(writer.layout.use_name)

        return ' '.join(modules)

    print(module_str(specs))


def rm(module_type, specs, args):
    """Deletes the module files associated with every spec in specs, for every
    module type in module types.
    """

    module_cls = spack.modules.module_types[module_type]
    module_exist = lambda x: os.path.exists(module_cls(x).layout.filename)

    specs_with_modules = [spec for spec in specs if module_exist(spec)]

    modules = [module_cls(spec) for spec in specs_with_modules]

    if not modules:
        tty.die('No module file matches your query')

    # Ask for confirmation
    if not args.yes_to_all:
        msg = 'You are about to remove {0} module files for:\n'
        tty.msg(msg.format(module_type))
        spack.cmd.display_specs(specs_with_modules, long=True)
        print('')
        answer = tty.get_yes_or_no('Do you want to proceed?')
        if not answer:
            tty.die('Will not remove any module files')

    # Remove the module files
    for s in modules:
        s.remove()


def refresh(module_type, specs, args):
    """Regenerates the module files for every spec in specs and every module
    type in module types.
    """

    # Prompt a message to the user about what is going to change
    if not specs:
        tty.msg('No package matches your query')
        return

    if not args.yes_to_all:
        msg = 'You are about to regenerate {types} module files for:\n'
        tty.msg(msg.format(types=module_type))
        spack.cmd.display_specs(specs, long=True)
        print('')
        answer = tty.get_yes_or_no('Do you want to proceed?')
        if not answer:
            tty.die('Module file regeneration aborted.')

    # Cycle over the module types and regenerate module files

    cls = spack.modules.module_types[module_type]

    # Skip unknown packages.
    writers = [
        cls(spec) for spec in specs
        if spack.repo.path.exists(spec.name)]

    # Filter blacklisted packages early
    writers = [x for x in writers if not x.conf.blacklisted]

    # Detect name clashes in module files
    file2writer = collections.defaultdict(list)
    for item in writers:
        file2writer[item.layout.filename].append(item)

    if len(file2writer) != len(writers):
        message = 'Name clashes detected in module files:\n'
        for filename, writer_list in file2writer.items():
            if len(writer_list) > 1:
                message += '\nfile: {0}\n'.format(filename)
                for x in writer_list:
                    message += 'spec: {0}\n'.format(x.spec.format())
        tty.error(message)
        tty.error('Operation aborted')
        raise SystemExit(1)

    if len(writers) == 0:
        msg = 'Nothing to be done for {0} module files.'
        tty.msg(msg.format(module_type))
        return

    # If we arrived here we have at least one writer
    module_type_root = writers[0].layout.dirname()
    # Proceed regenerating module files
    tty.msg('Regenerating {name} module files'.format(name=module_type))
    if os.path.isdir(module_type_root) and args.delete_tree:
        shutil.rmtree(module_type_root, ignore_errors=False)
    filesystem.mkdirp(module_type_root)
    for x in writers:
        try:
            x.write(overwrite=True)
        except Exception as e:
            msg = 'Could not write module file [{0}]'
            tty.warn(msg.format(x.layout.filename))
            tty.warn('\t--> {0} <--'.format(str(e)))


#: Dictionary populated with the list of sub-commands.
#: Each sub-command must be callable and accept 3 arguments:
#:
#:   - module_type: the type of module it refers to
#:   - specs : the list of specs to be processed
#:   - args : namespace containing the parsed command line arguments
callbacks = {
    'refresh': refresh,
    'rm': rm,
    'find': find,
    'loads': loads
}


def modules_cmd(parser, args, module_type, callbacks=callbacks):

    # Qualifiers to be used when querying the db for specs
    constraint_qualifiers = {
        'refresh': {
            'installed': True,
            'known': True
        },
    }
    query_args = constraint_qualifiers.get(args.subparser_name, {})

    # Get the specs that match the query from the DB
    specs = args.specs(**query_args)

    try:

        callbacks[args.subparser_name](module_type, specs, args)

    except MultipleSpecsMatch:
        msg = "the constraint '{query}' matches multiple packages:\n"
        for s in specs:
            msg += '\t' + s.cformat(format_string='$/ $_$@$+$%@+$+$=') + '\n'
        tty.error(msg.format(query=args.constraint))
        tty.die('In this context exactly **one** match is needed: please specify your constraints better.')  # NOQA: ignore=E501

    except NoSpecMatches:
        msg = "the constraint '{query}' matches no package."
        tty.error(msg.format(query=args.constraint))
        tty.die('In this context exactly **one** match is needed: please specify your constraints better.')  # NOQA: ignore=E501
