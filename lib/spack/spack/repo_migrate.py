# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ast
import os
import re
import shutil
import sys
from typing import IO, Dict, List, Optional, Set, Tuple

import spack.repo
import spack.util.naming
import spack.util.spack_yaml


def _same_contents(f: str, g: str) -> bool:
    """Return True if the files have the same contents."""
    try:
        with open(f, "rb") as f1, open(g, "rb") as f2:
            while True:
                b1 = f1.read(4096)
                b2 = f2.read(4096)
                if b1 != b2:
                    return False
                if not b1 and not b2:
                    break
            return True
    except OSError:
        return False


def migrate_v1_to_v2(
    repo: spack.repo.Repo, fix: bool, out: IO[str] = sys.stdout, err: IO[str] = sys.stderr
) -> Tuple[bool, Optional[spack.repo.Repo]]:
    """To upgrade a repo from Package API v1 to v2 we need to:
    1. ensure ``spack_repo/<namespace>`` parent dirs to the ``repo.yaml`` file.
    2. rename <pkg dir>/package.py to <pkg module>/package.py.
    3. bump the version in ``repo.yaml``.
    """
    if not (1, 0) <= repo.package_api < (2, 0):
        raise RuntimeError(f"Cannot upgrade from {repo.package_api_str} to v2.0")

    with open(os.path.join(repo.root, "repo.yaml"), encoding="utf-8") as f:
        updated_config = spack.util.spack_yaml.load(f)
        updated_config["repo"]["api"] = "v2.0"

    namespace = repo.namespace.split(".")

    if not all(
        spack.util.naming.valid_module_name(part, package_api=(2, 0)) for part in namespace
    ):
        print(
            f"Cannot upgrade from v1 to v2, because the namespace '{repo.namespace}' is not a "
            "valid Python module",
            file=err,
        )
        return False, None

    try:
        subdirectory = spack.repo._validate_and_normalize_subdir(
            repo.subdirectory, repo.root, package_api=(2, 0)
        )
    except spack.repo.BadRepoError:
        print(
            f"Cannot upgrade from v1 to v2, because the subdirectory '{repo.subdirectory}' is not "
            "a valid Python module",
            file=err,
        )
        return False, None

    new_root = os.path.join(repo.root, "spack_repo", *namespace)

    ino_to_relpath: Dict[int, str] = {}
    symlink_to_ino: Dict[str, int] = {}

    prefix_len = len(repo.root) + len(os.sep)

    rename: Dict[str, str] = {}
    dirs_to_create: List[str] = []
    files_to_copy: List[str] = []

    errors = False

    stack: List[Tuple[str, int]] = [(repo.root, 0)]
    while stack:
        path, depth = stack.pop()

        try:
            entries = os.scandir(path)
        except OSError:
            continue

        for entry in entries:
            rel_path = entry.path[prefix_len:]

            if depth == 0 and entry.name in ("spack_repo", "repo.yaml"):
                continue

            ino_to_relpath[entry.inode()] = entry.path[prefix_len:]

            if entry.is_symlink():
                symlink_to_ino[rel_path] = entry.stat(follow_symlinks=True).st_ino
                continue

            elif entry.is_dir(follow_symlinks=False):
                if entry.name == "__pycache__":
                    continue

                # check if this is a package
                if (
                    depth == 1
                    and rel_path.startswith(f"{subdirectory}{os.sep}")
                    and os.path.exists(os.path.join(entry.path, "package.py"))
                ):
                    if "_" in entry.name:
                        print(
                            f"Invalid package name '{entry.name}': underscores are not allowed in "
                            "package names, rename the package with hyphens as separators",
                            file=err,
                        )
                        errors = True
                        continue
                    pkg_dir = spack.util.naming.pkg_name_to_pkg_dir(entry.name, package_api=(2, 0))
                    if pkg_dir != entry.name:
                        rename[f"{subdirectory}{os.sep}{entry.name}"] = (
                            f"{subdirectory}{os.sep}{pkg_dir}"
                        )

                dirs_to_create.append(rel_path)

                stack.append((entry.path, depth + 1))
                continue

            files_to_copy.append(rel_path)

    if errors:
        return False, None

    rename_regex = re.compile("^(" + "|".join(re.escape(k) for k in rename.keys()) + ")")

    if fix:
        os.makedirs(new_root, exist_ok=True)

    def _relocate(rel_path: str) -> Tuple[str, str]:
        return os.path.join(repo.root, rel_path), os.path.join(
            new_root, rename_regex.sub(lambda m: rename[m.group(0)], rel_path)
        )

    if not fix:
        print("The following directories, files and symlinks will be created:\n", file=out)

    for rel_path in dirs_to_create:
        _, new_path = _relocate(rel_path)
        if fix:
            try:
                os.mkdir(new_path)
            except FileExistsError:  # not an error if the directory already exists
                continue
        else:
            print(f"create directory {new_path}", file=out)

    for rel_path in files_to_copy:
        old_path, new_path = _relocate(rel_path)
        if os.path.lexists(new_path):
            # if we already copied this file, don't error.
            if not _same_contents(old_path, new_path):
                print(
                    f"Cannot upgrade from v1 to v2, because the file '{new_path}' already exists",
                    file=err,
                )
                return False, None
            continue
        if fix:
            shutil.copy2(old_path, new_path)
        else:
            print(f"copy {old_path} -> {new_path}", file=out)

    for rel_path, ino in symlink_to_ino.items():
        old_path, new_path = _relocate(rel_path)
        if ino in ino_to_relpath:
            # link by path relative to the new root
            _, new_target = _relocate(ino_to_relpath[ino])
            tgt = os.path.relpath(new_target, new_path)
        else:
            tgt = os.path.realpath(old_path)

        # no-op if the same, error if different
        if os.path.lexists(new_path):
            if not os.path.islink(new_path) or os.readlink(new_path) != tgt:
                print(
                    f"Cannot upgrade from v1 to v2, because the file '{new_path}' already exists",
                    file=err,
                )
                return False, None
            continue

        if fix:
            os.symlink(tgt, new_path)
        else:
            print(f"create symlink {new_path} -> {tgt}", file=out)

    if fix:
        with open(os.path.join(new_root, "repo.yaml"), "w", encoding="utf-8") as f:
            spack.util.spack_yaml.dump(updated_config, f)
        updated_repo = spack.repo.from_path(new_root)
    else:
        print(file=out)
        updated_repo = repo  # compute the import diff on the v1 repo since v2 doesn't exist yet

    result = migrate_v2_imports(
        updated_repo.packages_path, updated_repo.root, fix=fix, out=out, err=err
    )

    return result, (updated_repo if fix else None)


