import spack
import spack.packages as packages

description = "Build and install packages"

def setup_parser(subparser):
    subparser.add_argument('name', metavar="PACKAGE", help="name of packages to get info on")


def info(parser, args):
    package = packages.get(args.name)
    print "Homepage:  ", package.homepage
    print "Download:  ", package.url
