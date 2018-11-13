# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import llnl.util.tty as tty

import spack.cmd
import spack.repo

description = "revert checked out package source code"
section = "build"
level = "long"


def setup_parser(subparser):
    subparser.add_argument('packages', nargs=argparse.REMAINDER,
                           help="specs of packages to restage")


def restage(parser, args):
    if not args.packages:
        tty.die("spack restage requires at least one package spec.")

    specs = spack.cmd.parse_specs(args.packages, concretize=True)
    for spec in specs:
        package = spack.repo.get(spec)
        package.do_restage()
