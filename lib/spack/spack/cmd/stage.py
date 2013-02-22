import spack.packages as packages

description="Expand downloaded archive in preparation for install"

def setup_parser(subparser):
    subparser.add_argument('name', help="name of package to stage")

def stage(parser, args):
    package = packages.get(args.name)
    package.do_stage()
