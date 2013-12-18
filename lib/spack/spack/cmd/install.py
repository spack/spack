import sys
import argparse

import spack
import spack.packages as packages
import spack.cmd

description = "Build and install packages"

def setup_parser(subparser):
    subparser.add_argument('-i', '--ignore-dependencies',
                           action='store_true', dest='ignore_dependencies',
                           help="Do not try to install dependencies of requested packages.")
    subparser.add_argument('-d', '--dirty', action='store_true', dest='dirty',
                           help="Don't clean up staging area when install completes.")
    subparser.add_argument('packages', nargs=argparse.REMAINDER, help="specs of packages to install")


def install(parser, args):
    if not args.packages:
        tty.die("install requires at least one package argument")

    spack.ignore_dependencies = args.ignore_dependencies
    specs = spack.cmd.parse_specs(args.packages)
    for spec in specs:
        package = packages.get(spec.name)
        package.dirty = args.dirty
        package.do_install()
