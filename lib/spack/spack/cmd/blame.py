# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import pathlib
import re
import sys
from typing import Optional, Union

import spack.config
import spack.llnl.util.tty as tty
import spack.repo
import spack.util.git
import spack.util.spack_json as sjson
from spack.cmd import spack_is_git_repo
from spack.llnl.util.filesystem import working_dir
from spack.llnl.util.lang import pretty_date
from spack.llnl.util.tty.colify import colify_table
from spack.util.executable import ProcessError

description = "show contributors to packages"
section = "developer"
level = "long"

git = spack.util.git.git(required=True)


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    view_group = subparser.add_mutually_exclusive_group()
    view_group.add_argument(
        "-t",
        "--time",
        dest="view",
        action="store_const",
        const="time",
        default="time",
        help="sort by last modification date (default)",
    )
    view_group.add_argument(
        "-p",
        "--percent",
        dest="view",
        action="store_const",
        const="percent",
        help="sort by percent of code",
    )
    view_group.add_argument(
        "-g",
        "--git",
        dest="view",
        action="store_const",
        const="git",
        help="show git blame output instead of summary",
    )
    subparser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="output blame as machine-readable json records",
    )

    subparser.add_argument(
        "package_or_file",
        help="name of package to show contributions for, or path to a file in the spack repo",
    )


def print_table(rows, last_mod, total_lines, emails):
    """
    Given a set of rows with authors and lines, print a table.
    """
    table = [["LAST_COMMIT", "LINES", "%", "AUTHOR", "EMAIL"]]
    for author, nlines in rows:
        table += [
            [
                pretty_date(last_mod[author]),
                nlines,
                round(nlines / float(total_lines) * 100, 1),
                author,
                emails[author],
            ]
        ]

    table += [[""] * 5]
    table += [[pretty_date(max(last_mod.values())), total_lines, "100.0"] + [""] * 3]

    colify_table(table)


def dump_json(rows, last_mod, total_lines, emails):
    """
    Dump the blame as a json object to the terminal.
    """
    result = {}
    authors = []
    for author, nlines in rows:
        authors.append(
            {
                "last_commit": pretty_date(last_mod[author]),
                "lines": nlines,
                "percentage": round(nlines / float(total_lines) * 100, 1),
                "author": author,
                "email": emails[author],
            }
        )

    result["authors"] = authors
    result["totals"] = {
        "last_commit": pretty_date(max(last_mod.values())),
        "lines": total_lines,
        "percentage": "100.0",
    }

    sjson.dump(result, sys.stdout)


def git_prefix(path: Union[str, pathlib.Path]) -> Optional[pathlib.Path]:
    """Return the top level directory if path is under a git repository.

    Args:
      path: path of the item presumably under a git repository

    Returns: path to the root of the git repository
    """
    if not os.path.exists(path):
        return None

    work_dir = path if os.path.isdir(path) else os.path.dirname(path)
    with working_dir(work_dir):
        try:
            result = git("rev-parse", "--show-toplevel", output=str, error=str)
            return pathlib.Path(result.split("\n")[0])
        except ProcessError:
            tty.die(f"'{path}' is not in a git repository.")


def package_repo_root(path: Union[str, pathlib.Path]) -> Optional[pathlib.Path]:
    """Find the appropriate package repository's git root directory.

    Provides a warning for a remote package repository since there is a risk that
    the blame results are inaccurate.

    Args:
      path: path to an arbitrary file presumably in one of the spack package repos

    Returns: path to the package repository's git root directory or None
    """
    descriptors = spack.repo.RepoDescriptors.from_config(
        lock=spack.repo.package_repository_lock(), config=spack.config.CONFIG
    )
    path = pathlib.Path(path)
    prefix: Optional[pathlib.Path] = None
    for _, desc in descriptors.items():
        # Handle the remote case, whose destination is by definition the git root
        if hasattr(desc, "destination"):
            repo_dest = pathlib.Path(desc.destination)
            if (repo_dest / ".git").exists():
                prefix = repo_dest

                # TODO: replace check with `is_relative_to` once supported
                if prefix and str(path).startswith(str(prefix)):
                    return prefix

        # Handle the local repository case, making sure it's a spack repository.
        if hasattr(desc, "path"):
            repo_path = pathlib.Path(desc.path)
            if "spack_repo" in repo_path.parts:
                prefix = git_prefix(repo_path)

                # TODO: replace check with `is_relative_to` once supported
                if prefix and str(path).startswith(str(prefix)):
                    return prefix

    return None


