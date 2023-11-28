# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
from typing import List

import llnl.util.tty as tty

import spack.cmd

display_args = {"long": True, "show_flags": False, "variants": False, "indent": 4}


def confirm_action(specs: List[spack.spec.Spec], participle: str, noun: str):
    """Display the list of specs to be acted on and ask for confirmation.

    Args:
        specs: specs to be removed
        participle: action expressed as a participle, e.g. "uninstalled"
        noun: action expressed as a noun, e.g. "uninstallation"
    """
    tty.msg(f"The following {len(specs)} packages will be {participle}:\n")
    spack.cmd.display_specs(specs, **display_args)
    print("")
    answer = tty.get_yes_or_no("Do you want to proceed?", default=False)
    if not answer:
        tty.msg(f"Aborting {noun}")
        sys.exit(0)
