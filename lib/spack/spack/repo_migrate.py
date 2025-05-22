# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ast
import difflib
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
    repo: spack.repo.Repo, *, patch_file: Optional[IO[bytes]], err: IO[str] = sys.stderr
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

    stack: List[Tuple[str, int]] = [(repo.packages_path, 0)]

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
                try:
                    symlink_to_ino[rel_path] = entry.stat(follow_symlinks=True).st_ino
                except OSError:
                    symlink_to_ino[rel_path] = -1  # dangling or no access

                continue

            elif entry.is_dir(follow_symlinks=False):
                if entry.name == "__pycache__":
                    continue

                # check if this is a package
                if depth == 0 and os.path.exists(os.path.join(entry.path, "package.py")):
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

    if not patch_file:
        os.makedirs(os.path.join(new_root, repo.subdirectory), exist_ok=True)

    def _relocate(rel_path: str) -> Tuple[str, str]:
        old = os.path.join(repo.root, rel_path)
        if rename:
            new_rel = rename_regex.sub(lambda m: rename[m.group(0)], rel_path)
        else:
            new_rel = rel_path
        new = os.path.join(new_root, new_rel)
        return old, new

    if patch_file:
        patch_file.write(b"The following directories, files and symlinks will be created:\n")

    for rel_path in dirs_to_create:
        _, new_path = _relocate(rel_path)
        if not patch_file:
            try:
                os.mkdir(new_path)
            except FileExistsError:  # not an error if the directory already exists
                continue
        else:
            patch_file.write(b"create directory ")
            patch_file.write(new_path.encode("utf-8"))
            patch_file.write(b"\n")

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
        if not patch_file:
            shutil.copy2(old_path, new_path)
        else:
            patch_file.write(b"copy ")
            patch_file.write(old_path.encode("utf-8"))
            patch_file.write(b" -> ")
            patch_file.write(new_path.encode("utf-8"))
            patch_file.write(b"\n")

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

        if not patch_file:
            os.symlink(tgt, new_path)
        else:
            patch_file.write(b"create symlink ")
            patch_file.write(new_path.encode("utf-8"))
            patch_file.write(b" -> ")
            patch_file.write(tgt.encode("utf-8"))
            patch_file.write(b"\n")

    if not patch_file:
        with open(os.path.join(new_root, "repo.yaml"), "w", encoding="utf-8") as f:
            spack.util.spack_yaml.dump(updated_config, f)
        updated_repo = spack.repo.from_path(new_root)
    else:
        patch_file.write(b"\n")
        updated_repo = repo  # compute the import diff on the v1 repo since v2 doesn't exist yet

    result = migrate_v2_imports(
        updated_repo.packages_path, updated_repo.root, patch_file=patch_file, err=err
    )

    return result, (updated_repo if patch_file else None)


def _pkg_module_update(pkg_module: str) -> str:
    return re.sub(r"^num(\d)", r"_\1", pkg_module)  # num7zip -> _7zip.


def _spack_pkg_to_spack_repo(modulename: str) -> str:
    # rewrite spack.pkg.builtin.foo -> spack_repo.builtin.packages.foo.package
    parts = modulename.split(".")
    assert parts[:2] == ["spack", "pkg"]
    parts[0:2] = ["spack_repo"]
    parts.insert(2, "packages")
    parts[3] = _pkg_module_update(parts[3])
    parts.append("package")
    return ".".join(parts)


