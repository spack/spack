# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import spack.cmd.style


description = spack.cmd.style.description
section = spack.cmd.style.section
level = spack.cmd.style.level


def setup_parser(subparser):
    spack.cmd.style.setup_parser(subparser)


def flake8(parser, args):
    print("=======================================================")
    print(
        "spack flake8 is deprecated, please use `spack style` to run style"
        + " checks"
    )
    print("=======================================================")
    return spack.cmd.style.style(parser, args)
