import spack.packages as packages

def setup_parser(subparser):
    subparser.add_argument('name', help="name of package to clean")
    subparser.add_argument('-a', "--all", action="store_true", dest="all",
                           help="delete the entire stage directory")

def clean(args):
    package_class = packages.get(args.name)
    package = package_class()
    if args.all:
        package.do_clean_all()
    else:
        package.do_clean()


