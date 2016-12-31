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
from __future__ import print_function

import os
import re
import sys

import llnl.util.tty as tty
import spack
import spack.cmd
import spack.cmd.checksum
import spack.url
import spack.util.web
from llnl.util.filesystem import mkdirp
from ordereddict_backport import OrderedDict
from spack.repository import Repo, RepoError
from spack.spec import Spec
from spack.util.executable import which
from spack.util.naming import *

description = "Create a new package file"


class PackageTemplate(object):
    """Provides the default values to be used for the package file template"""
    base_class_name = 'Package'

    dependencies = """\
    # FIXME: Add dependencies if required.
    # depends_on('foo')"""

    body = """\
    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')"""

    def __init__(self, name, url, version_hash_tuples):
        self.name = name
        self.class_name = mod_to_class(name)
        self.url = url
        self.version_hash_tuples = version_hash_tuples

    @property
    def versions(self):
        """Adds a version() call to the package for each version found."""
        max_len = max(len(str(v)) for v, h in self.version_hash_tuples)
        format = "    version(%%-%ds, '%%s')" % (max_len + 2)
        return '\n'.join(
            format % ("'%s'" % v, h) for v, h in self.version_hash_tuples
        )

    def write(self, pkg_path):
        """Writes the new package file."""

        # Write out a template for the file
        with open(pkg_path, "w") as pkg_file:
            pkg_file.write("""\
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
#     spack install {name}
#
# You can edit this file again by typing:
#
#     spack edit {name}
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class {class_name}({base_class_name}):
    ""\"FIXME: Put a proper description of your package here.""\"

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "{url}"

{versions}

{dependencies}

{body}
""".format(name=self.name,
           class_name=self.class_name,
           base_class_name=self.base_class_name,
           url=self.url,
           versions=self.versions,
           dependencies=self.dependencies,
           body=self.body))


class AutotoolsPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for autotools-based packages"""
    base_class_name = 'AutotoolsPackage'

    dependencies = """\
    # FIXME: Add dependencies if required.
    # depends_on('m4', type='build')
    # depends_on('autoconf', type='build')
    # depends_on('automake', type='build')
    # depends_on('libtool', type='build')
    # depends_on('foo')"""

    body = """\
    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete the function
        args = []
        return args"""


class CMakePackageTemplate(PackageTemplate):
    """Provides appropriate overrides for cmake-based packages"""
    base_class_name = 'CMakePackage'

    dependencies = """\
    # FIXME: Add additional dependencies if required.
    depends_on('cmake', type='build')"""

    body = """\
    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete the function
        args = []
        return args"""


class SconsPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for scons-based packages"""
    dependencies = """\
    # FIXME: Add additional dependencies if required.
    depends_on('scons', type='build')"""

    body = """\
    def install(self, spec, prefix):
        # FIXME: Add logic to build and install here.
        scons('prefix={0}'.format(prefix))
        scons('install')"""


class BazelPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for bazel-based packages"""
    dependencies = """\
    # FIXME: Add additional dependencies if required.
    depends_on('bazel', type='build')"""

    body = """\
    def install(self, spec, prefix):
        # FIXME: Add logic to build and install here.
        bazel()"""


class PythonPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for python extensions"""
    dependencies = """\
    extends('python')

    # FIXME: Add additional dependencies if required.
    # depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=nolink)"""

    body = """\
    def install(self, spec, prefix):
        # FIXME: Add logic to build and install here.
        setup_py('install', '--prefix={0}'.format(prefix))"""

    def __init__(self, name, *args):
        name = 'py-{0}'.format(name)
        super(PythonPackageTemplate, self).__init__(name, *args)


class RPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for R extensions"""
    dependencies = """\
    extends('r')

    # FIXME: Add additional dependencies if required.
    # depends_on('r-foo', type=nolink)"""

    body = """\
    def install(self, spec, prefix):
        # FIXME: Add logic to build and install here.
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)"""

    def __init__(self, name, *args):
        name = 'r-{0}'.format(name)
        super(RPackageTemplate, self).__init__(name, *args)


class OctavePackageTemplate(PackageTemplate):
    """Provides appropriate overrides for octave packages"""
    dependencies = """\
    extends('octave')

    # FIXME: Add additional dependencies if required.
    # depends_on('octave-foo', type=nolink)"""

    body = """\
    def install(self, spec, prefix):
        # FIXME: Add logic to build and install here.
        octave('--quiet', '--norc',
               '--built-in-docstrings-file=/dev/null',
               '--texi-macros-file=/dev/null',
               '--eval', 'pkg prefix {0}; pkg install {1}'.format(
                   prefix, self.stage.archive_file))"""

    def __init__(self, name, *args):
        name = 'octave-{0}'.format(name)
        super(OctavePackageTemplate, self).__init__(name, *args)


templates = {
    'autotools': AutotoolsPackageTemplate,
    'cmake':     CMakePackageTemplate,
    'scons':     SconsPackageTemplate,
    'bazel':     BazelPackageTemplate,
    'python':    PythonPackageTemplate,
    'r':         RPackageTemplate,
    'octave':    OctavePackageTemplate,
    'default':   PackageTemplate
}


def setup_parser(subparser):
    subparser.add_argument(
        'url', nargs='?',
        help="url of package archive")
    subparser.add_argument(
        '--keep-stage', action='store_true',
        help="don't clean up staging area when command completes")
    subparser.add_argument(
        '-n', '--name',
        help="name of the package to create")
    subparser.add_argument(
        '-t', '--template', metavar='TEMPLATE', choices=templates.keys(),
        help="build system template to use. options: %(choices)s")
    subparser.add_argument(
        '-r', '--repo',
        help="path to a repository where the package should be created")
    subparser.add_argument(
        '-N', '--namespace',
        help="namespace for the package")
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="overwrite any existing package file with the same name")

    setup_parser.subparser = subparser


