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
        '-l', '--list', action='store_true', dest='list', help="Show available tests")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="verbose output")


def test(parser, args):
    if args.list:
        print "Available tests:"
        colify(list_modules(spack.test_path, directories=False))

    elif not args.names:
        for name in list_modules(spack.test_path, directories=False):
            print "Running Tests: %s" % name
            spack.test.run(name, verbose=args.verbose)

    else:
        for name in  args.names:
            spack.test.run(name, verbose=args.verbose)
