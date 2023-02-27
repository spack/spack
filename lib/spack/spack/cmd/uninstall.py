# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import sys

from llnl.util import tty
from llnl.util.tty.colify import colify

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.error
import spack.package_base
import spack.repo
import spack.store
import spack.traverse as traverse
from spack.database import InstallStatuses

description = "remove installed packages"
section = "build"
level = "short"

error_message = """You can either:
    a) use a more specific spec, or
    b) specify the spec by its hash (e.g. `spack uninstall /hash`), or
    c) use `spack uninstall --all` to uninstall ALL matching specs.
"""

# Arguments for display_specs when we find ambiguity
display_args = {"long": True, "show_flags": False, "variants": False, "indent": 4}


def setup_parser(subparser):
    epilog_msg = (
        "Specs to be uninstalled are specified using the spec syntax"
        " (`spack help --spec`) and can be identified by their "
        "hashes. To remove packages that are needed only at build "
        "time and were not explicitly installed see `spack gc -h`."
        "\n\nWhen using the --all option ALL packages matching the "
        "supplied specs will be uninstalled. For instance, "
        "`spack uninstall --all libelf` uninstalls all the versions "
        "of `libelf` currently present in Spack's store. If no spec "
        "is supplied, all installed packages will be uninstalled. "
        "If used in an environment, all packages in the environment "
        "will be uninstalled."
    )
    subparser.epilog = epilog_msg
    subparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        dest="force",
        help="remove regardless of whether other packages or environments " "depend on this one",
    )
    subparser.add_argument(
        "--remove",
        action="store_true",
        dest="remove",
        help="if in an environment, then the spec should also be removed from "
        "the environment description",
    )
    arguments.add_common_arguments(
        subparser, ["recurse_dependents", "yes_to_all", "installed_specs"]
    )
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="all",
        help="remove ALL installed packages that match each supplied spec",
    )
    subparser.add_argument(
        "--origin", dest="origin", help="only remove DB records with the specified origin"
    )


def find_matching_specs(env, specs, allow_multiple_matches=False, force=False, origin=None):
    """Returns a list of specs matching the not necessarily
       concretized specs given from cli

    Args:
        env (spack.environment.Environment): active environment, or ``None``
            if there is not one
        specs (list): list of specs to be matched against installed packages
        allow_multiple_matches (bool): if True multiple matches are admitted

    Return:
        list: list of specs
    """
    # constrain uninstall resolution to current environment if one is active
    hashes = env.all_hashes() if env else None

    # List of specs that match expressions given via command line
    specs_from_cli = []
    has_errors = False
    for spec in specs:
        install_query = [InstallStatuses.INSTALLED, InstallStatuses.DEPRECATED]
        matching = spack.store.db.query_local(
            spec, hashes=hashes, installed=install_query, origin=origin
        )
        # For each spec provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matching) > 1:
            tty.error("{0} matches multiple packages:".format(spec))
            sys.stderr.write("\n")
            spack.cmd.display_specs(matching, output=sys.stderr, **display_args)
            sys.stderr.write("\n")
            sys.stderr.flush()
            has_errors = True

        # No installed package matches the query
        if len(matching) == 0 and spec is not any:
            if env:
                pkg_type = "packages in environment '%s'" % env.name
            else:
                pkg_type = "installed packages"
            tty.die("{0} does not match any {1}.".format(spec, pkg_type))

        specs_from_cli.extend(matching)

    if has_errors:
        tty.die(error_message)

    return specs_from_cli


def installed_runtime_dependents(specs, env):
    """Map each spec to a list of its installed dependents.

    Args:
        specs (list): list of Specs
        env (spack.environment.Environment or None): the active environment, or None

    Returns:
        tuple: two mappings: one from specs to their dependent installs in the
        active environment, and one from specs to dependent installs outside of
        the active environment.

        Every installed dependent spec is listed once.

        If there is not current active environment, the first mapping will be
        empty.
    """
    active_dpts = {}
    outside_dpts = {}

    env_hashes = set(env.all_hashes()) if env else set()

    # Ensure we stop traversal at input specs.
    visited = set(s.dag_hash() for s in specs)

    for spec in specs:
        for dpt in traverse.traverse_nodes(
            spec.dependents(deptype=("link", "run")),
            direction="parents",
            visited=visited,
            deptype=("link", "run"),
            root=True,
            key=lambda s: s.dag_hash(),
        ):
            hash = dpt.dag_hash()
            # Ensure that all the specs we get are installed
            record = spack.store.db.query_local_by_spec_hash(hash)
            if record is None or not record.installed:
                continue
            if hash in env_hashes:
                active_dpts.setdefault(spec, set()).add(dpt)
            else:
                outside_dpts.setdefault(spec, set()).add(dpt)

    return active_dpts, outside_dpts


