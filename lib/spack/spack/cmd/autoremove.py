# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    # Mock the attributes that spack uninstall expects
    args.all = False
    args.force = False
    args.dependents = False
    args.packages = []
    spack.cmd.uninstall.uninstall_specs(args, specs)
