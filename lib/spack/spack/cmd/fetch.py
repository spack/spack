import spack.packages as packages

description = "Fetch archives for packages"

def setup_parser(subparser):
    subparser.add_argument('names', nargs='+', help="names of packages to fetch")


def fetch(parser, args):
    for name in args.names:
        package = packages.get(name)
        package.do_fetch()
