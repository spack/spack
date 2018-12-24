# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os
import re
import itertools

import platform as py_platform

import llnl.util.lang
import llnl.util.multiproc
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
    def search_compiler_commands(cls, operating_system, *search_paths):
        """Returns a list of commands that, when invoked, search for compilers
        in the paths supplied.

        Args:
            operating_system (OperatingSystem): the OS requesting the search
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
        search_directories = list(filter(is_accessible_dir, search_paths))

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
                            key = (detect_version, full_path, operating_system,
                                   cls, language) + tuple(match.groups())
                            search_args.append(key)

        # The 'successful' list is ordered like the input paths.
        # Reverse it here so that the dict creation (last insert wins)
        # does not spoil the intended precedence.
        return [detect_version_command(*args)
                for args in reversed(search_args)]

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


@llnl.util.multiproc.deferred
def detect_version_command(
        callback, path, operating_system, cmp_cls, lang, prefix, suffix
):
    """Search for a compiler and eventually detect its version.

    Args:
        callback (callable): function that given the full path to search
            returns a tuple of (CompilerKey, full path) or None
        path (path): absolute path to search
        operating_system (OperatingSystem): the OS for which we are
            looking for a compiler
        cmp_cls (Compiler): compiler class for this specific compiler
        lang (str): language of the compiler
        prefix (str): prefix of the compiler name
        suffix (str): suffix of the compiler name

    Returns:
        A (CompilerKey, path) tuple if anything is found, else None
    """
    try:
        version = callback(path)
        if (not version) or (not str(version).strip()):
            tty.debug(
                "Couldn't get version for compiler %s" % path)
            return None
        return CompilerKey(
            operating_system, cmp_cls, lang, version, prefix, suffix
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


def _discard_invalid(compilers):
    """Removes invalid compilers from the list"""
    # Remove search with no results
    compilers = filter(None, compilers)

    # Skip compilers with unknown version
    def has_known_version(compiler_entry):
        """Returns True if the key has not an unknown version."""
        compiler_key, _ = compiler_entry
        return compiler_key.version != 'unknown'

    return filter(has_known_version, compilers)


def make_compiler_list(compilers):
    compilers = _discard_invalid(compilers)

    # Group by (os, compiler type, version), (prefix, suffix), language
    def sort_key_fn(item):
        key, _ = item
        return (key.os, str(key.cmp_cls), key.version), \
               (key.prefix, key.suffix), key.language

    compilers_s = sorted(compilers, key=sort_key_fn)
    # This dictionary is needed because a class (NOT an instance of it)
    # doesn't have __lt__ or other similar functions defined. Therefore
    # we sort on its string representation and need to maintain the map
    # to the class here
    cmp_cls_d = {str(key.cmp_cls): key.cmp_cls for key, _ in compilers_s}

    compilers_d = {}
    for sort_key, group in itertools.groupby(compilers_s, sort_key_fn):
        compiler_entry, ps, language = sort_key
        by_compiler_entry = compilers_d.setdefault(compiler_entry, {})
        by_ps = by_compiler_entry.setdefault(ps, {})
        by_ps[language] = list(x[1] for x in group).pop()

    # For each (os, compiler type, version) select the compiler
    # with most entries and add it to a list
    compilers = []
    for compiler_entry, by_compiler_entry in compilers_d.items():
        # Select the (prefix, suffix) match with most entries
        max_lang, max_ps = max(
            (len(by_compiler_entry[ps]), ps) for ps in by_compiler_entry
        )

        # Add it to the list of compilers
        operating_system, cmp_cls_key, version = compiler_entry
        cmp_cls = cmp_cls_d[cmp_cls_key]
        spec = spack.spec.CompilerSpec(cmp_cls.name, version)
        paths = [by_compiler_entry[max_ps].get(language, None)
                 for language in ('cc', 'cxx', 'f77', 'fc')]
        compilers.append(
            cmp_cls(spec, operating_system, py_platform.machine(), paths)
        )

    return compilers


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
