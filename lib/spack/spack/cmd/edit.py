# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import errno
import glob
import os

import spack.cmd
import spack.llnl.util.tty as tty
import spack.paths
import spack.repo
import spack.util.editor

description = "open package files in $EDITOR"
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


def locate_package(name: str, repo: spack.repo.Repo) -> str:
    path = repo.filename_for_package_name(name)

    try:
        with open(path, "r", encoding="utf-8"):
            return path
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise spack.repo.UnknownPackageError(name) from e
        tty.die(f"Cannot edit package: {e}")


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


def repo_from_args(args):
    if args.repo:
        return spack.repo.from_path(args.repo)
    elif args.namespace:
        return spack.repo.PATH.get_repo(args.namespace)
    elif args.package and not args.path:
        # for package names, we can take a RepoPath and find which repo they're in
        return spack.repo.PATH
    else:
        # If there's a fullname for a build system, use the first one
        for name in args.package:
            if "." in name:
                return spack.repo.PATH.get_repo(name.rsplit(".", 1)[0])
        # for build systems or packages_path, just take the first repo
        return spack.repo.PATH.first_repo()


def edit(parser, args):
    names = args.package

    # If `--command`, `--test`, `--docs`, or `--module` is chosen, edit those instead
    if args.path and args.path != "BUILD_SYSTEM":
        paths = [locate_file(name, args.path) for name in names] if names else [args.path]
        spack.util.editor.editor(*paths)
        return

    repo = repo_from_args(args)
    if args.path == "BUILD_SYSTEM":
        # Ignore namespaces -- we've already found the repo
        names = [name.rsplit(".", 1)[-1] for name in names]
        root = repo.build_systems_path
        paths = [locate_file(name, root) for name in names] if names else [root]
        spack.util.editor.editor(*paths)
    elif names:
        paths = [locate_package(name, repo) for name in names]
        spack.util.editor.editor(*paths)
    else:
        # By default open the directory where packages live
        spack.util.editor.editor(repo.packages_path)
