import argparse

import spack.cmd
import spack.packages as packages
import spack.tty as tty
import spack.stage as stage

description = "Remove staged files for packages"

def setup_parser(subparser):
    subparser.add_argument('-c', "--clean", action="store_true", dest='clean',
                           help="run make clean in the build directory (default)")
    subparser.add_argument('-w', "--work", action="store_true", dest='work',
                           help="delete the build directory and re-expand it from its archive.")
    subparser.add_argument('-d', "--dist", action="store_true", dest='dist',
                           help="delete the downloaded archive.")
    subparser.add_argument('packages', nargs=argparse.REMAINDER,
                           help="specs of packages to clean")


def clean(parser, args):
    if not args.packages:
        tty.die("spack clean requires at least one package argument")

    specs = spack.cmd.parse_specs(args.packages, concretize=True)
    for spec in specs:
        tty.message("Cleaning for spec:", spec)
        package = packages.get(spec.name)
        if args.dist:
            package.do_clean_dist()
        elif args.work:
            package.do_clean_work()
        else:
            package.do_clean()
