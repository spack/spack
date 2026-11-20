# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import warnings

import spack.config
import spack.error
import spack.cmd
import spack.environment
import spack.spec
from spack.cmd.common import arguments

description = "change an existing spec in an environment"
section = "environments"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "-l",
        "--list-name",
        dest="list_name",
        default="specs",
        help="name of the list to remove abstract specs from",
    )
    subparser.add_argument(
        "--match-spec",
        dest="match_spec",
        help="change all specs matching match-spec (default is match by spec name)",
    )
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="change all matching abstract specs (allow changing more than one abstract spec)",
    )
    subparser.add_argument(
        "-c",
        "--concrete",
        action="store_true",
        default=False,
        help="change concrete specs in the environment",
    )
    subparser.add_argument(
        "-C",
        "--concrete-only",
        action="store_true",
        default=False,
        help="change only concrete specs in the environment",
    )
    arguments.add_common_arguments(subparser, ["specs"])
    subparser.add_argument(
        "--config",
        action="store_true",
        default=False,
        help="also apply the change to package config requirements (packages:name:require)",
    )


def change(parser, args):
    if args.all and args.concrete_only:
        warnings.warn("'spack change --all' argument is ignored with '--concrete-only'")
    if args.list_name != "specs" and args.concrete_only:
        warnings.warn("'spack change --list-name' argument is ignored with '--concrete-only'")

    env = spack.cmd.require_active_env(args.subparser)

    match_spec = None
    if args.match_spec:
        match_spec = spack.cmd.parse_specs([args.match_spec])[0]
    specs = spack.cmd.parse_specs(args.specs)

    # Check if spec list will change (without actually changing it yet)
    spec_will_change = False
    if not args.concrete_only:
        # Check if any specs match in the spec list
        list_to_check = env.spec_lists[args.list_name]
        check_match_spec = match_spec or (specs[0] if specs and specs[0].name else None)
        if check_match_spec:
            matches = [x for x in list_to_check if x.satisfies(check_match_spec)]
            spec_will_change = len(matches) > 0
    elif args.concrete or args.concrete_only:
        # Assume concrete changes will succeed
        spec_will_change = True

    # Apply config changes FIRST
    config_changed = False
    if args.config:
        from spack.cmd.config import _config_change

        for spec in specs:
            # Determine the package name for the config path
            # Use match_spec.name if available, otherwise spec.name
            if match_spec and match_spec.name:
                pkg_name = match_spec.name
            elif spec.name:
                pkg_name = spec.name
            else:
                # Anonymous spec without match_spec - can't determine package name
                continue

            # Construct config path: packages:name:require:spec
            config_path = f"packages:{pkg_name}:require:{str(spec)}"

            try:
                match_spec_str = str(match_spec) if match_spec else None
                # Only add new requirements if the spec list will NOT change
                # (if spec list will change, only modify existing config requirements)
                changed = _config_change(config_path, match_spec_str, add_if_no_match=not spec_will_change)
                config_changed = config_changed or changed
            except (ValueError, spack.error.ConfigError):
                # Config change failed or not applicable, continue
                pass

        # If config changed, reload the environment to pick up changes into yaml_content
        if config_changed:
            env = spack.environment.Environment(env.path)

    # Now apply spec list changes
    spec_changed = False
    with env.write_transaction():
        if not args.concrete_only:
            try:
                for spec in specs:
                    env.change_existing_spec(
                        spec,
                        list_name=args.list_name,
                        match_spec=match_spec,
                        allow_changing_multiple_specs=args.all,
                    )
                # change_existing_spec raises NoSpecsMatchedError if no specs match,
                # so if we got here, at least one abstract spec changed
                spec_changed = True
            except spack.environment.NoSpecsMatchedError as e:
                # No specs matched in the spec list
                if not args.config:
                    # No config flag and no spec matches → real error
                    msg = f"Cannot change abstract specs: {e}."
                    msg += " Try again with '--concrete-only' to change concrete specs only."
                    raise ValueError(msg) from e
                # else: --config flag set, so it's OK that spec list had no matches
            except (ValueError, spack.environment.SpackEnvironmentError) as e:
                # Other errors (multiple matches without --all, etc.) still fail
                msg = f"Cannot change abstract specs: {e}."
                msg += " Try again with '--concrete-only' to change concrete specs only."
                raise ValueError(msg) from e

        if args.concrete or args.concrete_only:
            selectors = []
            mutators = []
            for spec in specs:
                selectors.append(match_spec or spack.spec.Spec(spec.name))
                mutators.append(spec)

            env.mutate(selectors=selectors, mutators=mutators)

        env.write()

    # There are other cases where nothing changed (e.g. if we specified --concrete but
    # none of the lockfile specs matched), but this case is easy to detect and we might
    # as well warn when we do
    if not config_changed and not spec_changed and not (args.concrete or args.concrete_only):
        warnings.warn("No config requirements or spec list specs were changed")
