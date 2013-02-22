import inspect
import os
import re
import subprocess
import platform
import shutil

from spack import *
import packages
import tty
import attr
import validate
import version
import arch
from stage import Stage


DEPENDS_ON = "depends_on"

class Dependency(object):
    """Represents a dependency from one package to another."""
    def __init__(self, name, **kwargs):
        self.name = name
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @property
    def package(self):
        return packages.get(self.name)

    def __repr__(self):
        return "<dep: %s>" % self.name

    def __str__(self):
        return self.__repr__()


def depends_on(*args, **kwargs):
    """Adds a depends_on local variable in the locals of
       the calling class, based on args.
    """
    stack = inspect.stack()
    try:
        locals = stack[1][0].f_locals
    finally:
        del stack

        dependencies = locals.setdefault("dependencies", [])
    for name in args:
        dependencies.append(Dependency(name))


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


class Package(object):
    def __init__(self, arch=arch.sys_type()):
        attr.required(self, 'homepage')
        attr.required(self, 'url')
        attr.required(self, 'md5')

        attr.setdefault(self, 'dependencies', [])
        attr.setdefault(self, 'parallel', True)

        # Architecture for this package.
        self.arch = arch

        # Name of package is the name of its module (the file that contains it)
        self.name = inspect.getmodulename(self.module.__file__)

        # Don't allow the default homepage.
        if re.search(r'example.com', self.homepage):
            tty.die("Bad homepage in %s: %s" % (self.name, self.homepage))

        # Make sure URL is an allowed type
        validate.url(self.url)

        # Set up version
        attr.setdefault(self, 'version', version.parse_version(self.url))
        if not self.version:
            tty.die("Couldn't extract version from %s. " +
                    "You must specify it explicitly for this URL." % self.url)

        # This adds a bunch of convenient commands to the package's module scope.
        self.add_commands_to_module()

        # Controls whether install and uninstall check deps before acting.
        self.ignore_dependencies = False

        # Empty at first; only compute dependents if necessary
        self._dependents = None

        # Whether to remove intermediate build/install when things go wrong.
        self.dirty = False

        # stage used to build this package.
        self.stage = Stage(self.stage_name, self.url)


    def make_make(self):
        """Create a make command set up with the proper default arguments."""
        make = which('make', required=True)
        return make


    def add_commands_to_module(self):
        """Populate the module scope of install() with some useful functions.
           This makes things easier for package writers.
        """
        self.module.make = MakeExecutable('make', self.parallel)
        self.module.gmake = MakeExecutable('gmake', self.parallel)

        # number of jobs spack prefers to build with.
        self.module.make_jobs = multiprocessing.cpu_count()

        # Find the configure script in the archive path
        # Don't use which for this; we want to find it in the current dir.
        self.module.configure = Executable('./configure')
        self.module.cmake = which("cmake")

        # standard CMake arguments
        self.module.std_cmake_args = [
            '-DCMAKE_INSTALL_PREFIX=%s' % self.prefix,
            '-DCMAKE_BUILD_TYPE=None']
        if platform.mac_ver()[0]:
            self.module.std_cmake_args.append('-DCMAKE_FIND_FRAMEWORK=LAST')

        # Emulate some shell commands for convenience
        self.module.cd         = os.chdir
        self.module.mkdir      = os.mkdir
        self.module.makedirs   = os.makedirs
        self.module.removedirs = os.removedirs

        self.module.mkdirp     = mkdirp
        self.module.install    = install
        self.module.rmtree     = shutil.rmtree
        self.module.move       = shutil.move
        self.module.remove     = os.remove

        # Useful directories within the prefix
        self.module.prefix  = self.prefix
        self.module.bin     = new_path(self.prefix, 'bin')
        self.module.sbin    = new_path(self.prefix, 'sbin')
        self.module.etc     = new_path(self.prefix, 'etc')
        self.module.include = new_path(self.prefix, 'include')
        self.module.lib     = new_path(self.prefix, 'lib')
        self.module.lib64   = new_path(self.prefix, 'lib64')
        self.module.libexec = new_path(self.prefix, 'libexec')
        self.module.share   = new_path(self.prefix, 'share')
        self.module.doc     = new_path(self.module.share, 'doc')
        self.module.info    = new_path(self.module.share, 'info')
        self.module.man     = new_path(self.module.share, 'man')
        self.module.man1    = new_path(self.module.man, 'man1')
        self.module.man2    = new_path(self.module.man, 'man2')
        self.module.man3    = new_path(self.module.man, 'man3')
        self.module.man4    = new_path(self.module.man, 'man4')
        self.module.man5    = new_path(self.module.man, 'man5')
        self.module.man6    = new_path(self.module.man, 'man6')
        self.module.man7    = new_path(self.module.man, 'man7')
        self.module.man8    = new_path(self.module.man, 'man8')


    @property
    def dependents(self):
        """List of names of packages that depend on this one."""
        if self._dependents is None:
            packages.compute_dependents()
        return tuple(self._dependents)


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
    def stage_name(self):
        return "%s-%s" % (self.name, self.version)


    @property
    def platform_path(self):
        """Directory for binaries for the current platform."""
        return new_path(install_path, self.arch)


    @property
    def package_path(self):
        """Directory for different versions of this package.  Lives just above prefix."""
        return new_path(self.platform_path, self.name)


    @property
    def installed_versions(self):
        return [ver for ver in os.listdir(self.package_path)
                if os.path.isdir(new_path(self.package_path, ver))]


    @property
    def prefix(self):
        """Packages are installed in $spack_prefix/opt/<sys_type>/<name>/<version>"""
        return new_path(self.package_path, self.version)


    def remove_prefix(self):
        """Removes the prefix for a package along with any empty parent directories."""
        if os.path.exists(self.prefix):
            shutil.rmtree(self.prefix, True)

        for dir in (self.package_path, self.platform_path):
            if not os.path.isdir(dir):
                continue
            if not os.listdir(dir):
                os.rmdir(dir)
            else:
                break


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
        if os.path.exists(self.prefix):
            tty.msg("%s is already installed." % self.name)
            tty.pkg(self.prefix)
            return

        if not self.ignore_dependencies:
            self.do_install_dependencies()

        self.do_stage()
        self.setup_install_environment()

        tty.msg("Building %s." % self.name)
        try:
            self.install(self.prefix)
            if not os.path.isdir(self.prefix):
                tty.die("Install failed for %s.  No install dir created." % self.name)
        except subprocess.CalledProcessError, e:
            if not self.dirty:
                self.remove_prefix()
            tty.die("Install failed for %s" % self.name, e.message)
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
                 [dep.package.prefix for dep in self.dependencies])

        # Install location
        os.environ[SPACK_PREFIX] = self.prefix

        # Build root for logging.
        os.environ[SPACK_BUILD_ROOT] = self.stage.expanded_archive_path


    def do_install_dependencies(self):
        # Pass along paths of dependencies here
        for dep in self.dependencies:
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
