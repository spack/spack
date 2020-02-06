# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.cmd.dev_build
import llnl.util.tty as tty

description = "DEPRECATED: do-it-yourself: build from local source directory"
section = "build"
level = "long"


def setup_parser(subparser):
    spack.cmd.dev_build.setup_parser(subparser)


def diy(self, args):
    tty.warn("`spack diy` has been renamed to `spack dev-build`."
             "The `diy` command will be removed in a future version of Spack")
    spack.cmd.dev_build.dev_build(self, args)
