# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
from spack.config import config as spack_config


def update_compiler(prefix, rpaths):
    compilers_config = spack_config.get('compilers')

    for compiler_entry in compilers_config:
        if compiler_entry['compiler']['paths']['cc'].startswith(prefix):
            print('found target compiler: {0}'.format(
                compiler_entry['compiler']['spec']))
            compiler_entry['compiler']['extra_rpaths'].append(rpaths)

    spack_config.update_config('compilers', compilers_config)


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Add extra_rpaths to default system compilers.yaml")

    parser.add_argument('-p', '--prefix', default=None,
                        help="Install prefix of compiler to update")
    parser.add_argument('-r', '--rpaths', default=None,
                        help="Extra rpaths to add to target compiler")

    args = parser.parse_args()

    update_compiler(args.prefix, args.rpaths)
