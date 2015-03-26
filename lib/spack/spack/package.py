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
"""
This is where most of the action happens in Spack.
See the Package docs for detailed instructions on how the class works
and on how to write your own packages.

The spack package structure is based strongly on Homebrew
(http://wiki.github.com/mxcl/homebrew/), mainly because
Homebrew makes it very easy to create packages.  For a complete
rundown on spack and how it differs from homebrew, look at the
README.
"""
import os
import re
import time
import inspect
import subprocess
import platform as py_platform
import multiprocessing
from urlparse import urlparse, urljoin
import textwrap
from StringIO import StringIO
from sets import Set

import llnl.util.tty as tty
from llnl.util.link_tree import LinkTree
from llnl.util.filesystem import *
from llnl.util.lang import *

import spack
import spack.spec
import spack.error
import spack.compilers
import spack.mirror
import spack.hooks
import spack.build_environment as build_env
import spack.url as url
import spack.fetch_strategy as fs
from spack.version import *
from spack.stage import Stage
from spack.util.web import get_pages
from spack.util.compression import allowed_archive, extension
from spack.util.executable import ProcessError

from spack.symlinks import *

"""Allowed URL schemes for spack packages."""
_ALLOWED_URL_SCHEMES = ["http", "https", "ftp", "file", "git"]

installed_package_names = Set()


