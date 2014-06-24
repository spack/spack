##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import shutil
import argparse
from datetime import datetime
from contextlib import closing

import llnl.util.tty as tty
from llnl.util.tty.colify import colify
from llnl.util.filesystem import mkdirp, join_path

import spack
import spack.cmd
import spack.config
from spack.spec import Spec
from spack.error import SpackError
from spack.stage import Stage
from spack.util.compression import extension


description = "Manage spack mirrors."

def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='mirror_command')

    create_parser = sp.add_parser('create', help=mirror_create.__doc__)
    create_parser.add_argument('-d', '--directory', default=None,
                               help="Directory in which to create mirror.")
    create_parser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="Specs of packages to put in mirror")
    create_parser.add_argument(
        '-f', '--file', help="File with specs of packages to put in mirror.")

    add_parser = sp.add_parser('add', help=mirror_add.__doc__)
    add_parser.add_argument('name', help="Mnemonic name for mirror.")
    add_parser.add_argument(
        'url', help="URL of mirror directory created by 'spack mirror create'.")

    remove_parser = sp.add_parser('remove', help=mirror_remove.__doc__)
    remove_parser.add_argument('name')

    list_parser = sp.add_parser('list', help=mirror_list.__doc__)


def mirror_add(args):
    """Add a mirror to Spack."""
    config = spack.config.get_config('user')
    config.set_value('mirror', args.name, 'url', args.url)
    config.write()


def mirror_remove(args):
    """Remove a mirror by name."""
    config = spack.config.get_config('user')
    name = args.name

    if not config.has_named_section('mirror', name):
        tty.die("No such mirror: %s" % name)
    config.remove_named_section('mirror', name)
    config.write()


def mirror_list(args):
    """Print out available mirrors to the console."""
    config = spack.config.get_config()
    sec_names = config.get_section_names('mirror')

    if not sec_names:
        tty.msg("No mirrors configured.")
        return

    max_len = max(len(s) for s in sec_names)
    fmt = "%%-%ds%%s" % (max_len + 4)

    for name in sec_names:
        val = config.get_value('mirror', name, 'url')
        print fmt % (name, val)


def mirror_create(args):
    """Create a directory to be used as a spack mirror, and fill it with
       package archives."""
    # try to parse specs from the command line first.
    args.specs = spack.cmd.parse_specs(args.specs)

    # If there is a file, parse each line as a spec and add it to the list.
    if args.file:
        with closing(open(args.file, "r")) as stream:
            for i, string in enumerate(stream):
                try:
                    s = Spec(string)
                    s.package
                    args.specs.append(s)
                except SpackError, e:
                    tty.die("Parse error in %s, line %d:" % (args.file, i+1),
                            ">>> " + string, str(e))

    if not args.specs:
        args.specs = spack.db.all_package_names()

    # Default name for directory is spack-mirror-<DATESTAMP>
    if not args.directory:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        args.directory = 'spack-mirror-' + timestamp

    # Make sure nothing is in the way.
    if os.path.isfile(args.directory):
        tty.error("%s already exists and is a file." % args.directory)

    # Create a directory if none exists
    if not os.path.isdir(args.directory):
        mkdirp(args.directory)
        tty.msg("Created new mirror in %s" % args.directory)
    else:
        tty.msg("Adding to existing mirror in %s" % args.directory)

    # Things to keep track of while parsing specs.
    working_dir = os.getcwd()
    num_mirrored = 0
    num_error = 0

    # Iterate through packages and download all the safe tarballs for each of them
    for spec in args.specs:
        pkg = spec.package

        # Skip any package that has no checksummed versions.
        if not pkg.versions:
            tty.msg("No safe (checksummed) versions for package %s."
                    % pkg.name)
            continue

        # create a subdir for the current package.
        pkg_path = join_path(args.directory, pkg.name)
        mkdirp(pkg_path)

        # Download all the tarballs using Stages, then move them into place
        for version in pkg.versions:
            # Skip versions that don't match the spec
            vspec = Spec('%s@%s' % (pkg.name, version))
            if not vspec.satisfies(spec):
                continue

            mirror_path = "%s/%s-%s.%s" % (
                pkg.name, pkg.name, version, extension(pkg.url))

            os.chdir(working_dir)
            mirror_file = join_path(args.directory, mirror_path)
            if os.path.exists(mirror_file):
                tty.msg("Already fetched %s. Skipping." % mirror_file)
                num_mirrored += 1
                continue

            # Get the URL for the version and set up a stage to download it.
            url = pkg.url_for_version(version)
            stage = Stage(url)
            try:
                # fetch changes directory into the stage
                stage.fetch()

                # change back and move the new archive into place.
                os.chdir(working_dir)
                shutil.move(stage.archive_file, mirror_file)
                tty.msg("Added %s to mirror" % mirror_file)
                num_mirrored += 1

            except Exception, e:
                 tty.warn("Error while fetching %s.  Skipping." % url, e.message)
                 num_error += 1

            finally:
                stage.destroy()

    # If nothing happened, try to say why.
    if not num_mirrored:
        if num_error:
            tty.warn("No packages added to mirror.",
                     "All packages failed to fetch.")
        else:
            tty.warn("No packages added to mirror. No versions matched specs:")
            colify(args.specs, indent=4)


def mirror(parser, args):
    action = { 'create' : mirror_create,
               'add'    : mirror_add,
               'remove' : mirror_remove,
               'list'   : mirror_list }
    action[args.mirror_command](args)
