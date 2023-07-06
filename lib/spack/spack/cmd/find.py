# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import copy
import sys

import llnl.util.lang
import llnl.util.tty as tty
import llnl.util.tty.color as color

import spack.bootstrap
import spack.cmd as cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.repo
from spack.database import InstallStatuses

description = "list and search installed packages"
section = "basic"
level = "short"


def setup_parser(subparser):
    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument(
        "--format",
        action="store",
        default=None,
        help="output specs with the specified format string",
    )
    format_group.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="output specs as machine-readable json records",
    )

    subparser.add_argument(
        "-d", "--deps", action="store_true", help="output dependencies along with found specs"
    )

    subparser.add_argument(
        "-p", "--paths", action="store_true", help="show paths to package install directories"
    )
    subparser.add_argument(
        "--groups",
        action="store_true",
        default=None,
        dest="groups",
        help="display specs in arch/compiler groups (default on)",
    )
    subparser.add_argument(
        "--no-groups",
        action="store_false",
        default=None,
        dest="groups",
        help="do not group specs by arch/compiler",
    )

    arguments.add_common_arguments(subparser, ["long", "very_long", "tags"])

    subparser.add_argument(
        "-c",
        "--show-concretized",
        action="store_true",
        help="show concretized specs in an environment",
    )
    subparser.add_argument(
        "-f",
        "--show-flags",
        action="store_true",
        dest="show_flags",
        help="show spec compiler flags",
    )
    subparser.add_argument(
        "--show-full-compiler",
        action="store_true",
        dest="show_full_compiler",
        help="show full compiler specs",
    )
    implicit_explicit = subparser.add_mutually_exclusive_group()
    implicit_explicit.add_argument(
        "-x",
        "--explicit",
        action="store_true",
        help="show only specs that were installed explicitly",
    )
    implicit_explicit.add_argument(
        "-X",
        "--implicit",
        action="store_true",
        help="show only specs that were installed as dependencies",
    )
    subparser.add_argument(
        "-u",
        "--unknown",
        action="store_true",
        dest="unknown",
        help="show only specs Spack does not have a package for",
    )
    subparser.add_argument(
        "-m",
        "--missing",
        action="store_true",
        dest="missing",
        help="show missing dependencies as well as installed specs",
    )
    subparser.add_argument(
        "-v",
        "--variants",
        action="store_true",
        dest="variants",
        help="show variants in output (can be long)",
    )
    subparser.add_argument(
        "--loaded", action="store_true", help="show only packages loaded in the user environment"
    )
    subparser.add_argument(
        "-M",
        "--only-missing",
        action="store_true",
        dest="only_missing",
        help="show only missing dependencies",
    )
    subparser.add_argument(
        "--deprecated",
        action="store_true",
        help="show deprecated packages as well as installed specs",
    )
    subparser.add_argument(
        "--only-deprecated", action="store_true", help="show only deprecated packages"
    )
    subparser.add_argument(
        "-N", "--namespace", action="store_true", help="show fully qualified package names"
    )

    subparser.add_argument("--start-date", help="earliest date of installation [YYYY-MM-DD]")
    subparser.add_argument("--end-date", help="latest date of installation [YYYY-MM-DD]")
    arguments.add_common_arguments(subparser, ["constraint"])


def query_arguments(args):
    # Set up query arguments.
    installed = []
    if not (args.only_missing or args.only_deprecated):
        installed.append(InstallStatuses.INSTALLED)
    if (args.deprecated or args.only_deprecated) and not args.only_missing:
        installed.append(InstallStatuses.DEPRECATED)
    if (args.missing or args.only_missing) and not args.only_deprecated:
        installed.append(InstallStatuses.MISSING)

    known = any
    if args.unknown:
        known = False

    explicit = any
    if args.explicit:
        explicit = True
    if args.implicit:
        explicit = False

    q_args = {"installed": installed, "known": known, "explicit": explicit}

    # Time window of installation
    for attribute in ("start_date", "end_date"):
        date = getattr(args, attribute)
        if date:
            q_args[attribute] = llnl.util.lang.pretty_string_to_date(date)

    return q_args


def setup_env(env):
    """Create a function for decorating specs when in an environment."""

    def strip_build(seq):
        return set(s.copy(deps=("link", "run")) for s in seq)

    added = set(strip_build(env.added_specs()))
    roots = set(strip_build(env.roots()))
    removed = set(strip_build(env.removed_specs()))

    def decorator(spec, fmt):
        # add +/-/* to show added/removed/root specs
        if any(spec.dag_hash() == r.dag_hash() for r in roots):
            return color.colorize("@*{%s}" % fmt)
        elif spec in removed:
            return color.colorize("@K{%s}" % fmt)
        else:
            return "%s" % fmt

    return decorator, added, roots, removed


def display_env(env, args, decorator, results):
    """Display extra find output when running in an environment.

    Find in an environment outputs 2 or 3 sections:

    1. Root specs
    2. Concretized roots (if asked for with -c)
    3. Installed specs

    """
    tty.msg("In environment %s" % env.name)

    if not env.user_specs:
        tty.msg("No root specs")
    else:
        tty.msg("Root specs")

        # Root specs cannot be displayed with prefixes, since those are not
        # set for abstract specs. Same for hashes
        root_args = copy.copy(args)
        root_args.paths = False

        # Roots are displayed with variants, etc. so that we can see
        # specifically what the user asked for.
        cmd.display_specs(
            env.user_specs,
            root_args,
            decorator=lambda s, f: color.colorize("@*{%s}" % f),
            namespace=True,
            show_flags=True,
            show_full_compiler=True,
            variants=True,
        )
        print()

    if args.show_concretized:
        tty.msg("Concretized roots")
        cmd.display_specs(env.specs_by_hash.values(), args, decorator=decorator)
        print()

    # Display a header for the installed packages section IF there are installed
    # packages. If there aren't any, we'll just end up printing "0 installed packages"
    # later.
    if results:
        tty.msg("Installed packages")


def find(parser, args):
    q_args = query_arguments(args)
    results = args.specs(**q_args)

    env = ev.active_environment()
    decorator = lambda s, f: f
    if env:
        decorator, _, roots, _ = setup_env(env)

    # use groups by default except with format.
    if args.groups is None:
        args.groups = not args.format

    # Exit early with an error code if no package matches the constraint
    if not results and args.constraint:
        msg = "No package matches the query: {0}"
        msg = msg.format(" ".join(args.constraint))
        tty.msg(msg)
        raise SystemExit(1)

    # If tags have been specified on the command line, filter by tags
    if args.tags:
        packages_with_tags = spack.repo.path.packages_with_tags(*args.tags)
        results = [x for x in results if x.name in packages_with_tags]

    if args.loaded:
        results = spack.cmd.filter_loaded_specs(results)

    # Display the result
    if args.json:
        cmd.display_specs_as_json(results, deps=args.deps)
    else:
        if not args.format:
            if env:
                display_env(env, args, decorator, results)

        cmd.display_specs(results, args, decorator=decorator, all_headers=True)

        # print number of installed packages last (as the list may be long)
        if sys.stdout.isatty() and args.groups:
            pkg_type = "loaded" if args.loaded else "installed"
            spack.cmd.print_how_many_pkgs(results, pkg_type)