def dependent_environments(specs):
    """Map each spec to environments that depend on it.

    Args:
        specs (list): list of Specs

    Returns:
        dict: mapping from spec to lists of dependent Environments
    """
    dependents = {}
    for env in ev.all_environments():
        hashes = set(env.all_hashes())
        for spec in specs:
            if spec.dag_hash() in hashes:
                dependents.setdefault(spec, []).append(env)
    return dependents


def inactive_dependent_environments(spec_envs):
    """Strip the active environment from a dependent map.

    Take the output of ``dependent_environment()`` and remove the active
    environment from all mappings.  Remove any specs in the map that now
    have no dependent environments.  Return the result.

    Args:
        spec_envs (dict): mapping from spec to lists of dependent Environments

    Returns:
        dict: mapping from spec to lists of *inactive* dependent Environments
    """
    spec_inactive_envs = {}
    for spec, de_list in spec_envs.items():
        inactive = [de for de in de_list if not de.active]
        if inactive:
            spec_inactive_envs[spec] = inactive

    return spec_inactive_envs


def _remove_from_env(spec, env):
    """Remove a spec from an environment if it is a root."""
    try:
        # try removing the spec from the current active
        # environment. this will fail if the spec is not a root
        env.remove(spec, force=True)
    except ev.SpackEnvironmentError:
        pass  # ignore non-root specs


def do_uninstall(specs, force=False):
    # TODO: get rid of the call-sites that use this function,
    # so that we don't have to do a dance of list -> set -> list -> set
    hashes_to_remove = set(s.dag_hash() for s in specs)

    for s in traverse.traverse_nodes(
        specs, order="topo", direction="children", root=True, cover="nodes", deptype="all"
    ):
        if s.dag_hash() in hashes_to_remove:
            spack.package_base.PackageBase.uninstall_by_spec(s, force=force)


