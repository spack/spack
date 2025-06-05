# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shlex
import sys
import tempfile
from typing import Any, Dict, List, Optional, Union

import llnl.util.tty as tty
from llnl.util.tty import color

import spack
import spack.caches
import spack.config
import spack.repo
import spack.util.executable
import spack.util.path
from spack.cmd.common import arguments
from spack.error import SpackError

description = "manage package source repositories"
section = "config"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser):
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
    add_parser.add_argument(
        "path_or_repo", help="path or git repository of a Spack package repository"
    )
    # optional positional argument for destination name in case of git repository
    add_parser.add_argument(
        "destination",
        nargs="?",
        default=None,
        help="destination to clone git repository into (defaults to cache directory)",
    )
    add_parser.add_argument(
        "--name",
        action="store",
        help="config name for the package repository, defaults to the namespace of the repository",
    )
    add_parser.add_argument(
        "--path",
        help="relative path to the Spack package repository inside a git repository. Can be "
        "repeated to add multiple package repositories in case of a monorepo",
        action="append",
        default=[],
    )
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
    patch_or_fix = migrate_parser.add_mutually_exclusive_group(required=True)
    patch_or_fix.add_argument(
        "--dry-run",
        action="store_true",
        help="do not modify the repository, but dump a patch file",
    )
    patch_or_fix.add_argument(
        "--fix",
        action="store_true",
        help="automatically migrate the repository to the latest Package API",
    )


def repo_create(args):
    """create a new package repository"""
    full_path, namespace = spack.repo.create_repo(args.directory, args.namespace, args.subdir)
    tty.msg("Created repo with namespace '%s'." % namespace)
    tty.msg("To register it with spack, run this command:", "spack repo add %s" % full_path)


def _add_repo(
    path_or_repo: str,
    name: Optional[str],
    scope: Optional[str],
    paths: List[str],
    destination: Optional[str],
    config: Optional[spack.config.Configuration] = None,
) -> str:
    config = config or spack.config.CONFIG

    existing: Dict[str, Any] = config.get("repos", default={}, scope=scope)

    if name and name in existing:
        raise SpackError(f"A repository with the name '{name}' already exists.")

    # Interpret as a git URL when it contains a colon at index 2 or more, not preceded by a
    # forward slash. That allows C:/ windows paths, while following git's convention to distinguish
    # between local paths on the one hand and URLs and SCP like syntax on the other.
    entry: Union[str, Dict[str, Any]]
    colon_idx = path_or_repo.find(":")

    if colon_idx > 1 and "/" not in path_or_repo[:colon_idx]:  # git URL
        entry = {"git": path_or_repo}
        if len(paths) >= 1:
            entry["paths"] = paths
        if destination:
            entry["destination"] = destination
    else:  # local path
        if destination:
            raise SpackError("The 'destination' argument is only valid for git repositories")
        elif paths:
            raise SpackError("The --paths flag is only valid for git repositories")
        entry = spack.util.path.canonicalize_path(path_or_repo)

    descriptor = spack.repo.parse_config_descriptor(
        name or "<unnamed>", entry, lock=spack.repo.package_repository_lock()
    )
    descriptor.initialize(git=spack.util.executable.which("git"))

    packages_repos = descriptor.construct(cache=spack.caches.MISC_CACHE)

    usable_repos: Dict[str, spack.repo.Repo] = {}

    for _path, _repo_or_err in packages_repos.items():
        if isinstance(_repo_or_err, Exception):
            tty.warn(f"Skipping package repository '{_path}' due to: {_repo_or_err}")
        else:
            usable_repos[_path] = _repo_or_err

    if not usable_repos:
        raise SpackError(f"No package repository could be constructed from {path_or_repo}")

    # For the config key, default to --name, then to the namespace if there's only one repo.
    # Otherwise, the name is unclear and we require the user to specify it.
    if name:
        key = name
    elif len(usable_repos) == 1:
        key = next(iter(usable_repos.values())).namespace
    else:
        raise SpackError("Multiple package repositories found, please specify a name with --name.")

    if key in existing:
        raise SpackError(f"A repository with the name '{key}' already exists.")

    existing[key] = entry
    config.set("repos", existing, scope)
    return key


def repo_add(args):
    """add package repositories to Spack's configuration"""
    name = _add_repo(
        path_or_repo=args.path_or_repo,
        name=args.name,
        scope=args.scope,
        paths=args.path,
        destination=args.destination,
    )
    tty.msg(f"Added repo to config with name '{name}'.")


def repo_remove(args):
    """remove a repository from Spack's configuration"""
    namespace_or_path = args.namespace_or_path
    repos: Dict[str, str] = spack.config.get("repos", scope=args.scope)

    if namespace_or_path in repos:
        # delete by name (from config)
        key = namespace_or_path
    else:
        # delete by namespace or path (requires constructing the repo)
        canon_path = spack.util.path.canonicalize_path(namespace_or_path)
        descriptors = spack.repo.RepoDescriptors.from_config(
            spack.repo.package_repository_lock(), spack.config.CONFIG, scope=args.scope
        )
        for name, descriptor in descriptors.items():
            descriptor.initialize(fetch=False)

            # For now you cannot delete monorepos with multipe package repositories from config,
            # hence "all" and not "any". We can improve this later if needed.
            if all(
                r.namespace == namespace_or_path or r.root == canon_path
                for r in descriptor.construct(cache=spack.caches.MISC_CACHE).values()
                if isinstance(r, spack.repo.Repo)
            ):
                key = name
                break
        else:
            tty.die(f"No repository with path or namespace: {namespace_or_path}")

    del repos[key]
    spack.config.set("repos", repos, args.scope)
    tty.msg(f"Removed repository '{namespace_or_path}'.")


