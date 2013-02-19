import spack
import spack.packages as packages

def setup_parser(subparser):
    subparser.add_argument('names', nargs='+', help="name(s) of package(s) to install")
    subparser.add_argument('-i', '--ignore-dependencies',
                           action='store_true', dest='ignore_dependencies',
                           help="Do not try to install dependencies of requested packages.")

def install(args):
    spack.ignore_dependencies = args.ignore_dependencies
    for name in args.names:
        package = packages.get(name)
        package.do_install()
