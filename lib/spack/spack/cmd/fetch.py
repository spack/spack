import spack.packages as packages

def setup_parser(subparser):
    subparser.add_argument('name', help="name of package to fetch")
    subparser.add_argument('-f', '--file', dest='file', default=None,
                           help="supply an archive file instead of fetching from the package's URL.")


def fetch(parser, args):
    package = packages.get(args.name)
    package.do_fetch()
