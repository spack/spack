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

import llnl.util.tty as tty
import spack
import spack.cmd
import spack.cmd.checksum
import spack.url
import spack.util.web
from llnl.util.filesystem import mkdirp
from spack.repository import Repo
from spack.spec import Spec
from spack.util.executable import which
from spack.util.naming import *

description = "create a new package file"

package_template = '''\
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
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "{url}"

{versions}

{dependencies}

{body}
'''


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

    def __init__(self, name, url, versions):
        self.name       = name
        self.class_name = mod_to_class(name)
        self.url        = url
        self.versions   = versions

    def write(self, pkg_path):
        """Writes the new package file."""

        # Write out a template for the file
        with open(pkg_path, "w") as pkg_file:
            pkg_file.write(package_template.format(
                name=self.name,
                class_name=self.class_name,
                base_class_name=self.base_class_name,
                url=self.url,
                versions=self.versions,
                dependencies=self.dependencies,
                body=self.body))


class AutotoolsPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for Autotools-based packages
    that *do* come with a ``configure`` script"""

    base_class_name = 'AutotoolsPackage'

    dependencies = """\
    # FIXME: Add dependencies if required.
    # depends_on('foo')"""

    body = """\
    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args"""


class AutoreconfPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for Autotools-based packages
    that *do not* come with a ``configure`` script"""

    base_class_name = 'AutotoolsPackage'

    dependencies = """\
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    # FIXME: Add additional dependencies if required.
    # depends_on('foo')"""

    body = """\
    def autoreconf(self, spec, prefix):
        # FIXME: Modify the autoreconf method as necessary
        autoreconf('--install', '--verbose', '--force')

    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args"""


class CMakePackageTemplate(PackageTemplate):
    """Provides appropriate overrides for CMake-based packages"""

    base_class_name = 'CMakePackage'

    body = """\
    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args"""


class SconsPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for SCons-based packages"""

    dependencies = """\
    # FIXME: Add additional dependencies if required.
    depends_on('scons', type='build')"""

    body = """\
    def install(self, spec, prefix):
        # FIXME: Add logic to build and install here.
        scons('prefix={0}'.format(prefix))
        scons('install')"""


class BazelPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for Bazel-based packages"""

    dependencies = """\
    # FIXME: Add additional dependencies if required.
    depends_on('bazel', type='build')"""

    body = """\
    def install(self, spec, prefix):
        # FIXME: Add logic to build and install here.
        bazel()"""


class PythonPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for python extensions"""
    base_class_name = 'PythonPackage'

    dependencies = """\
    # FIXME: Add dependencies if required.
    # depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))"""

    body = """\
    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete the function
        args = []
        return args"""

    def __init__(self, name, *args):
        # If the user provided `--name py-numpy`, don't rename it py-py-numpy
        if not name.startswith('py-'):
            # Make it more obvious that we are renaming the package
            tty.msg("Changing package name from {0} to py-{0}".format(name))
            name = 'py-{0}'.format(name)

        super(PythonPackageTemplate, self).__init__(name, *args)


class RPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for R extensions"""
    base_class_name = 'RPackage'

    dependencies = """\
    # FIXME: Add dependencies if required.
    # depends_on('r-foo', type=('build', 'run'))"""

    body = """\
    # FIXME: Override install() if necessary."""

    def __init__(self, name, *args):
        # If the user provided `--name r-rcpp`, don't rename it r-r-rcpp
        if not name.startswith('r-'):
            # Make it more obvious that we are renaming the package
            tty.msg("Changing package name from {0} to r-{0}".format(name))
            name = 'r-{0}'.format(name)

        super(RPackageTemplate, self).__init__(name, *args)


class OctavePackageTemplate(PackageTemplate):
    """Provides appropriate overrides for octave packages"""

    dependencies = """\
    extends('octave')

    # FIXME: Add additional dependencies if required.
    # depends_on('octave-foo', type=('build', 'run'))"""

    body = """\
    def install(self, spec, prefix):
        # FIXME: Add logic to build and install here.
        octave('--quiet', '--norc',
               '--built-in-docstrings-file=/dev/null',
               '--texi-macros-file=/dev/null',
               '--eval', 'pkg prefix {0}; pkg install {1}'.format(
                   prefix, self.stage.archive_file))"""

    def __init__(self, name, *args):
        # If the user provided `--name octave-splines`, don't rename it
        # octave-octave-splines
        if not name.startswith('octave-'):
            # Make it more obvious that we are renaming the package
            tty.msg("Changing package name from {0} to octave-{0}".format(name))  # noqa
            name = 'octave-{0}'.format(name)

        super(OctavePackageTemplate, self).__init__(name, *args)


templates = {
    'autotools':  AutotoolsPackageTemplate,
    'autoreconf': AutoreconfPackageTemplate,
    'cmake':      CMakePackageTemplate,
    'scons':      SconsPackageTemplate,
    'bazel':      BazelPackageTemplate,
    'python':     PythonPackageTemplate,
    'r':          RPackageTemplate,
    'octave':     OctavePackageTemplate,
    'generic':    PackageTemplate
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
        help="specify a namespace for the package. must be the namespace of "
        "a repository registered with Spack")
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="overwrite any existing package file with the same name")


