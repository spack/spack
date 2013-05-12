import argparse
import spack.cmd
import spack.packages as packages

description = "Fetch archives for packages"

def setup_parser(subparser):
    subparser.add_argument('packages', nargs=argparse.REMAINDER, help="specs of packages to fetch")


def fetch(parser, args):
    if not args.packages:
        tty.die("fetch requires at least one package argument")

    specs = spack.cmd.parse_specs(args.packages)
    for spec in specs:
        package = packages.get(spec.name)
        package.do_fetch()
