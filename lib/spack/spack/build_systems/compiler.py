# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
import os
import re
from typing import Sequence

import llnl.util.tty as tty
from llnl.util.lang import classproperty

import spack.compiler
import spack.package_base


class CompilerPackage(spack.package_base.PackageBase):
    # metadata identifying this as a compiler for lmod
    family = "compiler"

    # Optional suffix regexes for searching for this type of compiler.
    # Suffixes are used by some frameworks, e.g. macports uses an '-mp-X.Y'
    # version suffix for gcc.
    suffixes: Sequence[str] = [r"-.*"]

    # Optional prefix regexes for searching for this compiler
    prefixes: Sequence[str] = []

    #: Compiler argument that produces version information
    version_argument = "-dumpversion"

    #: Return values to ignore when invoking the compiler to get its version
    ignore_version_errors: Sequence[int] = ()

    #: Regex used to extract version from compiler's output
    version_regex = "(.*)"

    #: Platform matcher for Platform objects supported by compiler
    is_supported_on_platform = lambda x: True

    #: Static definition of languages supported by this class
    compiler_languages = ["c", "cxx", "fortran"]

    #: Dynamic definition of languages supported by this package
    @property
    def supported_languages(self):
        return self.compiler_languages

    # TODO: how do these play nicely with other tags
    tags = ["compiler"]

    @classproperty
    def compiler_names(cls):
        names = []
        for language in cls.compiler_languages:
            names.extend(getattr(cls, f"{language}_names"))
        return names

    @classproperty
    def executables(cls):
        regexp_fmt = r"^({0}){1}({2})$"
        return [
            regexp_fmt.format(prefix, re.escape(name), suffix)
            for prefix, name, suffix in itertools.product(
                cls.prefixes + [""], cls.compiler_names, cls.suffixes + [""]
            )
        ]

    @classmethod
    def determine_version(cls, exe):
        try:
            output = spack.compiler.get_compiler_version_output(exe, cls.version_argument)
            match = re.search(cls.version_regex, output)
            if match:
                return ".".join(match.groups())
        except spack.util.executable.ProcessError:
            pass
        except Exception as e:
            tty.debug(e)

    @classmethod
    def determine_paths(cls, *, exes=None, prefix=None):
        assert exes is not None or prefix is not None

        if exes is None:
            exes = []
            bindir = os.path.join(prefix, "bin")
            for f, regex in itertools.product(os.listdir(bindir), cls.executables):
                if re.match(regex, f):
                    exes.append(os.path.join(bindir, f))

        # There are often at least two copies (not symlinks) of each compiler executable in the
        # same directory: one with a canonical name, e.g. "gfortran", and another one with the
        # target prefix, e.g. "x86_64-pc-linux-gnu-gfortran". There also might be a copy of "gcc"
        # with the version suffix, e.g. "x86_64-pc-linux-gnu-gcc-6.3.0". To ensure the consistency
        # of values in the "paths" dictionary (i.e. we prefer all of them to reference copies
        # with canonical names if possible), we iterate over the executables in the reversed sorted
        # order:
        # First pass over languages identifies exes that are perfect matches for canonical names
        # Second pass checks for names with prefix/suffix
        # Second pass is sorted by language name length because longer named languages
        # e.g. cxx can often contain the names of shorter named languages
        # e.g. c (e.g. clang/clang++)
        paths = {}
        exes = sorted(exes, reverse=True)
        languages = {
            lang: getattr(cls, f"{lang}_names")
            for lang in sorted(cls.compiler_languages, key=len, reverse=True)
        }
        for exe in exes:
            for lang, names in languages.items():
                if os.path.basename(exe) in names:
                    paths[lang] = exe
                    break
            else:
                for lang, names in languages.items():
                    if any(name in os.path.basename(exe) for name in names):
                        paths[lang] = exe
                        break

        return paths

    @classmethod
    def determine_variants(cls, exes, version_str):
        # path determination is separated so it can be reused in subclasses
        return "", {"paths": cls.determine_paths(exes=exes)}
