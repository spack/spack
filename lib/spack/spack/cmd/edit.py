# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import errno
import glob
import os
from typing import Optional, Union

import spack.cmd
import spack.llnl.util.tty as tty
import spack.paths
import spack.repo
import spack.util.editor

description = "open package files in ``$EDITOR``"
section = "packaging"
level = "short"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    excl_args = subparser.add_mutually_exclusive_group()

    # Various types of Spack files that can be edited
    # Edits package files by default
    # build systems require separate logic to find
    excl_args.add_argument(
        "-b",
        "--build-system",
        dest="path",
        action="store_const",
        const="BUILD_SYSTEM",  # placeholder for path that requires computing late
        help="edit the build system with the supplied name or fullname",
    )
    excl_args.add_argument(
        "-c",
        "--command",
        dest="path",
        action="store_const",
        const=spack.paths.command_path,
        help="edit the command with the supplied name",
    )
    excl_args.add_argument(
        "-d",
        "--docs",
        dest="path",
        action="store_const",
        const=os.path.join(spack.paths.lib_path, "docs"),
        help="edit the docs with the supplied name",
    )
    excl_args.add_argument(
        "-t",
        "--test",
        dest="path",
        action="store_const",
        const=spack.paths.test_path,
        help="edit the test with the supplied name",
    )
    excl_args.add_argument(
        "-m",
        "--module",
        dest="path",
        action="store_const",
        const=spack.paths.module_path,
        help="edit the main spack module with the supplied name",
    )

    # Options for editing packages and build systems
    subparser.add_argument(
        "-r", "--repo", default=None, help="path to repo to edit package or build system in"
    )
    subparser.add_argument(
        "-N", "--namespace", default=None, help="namespace of package or build system to edit"
    )

    subparser.add_argument("package", nargs="*", default=None, help="package name")


def locate_package(name: str, repo: Optional[spack.repo.Repo]) -> str:
    # if not given a repo, use the full repo path to choose one
    repo_like: Union[spack.repo.Repo, spack.repo.RepoPath] = repo or spack.repo.PATH
    path: str = repo_like.filename_for_package_name(name)

    try:
        with open(path, "r", encoding="utf-8"):
            return path
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise spack.repo.UnknownPackageError(name) from e
        tty.die(f"Cannot edit package: {e}")


def locate_build_system(name: str, repo: Optional[spack.repo.Repo]) -> str:
    # If given a fullname for a build system, split it into namespace and name
    namespace = None
    if "." in name:
        namespace, name = name.rsplit(".", 1)

    # If given a namespace and a repo, they better match
    if namespace and repo:
        if repo.namespace != namespace:
            msg = f"{namespace}.{name}: namespace conflicts with repo '{repo.namespace}'"
            msg += " specified from --repo or --namespace argument"
            raise ValueError(msg)

    if namespace:
        repo = spack.repo.PATH.get_repo(namespace)

    # If not given a namespace, use the default
    if not repo:
        repo = spack.repo.PATH.first_repo()

    assert repo
    return locate_file(name, repo.build_systems_path)


def locate_file(name: str, path: str) -> str:
    # convert command names to python module name
    if path == spack.paths.command_path:
        name = spack.cmd.python_name(name)

    file_path = os.path.join(path, name)

    # Try to open direct match.
    try:
        with open(file_path, "r", encoding="utf-8"):
            return file_path
    except OSError as e:
        if e.errno != errno.ENOENT:
            tty.die(f"Cannot edit file: {e}")
        pass

    # Otherwise try to find a file that starts with the name
    candidates = glob.glob(file_path + "*")
    exclude_list = [".pyc", "~"]  # exclude binaries and backups
    files = [f for f in candidates if not any(f.endswith(ext) for ext in exclude_list)]
    if len(files) > 1:
        tty.die(
            f"Multiple files start with `{name}`:\n"
            + "\n".join(f"        {os.path.basename(f)}" for f in files)
        )
    elif not files:
        tty.die(f"No file for '{name}' was found in {path}")
    return files[0]


def edit(parser, args):
    names = args.package

    # If `--command`, `--test`, `--docs`, or `--module` is chosen, edit those instead
    if args.path and args.path != "BUILD_SYSTEM":
        paths = [locate_file(name, args.path) for name in names] if names else [args.path]
        spack.util.editor.editor(*paths)
        return

    # Cannot set repo = spack.repo.PATH.first_repo() as default because packages and build_systems
    # can include repo information as part of their fullname
    repo = None
    if args.namespace:
        repo = spack.repo.PATH.get_repo(args.namespace)
    elif args.repo:
        repo = spack.repo.from_path(args.repo)
    # default_repo used when no name provided
    default_repo = repo or spack.repo.PATH.first_repo()

    if args.path == "BUILD_SYSTEM":
        if names:
            paths = [locate_build_system(n, repo) for n in names]
        else:
            paths = [default_repo.build_systems_path]
        spack.util.editor.editor(*paths)
        return

    paths = [locate_package(n, repo) for n in names] if names else [default_repo.packages_path]
    spack.util.editor.editor(*paths)
