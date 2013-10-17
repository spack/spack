import spack
import spack.packages as packages
import spack.test
from spack.util.lang import list_modules
from spack.colify import colify
from pprint import pprint

description ="Run unit tests"

def setup_parser(subparser):
    subparser.add_argument(
        'names', nargs='*', help="Names of packages to install")
    subparser.add_argument(
        '-a', '--all', action='store_true', dest='all', help="Run all tests")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="verbose output")


def test(parser, args):
    if args.all:
        for name in list_modules(spack.test_path, directories=False):
            print "Running Tests: %s" % name
            spack.test.run(name, verbose=args.verbose)

    elif not args.names:
        print "Available tests:"
        colify(list_modules(spack.test_path, directories=False))

    else:
        for name in  args.names:
            spack.test.run(name, verbose=args.verbose)
