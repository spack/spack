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
import string
import os
import re

from ordereddict_backport import OrderedDict
import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack
import spack.cmd
import spack.cmd.checksum
import spack.url
import spack.util.web
from spack.spec import Spec
from spack.util.naming import *
from spack.repository import Repo, RepoError

from spack.util.executable import which


description = "Create a new package file from an archive URL"

package_template = string.Template("""\
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install ${name}
#
# You can edit this file again by typing:
#
#     spack edit ${name}
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class ${class_name}(Package):
    ""\"FIXME: Put a proper description of your package here.""\"

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "${url}"

${versions}
${extends}
    # FIXME: Add dependencies if this package requires them.
    # depends_on("foo")

    def install(self, spec, prefix):
${install}
""")


def make_version_calls(ver_hash_tuples):
    """Adds a version() call to the package for each version found."""
    max_len = max(len(str(v)) for v, h in ver_hash_tuples)
    format = "    version(%%-%ds, '%%s')" % (max_len + 2)
    return '\n'.join(format % ("'%s'" % v, h) for v, h in ver_hash_tuples)


def setup_parser(subparser):
    subparser.add_argument('url', nargs='?', help="url of package archive")
    subparser.add_argument(
        '--keep-stage', action='store_true',
        help="Don't clean up staging area when command completes.")
    subparser.add_argument(
        '-n', '--name', dest='alternate_name', default=None, metavar='NAME',
        help="Override the autodetected name for the created package.")
    subparser.add_argument(
        '-r', '--repo', default=None,
        help="Path to a repository where the package should be created.")
    subparser.add_argument(
        '-N', '--namespace',
        help="Specify a namespace for the package. Must be the namespace of "
        "a repository registered with Spack.")
    subparser.add_argument(
        '-f', '--force', action='store_true', dest='force',
        help="Overwrite any existing package file with the same name.")

    setup_parser.subparser = subparser


class ConfigureGuesser(object):
    def __call__(self, stage):
        """Try to guess the type of build system used by the project.
        Set the appropriate default installation instructions and any
        necessary extensions for Python and R."""

        # Default installation instructions
        installDict = {
            'autotools': """\
        # FIXME: Modify the configure line to suit your build system here.
        configure('--prefix={0}'.format(prefix))

        # FIXME: Add logic to build and install here.
        make()
        make('install')""",

            'cmake':     """\
        with working_dir('spack-build', create=True):
            # FIXME: Modify the cmake line to suit your build system here.
            cmake('..', *std_cmake_args)

            # FIXME: Add logic to build and install here.
            make()
            make('install')""",

            'scons':     """\
        # FIXME: Add logic to build and install here.
        scons('prefix={0}'.format(prefix))
        scons('install')""",

            'python':    """\
        # FIXME: Add logic to build and install here.
        python('setup.py', 'install', '--prefix={0}'.format(prefix))""",

            'R':         """\
        # FIXME: Add logic to build and install here.
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),""" +
            " self.stage.source_path)""",

            'unknown':   """\
        # FIXME: Unknown build system
        make()
        make('install')"""
        }

        # A list of clues that give us an idea of the build system a package
        # uses. If the regular expression matches a file contained in the
        # archive, the corresponding build system is assumed.
        clues = [
            (r'/configure$',      'autotools'),
            (r'/CMakeLists.txt$', 'cmake'),
            (r'/SConstruct$',     'scons'),
            (r'/setup.py$',       'python'),
            (r'/NAMESPACE$',      'R')
        ]

        # Peek inside the compressed file.
        if stage.archive_file.endswith('.zip'):
            try:
                unzip  = which('unzip')
                output = unzip('-l', stage.archive_file, output=str)
            except:
                output = ''
        else:
            try:
                tar    = which('tar')
                output = tar('--exclude=*/*/*', '-tf',
                             stage.archive_file, output=str)
            except:
                output = ''
        lines = output.split('\n')

        # Determine the build system based on the files contained
        # in the archive.
        build_system = 'unknown'
        for pattern, bs in clues:
            if any(re.search(pattern, l) for l in lines):
                build_system = bs

        self.build_system = build_system

        # Set any necessary extensions for Python and R
        extensions = ''
        if build_system in ['python', 'R']:
            extensions = "\n    extends('{0}')\n".format(build_system)

        self.extends = extensions

        # Set the appropriate default installation instructions
        self.install = installDict[build_system]


