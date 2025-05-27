# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shlex
import sys
import tempfile
from typing import Any, List, Optional

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
            r = spack.repo.from_path(repo)
        except spack.repo.RepoError:
            continue
        if r.namespace == name_or_path:
            return r
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
