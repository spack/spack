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
import string
import os
import hashlib
import re
from contextlib import closing

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack
import spack.cmd
import spack.cmd.checksum
import spack.package
import spack.url
from spack.util.naming import mod_to_class
import spack.util.crypto as crypto

from spack.util.executable import which
from spack.stage import Stage


description = "Create a new package file from an archive URL"

package_template = string.Template("""\
# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install ${name}
#
# You can always get back here to change things with:
#
#     spack edit ${name}
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class ${class_name}(Package):
    ""\"FIXME: put a proper description of your package here.""\"
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "${url}"

    versions = ${versions}

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        ${configure}

        # FIXME: Add logic to build and install here
        make()
        make("install")
""")


def setup_parser(subparser):
    subparser.add_argument('url', nargs='?', help="url of package archive")
    subparser.add_argument(
        '--keep-stage', action='store_true', dest='keep_stage',
        help="Don't clean up staging area when command completes.")
    subparser.add_argument(
        '-f', '--force', action='store_true', dest='force',
        help="Overwrite any existing package file with the same name.")


class ConfigureGuesser(object):
    def __call__(self, stage):
        """Try to guess the type of build system used by the project, and return
           an appropriate configure line.
        """
        tar = which('tar')
        output = tar(
            "--exclude=*/*/*", "-tf", stage.archive_file, return_output=True)

        autotools = 'configure("--prefix=%s" % prefix)'
        cmake     = 'cmake(".", *std_cmake_args)'
        lines = output.split('\n')

        if any(re.search(r'/configure$', l) for l in lines):
            self.configure = autotools
        elif  any(re.search(r'/CMakeLists.txt$', l) for l in lines):
            self.configure = cmake
        else:
            # Both, with cmake commented out
            self.configure = '%s\n        # %s' % (autotools, cmake)


def make_version_dict(ver_hash_tuples):
    max_len = max(len(str(v)) for v,hfg in ver_hash_tuples)
    width = max_len + 2
    format = "%-" + str(width) + "s : '%s',"
    sep = '\n                 '
    return '{ ' + sep.join(format % ("'%s'" % v, h)
                           for v, h in ver_hash_tuples) + ' }'


def get_name():
    """Prompt user to input a package name."""
    name = ""
    while not name:
        new_name = raw_input("Name: ")
        if spack.db.valid_name(name):
            name = new_name
        else:
            print "Package name can only contain A-Z, a-z, 0-9, '_' and '-'"
    return name


def create(parser, args):
    url = args.url

    # Try to deduce name and version of the new package from the URL
    name, version = spack.url.parse_name_and_version(url)
    if not name:
        tty.msg("Couldn't guess a name for this package.")
        name = get_name()

    if not version:
        tty.die("Couldn't guess a version string from %s." % url)

    tty.msg("This looks like a URL for %s version %s." % (name, version))
    tty.msg("Creating template for package %s" % name)

    # Create a directory for the new package.
    pkg_path = spack.db.filename_for_package_name(name)
    if os.path.exists(pkg_path) and not args.force:
        tty.die("%s already exists." % pkg_path)
    else:
        mkdirp(os.path.dirname(pkg_path))

    versions = list(reversed(spack.package.find_versions_of_archive(url)))

    archives_to_fetch = 1
    if not versions:
        # If the fetch failed for some reason, revert to what the user provided
        versions = [version]
        urls = [url]
    else:
        urls = [spack.url.substitute_version(url, v) for v in versions]
        if len(urls) > 1:
            tty.msg("Found %s versions of %s:" % (len(urls), name),
                    *spack.cmd.elide_list(
                    ["%-10s%s" % (v,u) for v, u in zip(versions, urls)]))
            print
            archives_to_fetch = tty.get_number(
                "Include how many checksums in the package file?",
                default=5, abort='q')

            if not archives_to_fetch:
                tty.msg("Aborted.")
                return

    guesser = ConfigureGuesser()
    ver_hash_tuples = spack.cmd.checksum.get_checksums(
        versions[:archives_to_fetch], urls[:archives_to_fetch],
        first_stage_function=guesser, keep_stage=args.keep_stage)

    if not ver_hash_tuples:
        tty.die("Could not fetch any tarballs for %s." % name)

    # Write out a template for the file
    with closing(open(pkg_path, "w")) as pkg_file:
        pkg_file.write(
            package_template.substitute(
                name=name,
                configure=guesser.configure,
                class_name=mod_to_class(name),
                url=url,
                versions=make_version_dict(ver_hash_tuples)))

    # If everything checks out, go ahead and edit.
    spack.editor(pkg_path)
    tty.msg("Created package %s." % pkg_path)
