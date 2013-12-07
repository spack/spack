import spack
import spack.packages as packages
import spack.test
from spack.util.lang import list_modules
from spack.colify import colify
from pprint import pprint

description ="Run unit tests"

def setup_parser(subparser):
    subparser.add_argument(
        'names', nargs='*', help="Names of tests to run.")
    subparser.add_argument(
        '-l', '--list', action='store_true', dest='list', help="Show available tests")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="verbose output")


def test(parser, args):
    if args.list:
        print "Available tests:"
        colify(spack.test.list_tests(), indent=2)

    else:
        spack.test.run(args.names, args.verbose)
