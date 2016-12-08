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
import sys

from llnl.util.lang import index_by
import llnl.util.tty as tty
from llnl.util.tty.colify import colify
import spack
import spack.cmd
import spack.compilers
import spack.config
import spack.external_package as ext_package
import spack.error
import spack.spec


description = "Add an external package entry to packages.yaml"


def setup_parser(subparser):
    """Sets up parser for external add and external rm.

    Sets up command line parser for the spack external command. Usage is as
    follows

        spack external add [package_spec] [path_or_module]
        spack external rm [package_spec]
        spack external list
    """
    scopes = spack.config.config_scopes
    # Set up subcommands external and rm and list
    sp = subparser.add_subparsers(metavar="SUBCOMMAND",
                                  dest="external_command")
    ################
    # external add
    ################
    add_parser = sp.add_parser('add',
                               help="Add packages to Spack's config file")
    add_parser.add_argument("package_spec",
                            help="spec for external package")
    add_parser.add_argument("external_location",
                            help="path or module (location) of external pkg")
    add_parser.add_argument("--scope", choices=scopes,
                            default=spack.cmd.default_modify_scope,
                            help="Configuration scope to modify.")

    ###############
    # external rm
    ###############
    rm_parser = sp.add_parser('remove', aliases=['rm'],
                              help="Delete an entry from packages.yaml")
    rm_parser.add_argument('-a', '--all', action='store_true',
                           help='Remove ALL compilers that match spec.')
    rm_parser.add_argument("package_spec",
                           help="spec of a package to delete")
    rm_parser.add_argument("--scope", choices=scopes,
                           default=spack.cmd.default_modify_scope,
                           help="Configuration scope to modify.")

    ###############
    # external list
    ###############
    ls_parser = sp.add_parser('list', help="List all available packages")
    ls_parser.add_argument("--scope", choices=scopes,
                           default=spack.cmd.default_list_scope,
                           help="Configuration scope to read from")


def external_add(args):
    """Add an external package to packages.yaml config."""
    package_spec = spack.spec.Spec(args.package_spec)
    external_location = args.external_location
    scope = args.scope
    external_package = ext_package.ExternalPackage.create_external_package(
        package_spec, external_location)
    ext_package.add_external_package(external_package, scope)
    filename = spack.config.get_config_filename(scope, "packages")
    tty.msg("Added {0} to {1}".format(package_spec, filename))


def external_rm(args):
    """Removes an external package from packages.yaml"""
    package_spec = spack.spec.Spec(args.package_spec)
    packages_config = ext_package.PackagesConfig(args.scope)
    package = packages_config.get_package(package_spec.name)
    if package.is_empty():
        tty.die("Could not find package for {0}".format(package_spec))

    matches = []
    specs = package.specs_section()
    for spec in specs.keys():  # follows {spec: path_or_mod}
        if spack.spec.Spec(spec).satisfies(package_spec):
            matches.append(spec)

    if not args.all and len(matches) > 1:
        tty.error(
            "Multiple packages match spec {0}. Choose one:".format(
                package_spec))
        colify(sorted(matches), indent=4)
        tty.msg("Or, use 'spack external rm -a' to remove all fo them.")
        sys.exit(1)

    for spec in matches:
        package.remove_spec(spec)
        tty.msg("Removed package: {0}".format(spec))

    if not package.contains_specs():
        packages_config.remove_entire_entry_from_config(package_spec.name)
    else:
        packages_config.update_package_config(package.config_entry())


def external_list(args):
    tty.msg("Available external packages")
    scope = args.scope
    packages_yaml = ext_package.PackagesConfig(scope)
    all_packages = packages_yaml.all_external_packages()
    index = index_by(all_packages, lambda p: p.package_name)
    for i, (name, package) in enumerate(index.iteritems()):
        if i >= 1:
            print
        tty.hline(name, char="-")
        display_package_specs(package)


def display_package_specs(package_object):
    """Helper function for displaying specs from PackageConfigEntry objects"""
    package = package_object[0]
    specs_to_display = package.specs_section()
    specs = specs_to_display.keys()
    colorized_specs = [spack.spec.colorize_spec(s) for s in specs]
    ext_location = specs_to_display.values()
    max_width = max([len(s) for s in colorized_specs])
    max_width += 3
    output = "{spec: <{width}}{external}"
    for spec, external in zip(colorized_specs, ext_location):
        print output.format(spec=spec, width=max_width, external=external)


def external(parser, args):
    action = {"add": external_add,
              "rm": external_rm,
              "list": external_list}
    action[args.external_command](args)
