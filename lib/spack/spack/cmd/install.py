import spack
import spack.packages as packages

description = "Build and install packages"

def setup_parser(subparser):
    subparser.add_argument('names', nargs='+', help="names of packages to install")
    subparser.add_argument('-i', '--ignore-dependencies',
                           action='store_true', dest='ignore_dependencies',
                           help="Do not try to install dependencies of requested packages.")
    subparser.add_argument('-d', '--dirty', action='store_true', dest='dirty',
                           help="Don't clean up partially completed build/installation on error.")

def install(parser, args):
    spack.ignore_dependencies = args.ignore_dependencies
    for name in args.names:
        package = packages.get(name)
        package.dirty = args.dirty
        package.do_install()
