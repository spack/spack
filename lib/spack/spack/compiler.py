##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import os
import re
import itertools

import llnl.util.tty as tty
import llnl.util.multiproc as mp

import spack.error
import spack.spec
import spack.architecture
from spack.util.executable import Executable, ProcessError
from spack.util.environment import get_path

__all__ = ['Compiler', 'get_compiler_version']


def _verify_executables(*paths):
    for path in paths:
        if not os.path.isfile(path) and os.access(path, os.X_OK):
            raise CompilerAccessError(path)


_version_cache = {}


def get_compiler_version(compiler_path, version_arg, regex='(.*)'):
    key = (compiler_path, version_arg, regex)
    if key not in _version_cache:
        compiler = Executable(compiler_path)
        output = compiler(version_arg, output=str, error=str)

        match = re.search(regex, output)
        _version_cache[key] = match.group(1) if match else 'unknown'

    return _version_cache[key]


def dumpversion(compiler_path):
    """Simple default dumpversion method -- this is what gcc does."""
    return get_compiler_version(compiler_path, '-dumpversion')


def tokenize_flags(flags_str):
    """Given a compiler flag specification as a string, this returns a list
       where the entries are the flags. For compiler options which set values
       using the syntax "-flag value", this function groups flags and their
       values together. Any token not preceded by a "-" is considered the
       value of a prior flag."""
    tokens = flags_str.split()
    if not tokens:
        return []
    flag = tokens[0]
    flags = []
    for token in tokens[1:]:
        if not token.startswith('-'):
            flag += ' ' + token
        else:
            flags.append(flag)
            flag = token
    flags.append(flag)
    return flags


