# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os

import spack.cmd
import spack.cmd.common
import spack.error
import spack.hooks.cache_shell_script as shell_script
import spack.store
import spack.user_environment as uenv
from spack.cmd.common import arguments

description = "remove package from the user environment"
section = "user environment"
level = "short"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    """Parser is only constructed so that this prints a nice help
    message with -h."""
    arguments.add_common_arguments(subparser, ["installed_specs"])

    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        "--sh",
        action="store_const",
        dest="shell",
        const="sh",
        help="print sh commands to activate the environment",
    )
    shells.add_argument(
        "--csh",
        action="store_const",
        dest="shell",
        const="csh",
        help="print csh commands to activate the environment",
    )
    shells.add_argument(
        "--fish",
        action="store_const",
        dest="shell",
        const="fish",
        help="print fish commands to load the package",
    )
    shells.add_argument(
        "--bat",
        action="store_const",
        dest="shell",
        const="bat",
        help="print bat commands to load the package",
    )
    shells.add_argument(
        "--pwsh",
        action="store_const",
        dest="shell",
        const="pwsh",
        help="print pwsh commands to load the package",
    )

    subparser.add_argument(
        "-a", "--all", action="store_true", help="unload all loaded Spack packages"
    )


def _get_environment_modifications(spec, shell) -> str:
    """Find the environment modifcations for spec

    Args:
        spec: the spec package
        shell: user's shell
    """

    env_mod = uenv.environment_modifications_for_specs(spec)
    env_mod.remove_path(uenv.spack_loaded_hashes_var, spec.dag_hash())

    return env_mod.shell_modifications(shell)


def _create_unload_shell_script(cmds, unload_script_location):
    """Creates & writes environment modification for spec's unload shell script

    Args:
        cmds: the commands to write in script
        unload_script_location: where to write unload shell script
    """

    with open(unload_script_location, "w", encoding="utf-8") as f:
        f.write(cmds)


def unload(parser, args):
    """unload spack packages from the user environment"""
    if args.specs and args.all:
        raise spack.error.SpackError(
            "Cannot specify specs on command line when unloading all specs with '--all'"
        )

    hashes = os.environ.get(uenv.spack_loaded_hashes_var, "").split(os.pathsep)
    if args.specs:
        specs = [
            spack.cmd.disambiguate_spec_from_hashes(spec, hashes)
            for spec in spack.cmd.parse_specs(args.specs)
        ]
    else:
        specs = spack.store.STORE.db.query(hashes=hashes)

    if not args.shell:
        specs_str = " ".join(args.specs) or "SPECS"

        spack.cmd.common.shell_init_instructions(
            "spack unload", "    eval `spack unload {sh_arg}` %s" % specs_str
        )
        return 1

    shell = args.shell if args.shell else os.environ.get("SPACK_SHELL")

    for spec in specs:
        commands = ""

        if spec.external:
            commands = _get_environment_modifications(spec, shell)
        else:
            unload_script = shell_script.path_to_unload_shell_script(spec, shell)

            if not os.path.isfile(unload_script):
                mods = _get_environment_modifications(spec, shell)
                _create_unload_shell_script(mods, unload_script)
            commands = f"source {unload_script}"

        print(f"{commands}")
