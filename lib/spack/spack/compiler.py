# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os
import re
import itertools

import functools_backport
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
            (tags, commands): ``tags`` is a list of compiler tags, containing
                all the information on a compiler, but version. ``commands``
                is a list of commands that, when executed, will detect the
                version of the corresponding compiler.
        """
        def is_accessible_dir(x):
            """Returns True if the argument is an accessible directory."""
            return os.path.isdir(x) and os.access(x, os.R_OK | os.X_OK)

        # Select accessible directories
        search_directories = list(filter(is_accessible_dir, search_paths))

        tags, commands = [], []
        for language in ('cc', 'cxx', 'f77', 'fc'):

            # Get compiler names and the callback to detect their versions
            compiler_names = getattr(cls, '{0}_names'.format(language))
            callback = getattr(cls, '{0}_version'.format(language))

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
                            tags.append(
                                (_CompilerID(operating_system, cls, None),
                                 _NameVariation(*match.groups()), language)
                            )
                            commands.append(
                                detect_version_command(callback, full_path)
                            )

        # Reverse it here so that the dict creation (last insert wins)
        # does not spoil the intended precedence.
        return reversed(tags), reversed(commands)

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


@functools_backport.total_ordering
class _CompilerID(collections.namedtuple('_CompilerIDBase', [
    'os', 'cmp_cls', 'version'
])):
    """Gathers the attribute values by which a detected compiler is unique."""
    def _tuple_repr(self):
        return self.os, str(self.cmp_cls), self.version

    def __eq__(self, other):
        if not isinstance(other, _CompilerID):
            return NotImplemented
        return self._tuple_repr() == other._tuple_repr()

    def __lt__(self, other):
        if not isinstance(other, _CompilerID):
            return NotImplemented
        return self._tuple_repr() < other._tuple_repr()

    def __hash__(self):
        return hash(self._tuple_repr())


#: Variations on a matched compiler name
_NameVariation = collections.namedtuple('_NameVariation', ['prefix', 'suffix'])


@llnl.util.multiproc.deferred
def detect_version_command(callback, path):
    """Detects the version of a compiler at a given path.

    Args:
        callback (callable): function that detects the version of
            the compiler at ``path``
        path (path): absolute path to search

    Returns:
        (value, error): if anything is found ``value`` is a ``(version, path)``
            tuple and ``error`` is None. If ``error`` is not None, ``value``
            is meaningless and can be discarded.
    """
    try:
        version = callback(path)
        if version and str(version).strip():
            return (version, path), None
        error = "Couldn't get version for compiler {0}".format(path)
    except spack.util.executable.ProcessError as e:
        error = "Couldn't get version for compiler {0}\n".format(path) + str(e)
    except Exception as e:
        # Catching "Exception" here is fine because it just
        # means something went wrong running a candidate executable.
        error = "Error while executing candidate compiler {0}" \
                "\n{1}: {2}".format(path, e.__class__.__name__, str(e))
    return None, error


def make_compiler_list(tags, compiler_versions):
    assert len(tags) == len(compiler_versions), \
        "the two arguments must have the same length"

    compilers_s = []
    for (compiler_id, name_variation, lang), (return_value, error) \
            in zip(tags, compiler_versions):
        # If we had an error, move to the next element
        if error:
            tty.debug(error)
            continue

        # Skip unknown versions
        version, path = return_value
        if version == 'unknown':
            continue

        tag = compiler_id._replace(version=version), name_variation, lang
        compilers_s.append((tag, path))

    compilers_s.sort()

    compilers_d = {}
    for sort_key, group in itertools.groupby(compilers_s, key=lambda x: x[0]):
        compiler_id, name_variation, language = sort_key
        by_compiler_id = compilers_d.setdefault(compiler_id, {})
        by_name_variation = by_compiler_id.setdefault(name_variation, {})
        by_name_variation[language] = list(x[1] for x in group).pop()

    # For each unique compiler_id select the name variation with most entries
    compilers = []
    for compiler_id, by_compiler_id in compilers_d.items():
        _, selected_name_variation = max(
            (len(by_compiler_id[variation]), variation)
            for variation in by_compiler_id
        )

        # Add it to the list of compilers
        operating_system, compiler_cls, version = compiler_id
        spec = spack.spec.CompilerSpec(compiler_cls.name, version)
        paths = [by_compiler_id[selected_name_variation].get(language, None)
                 for language in ('cc', 'cxx', 'f77', 'fc')]
        compilers.append(
            compiler_cls(spec, operating_system, py_platform.machine(), paths)
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