class Compiler(object):
    """This class encapsulates a Spack "compiler", which includes C,
       C++, and Fortran compilers.  Subclasses should implement
       support for specific compilers, their possible names, arguments,
       and how to identify the particular type of compiler."""

    # Subclasses use possible names of C compiler
    cc_names = []

    # Subclasses use possible names of C++ compiler
    cxx_names = []

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = []

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = []

    # Optional prefix regexes for searching for this type of compiler.
    # Prefixes are sometimes used for toolchains, e.g. 'powerpc-bgq-linux-'
    prefixes = []

    # Optional suffix regexes for searching for this type of compiler.
    # Suffixes are used by some frameworks, e.g. macports uses an '-mp-X.Y'
    # version suffix for gcc.
    suffixes = [r'-.*']

    # Default flags used by a compiler to set an rpath
    @property
    def cc_rpath_arg(self):
        return '-Wl,-rpath,'

    @property
    def cxx_rpath_arg(self):
        return '-Wl,-rpath,'

    @property
    def f77_rpath_arg(self):
        return '-Wl,-rpath,'

    @property
    def fc_rpath_arg(self):
        return '-Wl,-rpath,'
    # Cray PrgEnv name that can be used to load this compiler
    PrgEnv = None
    # Name of module used to switch versions of this compiler
    PrgEnv_compiler = None

    def __init__(self, cspec, operating_system, target,
                 paths, modules=[], alias=None, environment=None,
                 extra_rpaths=None, **kwargs):
        self.spec = cspec
        self.operating_system = str(operating_system)
        self.target = target
        self.modules = modules
        self.alias = alias

        def check(exe):
            if exe is None:
                return None
            _verify_executables(exe)
            return exe

        self.cc  = check(paths[0])
        self.cxx = check(paths[1])
        if len(paths) > 2:
            self.f77 = check(paths[2])
            if len(paths) == 3:
                self.fc = self.f77
            else:
                self.fc  = check(paths[3])

        self.environment = environment
        self.extra_rpaths = extra_rpaths or []

        # Unfortunately have to make sure these params are accepted
        # in the same order they are returned by sorted(flags)
        # in compilers/__init__.py
        self.flags = {}
        for flag in spack.spec.FlagMap.valid_compiler_flags():
            value = kwargs.get(flag, None)
            if value is not None:
                self.flags[flag] = tokenize_flags(value)

    @property
    def version(self):
        return self.spec.version

    # This property should be overridden in the compiler subclass if
    # OpenMP is supported by that compiler
    @property
    def openmp_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self, "OpenMP", "openmp_flag")

    # This property should be overridden in the compiler subclass if
    # C++98 is not the default standard for that compiler
    @property
    def cxx98_flag(self):
        return ""

    # This property should be overridden in the compiler subclass if
    # C++11 is supported by that compiler
    @property
    def cxx11_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self,
                                      "the C++11 standard",
                                      "cxx11_flag")

    # This property should be overridden in the compiler subclass if
    # C++14 is supported by that compiler
    @property
    def cxx14_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self,
                                      "the C++14 standard",
                                      "cxx14_flag")

    # This property should be overridden in the compiler subclass if
    # C++17 is supported by that compiler
    @property
    def cxx17_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self,
                                      "the C++17 standard",
                                      "cxx17_flag")

    #
    # Compiler classes have methods for querying the version of
    # specific compiler executables.  This is used when discovering compilers.
    #
    # Compiler *instances* are just data objects, and can only be
    # constructed from an actual set of executables.
    #
    @classmethod
    def default_version(cls, cc):
        """Override just this to override all compiler version functions."""
        return dumpversion(cc)

    @classmethod
    def cc_version(cls, cc):
        return cls.default_version(cc)

    @classmethod
    def cxx_version(cls, cxx):
        return cls.default_version(cxx)

    @classmethod
    def f77_version(cls, f77):
        return cls.default_version(f77)

    @classmethod
    def fc_version(cls, fc):
        return cls.default_version(fc)

    @classmethod
    def _find_matches_in_path(cls, compiler_names, detect_version, *path):
        """Finds compilers in the paths supplied.

           Looks for all combinations of ``compiler_names`` with the
           ``prefixes`` and ``suffixes`` defined for this compiler
           class.  If any compilers match the compiler_names,
           prefixes, or suffixes, uses ``detect_version`` to figure
           out what version the compiler is.

           This returns a dict with compilers grouped by (prefix,
           suffix, version) tuples.  This can be further organized by
           find().
        """
        if not path:
            path = get_path('PATH')

        prefixes = [''] + cls.prefixes
        suffixes = [''] + cls.suffixes

        checks = []
        for directory in path:
            if not (os.path.isdir(directory) and
                    os.access(directory, os.R_OK | os.X_OK)):
                continue

            files = os.listdir(directory)
            for exe in files:
                full_path = os.path.join(directory, exe)

                prod = itertools.product(prefixes, compiler_names, suffixes)
                for pre, name, suf in prod:
                    regex = r'^(%s)%s(%s)$' % (pre, re.escape(name), suf)

                    match = re.match(regex, exe)
                    if match:
                        key = (full_path,) + match.groups() + (detect_version,)
                        checks.append(key)

        successful = [k for k in mp.parmap(_get_versioned_tuple, checks)
                      if k is not None]

        # The 'successful' list is ordered like the input paths.
        # Reverse it here so that the dict creation (last insert wins)
        # does not spoil the intented precedence.
        successful.reverse()
        return dict(((v, p, s), path) for v, p, s, path in successful)

    def setup_custom_environment(self, pkg, env):
        """Set any environment variables necessary to use the compiler."""
        pass

    def __repr__(self):
        """Return a string representation of the compiler toolchain."""
        return self.__str__()

    def __str__(self):
        """Return a string representation of the compiler toolchain."""
        return "%s(%s)" % (
            self.name, '\n     '.join((str(s) for s in (
                self.cc, self.cxx, self.f77, self.fc, self.modules,
                str(self.operating_system)))))


def _get_versioned_tuple(compiler_check_tuple):
    full_path, prefix, suffix, detect_version = compiler_check_tuple
    try:
        version = detect_version(full_path)
        if (not version) or (not str(version).strip()):
            tty.debug(
                "Couldn't get version for compiler %s" % full_path)
            return None
        return (version, prefix, suffix, full_path)
    except ProcessError as e:
        tty.debug(
            "Couldn't get version for compiler %s" % full_path, e)
        return None
    except Exception as e:
        # Catching "Exception" here is fine because it just
        # means something went wrong running a candidate executable.
        tty.debug("Error while executing candidate compiler %s"
                  % full_path,
                  "%s: %s" % (e.__class__.__name__, e))
        return None


class CompilerAccessError(spack.error.SpackError):

    def __init__(self, path):
        super(CompilerAccessError, self).__init__(
            "'%s' is not a valid compiler." % path)


class InvalidCompilerError(spack.error.SpackError):

    def __init__(self):
        super(InvalidCompilerError, self).__init__(
            "Compiler has no executables.")


class UnsupportedCompilerFlag(spack.error.SpackError):

    def __init__(self, compiler, feature, flag_name, ver_string=None):
        super(UnsupportedCompilerFlag, self).__init__(
            "{0} ({1}) does not support {2} (as compiler.{3})."
            .format(compiler.name,
                    ver_string if ver_string else compiler.version,
                    feature,
                    flag_name),
            "If you think it should, please edit the compiler.{0} subclass to"
            .format(compiler.name) +
            " implement the {0} property and submit a pull request or issue."
            .format(flag_name)
        )
