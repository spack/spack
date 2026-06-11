# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import sys

import spack.cmd
import spack.cmd.common
import spack.hooks.generate_spec_scripts as generate_script
import spack.llnl.util.tty as tty
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

    shell = args.shell if args.shell else os.environ.get("SPACK_SHELL")

    if not shell:
        specs_str = " ".join(args.specs) or "SPECS"

        spack.cmd.common.shell_init_instructions(
            "spack unload", "    eval `spack unload {sh_arg}` %s" % specs_str
        )
        return 1

    for spec in specs:
        commands = ""

        if spec.external:
            _, commands = generate_script.get_environment_modifications(spec, shell)
        else:
            unload_script_path = generate_script.path_to_unload_shell_script(spec, shell)

            if not os.path.isfile(unload_script_path):
                try:
                    repo_path = generate_script.make_repo_path(os.path.join(spec.prefix, ".spack"))
                    cached_repo = repo_path if repo_path.repos else None
                    _, mods = generate_script.get_environment_modifications(
                        spec, shell, cached_repo
                    )

                    comments = "::" if shell == "bat" else "###"
                    generate_script.generate_script(unload_script_path, mods, comments)
                except Exception as err:
                    tty.die(f"Error writing to {unload_script_path}\n{err}")

            if shell in ("csh", "fish"):
                commands = f"source {unload_script_path}\n"
            elif shell == "bat":
                commands = f"call {unload_script_path}\n"
            else:  # sh, pwsh
                commands = f". {unload_script_path}\n"

        sys.stdout.write(commands)