class BuildSystemGuesser:

    def __call__(self, stage, url):
        """Try to guess the type of build system used by a project based on
        the contents of its archive or the URL it was downloaded from."""

        # Most octave extensions are hosted on Octave-Forge:
        #     http://octave.sourceforge.net/index.html
        # They all have the same base URL.
        if 'downloads.sourceforge.net/octave/' in url:
            self.build_system = 'octave'
            return

        # A list of clues that give us an idea of the build system a package
        # uses. If the regular expression matches a file contained in the
        # archive, the corresponding build system is assumed.
        clues = [
            (r'/configure$',      'autotools'),
            (r'/CMakeLists.txt$', 'cmake'),
            (r'/SConstruct$',     'scons'),
            (r'/setup.py$',       'python'),
            (r'/NAMESPACE$',      'r'),
            (r'/WORKSPACE$',      'bazel')
        ]

        # Peek inside the compressed file.
        if stage.archive_file.endswith('.zip'):
            try:
                unzip  = which('unzip')
                output = unzip('-lq', stage.archive_file, output=str)
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
        build_system = 'default'
        for pattern, bs in clues:
            if any(re.search(pattern, l) for l in lines):
                build_system = bs

        self.build_system = build_system


def fetch_tarballs(url, name):
    """Try to find versions of the supplied archive by scraping the web.
    Prompts the user to select how many to download if many are found."""
    versions = spack.util.web.find_versions_of_archive(url)
    rkeys = sorted(versions.keys(), reverse=True)
    versions = OrderedDict(zip(rkeys, (versions[v] for v in rkeys)))

    archives_to_fetch = 1
    if not versions:
        # If the fetch failed for some reason, revert to what the user provided
        version = spack.url.parse_version(url)
        versions = {version: url}
    elif len(versions) > 1:
        tty.msg("Found %s versions of %s:" % (len(versions), name),
                *spack.cmd.elide_list(
                    ["%-10s%s" % (v, u) for v, u in versions.iteritems()]))
        print('')
        archives_to_fetch = tty.get_number(
            "Include how many checksums in the package file?",
            default=5, abort='q')

        if not archives_to_fetch:
            tty.die("Aborted.")

    sorted_versions = sorted(versions.keys(), reverse=True)
    sorted_urls = [versions[v] for v in sorted_versions]
    return sorted_versions[:archives_to_fetch], sorted_urls[:archives_to_fetch]


def get_name(args):
    """Get the name of the package based on the supplied arguments.

    If a name was provided, always use that. Otherwise, if a URL was
    provided, extract the name from that.

    Returns package name."""

    name = 'example'
    if args.name:
        name = args.name
    elif args.url:
        try:
            name = spack.url.parse_name(args.url)
        except spack.url.UndetectableNameError:
            # Use a user-supplied name if one is present
            tty.die("Couldn't guess a name for this package. Try running:",
                    "  `spack create --name <name> <url>`")

    if not valid_fully_qualified_module_name(name):
        tty.die("Package name can only contain a-z, 0-9, and '-'")

    return name


def get_url(args):
    """Get the URL to use.

    Returns a default URL if none is provided."""

    url = 'http://www.example.com/example-1.2.3.tar.gz'
    if args.url:
        url = args.url

    return url


def get_versions(args, name):
    """Returns a tuple of versions and hashes for a package.

    Also returns a BuildSystemGuesser object.

    Returns default values if no URL is provided."""

    ver_hash_tuples = [('1.2.3', '0123456789abcdef0123456789abcdef')]
    guesser = BuildSystemGuesser()

    if args.url:
        versions, urls = fetch_tarballs(args.url, name)

        ver_hash_tuples = spack.cmd.checksum.get_checksums(
            versions, urls,
            first_stage_function=guesser,
            keep_stage=args.keep_stage)

    if not ver_hash_tuples:
        tty.die('Could not fetch any tarballs for {0}.'.format(name))

    return ver_hash_tuples, guesser


def get_build_system(args, guesser):
    """Determine the build system template.

    If a template is specified, always use that. Otherwise, if a URL
    is provided, download the tarball and peek inside to guess what
    build system it uses."""

    template = 'default'

    if args.template:
        template = args.template
    elif args.url:
        template = guesser.build_system

    return template


def get_repository(name, args):
    spec = Spec(name)
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


def create(parser, args):
    # Gather information about the package to be created
    name = get_name(args)
    url = get_url(args)
    version_hash_tuples, guesser = get_versions(args, name)
    build_system = get_build_system(args, guesser)

    PackageClass = templates[build_system]

    package = PackageClass(name, url, version_hash_tuples)

    repo = get_repository(name, args)

    # Create a directory for the new package.
    pkg_path = repo.filename_for_package_name(package.name)
    if os.path.exists(pkg_path) and not args.force:
        tty.die('{0} already exists.'.format(pkg_path),
                '  Try running `spack create --force` to overwrite it.')
    else:
        mkdirp(os.path.dirname(pkg_path))

    tty.msg("Creating template for package %s" % package.name)

    package.write(pkg_path)

    # If everything checks out, go ahead and edit.
    spack.editor(pkg_path)
    tty.msg("Created package %s" % pkg_path)
