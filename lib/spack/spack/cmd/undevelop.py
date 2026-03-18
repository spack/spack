# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import spack.cmd
import spack.config
import spack.llnl.util.tty as tty
import spack.spec
from spack.cmd.common import arguments

description = "remove specs from an environment"
section = "environments"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "--no-modify-concrete-specs",
        action="store_false",
        dest="apply_changes",
        help=(
            "do not mutate concrete specs to remove dev_path provenance."
            " This requires running `spack concretize -f` later to apply changes to concrete specs"
        ),
    )

    subparser.add_argument(
        "-a", "--all", action="store_true", help="remove all specs from (clear) the environment"
    )

    arguments.add_common_arguments(subparser, ["specs"])


def _update_config(specs_to_remove):
    def change_fn(dev_config):
        modified = False
        for spec in specs_to_remove:
            if spec.name in dev_config:
                tty.msg("Undevelop: removing {0}".format(spec.name))
                del dev_config[spec.name]
                modified = True
        return modified

    spack.config.update_all("develop", change_fn)


def undevelop(parser, args):
    # TODO: when https://github.com/spack/spack/pull/35307 is merged,
    # an active env is not required if a scope is specified
    env = spack.cmd.require_active_env(cmd_name="undevelop")

    if args.all:
        remove_specs = [spack.spec.Spec(s) for s in env.dev_specs]
    else:
        remove_specs = spack.cmd.parse_specs(args.specs)

    with env.write_transaction():
        _update_config(remove_specs)
        if args.apply_changes:
            for spec in remove_specs:
                env.apply_develop(spec, path=None)

    updated_all_dev_specs = set(spack.config.get("develop"))

    remove_spec_names = set(x.name for x in remove_specs)
    not_fully_removed = updated_all_dev_specs & remove_spec_names

    if not_fully_removed:
        tty.msg(
            "The following specs could not be removed as develop specs"
            " - see `spack config blame develop` to locate files requiring"
            f" manual edits: {', '.join(not_fully_removed)}"
        )
