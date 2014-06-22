"""
This module contains all routines related to setting up the package
build environment.  All of this is set up by package.py just before
install() is called.

There are two parts to the bulid environment:

1. Python build environment (i.e. install() method)

   This is how things are set up when install() is called.  Spack
   takes advantage of each package being in its own module by adding a
   bunch of command-like functions (like configure(), make(), etc.) in
   the package's module scope.  Ths allows package writers to call
   them all directly in Package.install() without writing 'self.'
   everywhere.  No, this isn't Pythonic.  Yes, it makes the code more
   readable and more like the shell script from whcih someone is
   likely porting.

2. Build execution environment

   This is the set of environment variables, like PATH, CC, CXX,
   etc. that control the build.  There are also a number of
   environment variables used to pass information (like RPATHs and
   other information about dependencies) to Spack's compiler wrappers.
   All of these env vars are also set up here.

Skimming this module is a nice way to get acquainted with the types of
calls you can make from within the install() function.
"""
import os
import shutil
import multiprocessing
import platform
from llnl.util.filesystem import *

import spack
import spack.compilers as compilers
from spack.util.executable import Executable, which
from spack.util.environment import *

#
# This can be set by the user to globally disable parallel builds.
#
SPACK_NO_PARALLEL_MAKE = 'SPACK_NO_PARALLEL_MAKE'

#
# These environment variables are set by
# set_build_environment_variables and used to pass parameters to
# Spack's compiler wrappers.
#
SPACK_LIB              = 'SPACK_LIB'
SPACK_ENV_PATH         = 'SPACK_ENV_PATH'
SPACK_DEPENDENCIES     = 'SPACK_DEPENDENCIES'
SPACK_PREFIX           = 'SPACK_PREFIX'
SPACK_DEBUG            = 'SPACK_DEBUG'
SPACK_SPEC             = 'SPACK_SPEC'
SPACK_DEBUG_LOG_DIR    = 'SPACK_DEBUG_LOG_DIR'


class MakeExecutable(Executable):
    """Special callable executable object for make so the user can
       specify parallel or not on a per-invocation basis.  Using
       'parallel' as a kwarg will override whatever the package's
       global setting is, so you can either default to true or false
       and override particular calls.

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


def set_compiler_environment_variables(pkg):
    assert(pkg.spec.concrete)
    compiler = compilers.compiler_for_spec(pkg.spec.compiler)

    # Set compiler variables used by CMake and autotools
    os.environ['CC']  = 'cc'
    os.environ['CXX'] = 'c++'
    os.environ['F77'] = 'f77'
    os.environ['FC']  = 'fc'

    # Set SPACK compiler variables so that our wrapper knows what to call
    if compiler.cc:
        os.environ['SPACK_CC']  = compiler.cc
    if compiler.cxx:
        os.environ['SPACK_CXX'] = compiler.cxx
    if compiler.f77:
        os.environ['SPACK_F77'] = compiler.f77
    if compiler.fc:
        os.environ['SPACK_FC']  = compiler.fc

    os.environ['SPACK_COMPILER_SPEC']  = str(pkg.spec.compiler)


def set_build_environment_variables(pkg):
    """This ensures a clean install environment when we build packages.
    """
    # This tells the compiler script where to find the Spack installation.
    os.environ[SPACK_LIB] = spack.lib_path

    # Add spack build environment path with compiler wrappers first in
    # the path.  We handle case sensitivity conflicts like "CC" and
    # "cc" by putting one in the <build_env_path>/case-insensitive
    # directory.  Add that to the path too.
    env_paths = [spack.build_env_path,
                 join_path(spack.build_env_path, 'case-insensitive')]
    path_put_first("PATH", env_paths)
    path_set(SPACK_ENV_PATH, env_paths)

    # Prefixes of all of the package's dependencies go in
    # SPACK_DEPENDENCIES
    dep_prefixes = [d.package.prefix for d in pkg.spec.dependencies.values()]
    path_set(SPACK_DEPENDENCIES, dep_prefixes)

    # Install prefix
    os.environ[SPACK_PREFIX] = pkg.prefix

    # Remove these vars from the environment during build becaus they
    # can affect how some packages find libraries.  We want to make
    # sure that builds never pull in unintended external dependencies.
    pop_keys(os.environ, "LD_LIBRARY_PATH", "LD_RUN_PATH", "DYLD_LIBRARY_PATH")

    # Add bin directories from dependencies to the PATH for the build.
    bin_dirs = ['%s/bin' % prefix for prefix in dep_prefixes]
    path_put_first('PATH', [bin for bin in bin_dirs if os.path.isdir(bin)])

    # Working directory for the spack command itself, for debug logs.
    if spack.debug:
        os.environ[SPACK_DEBUG] = "TRUE"
    os.environ[SPACK_SPEC] = str(pkg.spec)
    os.environ[SPACK_DEBUG_LOG_DIR] = spack.spack_working_dir


def set_module_variables_for_package(pkg):
    """Populate the module scope of install() with some useful functions.
       This makes things easier for package writers.
    """
    m = pkg.module

    m.make  = MakeExecutable('make', pkg.parallel)
    m.gmake = MakeExecutable('gmake', pkg.parallel)

    # number of jobs spack prefers to build with.
    m.make_jobs = multiprocessing.cpu_count()

    # Find the configure script in the archive path
    # Don't use which for this; we want to find it in the current dir.
    m.configure = Executable('./configure')

    # TODO: shouldn't really use "which" here.  Consider adding notion
    # TODO: of build dependencies, as opposed to link dependencies.
    # TODO: Currently, everything is a link dependency, but tools like
    # TODO: this shouldn't be.
    m.cmake = which("cmake")

    # standard CMake arguments
    m.std_cmake_args = ['-DCMAKE_INSTALL_PREFIX=%s' % pkg.prefix,
                        '-DCMAKE_BUILD_TYPE=None']
    if platform.mac_ver()[0]:
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
    m.prefix  = pkg.prefix
