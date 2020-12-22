# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import llnl.util.tty as tty

import spack.cmd.style


description = (
    "The flake8 command is deprecated, but re-directs to "
    + "the style command for now\n"
    + spack.cmd.style.description
)
section = spack.cmd.style.section
level = spack.cmd.style.level


def setup_parser(subparser):
    spack.cmd.style.setup_parser(subparser)


def flake8(parser, args):
    tty.warn(
        "spack flake8 is deprecated", "please use `spack style` to run style checks"
    )
    return spack.cmd.style.style(parser, args)
