import argparse
import spack.cmd

import spack.tty as tty
import spack.url as url
import spack

description = "print out abstract and concrete versions of a spec."

def setup_parser(subparser):
    subparser.add_argument('specs', nargs=argparse.REMAINDER, help="specs of packages")

def spec(parser, args):
    for spec in spack.cmd.parse_specs(args.specs):
        print "Input spec"
        print "------------------------------"
        print spec.tree(color=True, indent=2)

        print "Normalized"
        print "------------------------------"
        spec.normalize()
        print spec.tree(color=True, indent=2)

        print "Concretized"
        print "------------------------------"
        spec.concretize()
        print spec.tree(color=True, indent=2)
