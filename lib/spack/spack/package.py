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
import inspect
import os
import re
import subprocess
import platform as py_platform
import shutil

from spack import *
import spack.spec
import spack.error
import packages
import tty
import validate
import multiprocessing
import url

import spack.util.crypto as crypto
from spack.version import *
from spack.stage import Stage
from spack.util.lang import *
from spack.util.web import get_pages
from spack.util.environment import *
from spack.util.filesystem import touch


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
       a number, we prefix the class name with ``Num_``. Examples:

         Module Name       Class Name
          foo_bar           FooBar
          docbook-xml       DocbookXml
          FooBar            Foobar
          3proxy            Num_3proxy

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

       p.do_clean()              # runs make clean
       p.do_clean_work()         # removes the build directory and
                                 # re-expands the archive.
       p.do_clean_dist()         # removes the stage directory entirely

    The convention used here is that a do_* function is intended to be called
    internally by Spack commands (in spack.cmd).  These aren't for package
    writers to override, and doing so may break the functionality of the Package
    class.

    Package creators override functions like install() (all of them do this),
    clean() (some of them do this), and others to provide custom behavior.

    """

    #
    # These variables are defaults for the various relations defined on
    # packages.  Subclasses will have their own versions of these.
    #
    """Specs of dependency packages, keyed by name."""
    dependencies = {}

    """Specs of virtual packages provided by this package, keyed by name."""
    provided = {}

    """Specs of conflicting packages, keyed by name. """
    conflicted = {}

    """Patches to apply to newly expanded source, if any."""
    patches = {}

    #
    # These are default values for instance variables.
    #
    """By default we build in parallel.  Subclasses can override this."""
    parallel = True

    """Remove tarball and build by default.  If this is true, leave them."""
    dirty = False

    """Controls whether install and uninstall check deps before running."""
    ignore_dependencies = False

    """Dirty hack for forcing packages with uninterpretable URLs"""
    force_url = False


    def __init__(self, spec):
        # These attributes are required for all packages.
        attr_required(self.__class__, 'homepage')
        attr_required(self.__class__, 'url')

        # this determines how the package should be built.
        self.spec = spec

        # Name of package is the name of its module, without the
        # containing module names.
        self.name = self.module.__name__
        if '.' in self.name:
            self.name = self.name[self.name.rindex('.') + 1:]

        # Make sure URL is an allowed type
        validate.url(self.url)

        # patch up the URL with a new version if the spec version is concrete
        if self.spec.versions.concrete:
            self.url = self.url_for_version(self.spec.version)

        # This is set by scraping a web page.
        self._available_versions = None

        # versions should be a dict from version to checksum, for safe versions
        # of this package.  If it's not present, make it an empty dict.
        if not hasattr(self, 'versions'):
            self.versions = {}

        if not isinstance(self.versions, dict):
            raise ValueError("versions attribute of package %s must be a dict!"
                             % self.name)

        # Version-ize the keys in versions dict
        try:
            self.versions = { Version(v):h for v,h in self.versions.items() }
        except ValueError:
            raise ValueError("Keys of versions dict in package %s must be versions!"
                             % self.name)

        # stage used to build this package.
        self._stage = None

        # Set a default list URL (place to find available versions)
        if not hasattr(self, 'list_url'):
            self.list_url = None

        if not hasattr(self, 'list_depth'):
            self.list_depth = 1


    @property
    def default_version(self):
        """Get the version in the default URL for this package,
           or fails."""
        try:
            return url.parse_version(self.__class__.url)
        except UndetectableVersionError:
            tty.die("Couldn't extract a default version from %s. You " +
                    "must specify it explicitly in the package." % self.url)


    @property
    def version(self):
        if not self.spec.concrete:
            raise ValueError("Can only get version of concrete package.")
        return self.spec.versions[0]


    @property
    def stage(self):
        if not self.spec.concrete:
            raise ValueError("Can only get a stage for a concrete package.")

        if self._stage is None:
            mirror_path = "%s/%s" % (self.name, os.path.basename(self.url))
            self._stage = Stage(
                self.url, mirror_path=mirror_path, name=str(self.spec))
        return self._stage


    def add_commands_to_module(self):
        """Populate the module scope of install() with some useful functions.
           This makes things easier for package writers.
        """
        m = self.module

        m.make  = MakeExecutable('make', self.parallel)
        m.gmake = MakeExecutable('gmake', self.parallel)

        # number of jobs spack prefers to build with.
        m.make_jobs = multiprocessing.cpu_count()

        # Find the configure script in the archive path
        # Don't use which for this; we want to find it in the current dir.
        m.configure = Executable('./configure')
        m.cmake = which("cmake")

        # standard CMake arguments
        m.std_cmake_args = ['-DCMAKE_INSTALL_PREFIX=%s' % self.prefix,
                            '-DCMAKE_BUILD_TYPE=None']
        if py_platform.mac_ver()[0]:
            m.std_cmake_args.append('-DCMAKE_FIND_FRAMEWORK=LAST')

        # Emulate some shell commands for convenience
        m.cd         = os.chdir
        m.mkdir      = os.mkdir
        m.makedirs   = os.makedirs
        m.remove     = os.remove
        m.removedirs = os.removedirs

        m.mkdirp     = mkdirp
        m.install    = install
        m.rmtree     = shutil.rmtree
        m.move       = shutil.move

        # Useful directories within the prefix are encapsulated in
        # a Prefix object.
        m.prefix  = self.prefix


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

            for pkg in packages.get(name).preorder_traversal(visited, **kwargs):
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
        return os.path.exists(self.prefix)


    @property
    def installed_dependents(self):
        """Return a list of the specs of all installed packages that depend
           on this one."""
        dependents = []
        for spec in packages.installed_package_specs():
            if self.name in spec.dependencies:
                dep_spec = spec.dependencies[self.name]
                if self.spec == dep_spec:
                    dependents.append(dep_spec)
        return dependents


    @property
    def prefix(self):
        """Get the prefix into which this package should be installed."""
        return self.spec.prefix


    def url_version(self, version):
        """Given a version, this returns a string that should be substituted into the
           package's URL to download that version.
           By default, this just returns the version string. Subclasses may need to
           override this, e.g. for boost versions where you need to ensure that there
           are _'s in the download URL.
        """
        if self.force_url:
            return self.default_version
        return str(version)


    def url_for_version(self, version):
        """Gives a URL that you can download a new version of this package from."""
        if self.force_url:
            return self.url
        return url.substitute_version(self.__class__.url, self.url_version(version))


    def remove_prefix(self):
        """Removes the prefix for a package along with any empty parent directories."""
        if self.dirty:
            return
        spack.install_layout.remove_path_for_spec(self.spec)


    def do_fetch(self):
        """Creates a stage directory and downloads the taball for this package.
           Working directory will be set to the stage directory.
        """
        if not self.spec.concrete:
            raise ValueError("Can only fetch concrete packages.")

        if spack.do_checksum and not self.version in self.versions:
            tty.die("Cannot fetch %s@%s safely; there is no checksum on file for this "
                    "version." % (self.name, self.version),
                    "Add a checksum to the package file, or use --no-checksum to "
                    "skip this check.")

        self.stage.fetch()

        if self.version in self.versions:
            digest = self.versions[self.version]
            checker = crypto.Checker(digest)
            if checker.check(self.stage.archive_file):
                tty.msg("Checksum passed for %s" % self.name)
            else:
                tty.die("%s checksum failed for %s.  Expected %s but got %s."
                        % (checker.hash_name, self.name, digest, checker.sum))


    def do_stage(self):
        """Unpacks the fetched tarball, then changes into the expanded tarball
           directory."""
        if not self.spec.concrete:
            raise ValueError("Can only stage concrete packages.")

        self.do_fetch()

        archive_dir = self.stage.expanded_archive_path
        if not archive_dir:
            tty.msg("Staging archive: %s" % self.stage.archive_file)
            self.stage.expand_archive()
        else:
            tty.msg("Already staged %s" % self.name)
        self.stage.chdir_to_archive()


    def do_patch(self):
        """Calls do_stage(), then applied patches to the expanded tarball if they
           haven't been applied already."""
        if not self.spec.concrete:
            raise ValueError("Can only patch concrete packages.")

        self.do_stage()

        # Construct paths to special files in the archive dir used to
        # keep track of whether patches were successfully applied.
        archive_dir = self.stage.expanded_archive_path
        good_file = new_path(archive_dir, '.spack_patched')
        bad_file  = new_path(archive_dir, '.spack_patch_failed')

        # If we encounter an archive that failed to patch, restage it
        # so that we can apply all the patches again.
        if os.path.isfile(bad_file):
            tty.msg("Patching failed last time.  Restaging.")
            self.stage.restage()

        self.stage.chdir_to_archive()

        # If this file exists, then we already applied all the patches.
        if os.path.isfile(good_file):
            tty.msg("Already patched %s" % self.name)
            return

        # Apply all the patches for specs that match this on
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


    def do_install(self):
        """This class should call this version of the install method.
           Package implementations should override install().
        """
        if not self.spec.concrete:
            raise ValueError("Can only install concrete packages.")

        if os.path.exists(self.prefix):
            tty.msg("%s is already installed." % self.name)
            tty.pkg(self.prefix)
            return

        if not self.ignore_dependencies:
            self.do_install_dependencies()

        self.do_patch()
        self.setup_install_environment()

        # Add convenience commands to the package's module scope to
        # make building easier.
        self.add_commands_to_module()

        tty.msg("Building %s." % self.name)
        try:
            # create the install directory (allow the layout to handle this in
            # case it needs to add extra files)
            spack.install_layout.make_path_for_spec(self.spec)

            self.install(self.spec, self.prefix)
            if not os.path.isdir(self.prefix):
                tty.die("Install failed for %s.  No install dir created." % self.name)

        except Exception, e:
            if not self.dirty:
                self.remove_prefix()
            raise

        tty.msg("Successfully installed %s" % self.name)
        tty.pkg(self.prefix)

        # Once the install is done, destroy the stage where we built it,
        # unless the user wants it kept around.
        if not self.dirty:
            self.stage.destroy()


    def setup_install_environment(self):
        """This ensures a clean install environment when we build packages."""
        pop_keys(os.environ, "LD_LIBRARY_PATH", "LD_RUN_PATH", "DYLD_LIBRARY_PATH")

        # Add spack environment at front of path and pass the
        # lib location along so the compiler script can find spack
        os.environ[SPACK_LIB] = lib_path

        # Fix for case-insensitive file systems.  Conflicting links are
        # in directories called "case*" within the env directory.
        env_paths = [env_path]
        for file in os.listdir(env_path):
            path = new_path(env_path, file)
            if file.startswith("case") and os.path.isdir(path):
                env_paths.append(path)
        path_put_first("PATH", env_paths)
        path_set(SPACK_ENV_PATH, env_paths)

        # Pass along prefixes of dependencies here
        path_set(
            SPACK_DEPENDENCIES,
            [dep.package.prefix for dep in self.spec.dependencies.values()])

        # Install location
        os.environ[SPACK_PREFIX] = self.prefix

        # Build root for logging.
        os.environ[SPACK_BUILD_ROOT] = self.stage.expanded_archive_path


    def do_install_dependencies(self):
        # Pass along paths of dependencies here
        for dep in self.spec.dependencies.values():
            dep.package.do_install()


    @property
    def module(self):
        """Use this to add variables to the class's module's scope.
           This lets us use custom syntax in the install method.
        """
        return __import__(self.__class__.__module__,
                          fromlist=[self.__class__.__name__])


    def install(self, spec, prefix):
        """Package implementations override this with their own build configuration."""
        tty.die("Packages must provide an install method!")


    def do_uninstall(self):
        if not os.path.exists(self.prefix):
            tty.die(self.name + " is not installed.")

        if not self.ignore_dependencies:
            deps = self.installed_dependents
            if deps: tty.die(
                "Cannot uninstall %s. The following installed packages depend on it:"
                % self.name, " ".join(deps))

        self.remove_prefix()
        tty.msg("Successfully uninstalled %s." % self.name)


    def do_clean(self):
        if self.stage.expanded_archive_path:
            self.stage.chdir_to_archive()
            self.clean()


    def clean(self):
        """By default just runs make clean.  Override if this isn't good."""
        try:
            make = MakeExecutable('make', self.parallel)
            make('clean')
            tty.msg("Successfully cleaned %s" % self.name)
        except subprocess.CalledProcessError, e:
            tty.warn("Warning: 'make clean' didn't work.  Consider 'spack clean --work'.")


    def do_clean_work(self):
        """By default just blows away the stage directory and re-stages."""
        self.stage.restage()


    def do_clean_dist(self):
        """Removes the stage directory where this package was built."""
        if os.path.exists(self.stage.path):
            self.stage.destroy()
        tty.msg("Successfully cleaned %s" % self.name)


    def fetch_available_versions(self):
        # If not, then try to fetch using list_url
        if not self._available_versions:
            try:
                self._available_versions = find_versions_of_archive(
                    self.url,
                    list_url=self.list_url,
                    list_depth=self.list_depth)

                if not self._available_versions:
                    tty.warn("Found no versions for %s" % self.name,
                             "Check the list_url and list_depth attribute on the "
                             + self.name + " package.",
                             "Use them to tell Spack where to look for versions.")

            except spack.error.NoNetworkConnectionError, e:
                tty.die("Package.fetch_available_versions couldn't connect to:",
                        e.url, e.message)

        return self._available_versions


    @property
    def available_versions(self):
        # If the package overrode available_versions, then use that.
        if self.versions is not None:
            return VersionList(self.versions.keys())
        else:
            vlist = self.fetch_available_versions()
            if not vlist:
                vlist = ver([self.version])
            return vlist


