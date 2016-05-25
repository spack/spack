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
"""
This module contains all routines related to setting up the package
build environment.  All of this is set up by package.py just before
install() is called.

There are two parts to the build environment:

1. Python build environment (i.e. install() method)

   This is how things are set up when install() is called.  Spack
   takes advantage of each package being in its own module by adding a
   bunch of command-like functions (like configure(), make(), etc.) in
   the package's module scope.  Ths allows package writers to call
   them all directly in Package.install() without writing 'self.'
   everywhere.  No, this isn't Pythonic.  Yes, it makes the code more
   readable and more like the shell script from which someone is
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
import sys
import shutil
import multiprocessing
import platform

import llnl.util.tty as tty
from llnl.util.filesystem import *

import spack
from spack.environment import EnvironmentModifications, validate
from spack.util.environment import *
from spack.util.executable import Executable, which

#
# This can be set by the user to globally disable parallel builds.
#
SPACK_NO_PARALLEL_MAKE = 'SPACK_NO_PARALLEL_MAKE'

#
# These environment variables are set by
# set_build_environment_variables and used to pass parameters to
# Spack's compiler wrappers.
#
SPACK_ENV_PATH         = 'SPACK_ENV_PATH'
SPACK_DEPENDENCIES     = 'SPACK_DEPENDENCIES'
SPACK_PREFIX           = 'SPACK_PREFIX'
SPACK_INSTALL          = 'SPACK_INSTALL'
SPACK_DEBUG            = 'SPACK_DEBUG'
SPACK_SHORT_SPEC       = 'SPACK_SHORT_SPEC'
SPACK_DEBUG_LOG_DIR    = 'SPACK_DEBUG_LOG_DIR'


# Platform-specific library suffix.
dso_suffix = 'dylib' if sys.platform == 'darwin' else 'so'



class MakeExecutable(Executable):
    """Special callable executable object for make so the user can
       specify parallel or not on a per-invocation basis.  Using
       'parallel' as a kwarg will override whatever the package's
       global setting is, so you can either default to true or false
       and override particular calls.

       Note that if the SPACK_NO_PARALLEL_MAKE env var is set it overrides
       everything.
    """
    def __init__(self, name, jobs):
        super(MakeExecutable, self).__init__(name)
        self.jobs = jobs

    def __call__(self, *args, **kwargs):
        disable = env_flag(SPACK_NO_PARALLEL_MAKE)
        parallel = not disable and kwargs.get('parallel', self.jobs > 1)

        if parallel:
            jobs = "-j%d" % self.jobs
            args = (jobs,) + args

        return super(MakeExecutable, self).__call__(*args, **kwargs)


def set_compiler_environment_variables(pkg, env):
    assert pkg.spec.concrete
    compiler = pkg.compiler
    flags = pkg.spec.compiler_flags

    # Set compiler variables used by CMake and autotools
    assert all(key in compiler.link_paths for key in ('cc', 'cxx', 'f77', 'fc'))

    # Populate an object with the list of environment modifications
    # and return it
    # TODO : add additional kwargs for better diagnostics, like requestor, ttyout, ttyerr, etc.
    link_dir = spack.build_env_path
    env.set('CC',  join_path(link_dir, compiler.link_paths['cc']))
    env.set('CXX', join_path(link_dir, compiler.link_paths['cxx']))
    env.set('F77', join_path(link_dir, compiler.link_paths['f77']))
    env.set('FC',  join_path(link_dir, compiler.link_paths['fc']))

    # Set SPACK compiler variables so that our wrapper knows what to call
    if compiler.cc:
        env.set('SPACK_CC', compiler.cc)
    if compiler.cxx:
        env.set('SPACK_CXX', compiler.cxx)
    if compiler.f77:
        env.set('SPACK_F77', compiler.f77)
    if compiler.fc:
        env.set('SPACK_FC',  compiler.fc)

    # Set SPACK compiler rpath flags so that our wrapper knows what to use
    env.set('SPACK_CC_RPATH_ARG',  compiler.cc_rpath_arg)
    env.set('SPACK_CXX_RPATH_ARG', compiler.cxx_rpath_arg)
    env.set('SPACK_F77_RPATH_ARG', compiler.f77_rpath_arg)
    env.set('SPACK_FC_RPATH_ARG',  compiler.fc_rpath_arg)

    # Add every valid compiler flag to the environment, prefixed with "SPACK_"
    for flag in spack.spec.FlagMap.valid_compiler_flags():
        # Concreteness guarantees key safety here
        if flags[flag] != []:
            env.set('SPACK_' + flag.upper(), ' '.join(f for f in flags[flag]))

    env.set('SPACK_COMPILER_SPEC', str(pkg.spec.compiler))
    return env


def set_build_environment_variables(pkg, env):
    """
    This ensures a clean install environment when we build packages
    """
    # Add spack build environment path with compiler wrappers first in
    # the path. We add both spack.env_path, which includes default
    # wrappers (cc, c++, f77, f90), AND a subdirectory containing
    # compiler-specific symlinks.  The latter ensures that builds that
    # are sensitive to the *name* of the compiler see the right name
    # when we're building with the wrappers.
    #
    # Conflicts on case-insensitive systems (like "CC" and "cc") are
    # handled by putting one in the <build_env_path>/case-insensitive
    # directory.  Add that to the path too.
    env_paths = []
    for item in [spack.build_env_path, join_path(spack.build_env_path, pkg.compiler.name)]:
        env_paths.append(item)
        ci = join_path(item, 'case-insensitive')
        if os.path.isdir(ci):
            env_paths.append(ci)

    for item in reversed(env_paths):
        env.prepend_path('PATH', item)
    env.set_path(SPACK_ENV_PATH, env_paths)

    # Prefixes of all of the package's dependencies go in SPACK_DEPENDENCIES
    dep_prefixes = [d.prefix for d in pkg.spec.traverse(root=False)]
    env.set_path(SPACK_DEPENDENCIES, dep_prefixes)
    env.set_path('CMAKE_PREFIX_PATH', dep_prefixes)  # Add dependencies to CMAKE_PREFIX_PATH

    # Install prefix
    env.set(SPACK_PREFIX, pkg.prefix)

    # Install root prefix
    env.set(SPACK_INSTALL, spack.install_path)

    # Remove these vars from the environment during build because they
    # can affect how some packages find libraries.  We want to make
    # sure that builds never pull in unintended external dependencies.
    env.unset('LD_LIBRARY_PATH')
    env.unset('LD_RUN_PATH')
    env.unset('DYLD_LIBRARY_PATH')

    # Add bin directories from dependencies to the PATH for the build.
    bin_dirs = reversed(filter(os.path.isdir, ['%s/bin' % prefix for prefix in dep_prefixes]))
    for item in bin_dirs:
        env.prepend_path('PATH', item)

    # Working directory for the spack command itself, for debug logs.
    if spack.debug:
        env.set(SPACK_DEBUG, 'TRUE')
    env.set(SPACK_SHORT_SPEC, pkg.spec.short_spec)
    env.set(SPACK_DEBUG_LOG_DIR, spack.spack_working_dir)

    # Add any pkgconfig directories to PKG_CONFIG_PATH
    pkg_config_dirs = []
    for p in dep_prefixes:
        for maybe in ('lib', 'lib64', 'share'):
            pcdir = join_path(p, maybe, 'pkgconfig')
            if os.path.isdir(pcdir):
                pkg_config_dirs.append(pcdir)
    env.set_path('PKG_CONFIG_PATH', pkg_config_dirs)

    return env


def set_module_variables_for_package(pkg, module):
    """Populate the module scope of install() with some useful functions.
       This makes things easier for package writers.
    """
    # number of jobs spack will to build with.
    jobs = multiprocessing.cpu_count()
    if not pkg.parallel:
        jobs = 1
    elif pkg.make_jobs:
        jobs = pkg.make_jobs

    m = module
    m.make_jobs = jobs

    # TODO: make these build deps that can be installed if not found.
    m.make  = MakeExecutable('make', jobs)
    m.gmake = MakeExecutable('gmake', jobs)

    # easy shortcut to os.environ
    m.env = os.environ

    # Find the configure script in the archive path
    # Don't use which for this; we want to find it in the current dir.
    m.configure = Executable('./configure')

    # TODO: shouldn't really use "which" here.  Consider adding notion
    # TODO: of build dependencies, as opposed to link dependencies.
    # TODO: Currently, everything is a link dependency, but tools like
    # TODO: this shouldn't be.
    m.cmake = Executable('cmake')

    # standard CMake arguments
    m.std_cmake_args = ['-DCMAKE_INSTALL_PREFIX=%s' % pkg.prefix,
                        '-DCMAKE_BUILD_TYPE=RelWithDebInfo']
    if platform.mac_ver()[0]:
        m.std_cmake_args.append('-DCMAKE_FIND_FRAMEWORK=LAST')

    # Set up CMake rpath
    m.std_cmake_args.append('-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE')
    m.std_cmake_args.append('-DCMAKE_INSTALL_RPATH=%s' % ":".join(get_rpaths(pkg)))

    # Put spack compiler paths in module scope.
    link_dir = spack.build_env_path
    m.spack_cc  = join_path(link_dir, pkg.compiler.link_paths['cc'])
    m.spack_cxx = join_path(link_dir, pkg.compiler.link_paths['cxx'])
    m.spack_f77 = join_path(link_dir, pkg.compiler.link_paths['f77'])
    m.spack_fc  = join_path(link_dir, pkg.compiler.link_paths['fc'])

    # Emulate some shell commands for convenience
    m.pwd          = os.getcwd
    m.cd           = os.chdir
    m.mkdir        = os.mkdir
    m.makedirs     = os.makedirs
    m.remove       = os.remove
    m.removedirs   = os.removedirs
    m.symlink      = os.symlink

    m.mkdirp       = mkdirp
    m.install      = install
    m.install_tree = install_tree
    m.rmtree       = shutil.rmtree
    m.move         = shutil.move

    # Useful directories within the prefix are encapsulated in
    # a Prefix object.
    m.prefix  = pkg.prefix

    # Platform-specific library suffix.
    m.dso_suffix = dso_suffix


def get_rpaths(pkg):
    """Get a list of all the rpaths for a package."""
    rpaths = [pkg.prefix.lib, pkg.prefix.lib64]
    rpaths.extend(d.prefix.lib for d in pkg.spec.dependencies.values()
                  if os.path.isdir(d.prefix.lib))
    rpaths.extend(d.prefix.lib64 for d in pkg.spec.dependencies.values()
                  if os.path.isdir(d.prefix.lib64))
    return rpaths


def parent_class_modules(cls):
    """Get list of super class modules that are all descend from spack.Package"""
    if not issubclass(cls, spack.Package) or issubclass(spack.Package, cls):
        return []
    result = []
    module = sys.modules.get(cls.__module__)
    if module:
        result = [ module ]
    for c in cls.__bases__:
        result.extend(parent_class_modules(c))
    return result


def setup_package(pkg):
    """Execute all environment setup routines."""
    spack_env = EnvironmentModifications()
    run_env   = EnvironmentModifications()

    # Before proceeding, ensure that specs and packages are consistent
    #
    # This is a confusing behavior due to how packages are
    # constructed.  `setup_dependent_package` may set attributes on
    # specs in the DAG for use by other packages' install
    # method. However, spec.package will look up a package via
    # spack.repo, which defensively copies specs into packages.  This
    # code ensures that all packages in the DAG have pieces of the
    # same spec object at build time.
    #
    # This is safe for the build process, b/c the build process is a
    # throwaway environment, but it is kind of dirty.
    #
    # TODO: Think about how to avoid this fix and do something cleaner.
    for s in pkg.spec.traverse(): s.package.spec = s

    set_compiler_environment_variables(pkg, spack_env)
    set_build_environment_variables(pkg, spack_env)

    # traverse in postorder so package can use vars from its dependencies
    spec = pkg.spec
    for dspec in pkg.spec.traverse(order='post', root=False):
        # If a user makes their own package repo, e.g.
        # spack.repos.mystuff.libelf.Libelf, and they inherit from
        # an existing class like spack.repos.original.libelf.Libelf,
        # then set the module variables for both classes so the
        # parent class can still use them if it gets called.
        spkg = dspec.package
        modules = parent_class_modules(spkg.__class__)
        for mod in modules:
            set_module_variables_for_package(spkg, mod)
        set_module_variables_for_package(spkg, spkg.module)

        # Allow dependencies to modify the module
        dpkg = dspec.package
        dpkg.setup_dependent_package(pkg.module, spec)
        dpkg.setup_dependent_environment(spack_env, run_env, spec)

    set_module_variables_for_package(pkg, pkg.module)
    pkg.setup_environment(spack_env, run_env)

    # Make sure nothing's strange about the Spack environment.
    validate(spack_env, tty.warn)
    spack_env.apply_modifications()


def fork(pkg, function):
    """Fork a child process to do part of a spack build.

    Arguments:

    pkg -- pkg whose environemnt we should set up the
           forked process for.
    function -- arg-less function to run in the child process.

    Usage:
       def child_fun():
           # do stuff
       build_env.fork(pkg, child_fun)

    Forked processes are run with the build environment set up by
    spack.build_environment.  This allows package authors to have
    full control over the environment, etc. without affecting
    other builds that might be executed in the same spack call.

    If something goes wrong, the child process is expected to print
    the error and the parent process will exit with error as
    well. If things go well, the child exits and the parent
    carries on.
    """
    try:
        pid = os.fork()
    except OSError as e:
        raise InstallError("Unable to fork build process: %s" % e)

    if pid == 0:
        # Give the child process the package's build environment.
        setup_package(pkg)

        try:
            # call the forked function.
            function()

            # Use os._exit here to avoid raising a SystemExit exception,
            # which interferes with unit tests.
            os._exit(0)

        except spack.error.SpackError as e:
            e.die()

        except:
            # Child doesn't raise or return to main spack code.
            # Just runs default exception handler and exits.
            sys.excepthook(*sys.exc_info())
            os._exit(1)

    else:
        # Parent process just waits for the child to complete.  If the
        # child exited badly, assume it already printed an appropriate
        # message.  Just make the parent exit with an error code.
        pid, returncode = os.waitpid(pid, 0)
        if returncode != 0:
            raise InstallError("Installation process had nonzero exit code.".format(str(returncode)))


class InstallError(spack.error.SpackError):
    """Raised when a package fails to install"""
