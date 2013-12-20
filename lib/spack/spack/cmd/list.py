import spack.packages as packages
from spack.colify import colify

description ="List available spack packages"

def setup_parser(subparser):
    pass


def list(parser, args):
    # Print all the package names in columns
    colify(packages.all_package_names())