def get_uninstall_list(args, specs, env):
    """Returns uninstall_list and remove_list: these may overlap (some things
    may be both uninstalled and removed from the current environment).

    It is assumed we are in an environment if --remove is specified (this
    method raises an exception otherwise).

    uninstall_list is topologically sorted: dependents come before
    dependencies (so if a user uninstalls specs in the order provided,
    the dependents will always be uninstalled first).
    """
    if args.remove and not env:
        raise ValueError("Can only use --remove when in an environment")

    # Gets the list of installed specs that match the ones given via cli
    # args.all takes care of the case where '-a' is given in the cli
    base_uninstall_specs = set(find_matching_specs(env, specs, args.all, args.force))

    active_dpts, outside_dpts = installed_runtime_dependents(base_uninstall_specs, env)
    # It will be useful to track the unified set of specs with dependents, as
    # well as to separately track specs in the current env with dependents
    spec_to_dpts = {}
    for spec, dpts in active_dpts.items():
        spec_to_dpts[spec] = list(dpts)
    for spec, dpts in outside_dpts.items():
        if spec in spec_to_dpts:
            spec_to_dpts[spec].extend(dpts)
        else:
            spec_to_dpts[spec] = list(dpts)

    all_uninstall_specs = set(base_uninstall_specs)
    if args.dependents:
        for spec, lst in active_dpts.items():
            all_uninstall_specs.update(lst)
        for spec, lst in outside_dpts.items():
            all_uninstall_specs.update(lst)

    # For each spec that we intend to uninstall, this tracks the set of
    # environments outside the current active environment which depend on the
    # spec. There may be environments not managed directly with Spack: such
    # environments would not be included here.
    spec_to_other_envs = inactive_dependent_environments(
        dependent_environments(all_uninstall_specs)
    )

    has_error = not args.force and (
        # There are dependents in the current env and we didn't ask to remove
        # dependents
        (spec_to_dpts and not args.dependents)
        # An environment different than the current env (if any) depends on
        # one or more of the specs to be uninstalled. There may also be
        # packages in those envs which depend on the base set of packages
        # to uninstall, but this covers that scenario.
        or (not args.remove and spec_to_other_envs)
    )

    if has_error:
        # say why each problem spec is needed
        specs = set(spec_to_dpts)
        specs.update(set(spec_to_other_envs))  # environments depend on this

        for i, spec in enumerate(sorted(specs)):
            # space out blocks of reasons
            if i > 0:
                print()

            spec_format = "{name}{@version}{%compiler}{/hash:7}"
            tty.info("Will not uninstall %s" % spec.cformat(spec_format), format="*r")

            dependents = spec_to_dpts.get(spec)
            if dependents and not args.dependents:
                print("The following packages depend on it:")
                spack.cmd.display_specs(dependents, **display_args)

            envs = spec_to_other_envs.get(spec)
            if envs:
                if env:
                    env_context_qualifier = " other"
                else:
                    env_context_qualifier = ""
                print("It is used by the following{0} environments:".format(env_context_qualifier))
                colify([e.name for e in envs], indent=4)

        msgs = []
        if spec_to_dpts and not args.dependents:
            msgs.append("use `spack uninstall --dependents` to remove dependents too")
        if spec_to_other_envs:
            msgs.append("use `spack env remove` to remove from environments")
        print()
        tty.die("There are still dependents.", *msgs)

    # If we are in an environment, this will track specs in this environment
    # which should only be removed from the environment rather than uninstalled
    remove_only = set()
    if args.remove and not args.force:
        remove_only.update(spec_to_other_envs)
    if remove_only:
        tty.info(
            "The following specs will be removed but not uninstalled because"
            " they are also used by another environment: {speclist}".format(
                speclist=", ".join(x.name for x in remove_only)
            )
        )

    # Compute the set of specs that should be removed from the current env.
    # This may overlap (some specs may be uninstalled and also removed from
    # the current environment).
    if args.remove:
        remove_specs = set(base_uninstall_specs)
        if args.dependents:
            # Any spec matched from the cli, or dependent of, should be removed
            # from the environment
            for spec, lst in active_dpts.items():
                remove_specs.update(lst)
    else:
        remove_specs = set()

    all_uninstall_specs -= remove_only
    # Inefficient topological sort: uninstall dependents before dependencies
    all_uninstall_specs = sorted(
        all_uninstall_specs, key=lambda x: sum(1 for i in x.traverse()), reverse=True
    )

    return list(all_uninstall_specs), list(remove_specs)


def uninstall_specs(args, specs):
    env = ev.active_environment()

    uninstall_list, remove_list = get_uninstall_list(args, specs, env)

    if not uninstall_list:
        tty.warn("There are no package to uninstall.")
        return

    if not args.yes_to_all:
        confirm_removal(uninstall_list)

    # Uninstall everything on the list
    do_uninstall(uninstall_list, args.force)

    if env:
        with env.write_transaction():
            for spec in remove_list:
                _remove_from_env(spec, env)
            env.write()

        env.regenerate_views()


def confirm_removal(specs):
    """Display the list of specs to be removed and ask for confirmation.

    Args:
        specs (list): specs to be removed
    """
    tty.msg("The following packages will be uninstalled:\n")
    spack.cmd.display_specs(specs, **display_args)
    print("")
    answer = tty.get_yes_or_no("Do you want to proceed?", default=False)
    if not answer:
        tty.msg("Aborting uninstallation")
        sys.exit(0)


def uninstall(parser, args):
    if not args.specs and not args.all:
        tty.die(
            "uninstall requires at least one package argument.",
            "  Use `spack uninstall --all` to uninstall ALL packages.",
        )

    # [any] here handles the --all case by forcing all specs to be returned
    specs = spack.cmd.parse_specs(args.specs) if args.specs else [any]
    uninstall_specs(args, specs)