def repo_list(args):
    """show registered repositories and their namespaces"""
    descriptors = spack.repo.RepoDescriptors.from_config(
        lock=spack.repo.package_repository_lock(), config=spack.config.CONFIG, scope=args.scope
    )

    if not sys.stdout.isatty():
        for name in descriptors:
            print(name)
        return

    # Collect all repository information for aligned output
    repo_info = []

    for name, descriptor in descriptors.items():
        descriptor.initialize(fetch=False)
        repos_for_descriptor = descriptor.construct(cache=spack.caches.MISC_CACHE)

        # Register all repos and errors for this descriptor
        for path, maybe_repo in repos_for_descriptor.items():
            if isinstance(maybe_repo, spack.repo.Repo):
                repo_info.append(
                    ("@g{[+]}", maybe_repo.namespace, maybe_repo.package_api_str, maybe_repo.root)
                )
            else:  # exception
                repo_info.append(("@r{[-]}", name, "", f"{path}: {maybe_repo}"))

        # If there are no repos, it means it's not yet cloned; then we status + git repository
        if not repos_for_descriptor and isinstance(descriptor, spack.repo.RemoteRepoDescriptor):
            repo_info.append(("@K{ - }", name, "", descriptor.repository))

    if repo_info:
        max_namespace_width = max(len(namespace) for _, namespace, _, _ in repo_info) + 3
        max_api_width = max(len(api) for _, _, api, _ in repo_info) + 3

        # Print aligned output
        for status, namespace, api, path in repo_info:
            color.cprint(
                f"{status} {namespace:<{max_namespace_width}} {api:<{max_api_width}} {path}"
            )


def _get_repo(name_or_path: str) -> Optional[spack.repo.Repo]:
    """Get a repo by path or namespace"""
    try:
        return spack.repo.from_path(name_or_path)
    except spack.repo.RepoError:
        pass

    descriptors = spack.repo.RepoDescriptors.from_config(
        spack.repo.package_repository_lock(), spack.config.CONFIG
    )

    repo_path, _ = descriptors.construct(cache=spack.caches.MISC_CACHE, fetch=False)

    for repo in repo_path.repos:
        if repo.namespace == name_or_path:
            return repo

    return None


def repo_migrate(args: Any) -> int:
    """migrate a package repository to the latest Package API"""
    from spack.repo_migrate import migrate_v1_to_v2, migrate_v2_imports

    repo = _get_repo(args.namespace_or_path)

    if repo is None:
        tty.die(f"No such repository: {args.namespace_or_path}")

    if args.dry_run:
        fd, patch_file_path = tempfile.mkstemp(
            suffix=".patch", prefix="repo-migrate-", dir=os.getcwd()
        )
        patch_file = os.fdopen(fd, "bw")
        tty.msg(f"Patch file will be written to {patch_file_path}")
    else:
        patch_file_path = None
        patch_file = None

    try:
        if (1, 0) <= repo.package_api < (2, 0):
            success, repo_v2 = migrate_v1_to_v2(repo, patch_file=patch_file)
            exit_code = 0 if success else 1
        elif (2, 0) <= repo.package_api < (3, 0):
            repo_v2 = None
            exit_code = (
                0
                if migrate_v2_imports(repo.packages_path, repo.root, patch_file=patch_file)
                else 1
            )
        else:
            repo_v2 = None
            exit_code = 0
    finally:
        if patch_file is not None:
            patch_file.flush()
            patch_file.close()

    if patch_file_path:
        tty.warn(
            f"No changes were made to the '{repo.namespace}' repository with. Review "
            f"the changes written to {patch_file_path}. Run \n\n"
            f"    spack repo migrate --fix {args.namespace_or_path}\n\n"
            "to upgrade the repo."
        )

    elif exit_code == 1:
        tty.error(
            f"Repository '{repo.namespace}' could not be migrated to the latest Package API. "
            "Please check the error messages above."
        )

    elif isinstance(repo_v2, spack.repo.Repo):
        tty.info(
            f"Repository '{repo_v2.namespace}' was successfully migrated from "
            f"package API {repo.package_api_str} to {repo_v2.package_api_str}."
        )
        tty.warn(
            "Remove the old repository from Spack's configuration and add the new one using:\n"
            f"    spack repo remove {shlex.quote(repo.root)}\n"
            f"    spack repo add {shlex.quote(repo_v2.root)}"
        )

    else:
        tty.info(f"Repository '{repo.namespace}' was successfully migrated")

    return exit_code


def repo(parser, args):
    return {
        "create": repo_create,
        "list": repo_list,
        "add": repo_add,
        "remove": repo_remove,
        "rm": repo_remove,
        "migrate": repo_migrate,
    }[args.repo_command](args)