class Package(object):
    """This is the superclass for all spack packages.

    ***The Package class***

    Package is where the bulk of the work of installing packages is done.

    A package defines how to fetch, verfiy (via, e.g., md5), build, and
    install a piece of software.  A Package also defines what other
    packages it depends on, so that dependencies can be installed along
    with the package itself.  Packages are written in pure python.

    Packages are all submodules of spack.packages.  If spack is installed
    in $prefix, all of its python files are in $prefix/lib/spack.  Most
    of them are in the spack module, so all the packages live in
    $prefix/lib/spack/spack/packages.

    All you have to do to create a package is make a new subclass of Package
    in this directory.  Spack automatically scans the python files there
    and figures out which one to import when you invoke it.

    **An example package**

    Let's look at the cmake package to start with.  This package lives in
    $prefix/lib/spack/spack/packages/cmake.py:

    .. code-block:: python

       from spack import *
       class Cmake(Package):
           homepage  = 'https://www.cmake.org'
           url       = 'http://www.cmake.org/files/v2.8/cmake-2.8.10.2.tar.gz'
           md5       = '097278785da7182ec0aea8769d06860c'

           def install(self, spec, prefix):
               configure('--prefix=%s'   % prefix,
                         '--parallel=%s' % make_jobs)
               make()
               make('install')

    **Naming conventions**

    There are two names you should care about:

    1. The module name, ``cmake``.

       * User will refers to this name, e.g. 'spack install cmake'.
       * Corresponds to the name of the file, 'cmake.py', and it can
         include ``_``, ``-``, and numbers (it can even start with a
         number).

    2. The class name, "Cmake".  This is formed by converting `-` or
       ``_`` in the module name to camel case.  If the name starts with
       a number, we prefix the class name with ``_``. Examples:

         Module Name       Class Name
          foo_bar           FooBar
          docbook-xml       DocbookXml
          FooBar            Foobar
          3proxy            _3proxy

        The class name is what spack looks for when it loads a package module.

    **Required Attributes**

    Aside from proper naming, here is the bare minimum set of things you
    need when you make a package:

    homepage
      informational URL, so that users know what they're
      installing.

    url
      URL of the source archive that spack will fetch.

    install()
      This function tells spack how to build and install the
      software it downloaded.

    **Optional Attributes**

    You can also optionally add these attributes, if needed:

        list_url
            Webpage to scrape for available version strings. Default is the
            directory containing the tarball; use this if the default isn't
            correct so that invoking 'spack versions' will work for this
            package.

        url_version(self, version)
            When spack downloads packages at particular versions, it just
            converts version to string with str(version).  Override this if
            your package needs special version formatting in its URL.  boost
            is an example of a package that needs this.

    ***Creating Packages***

    As a package creator, you can probably ignore most of the preceding
    information, because you can use the 'spack create' command to do it
    all automatically.

    You as the package creator generally only have to worry about writing
    your install function and specifying dependencies.

    **spack create**

    Most software comes in nicely packaged tarballs, like this one:
        http://www.cmake.org/files/v2.8/cmake-2.8.10.2.tar.gz

    Taking a page from homebrew, spack deduces pretty much everything it
    needs to know from the URL above.  If you simply type this:

        spack create http://www.cmake.org/files/v2.8/cmake-2.8.10.2.tar.gz

    Spack will download the tarball, generate an md5 hash, figure out the
    version and the name of the package from the URL, and create a new
    package file for you with all the names and attributes set correctly.

    Once this skeleton code is generated, spack pops up the new package in
    your $EDITOR so that you can modify the parts that need changes.

    **Dependencies**

    If your package requires another in order to build, you can specify that
    like this:

    .. code-block:: python

       class Stackwalker(Package):
           ...
           depends_on("libdwarf")
           ...

    This tells spack that before it builds stackwalker, it needs to build
    the libdwarf package as well.  Note that this is the module name, not
    the class name (The class name is really only used by spack to find
    your package).

    Spack will download an install each dependency before it installs your
    package.  In addtion, it will add -L, -I, and rpath arguments to your
    compiler and linker for each dependency.  In most cases, this allows you
    to avoid specifying any dependencies in your configure or cmake line;
    you can just run configure or cmake without any additional arguments and
    it will find the dependencies automatically.


    **The Install Function**

    The install function is designed so that someone not too terribly familiar
    with Python could write a package installer.  For example, we put a number
    of commands in install scope that you can use almost like shell commands.
    These include make, configure, cmake, rm, rmtree, mkdir, mkdirp, and others.

    You can see above in the cmake script that these commands are used to run
    configure and make almost like they're used on the command line.  The
    only difference is that they are python function calls and not shell
    commands.

    It may be puzzling to you where the commands and functions in install live.
    They are NOT instance variables on the class; this would require us to
    type 'self.' all the time and it makes the install code unnecessarily long.
    Rather, spack puts these commands and variables in *module* scope for your
    Package subclass.  Since each package has its own module, this doesn't
    pollute other namespaces, and it allows you to more easily implement an
    install function.

    For a full list of commands and variables available in module scope, see the
    add_commands_to_module() function in this class. This is where most of
    them are created and set on the module.


    **Parallel Builds**

    By default, Spack will run make in parallel when you run make() in your
    install function.  Spack figures out how many cores are available on
    your system and runs make with -j<cores>.  If you do not want this behavior,
    you can explicitly mark a package not to use parallel make:

    .. code-block:: python

       class SomePackage(Package):
           ...
           parallel = False
           ...

    This changes thd default behavior so that make is sequential.  If you still
    want to build some parts in parallel, you can do this in your install function:

    .. code-block:: python

       make(parallel=True)

    Likewise, if you do not supply parallel = True in your Package, you can keep
    the default parallel behavior and run make like this when you want a
    sequential build:

    .. code-block:: python

       make(parallel=False)

    **Package Lifecycle**

    This section is really only for developers of new spack commands.

    A package's lifecycle over a run of Spack looks something like this:

    .. code-block:: python

       p = Package()             # Done for you by spack

       p.do_fetch()              # downloads tarball from a URL
       p.do_stage()              # expands tarball in a temp directory
       p.do_patch()              # applies patches to expanded source
       p.do_install()            # calls package's install() function
       p.do_uninstall()          # removes install directory

    There are also some other commands that clean the build area:

    .. code-block:: python

       p.do_clean()              # removes the stage directory entirely
       p.do_restage()            # removes the build directory and
                                 # re-expands the archive.

    The convention used here is that a do_* function is intended to be called
    internally by Spack commands (in spack.cmd).  These aren't for package
    writers to override, and doing so may break the functionality of the Package
    class.

    Package creators override functions like install() (all of them do this),
    clean() (some of them do this), and others to provide custom behavior.

    """

    #
    # These variables are defaults for the various "relations".
    #
    """Map of information about Versions of this package.
       Map goes: Version -> dict of attributes"""
    versions = {}

    """Specs of dependency packages, keyed by name."""
    dependencies = {}

    """Specs of virtual packages provided by this package, keyed by name."""
    provided = {}

    """Specs of conflicting packages, keyed by name. """
    conflicted = {}

    """Patches to apply to newly expanded source, if any."""
    patches = {}

    """Specs of package this one extends, or None.

    Currently, ppackages can extend at most one other package.
    """
    extendees = {}

    #
    # These are default values for instance variables.
    #
    """By default we build in parallel.  Subclasses can override this."""
    parallel = True

    """Most packages are NOT extendable.  Set to True if you want extensions."""
    extendable = False


    def __init__(self, spec):
        # this determines how the package should be built.
        self.spec = spec

        # Name of package is the name of its module, without the
        # containing module names.
        self.name = self.module.__name__
        if '.' in self.name:
            self.name = self.name[self.name.rindex('.') + 1:]

        # Sanity check some required variables that could be
        # overridden by package authors.
        def ensure_has_dict(attr_name):
            if not hasattr(self, attr_name):
                raise PackageError("Package %s must define %s" % attr_name)

            attr = getattr(self, attr_name)
            if not isinstance(attr, dict):
                raise PackageError("Package %s has non-dict %s attribute!"
                                   % (self.name, attr_name))
        ensure_has_dict('versions')
        ensure_has_dict('dependencies')
        ensure_has_dict('conflicted')
        ensure_has_dict('patches')

        # Check versions in the versions dict.
        for v in self.versions:
            assert(isinstance(v, Version))

        # Check version descriptors
        for v in sorted(self.versions):
            assert(isinstance(self.versions[v], dict))

        # Version-ize the keys in versions dict
        try:
            self.versions = dict((Version(v), h) for v,h in self.versions.items())
        except ValueError, e:
            raise ValueError("In package %s: %s" % (self.name, e.message))

        # stage used to build this package.
        self._stage = None

        # Init fetch strategy and url to None
        self._fetcher = None
        self.url = getattr(self.__class__, 'url', None)

        # Fix up self.url if this package fetches with a URLFetchStrategy.
        # This makes self.url behave sanely.
        if self.spec.versions.concrete:
            # TODO: this is a really roundabout way of determining the type
            # TODO: of fetch to do. figure out a more sane fetch strategy/package
            # TODO: init order (right now it's conflated with stage, package, and
            # TODO: the tests make assumptions)
            f = fs.for_package_version(self, self.version)
            if isinstance(f, fs.URLFetchStrategy):
                self.url = self.url_for_version(self.spec.version)

        # Set a default list URL (place to find available versions)
        if not hasattr(self, 'list_url'):
            self.list_url = None

        if not hasattr(self, 'list_depth'):
            self.list_depth = 1

        # Set up some internal variables for timing.
        self._fetch_time = 0.0
        self._total_time = 0.0

        if self.is_extension:
            spack.db.get(self.extendee_spec)._check_extendable()


    @property
    def version(self):
        if not self.spec.versions.concrete:
            raise ValueError("Can only get of package with concrete version.")
        return self.spec.versions[0]


    @memoized
    def version_urls(self):
        """Return a list of URLs for different versions of this
           package, sorted by version.  A version's URL only appears
           in this list if it has an explicitly defined URL."""
        version_urls = {}
        for v in sorted(self.versions):
            args = self.versions[v]
            if 'url' in args:
                version_urls[v] = args['url']
        return version_urls


    def nearest_url(self, version):
        """Finds the URL for the next lowest version with a URL.
           If there is no lower version with a URL, uses the
           package url property. If that isn't there, uses a
           *higher* URL, and if that isn't there raises an error.
        """
        version_urls = self.version_urls()
        url = getattr(self.__class__, 'url', None)

        for v in version_urls:
            if v > version and url:
                break
            if version_urls[v]:
                url = version_urls[v]
        return url


    # TODO: move this out of here and into some URL extrapolation module?
    def url_for_version(self, version):
        """Returns a URL that you can download a new version of this package from."""
        if not isinstance(version, Version):
            version = Version(version)

        cls = self.__class__
        if not (hasattr(cls, 'url') or self.version_urls()):
            raise NoURLError(cls)

        # If we have a specific URL for this version, don't extrapolate.
        version_urls = self.version_urls()
        if version in version_urls:
            return version_urls[version]

        # If we have no idea, try to substitute the version.
        return url.substitute_version(self.nearest_url(version),
                                      self.url_version(version))


    @property
    def stage(self):
        if not self.spec.concrete:
            raise ValueError("Can only get a stage for a concrete package.")

        if self._stage is None:
            mp = spack.mirror.mirror_archive_path(self.spec)
            self._stage = Stage(
                self.fetcher, mirror_path=mp, name=self.spec.short_spec)
        return self._stage


    @property
    def fetcher(self):
        if not self.spec.versions.concrete:
            raise ValueError(
                "Can only get a fetcher for a package with concrete versions.")

        if not self._fetcher:
            self._fetcher = fs.for_package_version(self, self.version)
        return self._fetcher


    @fetcher.setter
    def fetcher(self, f):
        self._fetcher = f


    @property
    def extendee_spec(self):
        """Spec of the extendee of this package, or None if it is not an extension."""
        if not self.extendees:
            return None
        name = next(iter(self.extendees))
        if not name in self.spec:
            spec, kwargs = self.extendees[name]
            return spec

        # Need to do this to get the concrete version of the spec
        return self.spec[name]


    @property
    def extendee_args(self):
        """Spec of the extendee of this package, or None if it is not an extension."""
        if not self.extendees:
            return None
        name = next(iter(self.extendees))
        return self.extendees[name][1]


    @property
    def is_extension(self):
        return len(self.extendees) > 0


    def extends(self, spec):
        return (spec.name in self.extendees and
                spec.satisfies(self.extendees[spec.name][0]))


    @property
    def activated(self):
        if not self.is_extension:
            raise ValueError("is_extension called on package that is not an extension.")
        exts = spack.install_layout.extension_map(self.extendee_spec)
        return (self.name in exts) and (exts[self.name] == self.spec)


    def preorder_traversal(self, visited=None, **kwargs):
        """This does a preorder traversal of the package's dependence DAG."""
        virtual = kwargs.get("virtual", False)

        if visited is None:
            visited = set()

        if self.name in visited:
            return
        visited.add(self.name)

        if not virtual:
            yield self

        for name in sorted(self.dependencies.keys()):
            spec = self.dependencies[name]

            # currently, we do not descend into virtual dependencies, as this
            # makes doing a sensible traversal much harder.  We just assume that
            # ANY of the virtual deps will work, which might not be true (due to
            # conflicts or unsatisfiable specs).  For now this is ok but we might
            # want to reinvestigate if we start using a lot of complicated virtual
            # dependencies
            # TODO: reinvestigate this.
            if spec.virtual:
                if virtual:
                    yield spec
                continue

            for pkg in spack.db.get(name).preorder_traversal(visited, **kwargs):
                yield pkg


    def validate_dependencies(self):
        """Ensure that this package and its dependencies all have consistent
           constraints on them.

           NOTE that this will NOT find sanity problems through a virtual
           dependency.  Virtual deps complicate the problem because we
           don't know in advance which ones conflict with others in the
           dependency DAG. If there's more than one virtual dependency,
           it's a full-on SAT problem, so hold off on this for now.
           The vdeps are actually skipped in preorder_traversal, so see
           that for details.

           TODO: investigate validating virtual dependencies.
        """
        # This algorithm just attempts to merge all the constraints on the same
        # package together, loses information about the source of the conflict.
        # What we'd really like to know is exactly which two constraints
        # conflict, but that algorithm is more expensive, so we'll do it
        # the simple, less informative way for now.
        merged = spack.spec.DependencyMap()

        try:
            for pkg in self.preorder_traversal():
                for name, spec in pkg.dependencies.iteritems():
                    if name not in merged:
                        merged[name] = spec.copy()
                    else:
                        merged[name].constrain(spec)

        except spack.spec.UnsatisfiableSpecError, e:
            raise InvalidPackageDependencyError(
                "Package %s has inconsistent dependency constraints: %s"
                % (self.name, e.message))


    def provides(self, vpkg_name):
        """True if this package provides a virtual package with the specified name."""
        return vpkg_name in self.provided


    def virtual_dependencies(self, visited=None):
        for spec in sorted(set(self.preorder_traversal(virtual=True))):
            yield spec


    @property
    def installed(self):
        return os.path.isdir(self.prefix)


    @property
    def installed_dependents(self):
        """Return a list of the specs of all installed packages that depend
           on this one."""
        dependents = []
        for spec in spack.db.installed_package_specs():
            if self.name != spec.name and self.spec in spec:
                dependents.append(spec)
        return dependents


    @property
    def prefix(self):
        """Get the prefix into which this package should be installed."""
        return self.spec.prefix


    @property
    def compiler(self):
        """Get the spack.compiler.Compiler object used to build this package."""
        if not self.spec.concrete:
            raise ValueError("Can only get a compiler for a concrete package.")
        return spack.compilers.compiler_for_spec(self.spec.compiler)


    def url_version(self, version):
        """Given a version, this returns a string that should be substituted into the
           package's URL to download that version.
           By default, this just returns the version string. Subclasses may need to
           override this, e.g. for boost versions where you need to ensure that there
           are _'s in the download URL.
        """
        return str(version)


    def remove_prefix(self):
        """Removes the prefix for a package along with any empty parent directories."""
        spack.install_layout.remove_path_for_spec(self.spec)


    def do_fetch(self):
        """Creates a stage directory and downloads the taball for this package.
           Working directory will be set to the stage directory.
        """
        if not self.spec.concrete:
            raise ValueError("Can only fetch concrete packages.")

        start_time = time.time()
        if spack.do_checksum and not self.version in self.versions:
            tty.warn("There is no checksum on file to fetch %s safely."
                     % self.spec.format('$_$@'))

            # Ask the user whether to skip the checksum if we're
            # interactive, but just fail if non-interactive.
            checksum_msg = "Add a checksum or use --no-checksum to skip this check."
            ignore_checksum = False
            if sys.stdout.isatty():
                ignore_checksum = tty.get_yes_or_no("  Fetch anyway?", default=False)
                if ignore_checksum:
                    tty.msg("Fetching with no checksum.", checksum_msg)

            if not ignore_checksum:
                raise FetchError(
                    "Will not fetch %s." % self.spec.format('$_$@'), checksum_msg)

        self.stage.fetch()
        self._fetch_time = time.time() - start_time

        if spack.do_checksum and self.version in self.versions:
            self.stage.check()


    def do_stage(self):
        """Unpacks the fetched tarball, then changes into the expanded tarball
           directory."""
        if not self.spec.concrete:
            raise ValueError("Can only stage concrete packages.")

        self.do_fetch()

        archive_dir = self.stage.source_path
        if not archive_dir:
            self.stage.expand_archive()
            tty.msg("Created stage in %s." % self.stage.path)
        else:
            tty.msg("Already staged %s in %s." % (self.name, self.stage.path))
        self.stage.chdir_to_source()


    def do_patch(self):
        """Calls do_stage(), then applied patches to the expanded tarball if they
           haven't been applied already."""
        if not self.spec.concrete:
            raise ValueError("Can only patch concrete packages.")

        # Kick off the stage first.
        self.do_stage()

        # Package can add its own patch function.
        has_patch_fun = hasattr(self, 'patch') and callable(self.patch)

        # If there are no patches, note it.
        if not self.patches and not has_patch_fun:
            tty.msg("No patches needed for %s." % self.name)
            return

        # Construct paths to special files in the archive dir used to
        # keep track of whether patches were successfully applied.
        archive_dir = self.stage.source_path
        good_file = join_path(archive_dir, '.spack_patched')
        bad_file  = join_path(archive_dir, '.spack_patch_failed')

        # If we encounter an archive that failed to patch, restage it
        # so that we can apply all the patches again.
        if os.path.isfile(bad_file):
            tty.msg("Patching failed last time.  Restaging.")
            self.stage.restage()

        self.stage.chdir_to_source()

        # If this file exists, then we already applied all the patches.
        if os.path.isfile(good_file):
            tty.msg("Already patched %s" % self.name)
            return

        # Apply all the patches for specs that match this one
        for spec, patch_list in self.patches.items():
            if self.spec.satisfies(spec):
                for patch in patch_list:
                    tty.msg('Applying patch %s' % patch.path_or_url)
                    try:
                        patch.apply(self.stage)
                    except:
                        # Touch bad file if anything goes wrong.
                        touch(bad_file)
                        raise

        # patch succeeded.  Get rid of failed file & touch good file so we
        # don't try to patch again again next time.
        if os.path.isfile(bad_file):
            os.remove(bad_file)
        touch(good_file)

        if has_patch_fun:
            self.patch()

        tty.msg("Patched %s" % self.name)


    def do_fake_install(self):
        """Make a fake install directory contaiing a 'fake' file in bin."""
        mkdirp(self.prefix.bin)
        touch(join_path(self.prefix.bin, 'fake'))
        mkdirp(self.prefix.lib)
        mkdirp(self.prefix.man1)


    def do_install(self, **kwargs):
        """This class should call this version of the install method.
           Package implementations should override install().
        """
        # whether to keep the prefix on failure.  Default is to destroy it.
        keep_prefix  = kwargs.get('keep_prefix', False)
        keep_stage   = kwargs.get('keep_stage', False)
        ignore_deps  = kwargs.get('ignore_deps', False)
        fake_install = kwargs.get('fake', False)

        if not self.spec.concrete:
            raise ValueError("Can only install concrete packages.")

        if os.path.exists(self.prefix):
            tty.msg("%s is already installed in %s." % (self.name, self.prefix))
            return

        tty.msg("Installing %s" % self.name)

        if not ignore_deps:
            self.do_install_dependencies(**kwargs)

        start_time = time.time()
        if not fake_install:
            self.do_patch()

        # create the install directory.  The install layout
        # handles this in case so that it can use whatever
        # package naming scheme it likes.
        spack.install_layout.make_path_for_spec(self.spec)

        def cleanup():
            if not keep_prefix:
                # If anything goes wrong, remove the install prefix
                self.remove_prefix()
            else:
                tty.warn("Keeping install prefix in place despite error.",
                         "Spack will think this package is installed." +
                         "Manually remove this directory to fix:",
                         self.prefix)

        def real_work():
            try:
                tty.msg("Building %s." % self.name)

                # Run the pre-install hook in the child process after
                # the directory is created.
                spack.hooks.pre_install(self)

                # Set up process's build environment before running install.
                self.stage.chdir_to_source()
                if fake_install:
                    self.do_fake_install()
                else:
                    # Subclasses implement install() to do the real work.
                    self.install(self.spec, self.prefix)

                # Ensure that something was actually installed.
                self._sanity_check_install()

                # On successful install, remove the stage.
                if not keep_stage:
                    self.stage.destroy()

                # Stop timer.
                self._total_time = time.time() - start_time
                build_time = self._total_time - self._fetch_time

                tty.msg("Successfully installed %s." % self.name,
                        "Fetch: %s.  Build: %s.  Total: %s."
                        % (_hms(self._fetch_time), _hms(build_time), _hms(self._total_time)))
                print_pkg(self.prefix)

            except ProcessError, e:
                # One of the processes returned an error code.
                # Suppress detailed stack trace here unless in debug mode
                if spack.debug:
                    raise e
                else:
                    tty.error(e)

                # Still need to clean up b/c there was an error.
                cleanup()

            except:
                # other exceptions just clean up and raise.
                cleanup()
                raise

        build_env.fork(self, real_work)

        # Once everything else is done, run post install hooks
        spack.hooks.post_install(self)

        installed_package_names.add(self.name)


    def _sanity_check_install(self):
        installed = set(os.listdir(self.prefix))
        installed.difference_update(spack.install_layout.hidden_file_paths)
        if not installed:
            raise InstallError(
                "Install failed for %s.  Nothing was installed!" % self.name)


    def do_install_dependencies(self, **kwargs):
        # Pass along paths of dependencies here
        for dep in self.spec.dependencies.values():
            dep.package.do_install(**kwargs)


    @property
    def module(self):
        """Use this to add variables to the class's module's scope.
           This lets us use custom syntax in the install method.
        """
        return __import__(self.__class__.__module__,
                          fromlist=[self.__class__.__name__])


    def setup_dependent_environment(self, module, spec, dependent_spec):
        """Called before the install() method of dependents.

        Default implementation does nothing, but this can be
        overridden by an extendable package to set up the install
        environment for its extensions.  This is useful if there are
        some common steps to installing all extensions for a
        certain package.

        Some examples:

        1. Installing python modules generally requires PYTHONPATH to
           point to the lib/pythonX.Y/site-packages directory in the
           module's install prefix.  This could set that variable.

        2. Extensions often need to invoke the 'python' interpreter
           from the Python installation being extended.  This routine can
           put a 'python' Execuable object in the module scope for the
           extension package to simplify extension installs.

        3. A lot of Qt extensions need QTDIR set.  This can be used to do that.

        """
        pass


    def install(self, spec, prefix):
        """Package implementations override this with their own build configuration."""
        raise InstallError("Package %s provides no install method!" % self.name)


    def do_uninstall(self, **kwargs):
        force = kwargs.get('force', False)

        if not self.installed:
            raise InstallError(str(self.spec) + " is not installed.")

        if not force:
            deps = self.installed_dependents
            formatted_deps = [s.format('$_$@$%@$+$=$#') for s in deps]
            if deps: raise InstallError(
                "Cannot uninstall %s." % self.spec,
                "The following installed packages depend on it: %s" %
                ' '.join(formatted_deps))

        # Pre-uninstall hook runs first.
        spack.hooks.pre_uninstall(self)

        # Uninstalling in Spack only requires removing the prefix.
        self.remove_prefix()
        tty.msg("Successfully uninstalled %s." % self.spec.short_spec)

        # Once everything else is done, run post install hooks
        spack.hooks.post_uninstall(self)


    def _check_extendable(self):
        if not self.extendable:
            raise ValueError("Package %s is not extendable!" % self.name)


    def _sanity_check_extension(self):
        if not self.is_extension:
            raise ActivationError("This package is not an extension.")

        extendee_package = self.extendee_spec.package
        extendee_package._check_extendable()

        if not extendee_package.installed:
            raise ActivationError("Can only (de)activate extensions for installed packages.")
        if not self.installed:
            raise ActivationError("Extensions must first be installed.")
        if not self.extendee_spec.name in self.extendees:
            raise ActivationError("%s does not extend %s!" % (self.name, self.extendee.name))


    def do_activate(self, **kwargs):
        """Called on an etension to invoke the extendee's activate method.

        Commands should call this routine, and should not call
        activate() directly.
        """
        self._sanity_check_extension()
        force = kwargs.get('force', False)

        # TODO: get rid of this normalize - DAG handling.
        self.spec.normalize()

        spack.install_layout.check_extension_conflict(self.extendee_spec, self.spec)

        if not force:
            for spec in self.spec.traverse(root=False):
                if spec.package.extends(self.extendee_spec):
                    # TODO: fix this normalize() requirement -- revisit DAG handling.
                    spec.package.spec.normalize()
                    if not spec.package.activated:
                        spec.package.do_activate(**kwargs)

        self.extendee_spec.package.activate(self, **self.extendee_args)

        spack.install_layout.add_extension(self.extendee_spec, self.spec)
        tty.msg("Activated extension %s for %s."
                % (self.spec.short_spec, self.extendee_spec.format("$_$@$+$%@")))


    def activate(self, extension, **kwargs):
        """Symlinks all files from the extension into extendee's install dir.

        Package authors can override this method to support other
        extension mechanisms.  Spack internals (commands, hooks, etc.)
        should call do_activate() method so that proper checks are
        always executed.

        """
        def ignore(filename):
            return (filename in spack.install_layout.hidden_file_paths or
                    kwargs.get('ignore', lambda f: False)(filename))

        tree = LinkTree(extension.prefix)
        conflict = tree.find_conflict(self.prefix, ignore=ignore)
        if conflict:
            raise ExtensionConflictError(conflict)
        tree.merge(self.prefix, ignore=ignore)


    def do_deactivate(self, **kwargs):
        """Called on the extension to invoke extendee's deactivate() method."""
        self._sanity_check_extension()
        force = kwargs.get('force', False)

        # Allow a force deactivate to happen.  This can unlink
        # spurious files if something was corrupted.
        if not force:
            spack.install_layout.check_activated(self.extendee_spec, self.spec)

            activated = spack.install_layout.extension_map(self.extendee_spec)
            for name, aspec in activated.items():
                if aspec != self.spec and self.spec in aspec:
                    raise ActivationError(
                        "Cannot deactivate %s beacuse %s is activated and depends on it."
                        % (self.spec.short_spec, aspec.short_spec))

        self.extendee_spec.package.deactivate(self, **self.extendee_args)

        # redundant activation check -- makes SURE the spec is not
        # still activated even if something was wrong above.
        if self.activated:
            spack.install_layout.remove_extension(self.extendee_spec, self.spec)

        tty.msg("Deactivated extension %s for %s."
                % (self.spec.short_spec, self.extendee_spec.format("$_$@$+$%@")))


    def deactivate(self, extension, **kwargs):
        """Unlinks all files from extension out of this package's install dir.

        Package authors can override this method to support other
        extension mechanisms.  Spack internals (commands, hooks, etc.)
        should call do_deactivate() method so that proper checks are
        always executed.

        """
        def ignore(filename):
            return (filename in spack.install_layout.hidden_file_paths or
                    kwargs.get('ignore', lambda f: False)(filename))

        tree = LinkTree(extension.prefix)
        tree.unmerge(self.prefix, ignore=ignore)


    def do_restage(self):
        """Reverts expanded/checked out source to a pristine state."""
        self.stage.restage()


    def do_clean(self):
        """Removes the package's build stage and source tarball."""
        if os.path.exists(self.stage.path):
            self.stage.destroy()


    def format_doc(self, **kwargs):
        """Wrap doc string at 72 characters and format nicely"""
        indent = kwargs.get('indent', 0)

        if not self.__doc__:
            return ""

        doc = re.sub(r'\s+', ' ', self.__doc__)
        lines = textwrap.wrap(doc, 72)
        results = StringIO()
        for line in lines:
            results.write((" " * indent) + line + "\n")
        return results.getvalue()


    @property
    def all_urls(self):
        urls = []
        if self.url:
            urls.append(self.url)

        for args in self.versions.values():
            if 'url' in args:
                urls.append(args['url'])
        return urls


    def fetch_remote_versions(self):
        """Try to find remote versions of this package using the
           list_url and any other URLs described in the package file."""
        if not self.all_urls:
            raise VersionFetchError(self.__class__)

        try:
            return find_versions_of_archive(
                *self.all_urls, list_url=self.list_url, list_depth=self.list_depth)
        except spack.error.NoNetworkConnectionError, e:
            tty.die("Package.fetch_versions couldn't connect to:",
                    e.url, e.message)


    @property
    def rpath(self):
        """Get the rpath this package links with, as a list of paths."""
        rpaths = [self.prefix.lib, self.prefix.lib64]
        rpaths.extend(d.prefix.lib for d in self.spec.traverse(root=False)
                      if os.path.isdir(d.prefix.lib))
        rpaths.extend(d.prefix.lib64 for d in self.spec.traverse(root=False)
                      if os.path.isdir(d.prefix.lib64))
        return rpaths


    @property
    def rpath_args(self):
        """Get the rpath args as a string, with -Wl,-rpath= for each element."""
        return " ".join("-Wl,-rpath=%s" % p for p in self.rpath)


