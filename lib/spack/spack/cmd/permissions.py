# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.store

import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.package_permissions as spp

description = "manage spack permissions"
section = "build"
level = "long"


def first_line(docstring):
    """Return the first line of the docstring."""
    return docstring.split('\n')[0]


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='COMMAND',
                                  dest='permissions_command')

    # Check
    check_parser = sp.add_parser('check', description=perm_check.__doc__,
                                 help=first_line(perm_check.__doc__))
    arguments.add_common_arguments(check_parser, ['installed_specs'])

    # Repair
    repair_parser = sp.add_parser('repair', description=perm_repair.__doc__,
                                  help=first_line(perm_repair.__doc__))
    arguments.add_common_arguments(repair_parser, ['installed_specs'])


def perm_check(args):
    """Check that permissions match those specified by packages.yaml."""
    # First check permissions for the database directory and its contents
    spp.check_permissions(spack.store.db._db_dir, None, contents=True)

    # Now check permissions for installed packages
    env = ev.get_env(args, 'permissions')
    hashes = env.all_hashes() if env else None
    specs = spack.store.db.query(hashes=hashes)
    for spec in specs:
        spp.check_permissions(spec.prefix, spec, contents=True)


def perm_repair(args):
    """Repair any permissions that do not match packages.yaml specs."""
    # TODO: Add the database and metadata directories

    env = ev.get_env(args, 'permissions')
    hashes = env.all_hashes() if env else None
    specs = spack.store.db.query(hashes=hashes)
    spack.cmd.display_specs(specs, long=True)
    raise NotImplementedError('The command is not yet implemented')


def permissions(parser, args):
    globals()['perm_{0}'.format(args.permissions_command)](args)
