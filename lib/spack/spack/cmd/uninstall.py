import spack.packages as packages

def setup_parser(subparser):
    subparser.add_argument('name', help="name of package to uninstall")

def uninstall(args):
    package_class = packages.get(args.name)
    package = package_class()
    package.do_uninstall()