def find_versions_of_archive(archive_url, **kwargs):
    list_url   = kwargs.get('list_url', None)
    list_depth = kwargs.get('list_depth', 1)

    if not list_url:
        list_url = os.path.dirname(archive_url)

    # This creates a regex from the URL with a capture group for the
    # version part of the URL.  The capture group is converted to a
    # generic wildcard, so we can use this to extract things on a page
    # that look like archive URLs.
    url_regex = url.wildcard_version(archive_url)

    # We'll be a bit more liberal and just look for the archive part,
    # not the full path.
    archive_regex = os.path.basename(url_regex)

    # Grab some web pages to scrape.
    page_map = get_pages(list_url, depth=list_depth)

    # Build a version list from all the matches we find
    versions = VersionList()
    for site, page in page_map.iteritems():
        # extract versions from matches.
        matches = re.finditer(archive_regex, page)
        version_strings = set(m.group(1) for m in matches)
        for v in version_strings:
            versions.add(Version(v))

    return versions


class MakeExecutable(Executable):
    """Special Executable for make so the user can specify parallel or
       not on a per-invocation basis.  Using 'parallel' as a kwarg will
       override whatever the package's global setting is, so you can
       either default to true or false and override particular calls.

       Note that if the SPACK_NO_PARALLEL_MAKE env var is set it overrides
       everything.
    """
    def __init__(self, name, parallel):
        super(MakeExecutable, self).__init__(name)
        self.parallel = parallel

    def __call__(self, *args, **kwargs):
        parallel = kwargs.get('parallel', self.parallel)
        disable_parallel = env_flag(SPACK_NO_PARALLEL_MAKE)

        if parallel and not disable_parallel:
            jobs = "-j%d" % multiprocessing.cpu_count()
            args = (jobs,) + args

        super(MakeExecutable, self).__call__(*args, **kwargs)


class InvalidPackageDependencyError(spack.error.SpackError):
    """Raised when package specification is inconsistent with requirements of
       its dependencies."""
    def __init__(self, message):
        super(InvalidPackageDependencyError, self).__init__(message)
