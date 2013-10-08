import os
import re
from subprocess import CalledProcessError

import spack
import spack.packages as packages
from spack.version import ver
from spack.colify import colify
import spack.url as url
import spack.tty as tty

description ="List spack packages"

def setup_parser(subparser):
    subparser.add_argument('-i', '--installed', action='store_true', dest='installed',
                           help='List installed packages for each platform along with versions.')


def list(parser, args):
    if args.installed:
        colify(str(pkg) for pkg in packages.installed_packages())
    else:
        colify(packages.all_package_names())
