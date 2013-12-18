import os
import argparse

import spack.cmd
import spack.packages
from spack.colify import colify

description ="List packages that provide a particular virtual package"

def setup_parser(subparser):
    subparser.add_argument('vpkg_spec', metavar='VPACKAGE_SPEC', nargs=argparse.REMAINDER,
                           help='Find packages that provide this virtual package')


def providers(parser, args):
    for spec in spack.cmd.parse_specs(args.vpkg_spec):
        colify(sorted(spack.packages.providers_for(spec)), indent=4)