def find_versions_of_archive(*archive_urls, **kwargs):
    list_url   = kwargs.get('list_url', None)
    list_depth = kwargs.get('list_depth', 1)

    # Generate a list of list_urls based on archive urls and any
    # explicitly listed list_url in the package
    list_urls = set()
    if list_url:
        list_urls.add(list_url)
    for aurl in archive_urls:
        list_urls.add(url.find_list_url(aurl))

    # Grab some web pages to scrape.
    page_map = {}
    for lurl in list_urls:
        page_map.update(get_pages(lurl, depth=list_depth))

    # Scrape them for archive URLs
    regexes = []
    for aurl in archive_urls:
        # This creates a regex from the URL with a capture group for
        # the version part of the URL.  The capture group is converted
        # to a generic wildcard, so we can use this to extract things
        # on a page that look like archive URLs.
        url_regex = url.wildcard_version(aurl)

        # We'll be a bit more liberal and just look for the archive
        # part, not the full path.
        regexes.append(os.path.basename(url_regex))

    # Build a version list from all the matches we find
    versions = {}
    for page_url, content in page_map.iteritems():
        # extract versions from matches.
        for regex in regexes:
            versions.update(
                (Version(m.group(1)), urljoin(page_url, m.group(0)))
                for m in re.finditer(regex, content))

    return versions


