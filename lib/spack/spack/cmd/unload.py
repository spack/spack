# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import sys

import spack.cmd
import spack.cmd.common
import spack.hooks.generate_spec_scripts as spec_script
import spack.store
import spack.user_environment as uenv
import spack.util.tty as tty
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
        args.subparser.error(
            "cannot specify specs on command line when unloading all specs with '--all'"
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
            _, commands = spec_script.get_environment_modifications(spec, shell)
        else:
            unload_script_path = spec_script.path_to_unload_shell_script(spec, shell)

            if not os.path.isfile(unload_script_path):
                spack_dir = os.path.join(spec.prefix, ".spack")

                try:
                    # Try to get cached repo if it exists
                    cached_repo = None
                    if os.path.isdir(spack_dir):
                        repo_path = spec_script.make_repo_path(spack_dir)
                        cached_repo = repo_path if repo_path and repo_path.repos else None

                    _, mods = spec_script.get_environment_modifications(spec, shell, cached_repo)
                except Exception as err:
                    tty.die(f"Error generating environment modifications for {spec}:\n{err}")
                try:
                    spec_script.write_script(unload_script_path, mods, shell)
                except Exception as err:
                    tty.debug(f"Error writing to {unload_script_path}\n{err}")
                    sys.stdout.write(mods)
                    return 1
            commands = spec_script.source_script(unload_script_path, shell)

        sys.stdout.write(commands)
