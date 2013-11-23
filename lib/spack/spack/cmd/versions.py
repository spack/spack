import os
import re
from subprocess import CalledProcessError

import spack.packages as packages
from spack.colify import colify

description ="List available versions of a package"

def setup_parser(subparser):
    subparser.add_argument('package', metavar='PACKAGE', help='Package to list versions for')


def versions(parser, args):
    pkg = packages.get(args.package)
    colify(reversed(pkg.fetch_available_versions()))
