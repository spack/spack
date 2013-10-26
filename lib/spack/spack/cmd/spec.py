import argparse
import spack.cmd

import spack.tty as tty
import spack

description = "parse specs and print them out to the command line."

def setup_parser(subparser):
    subparser.add_argument('specs', nargs=argparse.REMAINDER, help="specs of packages")

def spec(parser, args):
    specs = spack.cmd.parse_specs(args.specs)
    for spec in specs:
        spec.normalize()
        print spec.tree()

        spec.concretize()
        print spec.tree()
