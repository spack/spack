import os
import re
from subprocess import CalledProcessError

import spack
import spack.packages as packages
import spack.url as url
import spack.tty as tty
from spack.colify import colify
from spack.version import ver

description ="List available versions of a package"

def setup_parser(subparser):
    subparser.add_argument('package', metavar='PACKAGE', help='Package to list versions for')


def versions(parser, args):
    pkg = packages.get(args.package)
    colify(reversed(pkg.available_versions))
