import argparse

import spack.cmd
import spack.packages as packages

description = "Fetch archives for packages"

def setup_parser(subparser):
    subparser.add_argument(
        '-n', '--no-checksum', action='store_true', dest='no_checksum',
        help="Do not check packages against checksum")
    subparser.add_argument(
        'packages', nargs=argparse.REMAINDER, help="specs of packages to fetch")


def fetch(parser, args):
    if not args.packages:
        tty.die("fetch requires at least one package argument")

    if args.no_checksum:
        spack.do_checksum = False

    specs = spack.cmd.parse_specs(args.packages, concretize=True)
    for spec in specs:
        package = packages.get(spec)
        package.do_fetch()
