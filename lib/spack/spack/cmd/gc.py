# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd.common.arguments
import spack.cmd.uninstall
import spack.environment
import spack.store

description = "remove specs that are now no longer needed"
section = "build"
level = "short"


def setup_parser(subparser):
    spack.cmd.common.arguments.add_common_arguments(subparser, ['yes_to_all'])


def gc(parser, args):
    specs = spack.store.unused_specs()

    # If we are in an env context be sure to preserve root specs
    env = spack.environment.get_env(args=None, cmd_name='gc')
    if env:
        env.concretize()
        hashes = set([s.dag_hash() for x in env.roots()
                      for s in x.traverse(deptype=('link', 'run'))])
        if hashes:
            msg = 'Filtering out specs needed by the "{0}" environment'
            tty.msg(msg.format(env.name))
            specs = [s for s in specs if s.dag_hash() not in hashes]

    if not specs:
        msg = "There are no unused specs. Spack's store is clean."
        tty.msg(msg)
        return

    if not args.yes_to_all:
        spack.cmd.uninstall.confirmation_before_removal(specs)

    spack.cmd.uninstall.do_uninstall(None, specs, force=False)