def git_supports_unshallow() -> bool:
    output = git("fetch", "--help", output=str, error=str)
    return "--unshallow" in output


def ensure_full_history(prefix: str, path: str) -> None:
    """Ensure the git repository at the prefix has its full history.

    Args:
        prefix: the root directory of the git repository
        path: the package or file name under consideration (for messages)
    """
    assert os.path.isdir(prefix)

    with working_dir(prefix):
        shallow_dir = os.path.join(prefix, ".git", "shallow")
        if os.path.isdir(shallow_dir):
            if git_supports_unshallow():
                try:
                    # Capture the error output (e.g., irrelevant for full repo)
                    # to ensure the output is clean.
                    git("fetch", "--unshallow", error=str)
                except ProcessError as e:
                    tty.die(
                        f"Cannot report blame for {path}.\n"
                        "Unable to retrieve the full git history for "
                        f'{prefix} due to "{str(e)}" error.'
                    )
            else:
                tty.die(
                    f"Cannot report blame for {path}.\n"
                    f"Unable to retrieve the full git history for {prefix}. "
                    "Use a newer 'git' that supports 'git fetch --unshallow'."
                )


def blame(parser, args):
    # make sure this is a git repo
    if not spack_is_git_repo():
        tty.die("This spack is not a git clone. You cannot use 'spack blame'.")

    # Get the name of the path to blame and its repository prefix
    # so we can honor any .git-blame-ignore-revs that may be present.
    blame_file = None
    prefix = None
    if os.path.exists(args.package_or_file):
        blame_file = os.path.realpath(args.package_or_file)
        prefix = package_repo_root(blame_file)

    # Get path to what we assume is a package (including to a cached version
    # of a remote package repository.)
    if not blame_file:
        try:
            blame_file = spack.repo.PATH.filename_for_package_name(args.package_or_file)
        except spack.repo.UnknownNamespaceError:
            # the argument is not a package (or does not exist)
            pass

        if blame_file and os.path.isfile(blame_file):
            prefix = package_repo_root(blame_file)

    if not blame_file or not os.path.exists(blame_file):
        tty.die(f"'{args.package_or_file}' does not exist.")

    if prefix is None:
        tty.msg(f"'{args.package_or_file}' is not within a spack package repository")

    path_prefix = git_prefix(blame_file)
    if path_prefix != prefix:
        # You are attempting to get 'blame' for a path outside of a configured
        # package repository (e.g., within a spack/spack clone). We'll use the
        # path's prefix instead to ensure working under the proper git
        # repository.
        prefix = path_prefix

    # Make sure we can get the full/known blame even when the repository
    # is remote.
    ensure_full_history(prefix, args.package_or_file)

    # Get blame information for the path EVEN when it is located in a different
    # spack repository (e.g., spack/spack-packages) or a different git
    # repository.
    with working_dir(prefix):
        # Now we can get the blame results.
        options = ["blame"]

        # ignore the great black reformatting of 2022
        ignore_file = prefix / ".git-blame-ignore-revs"
        if ignore_file.exists():
            options.extend(["--ignore-revs-file", str(ignore_file)])

        try:
            if args.view == "git":
                options.append(str(blame_file))
                git(*options)
                return
            else:
                options.extend(["--line-porcelain", str(blame_file)])
                output = git(*options, output=str, error=str)
                lines = output.split("\n")
        except ProcessError as err:
            # e.g., blame information is not tracked if the path is a directory
            tty.die(f"Blame information is not tracked for '{blame_file}':\n{err.long_message}")

    # Histogram authors
    counts = {}
    emails = {}
    last_mod = {}
    total_lines = 0
    for line in lines:
        match = re.match(r"^author (.*)", line)
        if match:
            author = match.group(1)

        match = re.match(r"^author-mail (.*)", line)
        if match:
            email = match.group(1)

        match = re.match(r"^author-time (.*)", line)
        if match:
            mod = int(match.group(1))
            last_mod[author] = max(last_mod.setdefault(author, 0), mod)

        # ignore comments
        if re.match(r"^\t[^#]", line):
            counts[author] = counts.setdefault(author, 0) + 1
            emails.setdefault(author, email)
            total_lines += 1

    if args.view == "time":
        rows = sorted(counts.items(), key=lambda t: last_mod[t[0]], reverse=True)
    else:  # args.view == 'percent'
        rows = sorted(counts.items(), key=lambda t: t[1], reverse=True)

    # Dump as json
    if args.json:
        dump_json(rows, last_mod, total_lines, emails)

    # Print a nice table with authors and emails
    else:
        print_table(rows, last_mod, total_lines, emails)
