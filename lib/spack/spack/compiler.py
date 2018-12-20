# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os
import re
import itertools

import llnl.util.lang
import llnl.util.tty as tty

import spack.error
import spack.spec
import spack.architecture
import spack.util.executable

__all__ = ['Compiler']


def _verify_executables(*paths):
    for path in paths:
        if not os.path.isfile(path) and os.access(path, os.X_OK):
            raise CompilerAccessError(path)


@llnl.util.lang.memoized
def get_compiler_version_output(compiler_path, version_arg):
    """Invokes the compiler at a given path passing a single
    version argument and returns the output.

    Args:
        compiler_path (path): path of the compiler to be invoked
        version_arg (str): the argument used to extract version information
    """
    compiler = Executable(compiler_path)
    output = compiler(version_arg, output=str, error=str)
    return output


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

    #: Compiler argument that produces version information
    version_argument = '-dumpversion'

    #: Regex used to extract version from compiler's output
    version_regex = '(.*)'

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

    # This property should be overridden in the compiler subclass if
    # C99 is supported by that compiler
    @property
    def c99_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self,
                                      "the C99 standard",
                                      "c99_flag")

    # This property should be overridden in the compiler subclass if
    # C11 is supported by that compiler
    @property
    def c11_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self,
                                      "the C11 standard",
                                      "c11_flag")

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
        output = get_compiler_version_output(cc, cls.version_argument)
        return cls.extract_version_from_output(output)

    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        """Extracts the version from compiler's output."""
        match = re.search(cls.version_regex, output)
        return match.group(1) if match else 'unknown'

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
    def search_compiler_commands(cls, *search_paths):
        """Returns a list of commands that, when invoked, search for compilers
        in the paths supplied.

        Args:
            *search_paths (list of paths): paths where to look for a
                compiler

        Returns:
            Dictionary with compilers grouped by (version, prefix, suffix)
            tuples.
        """
        def is_accessible_dir(x):
            """Returns True if the argument is an accessible directory."""
            return os.path.isdir(x) and os.access(x, os.R_OK | os.X_OK)

        # Select accessible directories
        search_directories = filter(is_accessible_dir, search_paths)

        search_args = []
        for language in ('cc', 'cxx', 'f77', 'fc'):

            # Get compiler names and the callback to detect their versions
            compiler_names = getattr(cls, '{0}_names'.format(language))
            detect_version = getattr(cls, '{0}_version'.format(language))

            # Compile all the regular expressions used for files beforehand.
            # This searches for any combination of <prefix><name><suffix>
            # defined for the compiler
            prefixes = [''] + cls.prefixes
            suffixes = [''] + cls.suffixes
            regexp_fmt = r'^({0}){1}({2})$'
            search_regexps = [
                re.compile(regexp_fmt.format(prefix, re.escape(name), suffix))
                for prefix, name, suffix in
                itertools.product(prefixes, compiler_names, suffixes)
            ]

            # Select only the files matching a regexp
            for d in search_directories:
                # Only select actual files, use the full path
                files = filter(
                    os.path.isfile, [os.path.join(d, f) for f in os.listdir(d)]
                )
                for full_path in files:
                    file = os.path.basename(full_path)
                    for regexp in search_regexps:
                        match = regexp.match(file)
                        if match:
                            key = (detect_version, full_path, cls, language) \
                                + tuple(match.groups())
                            search_args.append(key)

        commands = [detect_version_command(*args) for args in search_args]
        return commands

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


CompilerKey = collections.namedtuple('CompilerKey', [
    'os', 'cmp_cls', 'language', 'version', 'prefix', 'suffix'
])


def detect_version_command(callback, path, cmp_cls, lang, prefix, suffix):
    """Returns a command that, when invoked, searches for a compiler and
    detects its version.

    Args:
        callback (callable): function that given the full path to search
            returns a tuple of (CompilerKey, full path) or None
        path (path): absolute path to search
        cmp_cls (Compiler): compiler class for this specific compiler
        lang (str): language of the compiler
        prefix (str): prefix of the compiler name
        suffix (str): suffix of the compiler name

    Returns:
        Callable to be invoked.
    """
    def _detect_version():
        try:
            version = callback(path)
            if (not version) or (not str(version).strip()):
                tty.debug(
                    "Couldn't get version for compiler %s" % path)
                return None
            return CompilerKey(
                None, cmp_cls, lang, version, prefix, suffix
            ), path
        except spack.util.executable.ProcessError as e:
            tty.debug(
                "Couldn't get version for compiler %s" % path, e)
            return None
        except Exception as e:
            # Catching "Exception" here is fine because it just
            # means something went wrong running a candidate executable.
            tty.debug("Error while executing candidate compiler %s"
                      % path,
                      "%s: %s" % (e.__class__.__name__, e))
            return None
    return _detect_version


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
