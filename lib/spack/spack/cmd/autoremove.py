# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.store
import spack.cmd.common.arguments
import spack.cmd.uninstall

description = "remove specs that are now no longer needed"
section = "build"
level = "short"


def setup_parser(subparser):
    spack.cmd.common.arguments.add_common_arguments(subparser, ['yes_to_all'])


def autoremove(parser, args):
    specs = spack.store.unused_specs()
    if not specs:
        msg = "There are no unused specs. Spack's store is clean."
        tty.msg(msg)
        return

    if not args.yes_to_all:
        spack.cmd.uninstall.confirmation_before_removal(specs)

    spack.cmd.uninstall.do_uninstall(None, specs, force=False)