def migrate_v2_imports(
    packages_dir: str, root: str, patch_file: Optional[IO[bytes]], err: IO[str] = sys.stderr
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
        except FileNotFoundError:
            continue
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
        module_replacements: Dict[str, str] = {}
        parent: Dict[int, ast.AST] = {}

        #: List of (line, col start, old, new) tuples of strings to be replaced inline.
        inline_updates: List[Tuple[int, int, str, str]] = []

        #: List of (line from, line to, new lines) tuples of line replacements
        multiline_updates: List[Tuple[int, int, List[str]]] = []

        try:
            with open(pkg_path, "r", encoding="utf-8", newline="") as file:
                original_lines = file.readlines()
        except (OSError, UnicodeDecodeError) as e:
            success = False
            print(f"Skipping {pkg_path}: {e}", file=err)
            continue

        if len(original_lines) < 2:  # assume package.py files have at least 2 lines...
            continue

        if original_lines[0].endswith("\r\n"):
            newline = "\r\n"
        elif original_lines[0].endswith("\n"):
            newline = "\n"
        elif original_lines[0].endswith("\r"):
            newline = "\r"
        else:
            success = False
            print(f"{pkg_path}: unknown line ending, cannot fix", file=err)
            continue

        updated_lines = original_lines.copy()

        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Attribute):
                    parent[id(child)] = node

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

                    is_import = isinstance(child, (ast.Import, ast.ImportFrom))

                    if is_import:
                        if isinstance(child, (ast.stmt, ast.expr)):
                            end_lineno = getattr(child, "end_lineno", None)
                            if end_lineno is not None:
                                # put it right after the last import statement
                                best_line = end_lineno + 1
                            else:  # old versions of python don't have end_lineno; put it before.
                                best_line = child.lineno

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

            # Find lines where spack.pkg is used.
            elif (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id == "spack"
                and node.attr == "pkg"
            ):
                # go as many attrs up until we reach a known module name to be replaced
                known_module = "spack.pkg"
                ancestor = node
                while True:
                    next_parent = parent.get(id(ancestor))
                    if next_parent is None or not isinstance(next_parent, ast.Attribute):
                        break
                    ancestor = next_parent
                    known_module = f"{known_module}.{ancestor.attr}"
                    if known_module in module_replacements:
                        break

                inline_updates.append(
                    (
                        ancestor.lineno,
                        ancestor.col_offset,
                        known_module,
                        module_replacements[known_module],
                    )
                )

            elif isinstance(node, ast.ImportFrom):
                # Keep track of old style spack.pkg imports, to be replaced.
                if node.module and node.module.startswith("spack.pkg.") and node.level == 0:

                    depth = node.module.count(".")

                    # not all python versions have end_lineno for ImportFrom
                    end_lineno = getattr(node, "end_lineno", None)

                    # simple case of find and replace
                    # from spack.pkg.builtin.my_pkg import MyPkg
                    # -> from spack_repo.builtin.packages.my_pkg.package import MyPkg
                    if depth == 3:
                        module_replacements[node.module] = _spack_pkg_to_spack_repo(node.module)
                        inline_updates.append(
                            (
                                node.lineno,
                                node.col_offset,
                                node.module,
                                module_replacements[node.module],
                            )
                        )

                    # non-trivial possible multiline case
                    # from spack.pkg.builtin import (boost, cmake as foo)
                    # -> import spack_repo.builtin.packages.boost.package as boost
                    # -> import spack_repo.builtin.packages.cmake.package as foo
                    elif depth == 2:
                        if end_lineno is None:
                            success = False
                            print(
                                f"{pkg_path}:{node.lineno}: cannot rewrite {node.module} "
                                "import statement, since this Python version does not "
                                "provide end_lineno. Best to update to Python 3.8+",
                                file=err,
                            )
                            continue

                        _, _, namespace = node.module.rpartition(".")
                        indent = original_lines[node.lineno - 1][: node.col_offset]
                        new_lines = []
                        for alias in node.names:
                            pkg_module = _pkg_module_update(alias.name)
                            new_lines.append(
                                f"{indent}import spack_repo.{namespace}.packages."
                                f"{pkg_module}.package as {alias.asname or pkg_module}"
                                f"{newline}"
                            )
                        multiline_updates.append((node.lineno, end_lineno + 1, new_lines))

                    else:
                        success = False
                        print(
                            f"{pkg_path}:{node.lineno}: don't know how to rewrite `{node.module}`",
                            file=err,
                        )
                        continue

                elif node.module is not None and node.level == 1 and "." not in node.module:
                    # rewrite `from .blt import ...` -> `from ..blt.package import ...`
                    pkg_module = _pkg_module_update(node.module)
                    inline_updates.append(
                        (
                            node.lineno,
                            node.col_offset,
                            f".{node.module}",
                            f"..{pkg_module}.package",
                        )
                    )

                # Subtract the symbols that are imported so we don't repeatedly add imports.
                for alias in node.names:
                    if alias.name in symbol_to_module:
                        if alias.asname is None:
                            defined_symbols.add(alias.name)

                        # error when symbols are explicitly imported that are no longer available
                        if node.module == "spack.package" and node.level == 0:
                            success = False
                            print(
                                f"{pkg_path}:{node.lineno}: `{alias.name}` is imported from "
                                "`spack.package`, which no longer provides this symbol",
                                file=err,
                            )

                    if alias.asname and alias.asname in symbol_to_module:
                        defined_symbols.add(alias.asname)

            elif isinstance(node, ast.Import):
                # normal imports are easy find and replace since they are single lines.
                for alias in node.names:
                    if alias.asname and alias.asname in symbol_to_module:
                        defined_symbols.add(alias.name)
                    elif alias.asname is None and alias.name.startswith("spack.pkg."):
                        module_replacements[alias.name] = _spack_pkg_to_spack_repo(alias.name)
                        inline_updates.append(
                            (
                                node.lineno,
                                node.col_offset,
                                alias.name,
                                module_replacements[alias.name],
                            )
                        )

        # Remove imported symbols from the referenced symbols
        referenced_symbols.difference_update(defined_symbols)

        # Sort from last to first so we can modify without messing up the line / col offsets
        inline_updates.sort(reverse=True)

        # Nothing to change here.
        if not inline_updates and not referenced_symbols:
            continue

        # First do module replacements of spack.pkg imports
        for line, col, old, new in inline_updates:
            updated_lines[line - 1] = updated_lines[line - 1][:col] + updated_lines[line - 1][
                col:
            ].replace(old, new, 1)

        # Then insert new imports for symbols referenced in the package
        if referenced_symbols:
            if best_line is None:
                print(f"{pkg_path}: failed to update imports", file=err)
                success = False
                continue

            # Group missing symbols by their module
            missing_imports_by_module: Dict[str, list] = {}
            for symbol in referenced_symbols:
                module = symbol_to_module[symbol]
                if module not in missing_imports_by_module:
                    missing_imports_by_module[module] = []
                missing_imports_by_module[module].append(symbol)

            new_lines = [
                f"from {module} import {', '.join(sorted(symbols))}{newline}"
                for module, symbols in sorted(missing_imports_by_module.items())
            ]

            if not seen_import:
                new_lines.extend((newline, newline))

            multiline_updates.append((best_line, best_line, new_lines))

        multiline_updates.sort(reverse=True)
        for start, end, new_lines in multiline_updates:
            updated_lines[start - 1 : end - 1] = new_lines

        if patch_file:
            rel_pkg_path = os.path.relpath(pkg_path, start=root).replace(os.sep, "/")
            diff = difflib.unified_diff(
                original_lines,
                updated_lines,
                n=3,
                fromfile=f"a/{rel_pkg_path}",
                tofile=f"b/{rel_pkg_path}",
                lineterm="\n",
            )
            for _line in diff:
                patch_file.write(_line.encode("utf-8"))
            continue

        tmp_file = pkg_path + ".tmp"

        # binary mode to avoid newline conversion issues; utf-8 was already required upon read.
        with open(tmp_file, "wb") as file:
            for _line in updated_lines:
                file.write(_line.encode("utf-8"))

        os.replace(tmp_file, pkg_path)

    return success
