# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import warnings

import spack.cmd.spec

description = "concretize a specs using an ASP solver"
section = "developer"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    spack.cmd.spec.setup_parser(subparser)


def solve(parser, args):
    msg = (
        "The `spack solve` command is deprecated in favor of options added to the "
        "`spack spec` command and will be removed in Spack v1.4"
    )
    warnings.warn(msg)

    spack.cmd.spec.spec(parser, args)
