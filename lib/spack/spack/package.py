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
import url

from spack.multi_function import platform
from spack.version import *
from spack.stage import Stage
from spack.util.lang import *
from spack.util.crypto import md5
from spack.util.web import get_pages


class Package(object):
    """This is the superclass for all spack packages.

    The Package class
    ==================
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

    An example package
    ====================
    Let's look at the cmake package to start with.  This package lives in
    $prefix/lib/spack/spack/packages/cmake.py:

    from spack import *
    class Cmake(Package):
        homepage  = 'https://www.cmake.org'
        url       = 'http://www.cmake.org/files/v2.8/cmake-2.8.10.2.tar.gz'
        md5       = '097278785da7182ec0aea8769d06860c'

        def install(self, prefix):
            configure('--prefix=%s'   % prefix,
                      '--parallel=%s' % make_jobs)
            make()
            make('install')

    Naming conventions
    ---------------------
    There are two names you should care about:

    1. The module name, 'cmake'.
       - User will refers to this name, e.g. 'spack install cmake'.
       - Corresponds to the name of the file, 'cmake.py', and it can
         include _, -, and numbers (it can even start with a number).

    2. The class name, "Cmake".  This is formed by converting -'s or _'s
       in the module name to camel case.  If the name starts with a number,
       we prefix the class name with 'Num_'. Examples:

         Module Name       Class Name
          foo_bar           FooBar
          docbook-xml       DocbookXml
          FooBar            Foobar
          3proxy            Num_3proxy

        The class name is what spack looks for when it loads a package module.

    Required Attributes
    ---------------------
    Aside from proper naming, here is the bare minimum set of things you
    need when you make a package:
        homepage   informational URL, so that users know what they're
                   installing.

        url        URL of the source archive that spack will fetch.

        md5        md5 hash of the source archive, so that we can
                   verify that it was downloaded securely and correctly.

        install()  This function tells spack how to build and install the
                   software it downloaded.

    Optional Attributes
    ---------------------
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

    Creating Packages
    ===================
    As a package creator, you can probably ignore most of the preceding
    information, because you can use the 'spack create' command to do it
    all automatically.

    You as the package creator generally only have to worry about writing
    your install function and specifying dependencies.

    spack create
    ----------------
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

    Dependencies
    ---------------
    If your package requires another in order to build, you can specify that
    like this:

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


    The Install Function
    ----------------------
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


    Parallel Builds
    -------------------
    By default, Spack will run make in parallel when you run make() in your
    install function.  Spack figures out how many cores are available on
    your system and runs make with -j<cores>.  If you do not want this behavior,
    you can explicitly mark a package not to use parallel make:

    class SomePackage(Package):
        ...
        parallel = False
        ...

    This changes thd default behavior so that make is sequential.  If you still
    want to build some parts in parallel, you can do this in your install function:

        make(parallel=True)

    Likewise, if you do not supply parallel = True in your Package, you can keep
    the default parallel behavior and run make like this when you want a
    sequential build:

        make(parallel=False)

    Package Lifecycle
    ==================
    This section is really only for developers of new spack commands.

    A package's lifecycle over a run of Spack looks something like this:

        p = Package()             # Done for you by spack

        p.do_fetch()              # called by spack commands in spack/cmd.
        p.do_stage()              # see spack.stage.Stage docs.
        p.do_install()            # calls package's install() function
        p.do_uninstall()

    There are also some other commands that clean the build area:
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
    # These variables are per-package metadata will be defined by subclasses.
    #
    """By default a package has no dependencies."""
    dependencies = {}

    """List of specs of virtual packages provided by this package."""
    provided = {}

    """List of specs of conflicting packages.
       TODO: implement conflicts.
    """
    conflicted = {}

    #
    # These are default values for instance variables.
    #
    """By default we build in parallel.  Subclasses can override this."""
    parallel = True

    """Remove tarball and build by default.  If this is true, leave them."""
    dirty = False

    """Controls whether install and uninstall check deps before running."""
    ignore_dependencies = False

    def __init__(self, spec):
        # These attributes are required for all packages.
        attr_required(self, 'homepage')
        attr_required(self, 'url')
        attr_required(self, 'md5')

        # this determines how the package should be built.
        self.spec = spec

        # Name of package is the name of its module (the file that contains it)
        self.name = inspect.getmodulename(self.module.__file__)

        # Don't allow the default homepage.
        if re.search(r'example.com', self.homepage):
            tty.die("Bad homepage in %s: %s" % (self.name, self.homepage))

        # Make sure URL is an allowed type
        validate.url(self.url)

        # Set up version
        if not hasattr(self, 'version'):
            try:
                self.version = url.parse_version(self.url)
            except UndetectableVersionError:
                tty.die("Couldn't extract a default version from %s. You " +
                        "must specify it explicitly in the package." % self.url)
        elif type(self.version) == string:
            self.version = Version(self.version)

        # Empty at first; only compute dependent packages if necessary
        self._dependents = None

        # This is set by scraping a web page.
        self._available_versions = None

        # This list overrides available_versions if set by the user.
        attr_setdefault(self, 'versions', None)
        if self.versions and type(self.versions) != VersionList:
            self.versions = VersionList(self.versions)

        # stage used to build this package.
        self.stage = Stage("%s-%s" % (self.name, self.version), self.url)

        # Set a default list URL (place to find available versions)
        if not hasattr(self, 'list_url'):
            self.list_url = os.path.dirname(self.url)

        if not hasattr(self, 'list_depth'):
            self.list_depth = 1


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

        # Useful directories within the prefix
        m.prefix  = self.prefix
        m.bin     = new_path(self.prefix, 'bin')
        m.sbin    = new_path(self.prefix, 'sbin')
        m.etc     = new_path(self.prefix, 'etc')
        m.include = new_path(self.prefix, 'include')
        m.lib     = new_path(self.prefix, 'lib')
        m.lib64   = new_path(self.prefix, 'lib64')
        m.libexec = new_path(self.prefix, 'libexec')
        m.share   = new_path(self.prefix, 'share')
        m.doc     = new_path(m.share, 'doc')
        m.info    = new_path(m.share, 'info')
        m.man     = new_path(m.share, 'man')
        m.man1    = new_path(m.man, 'man1')
        m.man2    = new_path(m.man, 'man2')
        m.man3    = new_path(m.man, 'man3')
        m.man4    = new_path(m.man, 'man4')
        m.man5    = new_path(m.man, 'man5')
        m.man6    = new_path(m.man, 'man6')
        m.man7    = new_path(m.man, 'man7')
        m.man8    = new_path(m.man, 'man8')

    @property
    def dependents(self):
        """List of names of packages that depend on this one."""
        if self._dependents is None:
            packages.compute_dependents()
        return tuple(self._dependents)


    def preorder_traversal(self, visited=None):
        if visited is None:
            visited = set()

        if self.name in visited:
            return
        visited.add(self.name)

        yield self
        for name in sorted(self.dependencies.keys()):
            spec = self.dependencies[name]
            for pkg in packages.get(name).preorder_traversal(visited):
                yield pkg


    def validate_dependencies(self):
        """Ensure that this package and its dependencies all have consistent
           constraints on them.
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


    @property
    @memoized
    def all_dependencies(self):
        """Dict(str -> Package) of all transitive dependencies of this package."""
        all_deps = {name : dep for dep in self.preorder_traversal}
        del all_deps[self.name]
        return all_deps


    @property
    def installed(self):
        return os.path.exists(self.prefix)


    @property
    def installed_dependents(self):
        installed = [d for d in self.dependents if packages.get(d).installed]
        all_deps = []
        for d in installed:
            all_deps.append(d)
            all_deps.extend(packages.get(d).installed_dependents)
        return tuple(all_deps)


    @property
    def all_dependents(self):
        all_deps = list(self.dependents)
        for pkg in self.dependents:
            all_deps.extend(packages.get(pkg).all_dependents)
        return tuple(all_deps)


    @property
    def prefix(self):
        """Get the prefix into which this package should be installed."""
        return spack.install_layout.path_for_spec(self.spec)


    def url_version(self, version):
        """Given a version, this returns a string that should be substituted into the
           package's URL to download that version.
           By default, this just returns the version string. Subclasses may need to
           override this, e.g. for boost versions where you need to ensure that there
           are _'s in the download URL.
        """
        return str(version)


    def url_for_version(self, version):
        """Gives a URL that you can download a new version of this package from."""
        return url.substitute_version(self.url, self.url_version(version))


    def remove_prefix(self):
        """Removes the prefix for a package along with any empty parent directories."""
        if self.dirty:
            return
        spack.install_layout.remove_path_for_spec(self.spec)


    def do_fetch(self):
        """Creates a stage directory and downloads the taball for this package.
           Working directory will be set to the stage directory.
        """
        stage = self.stage
        stage.setup()
        stage.fetch()

        archive_md5 = md5(stage.archive_file)
        if archive_md5 != self.md5:
            tty.die("MD5 Checksum failed for %s.  Expected %s but got %s."
                    % (self.name, self.md5, archive_md5))


    def do_stage(self):
        """Unpacks the fetched tarball, then changes into the expanded tarball directory."""
        self.do_fetch()
        stage = self.stage

        archive_dir = stage.expanded_archive_path
        if not archive_dir:
            tty.msg("Staging archive: %s" % stage.archive_file)
            stage.expand_archive()
        else:
            tty.msg("Already staged %s" % self.name)
        stage.chdir_to_archive()


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

        self.do_stage()
        self.setup_install_environment()

        # Add convenience commands to the package's module scope to
        # make building easier.
        self.add_commands_to_module()

        tty.msg("Building %s." % self.name)
        try:
            self.install(self.prefix)
            if not os.path.isdir(self.prefix):
                tty.die("Install failed for %s.  No install dir created." % self.name)

        except subprocess.CalledProcessError, e:
            self.remove_prefix()
            tty.die("Install failed for %s" % self.name, e.message)

        except KeyboardInterrupt, e:
            self.remove_prefix()
            raise

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
        path_set(SPACK_DEPENDENCIES,
                 [dep.package.prefix for dep in self.dependencies.values()])

        # Install location
        os.environ[SPACK_PREFIX] = self.prefix

        # Build root for logging.
        os.environ[SPACK_BUILD_ROOT] = self.stage.expanded_archive_path


    def do_install_dependencies(self):
        # Pass along paths of dependencies here
        for dep in self.dependencies.values():
            dep.package.do_install()


    @property
    def module(self):
        """Use this to add variables to the class's module's scope.
           This lets us use custom syntax in the install method.
        """
        return __import__(self.__class__.__module__,
                          fromlist=[self.__class__.__name__])


    def install(self, prefix):
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
            self._available_versions = VersionList()
            url_regex = os.path.basename(url.wildcard_version(self.url))
            wildcard = self.version.wildcard()

            page_map = get_pages(self.list_url, depth=self.list_depth)
            for site, page in page_map.iteritems():
                strings = re.findall(url_regex, page)

                for s in strings:
                    match = re.search(wildcard, s)
                    if match:
                        v = match.group(0)
                        self._available_versions.add(Version(v))

            if not self._available_versions:
                tty.warn("Found no versions for %s" % self.name,
                         "Check the list_url and list_depth attribute on the "
                         + self.name + " package.",
                         "Use them to tell Spack where to look for versions.")

        return self._available_versions


    @property
    def available_versions(self):
        # If the package overrode available_versions, then use that.
        if self.versions is not None:
            return self.versions
        else:
            vlist = self.fetch_available_versions()
            if not vlist:
                vlist = ver([self.version])
            return vlist


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
