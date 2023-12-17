# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd.common.arguments
import spack.cmd.common.confirmation
import spack.cmd.uninstall
import spack.environment as ev
import spack.store

description = "remove specs that are now no longer needed"
section = "build"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        "-E",
        "--except-any-environment",
        action="store_true",
        help="remove everything unless needed by an environment",
    )
    subparser.add_argument(
        "-e",
        "--except-environment",
        metavar="ENV",
        action="append",
        default=[],
        help="remove everything unless needed by specified environment\n"
        "you can list multiple environments, or specify directory\n"
        "environments by path.",
    )
    subparser.add_argument(
        "-b",
        "--keep-build-dependencies",
        action="store_true",
        help="do not remove installed build-only dependencies of roots\n"
        "(default is to keep only link & run dependencies)",
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ["yes_to_all"])


def gc(parser, args):
    deptypes = ("link", "run")
    if args.keep_build_dependencies:
        deptypes += ("build",)

    active_env = ev.active_environment()

    # if we're using -E or -e, make a list of environments whose roots we should consider.
    all_environments = []

    # -E will garbage collect anything not needed by any env, including the current one
    if args.except_any_environment:
        all_environments += list(ev.all_environments())
        if active_env:
            all_environments.append(active_env)

    # -e says "also preserve things needed by this particular env"
    for env_name_or_dir in args.except_environment:
        all_environments.append(ev.read(env_name_or_dir))

    # add root hashes from all considered environments to list of roots
    root_hashes = set()
    for env in all_environments:
        root_hashes |= set(env.concretized_order)

    # if the user didn't specify they wanted to gc everything BUT particular envs,
    # do normal garbage collection.
    if not root_hashes:
        # only gc the current environment (note: `spack -e ENV gc -b` likely does nothing)
        if active_env:
            tty.msg(f"Restricting garbage collection to environment '{env.name}'")
            root_hashes = set(spack.store.STORE.db.all_hashes())  # keep everything
            root_hashes -= set(active_env.all_hashes())  # except this env
            root_hashes |= set(active_env.concretized_order)  # but keep its roots
        else:
            # consider all explicit specs roots (this is the default for db.unused_specs())
            root_hashes = None

    specs = spack.store.STORE.db.unused_specs(root_hashes=root_hashes, deptypes=deptypes)
    if not specs:
        tty.msg("There are no unused specs. Spack's store is clean.")
        return

    if not args.yes_to_all:
        spack.cmd.common.confirmation.confirm_action(specs, "uninstalled", "uninstall")

    spack.cmd.uninstall.do_uninstall(specs, force=False)