def validate_package_url(url_string):
    """Determine whether spack can handle a particular URL or not."""
    url = urlparse(url_string)
    if url.scheme not in _ALLOWED_URL_SCHEMES:
        tty.die("Invalid protocol in URL: '%s'" % url_string)

    if not allowed_archive(url_string):
        tty.die("Invalid file type in URL: '%s'" % url_string)


def print_pkg(message):
    """Outputs a message with a package icon."""
    from llnl.util.tty.color import cwrite
    cwrite('@*g{[+]} ')
    print message


def _hms(seconds):
    """Convert time in seconds to hours, minutes, seconds."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    parts = []
    if h: parts.append("%dh" % h)
    if m: parts.append("%dm" % m)
    if s: parts.append("%.2fs" % s)
    return ' '.join(parts)


class FetchError(spack.error.SpackError):
    """Raised when something goes wrong during fetch."""
    def __init__(self, message, long_msg=None):
        super(FetchError, self).__init__(message, long_msg)


class InstallError(spack.error.SpackError):
    """Raised when something goes wrong during install or uninstall."""
    def __init__(self, message, long_msg=None):
        super(InstallError, self).__init__(message, long_msg)


class PackageError(spack.error.SpackError):
    """Raised when something is wrong with a package definition."""
    def __init__(self, message, long_msg=None):
        super(PackageError, self).__init__(message, long_msg)


class InvalidPackageDependencyError(PackageError):
    """Raised when package specification is inconsistent with requirements of
       its dependencies."""
    def __init__(self, message):
        super(InvalidPackageDependencyError, self).__init__(message)


class PackageVersionError(PackageError):
    """Raised when a version URL cannot automatically be determined."""
    def __init__(self, version):
        super(PackageVersionError, self).__init__(
            "Cannot determine a URL automatically for version %s." % version,
            "Please provide a url for this version in the package.py file.")


class VersionFetchError(PackageError):
    """Raised when a version URL cannot automatically be determined."""
    def __init__(self, cls):
        super(VersionFetchError, self).__init__(
            "Cannot fetch versions for package %s " % cls.__name__ +
            "because it does not define any URLs to fetch.")


class NoURLError(PackageError):
    """Raised when someone tries to build a URL for a package with no URLs."""
    def __init__(self, cls):
        super(NoURLError, self).__init__(
            "Package %s has no version with a URL." % cls.__name__)


class ExtensionError(PackageError): pass


class ExtensionConflictError(ExtensionError):
    def __init__(self, path):
        super(ExtensionConflictError, self).__init__(
            "Extension blocked by file: %s" % path)


class ActivationError(ExtensionError):
    def __init__(self, msg, long_msg=None):
        super(ActivationError, self).__init__(msg, long_msg)
