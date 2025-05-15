# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ast
import os
import sys
from typing import Any, Dict, List, Optional, Set

import llnl.util.tty as tty

import spack
import spack.config
import spack.repo
import spack.util.path
from spack.cmd.common import arguments

description = "manage package source repositories"
section = "config"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="repo_command")

    # Create
    create_parser = sp.add_parser("create", help=repo_create.__doc__)
    create_parser.add_argument("directory", help="directory to create the repo in")
    create_parser.add_argument(
        "namespace", help="name or namespace to identify packages in the repository"
    )
    create_parser.add_argument(
        "-d",
        "--subdirectory",
        action="store",
        dest="subdir",
        default=spack.repo.packages_dir_name,
        help="subdirectory to store packages in the repository\n\n"
        "default 'packages'. use an empty string for no subdirectory",
    )

    # List
    list_parser = sp.add_parser("list", help=repo_list.__doc__)
    list_parser.add_argument(
        "--scope", action=arguments.ConfigScope, help="configuration scope to read from"
    )

    # Add
    add_parser = sp.add_parser("add", help=repo_add.__doc__)
    add_parser.add_argument("path", help="path to a Spack package repository directory")
    add_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )

    # Remove
    remove_parser = sp.add_parser("remove", help=repo_remove.__doc__, aliases=["rm"])
    remove_parser.add_argument(
        "namespace_or_path", help="namespace or path of a Spack package repository"
    )
    remove_parser.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )

    # Migrate
    migrate_parser = sp.add_parser("migrate", help=repo_migrate.__doc__)
    migrate_parser.add_argument(
        "namespace_or_path", help="path to a Spack package repository directory"
    )


def repo_create(args):
    """create a new package repository"""
    full_path, namespace = spack.repo.create_repo(args.directory, args.namespace, args.subdir)
    tty.msg("Created repo with namespace '%s'." % namespace)
    tty.msg("To register it with spack, run this command:", "spack repo add %s" % full_path)


def repo_add(args):
    """add a package source to Spack's configuration"""
    path = args.path

    # real_path is absolute and handles substitution.
    canon_path = spack.util.path.canonicalize_path(path)

    # check if the path exists
    if not os.path.exists(canon_path):
        tty.die("No such file or directory: %s" % path)

    # Make sure the path is a directory.
    if not os.path.isdir(canon_path):
        tty.die("Not a Spack repository: %s" % path)

    # Make sure it's actually a spack repository by constructing it.
    repo = spack.repo.from_path(canon_path)

    # If that succeeds, finally add it to the configuration.
    repos = spack.config.get("repos", scope=args.scope)
    if not repos:
        repos = []

    if repo.root in repos or path in repos:
        tty.die("Repository is already registered with Spack: %s" % path)

    repos.insert(0, canon_path)
    spack.config.set("repos", repos, args.scope)
    tty.msg("Added repo with namespace '%s'." % repo.namespace)


def repo_remove(args):
    """remove a repository from Spack's configuration"""
    repos = spack.config.get("repos", scope=args.scope)
    namespace_or_path = args.namespace_or_path

    # If the argument is a path, remove that repository from config.
    canon_path = spack.util.path.canonicalize_path(namespace_or_path)
    for repo_path in repos:
        repo_canon_path = spack.util.path.canonicalize_path(repo_path)
        if canon_path == repo_canon_path:
            repos.remove(repo_path)
            spack.config.set("repos", repos, args.scope)
            tty.msg("Removed repository %s" % repo_path)
            return

    # If it is a namespace, remove corresponding repo
    for path in repos:
        try:
            repo = spack.repo.from_path(path)
            if repo.namespace == namespace_or_path:
                repos.remove(path)
                spack.config.set("repos", repos, args.scope)
                tty.msg("Removed repository %s with namespace '%s'." % (repo.root, repo.namespace))
                return
        except spack.repo.RepoError:
            continue

    tty.die("No repository with path or namespace: %s" % namespace_or_path)


def repo_list(args):
    """show registered repositories and their namespaces"""
    roots = spack.config.get("repos", scope=args.scope)
    repos: List[spack.repo.Repo] = []
    for r in roots:
        try:
            repos.append(spack.repo.from_path(r))
        except spack.repo.RepoError:
            continue

    if sys.stdout.isatty():
        tty.msg(f"{len(repos)} package repositor" + ("y." if len(repos) == 1 else "ies."))

    if not repos:
        return

    max_ns_len = max(len(r.namespace) for r in repos)
    for repo in repos:
        print(f"{repo.namespace:<{max_ns_len + 4}}{repo.package_api_str:<8}{repo.root}")


def _get_repo(name_or_path: str) -> Optional[spack.repo.Repo]:
    try:
        return spack.repo.from_path(name_or_path)
    except spack.repo.RepoError:
        pass

    for repo in spack.config.get("repos"):
        try:
            r = spack.repo.from_path(spack.util.path.canonicalize_path(repo))
        except spack.repo.RepoError:
            continue
        if r.namespace == name_or_path or os.path.samefile(r.root, name_or_path):
            return r

    return None


def repo_migrate(args: Any) -> None:
    """migrate a package repository to the latest Package API"""
    repo = _get_repo(args.namespace_or_path)

    if repo is None:
        tty.die(f"No such repository: {args.namespace_or_path}")

    if repo.package_api < (2, 0):
        tty.die("Migration from Spack repo API < 2.0 is not supported yet")

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

    for f in os.scandir(repo.packages_path):
        pkg_path = os.path.join(f.path, "package.py")
        try:
            if f.name in ("__init__.py", "__pycache__") or not f.is_dir():
                continue
            with open(pkg_path, "rb") as file:
                tree = ast.parse(file.read())
        except (OSError, SyntaxError) as e:
            print(f"Skipping {pkg_path}: {e}", file=sys.stderr)
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
                        file=sys.stderr,
                    )
                    defined_symbols.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in symbol_to_module:
                        print(
                            f"{pkg_path}:{target.lineno}: redefinition of `{target.id}` skipped",
                            file=sys.stderr,
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
                            print(
                                f"{pkg_path}:{node.lineno}: `{alias.name}` is imported from "
                                "`spack.package`, which no longer provides this symbol",
                                file=sys.stderr,
                            )

                    if alias.asname and alias.asname in symbol_to_module:
                        defined_symbols.add(alias.asname)

        # Remove imported symbols from the referenced symbols
        referenced_symbols.difference_update(defined_symbols)

        if not referenced_symbols:
            continue

        if best_line is None:
            print(f"{pkg_path}: failed to update imports", file=sys.stderr)
            continue

        # Add the missing imports right after the last import statement
        with open(pkg_path, "r", encoding="utf-8") as file:
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

        lines[best_line - 1 : best_line - 1] = new_lines

        tmp_file = pkg_path + ".tmp"

        with open(tmp_file, "w", encoding="utf-8") as file:
            file.writelines(lines)

        os.replace(tmp_file, pkg_path)


def repo(parser, args):
    action = {
        "create": repo_create,
        "list": repo_list,
        "add": repo_add,
        "remove": repo_remove,
        "rm": repo_remove,
        "migrate": repo_migrate,
    }
    action[args.repo_command](args)
