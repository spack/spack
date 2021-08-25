# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.dag as spack_dag
import spack.mirror

description = "generate DAGs for workflows using spack"
section = "build"
level = "long"


def get_env_var(variable_name):
    if variable_name in os.environ:
        return os.environ.get(variable_name)
    return None


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help='CI sub-commands')

    # Dynamic generation of the jobs yaml from a spack environment
    generate = subparsers.add_parser('generate-snakemake',
                                     help=generate_snakemake.__doc__)
    generate.add_argument(
        '--output-file', default=None,
        help="Path to file where generated DAG file should be " +
             "written.  The default will depend on your workflow chosen.")
    generate.set_defaults(func=generate_snakemake)


def generate_snakemake(args):
    """Generate a Snakefile with a DAG to install things with Spack."""
    env = spack.cmd.require_active_env(cmd_name='dag generate-snakemake')

    output_file = os.path.abspath(args.output_file or "Snakefile")

    # Generate the dag
    spack_dag.generate_snakefile(env, True, output_file)


def dag(parser, args):
    if args.func:
        return args.func(args)