class BuildSystemGuesser:
    """An instance of BuildSystemGuesser provides a callable object to be used
    during ``spack create``. By passing this object to ``spack checksum``, we
    can take a peek at the fetched tarball and discern the build system it uses
    """

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
            (r'/configure$',         'autotools'),
            (r'/configure.(in|ac)$', 'autoreconf'),
            (r'/Makefile.am$',       'autoreconf'),
            (r'/CMakeLists.txt$',    'cmake'),
            (r'/SConstruct$',        'scons'),
            (r'/setup.py$',          'python'),
            (r'/NAMESPACE$',         'r'),
            (r'/WORKSPACE$',         'bazel')
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
        build_system = 'generic'
        for pattern, bs in clues:
            if any(re.search(pattern, l) for l in lines):
                build_system = bs
                break

        self.build_system = build_system


def get_name(args):
    """Get the name of the package based on the supplied arguments.

    If a name was provided, always use that. Otherwise, if a URL was
    provided, extract the name from that. Otherwise, use a default.

    :param argparse.Namespace args: The arguments given to ``spack create``

    :returns: The name of the package
    :rtype: str
    """

    # Default package name
    name = 'example'

    if args.name:
        # Use a user-supplied name if one is present
        name = args.name
        tty.msg("Using specified package name: '{0}'".format(name))
    elif args.url:
        # Try to guess the package name based on the URL
        try:
            name = spack.url.parse_name(args.url)
            tty.msg("This looks like a URL for {0}".format(name))
        except spack.url.UndetectableNameError:
            tty.die("Couldn't guess a name for this package.",
                    "  Please report this bug. In the meantime, try running:",
                    "  `spack create --name <name> <url>`")

    if not valid_fully_qualified_module_name(name):
        tty.die("Package name can only contain a-z, 0-9, and '-'")

    return name


def get_url(args):
    """Get the URL to use.

    Use a default URL if none is provided.

    :param argparse.Namespace args: The arguments given to ``spack create``

    :returns: The URL of the package
    :rtype: str
    """

    # Default URL
    url = 'http://www.example.com/example-1.2.3.tar.gz'

    if args.url:
        # Use a user-supplied URL if one is present
        url = args.url

    return url


def get_versions(args, name):
    """Returns a list of versions and hashes for a package.

    Also returns a BuildSystemGuesser object.

    Returns default values if no URL is provided.

    :param argparse.Namespace args: The arguments given to ``spack create``
    :param str name: The name of the package

    :returns: Versions and hashes, and a BuildSystemGuesser object
    :rtype: str and BuildSystemGuesser
    """

    # Default version, hash, and guesser
    versions = """\
    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')"""

    guesser = BuildSystemGuesser()

    if args.url:
        # Find available versions
        url_dict = spack.util.web.find_versions_of_archive(args.url)

        if not url_dict:
            # If no versions were found, revert to what the user provided
            version = spack.url.parse_version(args.url)
            url_dict = {version: args.url}

        versions = spack.cmd.checksum.get_checksums(
            url_dict, name, first_stage_function=guesser,
            keep_stage=args.keep_stage)

    return versions, guesser


def get_build_system(args, guesser):
    """Determine the build system template.

    If a template is specified, always use that. Otherwise, if a URL
    is provided, download the tarball and peek inside to guess what
    build system it uses. Otherwise, use a generic template by default.

    :param argparse.Namespace args: The arguments given to ``spack create``
    :param BuildSystemGuesser guesser: The first_stage_function given to \
        ``spack checksum`` which records the build system it detects

    :returns: The name of the build system template to use
    :rtype: str
    """

    # Default template
    template = 'generic'

    if args.template:
        # Use a user-supplied template if one is present
        template = args.template
        tty.msg("Using specified package template: '{0}'".format(template))
    elif args.url:
        # Use whatever build system the guesser detected
        template = guesser.build_system
        if template == 'generic':
            tty.warn("Unable to detect a build system. "
                     "Using a generic package template.")
        else:
            msg = "This package looks like it uses the {0} build system"
            tty.msg(msg.format(template))

    return template


def get_repository(args, name):
    """Returns a Repo object that will allow us to determine the path where
    the new package file should be created.

    :param argparse.Namespace args: The arguments given to ``spack create``
    :param str name: The name of the package to create

    :returns: A Repo object capable of determining the path to the package file
    :rtype: Repo
    """
    spec = Spec(name)
    # Figure out namespace for spec
    if spec.namespace and args.namespace and spec.namespace != args.namespace:
        tty.die("Namespaces '{0}' and '{1}' do not match.".format(
            spec.namespace, args.namespace))

    if not spec.namespace and args.namespace:
        spec.namespace = args.namespace

    # Figure out where the new package should live
    repo_path = args.repo
    if repo_path is not None:
        repo = Repo(repo_path)
        if spec.namespace and spec.namespace != repo.namespace:
            tty.die("Can't create package with namespace {0} in repo with "
                    "namespace {0}".format(spec.namespace, repo.namespace))
    else:
        if spec.namespace:
            repo = spack.repo.get_repo(spec.namespace, None)
            if not repo:
                tty.die("Unknown namespace: '{0}'".format(spec.namespace))
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
    versions, guesser = get_versions(args, name)
    build_system = get_build_system(args, guesser)

    # Create the package template object
    PackageClass = templates[build_system]
    package = PackageClass(name, url, versions)
    tty.msg("Created template for {0} package".format(package.name))

    # Create a directory for the new package
    repo = get_repository(args, name)
    pkg_path = repo.filename_for_package_name(package.name)
    if os.path.exists(pkg_path) and not args.force:
        tty.die('{0} already exists.'.format(pkg_path),
                '  Try running `spack create --force` to overwrite it.')
    else:
        mkdirp(os.path.dirname(pkg_path))

    # Write the new package file
    package.write(pkg_path)
    tty.msg("Created package file: {0}".format(pkg_path))

    # Open up the new package file in your $EDITOR
    spack.editor(pkg_path)
