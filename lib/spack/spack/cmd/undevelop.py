# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments

description = "remove specs from an environment"
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "-a", "--all", action="store_true", help="remove all specs from (clear) the environment"
    )

    # Note: by default we want to modify the environment scope, but
    # config.default_modify_scope may not refer to the environment at
    # the time this parser is instantiated
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar
    subparser.add_argument(
        "--scope", choices=scopes, metavar=scopes_metavar, help="configuration scope to modify"
    )

    arguments.add_common_arguments(subparser, ["specs"])


def undevelop(parser, args):
    # TODO: until it's possible to specify a full .yaml path as a scope, it
    # only makes sense to undevelop specs that are mentioned in the config
    # that is stored in spack.yaml
    env = spack.cmd.require_active_env(cmd_name="develop")

    # TODO: if a user undevelops something in their active environment, but
    # lower scope also specifies that the spec is being developed, the only
    # way to ensure that we don't consider it is to completely override the
    # lower scopes with "::". For now we simply tell the user that they must
    # edit this manually
    all_dev_specs = spack.config.get("develop")
    local_dev_specs = spack.config.get("develop", scope="env:" + env.name)

    if args.all:
        remove_specs = local_dev_specs.keys()
    else:
        remove_specs = spack.cmd.parse_specs(args.specs)

    for spec in remove_specs:
        if spec.name in local_dev_specs:
            tty.msg("Undevelop: removing {0}".format(spec.name))
            del local_dev_specs[spec.name]
        elif spec.name not in all_dev_specs:
            tty.msg("Undevelop: spec is not present: {0}".format(spec.name))

    spack.config.set("develop", local_dev_specs, scope="env:" + env.name)

    updated_all_dev_specs = spack.config.get("develop")
    remaining_dev_specs = set(x.name for x in remove_specs) & set(updated_all_dev_specs.keys())
    for spec in remove_specs:
        if spec in remaining_dev_specs:
            tty.msg(
                "Undevelop: {0} is marked as develop outside the environment "
                " configuration; it must be updated manually".format(spec.name)
            )
        else:
            tty.msg("Undevelop: removed {0}".format(spec.name))

    # We need to force a re-read of the env
    with env.write_transaction():
        pass
