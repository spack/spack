# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import pathlib
import sys
import tempfile
import zipfile
from typing import List, Optional, Tuple

import llnl.util.tty as tty

import spack.config
import spack.repo
import spack.util.path
from spack.cmd.common import arguments
from spack.util.archive import reproducible_zipfile_from_prefix

description = "manage package source repositories"
section = "config"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="repo_command")

    # Create
    create_parser = sp.add_parser("create", help=repo_create.__doc__)
    create_parser.add_argument("directory", help="directory to create the repo in")
    create_parser.add_argument(
        "namespace",
        help="namespace to identify packages in the repository (defaults to the directory name)",
        nargs="?",
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

    # Zip
    zip_parser = sp.add_parser("zip", help=repo_zip.__doc__)
    zip_parser.add_argument(
        "namespace_or_path", help="namespace or path of a Spack package repository"
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

    key, repo = _get_repo(repos, args.namespace_or_path)

    if not key:
        tty.die(f"No repository with path or namespace: {args.namespace_or_path}")

    repos.remove(key)
    spack.config.set("repos", repos, args.scope)
    if repo:
        tty.msg(f"Removed repository {repo.root} with namespace '{repo.namespace}'")
    else:
        tty.msg(f"Removed repository {key}")


def repo_list(args):
    """show registered repositories and their namespaces"""
    roots = spack.config.get("repos", scope=args.scope)
    repos = []
    for r in roots:
        try:
            repos.append(spack.repo.from_path(r))
        except spack.repo.RepoError:
            continue

    if sys.stdout.isatty():
        tty.msg(f"{len(repos)} package repositor{'y.' if len(repos) == 1 else 'ies.'}")

    if not repos:
        return

    max_ns_len = max(len(r.namespace) for r in repos)
    for repo in repos:
        print(f"{repo.namespace:<{max_ns_len}} {repo.root}")


def repo_zip(args):
    """zip a package repository to make it immutable and faster to load"""
    key, _ = _get_repo(spack.config.get("repos"), args.namespace_or_path)

    if not key:
        tty.die(f"No repository with path or namespace: {args.namespace_or_path}")

    try:
        repo = spack.repo.from_path(key)
    except spack.repo.RepoError:
        tty.die(f"No repository at path: {key}")

    def _zip_repo_skip(entry: os.DirEntry, depth: int):
        if entry.name == "__pycache__":
            return True
        if depth == 0 and not os.path.exists(os.path.join(entry.path, "package.py")):
            return True
        return False

    def _zip_repo_path_to_name(path: str) -> str:
        # use spack/pkg/<repo>/* prefix and rename `package.py` as `__init__.py`
        rel_path = pathlib.PurePath(path).relative_to(repo.packages_path)
        if rel_path.name == "package.py":
            rel_path = rel_path.with_name("__init__.py")
        return str(rel_path)

    # Create a zipfile in a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode="wb", dir=repo.root) as f, zipfile.ZipFile(
        f, "w", compression=zipfile.ZIP_DEFLATED
    ) as zip:
        reproducible_zipfile_from_prefix(
            zip, repo.packages_path, skip=_zip_repo_skip, path_to_name=_zip_repo_path_to_name
        )

    packages_zip = os.path.join(repo.root, "packages.zip")
    try:
        # Inform the user whether or not the repo was modified since it was last zipped
        if os.path.exists(packages_zip) and filecmp.cmp(f.name, packages_zip):
            tty.msg(f"{repo.namespace}: {packages_zip} is up to date")
            return
        else:
            os.rename(f.name, packages_zip)
            tty.msg(f"{repo.namespace} was zipped: {packages_zip}")
    finally:
        try:
            os.unlink(f.name)
        except OSError:
            pass


def _get_repo(repos: List[str], path_or_name) -> Tuple[Optional[str], Optional[spack.repo.Repo]]:
    """Find repo by path or namespace"""
    canon_path = spack.util.path.canonicalize_path(path_or_name)
    for path in repos:
        if canon_path == spack.util.path.canonicalize_path(path):
            return path, None

    for path in repos:
        try:
            repo = spack.repo.from_path(path)
        except spack.repo.RepoError:
            continue
        if repo.namespace == path_or_name:
            return path, repo
    return None, None


def repo(parser, args):
    action = {
        "create": repo_create,
        "list": repo_list,
        "add": repo_add,
        "remove": repo_remove,
        "rm": repo_remove,
        "zip": repo_zip,
    }
    action[args.repo_command](args)
