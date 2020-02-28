# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import spack.container

description = ("creates recipes to build images for different"
               " container runtimes")
section = "container"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--file', default=None,
        dest='specfile', metavar='SPEC_YAML_FILE',
        help="spack.yaml for which to generate the recipe. If not provided"
             "try the env_dir provided by `spack -e`, if that also doesn't"
             "exist try `./spack.yaml`.")
    subparser.add_argument(
        '-r', '--recipefile', default=None,
        dest='recipefile',
        help="name of the recipefile to generate. If None print to stdout.")


def containerize(parser, args):
    if args.specfile is not None:
        config_file = args.specfile
        print(config_file)
    else:
        config_dir = args.env_dir or os.getcwd()
        config_file = os.path.abspath(os.path.join(config_dir, 'spack.yaml'))
        if not os.path.exists(config_file):
            msg = "No spack.yaml explicitly provided (-f) and "
            if args.env_dir:
                msg += "the environment {0} does not have a spack.yaml"
                msg = msg.format(args.env_dir)
            else:
                msg += "the current directory does not have a spack.yaml"
            raise ValueError(msg.format(config_file))

    config = spack.container.validate(config_file)

    recipe = spack.container.recipe(config)
    if args.specfile is not None:
        with open(args.recipefile, 'w') as f:
            print("Writing container recipe to {0}".format(args.recipefile))
            f.write(recipe)
    else:
        print(recipe)
