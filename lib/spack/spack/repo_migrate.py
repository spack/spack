# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ast
import os
import sys
from typing import IO, Dict, Optional, Set

import spack.repo


def migrate_v1_to_v2(repo: spack.repo.Repo, fix: bool) -> bool:
    """To upgrade a repo from Package API v1 to v2 we need to:
    1. ensure ``spack_repo/<namespace>`` parent dirs to the ``repo.yaml`` file.
    2. rename <pkg dir>/package.py to <pkg module>/package.py.
    3. bump the version in ``repo.yaml``.
    """
    return True


def migrate_v2_imports(
    repo: spack.repo.Repo, fix: bool, out: IO[str] = sys.stdout, err: IO[str] = sys.stderr
) -> bool:
    """In Package API v2.0, packages need to explicitly import package classes and a few other
    symbols from the build_systems module. This function automatically adds the missing imports
    to each package.py file in the repository."""

    if repo.package_api < (2, 0):
        return True  # nothing to do

    symbol_to_module = {
        "AspellDictPackage": "spack.build_systems.aspell_dict",
        "AutotoolsPackage": "spack.build_systems.autotools",
        "BundlePackage": "spack.build_systems.bundle",
        "CachedCMakePackage": "spack.build_systems.cached_cmake",
        "cmake_cache_filepath": "spack.build_systems.cached_cmake",
        "cmake_cache_option": "spack.build_systems.cached_cmake",
        "cmake_cache_path": "spack.build_systems.cached_cmake",
        "cmake_cache_string": "spack.build_systems.cached_cmake",
        "CargoPackage": "spack.build_systems.cargo",
        "CMakePackage": "spack.build_systems.cmake",
        "generator": "spack.build_systems.cmake",
        "CompilerPackage": "spack.build_systems.compiler",
        "CudaPackage": "spack.build_systems.cuda",
        "Package": "spack.build_systems.generic",
        "GNUMirrorPackage": "spack.build_systems.gnu",
        "GoPackage": "spack.build_systems.go",
        "IntelPackage": "spack.build_systems.intel",
        "LuaPackage": "spack.build_systems.lua",
        "MakefilePackage": "spack.build_systems.makefile",
        "MavenPackage": "spack.build_systems.maven",
        "MesonPackage": "spack.build_systems.meson",
        "MSBuildPackage": "spack.build_systems.msbuild",
        "NMakePackage": "spack.build_systems.nmake",
        "OctavePackage": "spack.build_systems.octave",
        "INTEL_MATH_LIBRARIES": "spack.build_systems.oneapi",
        "IntelOneApiLibraryPackage": "spack.build_systems.oneapi",
        "IntelOneApiLibraryPackageWithSdk": "spack.build_systems.oneapi",
        "IntelOneApiPackage": "spack.build_systems.oneapi",
        "IntelOneApiStaticLibraryList": "spack.build_systems.oneapi",
        "PerlPackage": "spack.build_systems.perl",
        "PythonExtension": "spack.build_systems.python",
        "PythonPackage": "spack.build_systems.python",
        "QMakePackage": "spack.build_systems.qmake",
        "RPackage": "spack.build_systems.r",
        "RacketPackage": "spack.build_systems.racket",
        "ROCmPackage": "spack.build_systems.rocm",
        "RubyPackage": "spack.build_systems.ruby",
        "SConsPackage": "spack.build_systems.scons",
        "SIPPackage": "spack.build_systems.sip",
        "SourceforgePackage": "spack.build_systems.sourceforge",
        "SourcewarePackage": "spack.build_systems.sourceware",
        "WafPackage": "spack.build_systems.waf",
        "XorgPackage": "spack.build_systems.xorg",
    }

    success = True

    for f in os.scandir(repo.packages_path):
        pkg_path = os.path.join(f.path, "package.py")
        rel_pkg_path = os.path.relpath(pkg_path, start=repo.root)
        try:
            if f.name in ("__init__.py", "__pycache__") or not f.is_dir():
                continue
            with open(pkg_path, "rb") as file:
                tree = ast.parse(file.read())
        except (OSError, SyntaxError) as e:
            print(f"Skipping {pkg_path}: {e}", file=err)
            continue

        #: Symbols that are referenced in the package and may need to be imported.
        referenced_symbols: Set[str] = set()

        #: Set of symbols of interest that are already defined through imports, assignments, or
        #: function definitions.
        defined_symbols: Set[str] = set()

        best_line: Optional[int] = None

        seen_import = False

        for node in ast.walk(tree):
            # Get the last import statement from the first block of top-level imports
            if isinstance(node, ast.Module):
                for child in ast.iter_child_nodes(node):
                    # if we never encounter an import statement, the best line to add is right
                    # before the first node under the module
                    if best_line is None and isinstance(child, ast.stmt):
                        best_line = child.lineno

                    # prefer adding right before `from spack.package import ...`
                    if isinstance(child, ast.ImportFrom) and child.module == "spack.package":
                        seen_import = True
                        best_line = child.lineno  # add it right before spack.package
                        break

                    # otherwise put it right after the last import statement
                    is_import = isinstance(child, (ast.Import, ast.ImportFrom))

                    if is_import:
                        if isinstance(child, (ast.stmt, ast.expr)):
                            best_line = (child.end_lineno or child.lineno) + 1

                    if not seen_import and is_import:
                        seen_import = True
                    elif seen_import and not is_import:
                        break

            # Function definitions or assignments to variables whose name is a symbol of interest
            # are considered as redefinitions, so we skip them.
            elif isinstance(node, ast.FunctionDef):
                if node.name in symbol_to_module:
                    print(
                        f"{pkg_path}:{node.lineno}: redefinition of `{node.name}` skipped",
                        file=err,
                    )
                    defined_symbols.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in symbol_to_module:
                        print(
                            f"{pkg_path}:{target.lineno}: redefinition of `{target.id}` skipped",
                            file=err,
                        )
                        defined_symbols.add(target.id)

            # Register symbols that are not imported.
            elif isinstance(node, ast.Name) and node.id in symbol_to_module:
                referenced_symbols.add(node.id)

            # Register imported symbols to make this operation idempotent
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name in symbol_to_module:
                        defined_symbols.add(alias.name)
                        if node.module == "spack.package":
                            success = False
                            print(
                                f"{pkg_path}:{node.lineno}: `{alias.name}` is imported from "
                                "`spack.package`, which no longer provides this symbol",
                                file=err,
                            )

                    if alias.asname and alias.asname in symbol_to_module:
                        defined_symbols.add(alias.asname)

        # Remove imported symbols from the referenced symbols
        referenced_symbols.difference_update(defined_symbols)

        if not referenced_symbols:
            continue

        if best_line is None:
            print(f"{pkg_path}: failed to update imports", file=err)
            success = False
            continue

        # Add the missing imports right after the last import statement
        with open(pkg_path, "r", encoding="utf-8", newline="") as file:
            lines = file.readlines()

        # Group missing symbols by their module
        missing_imports_by_module: Dict[str, list] = {}
        for symbol in referenced_symbols:
            module = symbol_to_module[symbol]
            if module not in missing_imports_by_module:
                missing_imports_by_module[module] = []
            missing_imports_by_module[module].append(symbol)

        new_lines = [
            f"from {module} import {', '.join(sorted(symbols))}\n"
            for module, symbols in sorted(missing_imports_by_module.items())
        ]

        if not seen_import:
            new_lines.extend(("\n", "\n"))

        if not fix:  # only print the diff
            success = False  # packages need to be fixed, but we didn't do it
            diff_start, diff_end = max(1, best_line - 3), min(best_line + 2, len(lines))
            num_changed = diff_end - diff_start + 1
            num_added = num_changed + len(new_lines)
            out.write(f"--- a/{rel_pkg_path}\n+++ b/{rel_pkg_path}\n")
            out.write(f"@@ -{diff_start},{num_changed} +{diff_start},{num_added} @@\n")
            for line in lines[diff_start - 1 : best_line - 1]:
                out.write(f" {line}")
            for line in new_lines:
                out.write(f"+{line}")
            for line in lines[best_line - 1 : diff_end]:
                out.write(f" {line}")
            continue

        lines[best_line - 1 : best_line - 1] = new_lines

        tmp_file = pkg_path + ".tmp"

        with open(tmp_file, "w", encoding="utf-8") as file:
            file.writelines(lines)

        os.replace(tmp_file, pkg_path)

    return success
