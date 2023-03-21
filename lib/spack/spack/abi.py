# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from llnl.util.lang import memoized

import spack.spec
from spack.compilers.clang import Clang
from spack.spec import CompilerSpec
from spack.util.executable import Executable, ProcessError


class ABI(object):
    """This class provides methods to test ABI compatibility between specs.
    The current implementation is rather rough and could be improved."""

    def architecture_compatible(self, target, constraint):
        """Return true if architecture of target spec is ABI compatible
        to the architecture of constraint spec. If either the target
        or constraint specs have no architecture, target is also defined
        as architecture ABI compatible to constraint."""
        return (
            not target.architecture
            or not constraint.architecture
            or target.architecture.intersects(constraint.architecture)
        )

    @memoized
    def _gcc_get_libstdcxx_version(self, version):
        """Returns gcc ABI compatibility info by getting the library version of
        a compiler's libstdc++ or libgcc_s"""
        from spack.build_environment import dso_suffix

        spec = CompilerSpec("gcc", version)
        compilers = spack.compilers.compilers_for_spec(spec)
        if not compilers:
            return None
        compiler = compilers[0]
        rungcc = None
        libname = None
        output = None
        if compiler.cxx:
            rungcc = Executable(compiler.cxx)
            libname = "libstdc++." + dso_suffix
        elif compiler.cc:
            rungcc = Executable(compiler.cc)
            libname = "libgcc_s." + dso_suffix
        else:
            return None
        try:
            # Some gcc's are actually clang and don't respond properly to
            # --print-file-name (they just print the filename, not the
            # full path).  Ignore these and expect them to be handled as clang.
            if Clang.default_version(rungcc.exe[0]) != "unknown":
                return None

            output = rungcc("--print-file-name=%s" % libname, output=str)
        except ProcessError:
            return None
        if not output:
            return None
        libpath = os.path.realpath(output.strip())
        if not libpath:
            return None
        return os.path.basename(libpath)

    @memoized
    def _gcc_compiler_compare(self, pversion, cversion):
        """Returns true iff the gcc version pversion and cversion
        are ABI compatible."""
        plib = self._gcc_get_libstdcxx_version(pversion)
        clib = self._gcc_get_libstdcxx_version(cversion)
        if not plib or not clib:
            return False
        return plib == clib

    def _intel_compiler_compare(self, pversion, cversion):
        """Returns true iff the intel version pversion and cversion
        are ABI compatible"""

        # Test major and minor versions.  Ignore build version.
        if len(pversion.version) < 2 or len(cversion.version) < 2:
            return False
        return pversion.version[:2] == cversion.version[:2]

    def compiler_compatible(self, parent, child, **kwargs):
        """Return true if compilers for parent and child are ABI compatible."""
        if not parent.compiler or not child.compiler:
            return True

        if parent.compiler.name != child.compiler.name:
            # Different compiler families are assumed ABI incompatible
            return False

        if kwargs.get("loose", False):
            return True

        # TODO: Can we move the specialized ABI matching stuff
        # TODO: into compiler classes?
        for pversion in parent.compiler.versions:
            for cversion in child.compiler.versions:
                # For a few compilers use specialized comparisons.
                # Otherwise match on version match.
                if pversion.intersects(cversion):
                    return True
                elif parent.compiler.name == "gcc" and self._gcc_compiler_compare(
                    pversion, cversion
                ):
                    return True
                elif parent.compiler.name == "intel" and self._intel_compiler_compare(
                    pversion, cversion
                ):
                    return True
        return False

    def compatible(self, target, constraint, **kwargs):
        """Returns true if target spec is ABI compatible to constraint spec"""
        loosematch = kwargs.get("loose", False)
        return self.architecture_compatible(target, constraint) and self.compiler_compatible(
            target, constraint, loose=loosematch
        )