def guess_name_and_version(url, args):
    # Try to deduce name and version of the new package from the URL
    version = spack.url.parse_version(url)
    if not version:
        tty.die("Couldn't guess a version string from %s" % url)

    # Try to guess a name.  If it doesn't work, allow the user to override.
    if args.alternate_name:
        name = args.alternate_name
    else:
        try:
            name = spack.url.parse_name(url, version)
        except spack.url.UndetectableNameError:
            # Use a user-supplied name if one is present
            tty.die("Couldn't guess a name for this package. Try running:", "",
                    "spack create --name <name> <url>")

    if not valid_fully_qualified_module_name(name):
        tty.die("Package name can only contain A-Z, a-z, 0-9, '_' and '-'")

    return name, version


def find_repository(spec, args):
    # figure out namespace for spec
    if spec.namespace and args.namespace and spec.namespace != args.namespace:
        tty.die("Namespaces '%s' and '%s' do not match." % (spec.namespace,
                                                            args.namespace))

    if not spec.namespace and args.namespace:
        spec.namespace = args.namespace

    # Figure out where the new package should live.
    repo_path = args.repo
    if repo_path is not None:
        try:
            repo = Repo(repo_path)
            if spec.namespace and spec.namespace != repo.namespace:
                tty.die("Can't create package with namespace %s in repo with "
                        "namespace %s" % (spec.namespace, repo.namespace))
        except RepoError as e:
            tty.die(str(e))
    else:
        if spec.namespace:
            repo = spack.repo.get_repo(spec.namespace, None)
            if not repo:
                tty.die("Unknown namespace: %s" % spec.namespace)
        else:
            repo = spack.repo.first_repo()

    # Set the namespace on the spec if it's not there already
    if not spec.namespace:
        spec.namespace = repo.namespace

    return repo


def fetch_tarballs(url, name, version):
    """Try to find versions of the supplied archive by scraping the web.
    Prompts the user to select how many to download if many are found."""
    versions = spack.util.web.find_versions_of_archive(url)
    rkeys = sorted(versions.keys(), reverse=True)
    versions = OrderedDict(zip(rkeys, (versions[v] for v in rkeys)))

    archives_to_fetch = 1
    if not versions:
        # If the fetch failed for some reason, revert to what the user provided
        versions = {version: url}
    elif len(versions) > 1:
        tty.msg("Found %s versions of %s:" % (len(versions), name),
                *spack.cmd.elide_list(
                    ["%-10s%s" % (v, u) for v, u in versions.iteritems()]))
        print
        archives_to_fetch = tty.get_number(
            "Include how many checksums in the package file?",
            default=5, abort='q')

        if not archives_to_fetch:
            tty.die("Aborted.")

    sorted_versions = sorted(versions.keys(), reverse=True)
    sorted_urls = [versions[v] for v in sorted_versions]
    return sorted_versions[:archives_to_fetch], sorted_urls[:archives_to_fetch]


def create(parser, args):
    url = args.url
    if not url:
        setup_parser.subparser.print_help()
        return

    # Figure out a name and repo for the package.
    name, version = guess_name_and_version(url, args)
    spec = Spec(name)
    name = spec.name  # factors out namespace, if any
    repo = find_repository(spec, args)

    tty.msg("This looks like a URL for %s version %s" % (name, version))
    tty.msg("Creating template for package %s" % name)

    # Fetch tarballs (prompting user if necessary)
    versions, urls = fetch_tarballs(url, name, version)

    # Try to guess what configure system is used.
    guesser = ConfigureGuesser()
    ver_hash_tuples = spack.cmd.checksum.get_checksums(
        versions, urls,
        first_stage_function=guesser,
        keep_stage=args.keep_stage)

    if not ver_hash_tuples:
        tty.die("Could not fetch any tarballs for %s" % name)

    # Prepend 'py-' to python package names, by convention.
    if guesser.build_system == 'python':
        name = 'py-%s' % name

    # Prepend 'r-' to R package names, by convention.
    if guesser.build_system == 'R':
        name = 'r-%s' % name

    # Create a directory for the new package.
    pkg_path = repo.filename_for_package_name(name)
    if os.path.exists(pkg_path) and not args.force:
        tty.die("%s already exists." % pkg_path)
    else:
        mkdirp(os.path.dirname(pkg_path))

    # Write out a template for the file
    with open(pkg_path, "w") as pkg_file:
        pkg_file.write(
            package_template.substitute(
                name=name,
                class_name=mod_to_class(name),
                url=url,
                versions=make_version_calls(ver_hash_tuples),
                extends=guesser.extends,
                install=guesser.install))

    # If everything checks out, go ahead and edit.
    spack.editor(pkg_path)
    tty.msg("Created package %s" % pkg_path)
