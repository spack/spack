# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import sys
import warnings
from typing import List

import spack.cmd
import spack.cmd.common
import spack.environment.shell
import spack.store
import spack.user_environment as uenv
from spack.cmd.common import arguments
from spack.util.lang import dedupe

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

    hashes = uenv.loaded_hashes(os.environ)
    if args.specs:
        removed = list(
            dedupe(
                spack.cmd.disambiguate_spec_from_hashes(spec, hashes).dag_hash()
                for spec in spack.cmd.parse_specs(args.specs)
            )
        )
    else:
        removed = hashes

    if not args.shell:
        specs_str = " ".join(args.specs) or "SPECS"

        spack.cmd.common.shell_init_instructions(
            "spack unload", "    eval `spack unload {sh_arg}` %s" % specs_str
        )
        return 1

    record = spack.environment.shell.read_undo_record(os.environ)
    without_record = [h for h in removed if not uenv.unload(record, h)]
    if without_record:
        _warn_loaded_without_record(without_record)
    sys.stdout.write(uenv.shell_commands(record, args.shell, unloaded=removed))


def _warn_loaded_without_record(hashes: List[str]) -> None:
    specs = {s.dag_hash(): s for s in spack.store.STORE.db.query(hashes=hashes)}
    for dag_hash in hashes:
        spec = specs.get(dag_hash)
        label = spec.format("{name}{@version}{/hash:7}") if spec else f"/{dag_hash[:7]}"
        warnings.warn(
            f"{label} was loaded without an undo record, so its changes to environment variables "
            "are left in the shell"
        )