def migrate_v2_imports(
    packages_dir: str, root: str, fix: bool, out: IO[str] = sys.stdout, err: IO[str] = sys.stderr
) -> bool:
    """In Package API v2.0, packages need to explicitly import package classes and a few other
    symbols from the build_systems module. This function automatically adds the missing imports
    to each package.py file in the repository."""

    symbol_to_module = {
        "AspellDictPackage": "spack_repo.builtin.build_systems.aspell_dict",
        "AutotoolsPackage": "spack_repo.builtin.build_systems.autotools",
        "BundlePackage": "spack_repo.builtin.build_systems.bundle",
        "CachedCMakePackage": "spack_repo.builtin.build_systems.cached_cmake",
        "cmake_cache_filepath": "spack_repo.builtin.build_systems.cached_cmake",
        "cmake_cache_option": "spack_repo.builtin.build_systems.cached_cmake",
        "cmake_cache_path": "spack_repo.builtin.build_systems.cached_cmake",
        "cmake_cache_string": "spack_repo.builtin.build_systems.cached_cmake",
        "CargoPackage": "spack_repo.builtin.build_systems.cargo",
        "CMakePackage": "spack_repo.builtin.build_systems.cmake",
        "generator": "spack_repo.builtin.build_systems.cmake",
        "CompilerPackage": "spack_repo.builtin.build_systems.compiler",
        "CudaPackage": "spack_repo.builtin.build_systems.cuda",
        "Package": "spack_repo.builtin.build_systems.generic",
        "GNUMirrorPackage": "spack_repo.builtin.build_systems.gnu",
        "GoPackage": "spack_repo.builtin.build_systems.go",
        "IntelPackage": "spack_repo.builtin.build_systems.intel",
        "LuaPackage": "spack_repo.builtin.build_systems.lua",
        "MakefilePackage": "spack_repo.builtin.build_systems.makefile",
        "MavenPackage": "spack_repo.builtin.build_systems.maven",
        "MesonPackage": "spack_repo.builtin.build_systems.meson",
        "MSBuildPackage": "spack_repo.builtin.build_systems.msbuild",
        "NMakePackage": "spack_repo.builtin.build_systems.nmake",
        "OctavePackage": "spack_repo.builtin.build_systems.octave",
        "INTEL_MATH_LIBRARIES": "spack_repo.builtin.build_systems.oneapi",
        "IntelOneApiLibraryPackage": "spack_repo.builtin.build_systems.oneapi",
        "IntelOneApiLibraryPackageWithSdk": "spack_repo.builtin.build_systems.oneapi",
        "IntelOneApiPackage": "spack_repo.builtin.build_systems.oneapi",
        "IntelOneApiStaticLibraryList": "spack_repo.builtin.build_systems.oneapi",
        "PerlPackage": "spack_repo.builtin.build_systems.perl",
        "PythonExtension": "spack_repo.builtin.build_systems.python",
        "PythonPackage": "spack_repo.builtin.build_systems.python",
        "QMakePackage": "spack_repo.builtin.build_systems.qmake",
        "RPackage": "spack_repo.builtin.build_systems.r",
        "RacketPackage": "spack_repo.builtin.build_systems.racket",
        "ROCmPackage": "spack_repo.builtin.build_systems.rocm",
        "RubyPackage": "spack_repo.builtin.build_systems.ruby",
        "SConsPackage": "spack_repo.builtin.build_systems.scons",
        "SIPPackage": "spack_repo.builtin.build_systems.sip",
        "SourceforgePackage": "spack_repo.builtin.build_systems.sourceforge",
        "SourcewarePackage": "spack_repo.builtin.build_systems.sourceware",
        "WafPackage": "spack_repo.builtin.build_systems.waf",
        "XorgPackage": "spack_repo.builtin.build_systems.xorg",
    }

    success = True

    for f in os.scandir(packages_dir):
        pkg_path = os.path.join(f.path, "package.py")
        if (
            f.name in ("__init__.py", "__pycache__")
            or not f.is_dir(follow_symlinks=False)
            or os.path.islink(pkg_path)
        ):
            print(f"Skipping {f.path}", file=err)
            continue
        try:
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
            rel_pkg_path = os.path.relpath(pkg_path, start=root)
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

        with open(tmp_file, "w", encoding="utf-8", newline="") as file:
            file.writelines(lines)

        os.replace(tmp_file, pkg_path)

    return success
