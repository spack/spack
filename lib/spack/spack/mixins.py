# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains additional behavior that can be attached to any given package."""
import os
from typing import Optional

import spack.llnl.util.filesystem
import spack.phase_callbacks


def filter_compiler_wrappers(
    *files: str,
    after: str = "install",
    relative_root: Optional[str] = None,
    ignore_absent: bool = True,
    backup: bool = False,
    recursive: bool = False,
    **kwargs,  # for compatibility with package api v2.0
) -> None:
    """Registers a phase callback (e.g. post-install) to look for references to Spack's compiler
    wrappers in the given files and replace them with the underlying compilers.

    Example usage::

        class MyPackage(Package):

            filter_compiler_wrappers("mpicc", "mpicxx", relative_root="bin")

    This is useful for packages that register the path to the compiler they are built with to be
    used later at runtime. Spack's compiler wrappers cannot be used at runtime, as they require
    Spack's build environment to be set up. Using this function, the compiler wrappers are replaced
    with the actual compilers, so that the package works correctly at runtime.

    Args:
        *files: files to be filtered relative to the search root (install prefix by default).
        after: specifies after which phase the files should be filtered (defaults to
            ``"install"``).
        relative_root: path relative to install prefix where to start searching for the files to be
            filtered. If not set the install prefix will be used as the search root. It is *highly
            recommended* to set this, as searching recursively from the installation prefix can be
            very slow.
        ignore_absent: if present, will be forwarded to
            :func:`~spack.llnl.util.filesystem.filter_file`
        backup: if present, will be forwarded to
            :func:`~spack.llnl.util.filesystem.filter_file`
        recursive: if present, will be forwarded to :func:`~spack.llnl.util.filesystem.find`
    """

    def _filter_compiler_wrappers_impl(pkg_or_builder):
        pkg = getattr(pkg_or_builder, "pkg", pkg_or_builder)
        # Compute the absolute path of the search root
        root = os.path.join(pkg.prefix, relative_root) if relative_root else pkg.prefix

        # Compute the absolute path of the files to be filtered and remove links from the list.
        abs_files = spack.llnl.util.filesystem.find(root, files, recursive=recursive)
        abs_files = [x for x in abs_files if not os.path.islink(x)]

        x = spack.llnl.util.filesystem.FileFilter(*abs_files)

        compiler_vars = []
        if "c" in pkg.spec:
            compiler_vars.append(("CC", pkg.spec["c"].package.cc))

        if "cxx" in pkg.spec:
            compiler_vars.append(("CXX", pkg.spec["cxx"].package.cxx))

        if "fortran" in pkg.spec:
            compiler_vars.append(("FC", pkg.spec["fortran"].package.fortran))
            compiler_vars.append(("F77", pkg.spec["fortran"].package.fortran))

        # Some paths to the compiler wrappers might be substrings of the others.
        # For example:
        #   CC=/path/to/spack/lib/spack/env/cc (realpath to the wrapper)
        #   FC=/path/to/spack/lib/spack/env/cce/ftn
        # Therefore, we perform the filtering in the reversed sorted order of the substituted
        # strings. If, however, the strings are identical (e.g. both CC and FC are set using
        # realpath), the filtering is done according to the order in compiler_vars. To achieve
        # that, we populate the following array with tuples of three elements: path to the wrapper,
        # negated index of the variable in compiler_vars, path to the real compiler. This way, the
        # reversed sorted order of the resulting array is the order of replacements that we need.
        replacements = []

        for idx, (env_var, compiler_path) in enumerate(compiler_vars):
            if env_var in os.environ and compiler_path is not None:
                # filter spack wrapper and links to spack wrapper in case
                # build system runs realpath
                wrapper = os.environ[env_var]
                for wrapper_path in (wrapper, os.path.realpath(wrapper)):
                    replacements.append((wrapper_path, -idx, compiler_path))

        for wrapper_path, _, compiler_path in sorted(replacements, reverse=True):
            x.filter(
                wrapper_path,
                compiler_path,
                ignore_absent=ignore_absent,
                backup=backup,
                string=True,
            )

        # Remove this linking flag if present (it turns RPATH into RUNPATH)
        for compiler_lang in ("c", "cxx", "fortran"):
            if compiler_lang not in pkg.spec:
                continue
            compiler_pkg = pkg.spec[compiler_lang].package
            x.filter(
                f"{compiler_pkg.linker_arg}--enable-new-dtags",
                "",
                ignore_absent=ignore_absent,
                backup=backup,
                string=True,
            )

        # NAG compiler is usually mixed with GCC, which has a different
        # prefix for linker arguments.
        if pkg.compiler.name == "nag":
            x.filter(
                "-Wl,--enable-new-dtags",
                "",
                ignore_absent=ignore_absent,
                backup=backup,
                string=True,
            )

    spack.phase_callbacks.run_after(after)(_filter_compiler_wrappers_impl)
