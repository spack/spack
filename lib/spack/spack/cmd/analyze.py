# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.tty as tty

import spack.analyzers
import spack.build_environment
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.fetch_strategy
import spack.monitor
import spack.paths
import spack.report


description = "analyze installed packages"
section = "extensions"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        '--overwrite', action='store_true',
        help="re-analyze even if the output file already exists.")

    monitor_group = spack.monitor.get_monitor_group(subparser)  # noqa

    subparser.add_argument(
        '-o', '--outdir', default=None,
        dest='outdir',
        help="write output to a different directory than .spack metadata.")
    subparser.add_argument(
        '--list-analyzers', action="store_true",
        default=False,
        help="list available analyzers.")
    subparser.add_argument(
        '-a', '--analyzers', default=None,
        dest="analyzers", action="append",
        choices=list(spack.analyzers.analyzer_types.keys()) + ["all"],
        help="add an analyzer (defaults to all available)")
    arguments.add_common_arguments(subparser, ['spec'])


def analyze_spec(spec, analyzers=None, outdir=None, monitor=None):
    """Do an analysis for a spec, optionally adding monitoring and allowing
    the user to specify a custom output directory.

    analyze_spec(spec, args.analyzers, args.outdir, monitor)

    Args:
        spec (Spec): spec object of installed package
        analyzers (list): list of analyzer (keys) to run
        monitor (monitor.SpackMonitorClient): a monitor client
    """
    analyzers = analyzers or list(spack.analyzers.analyzer_types.keys())

    # If the package analyze folder does not exist, create it
    spack.analyzers.create_package_analyze_dir(spec)

    # Load the build environment from the spec install directory, and send
    # the spec to the monitor if it's not known
    if monitor:
        monitor.load_build_environment(spec)
        monitor.new_configuration([spec])

    for name in analyzers:

        # Instantiate the analyzer with the spec
        analyzer = spack.analyzers.get_analyzer(name)(spec)

        # Run the analyzer to get a json result - results are returned as
        # a dictionary with a key corresponding to the analyzer type, so
        # we can just update the data
        result = analyzer.run()

        # Send the result. We do them separately because:
        # 1. each analyzer might have differently organized output
        # 2. the size of a result can be large
        analyzer.save_result(result, outdir, monitor)


def analyze(parser, args, **kwargs):

    # If the user wants to list analyzers, do so and exit
    if args.list_analyzers:
        spack.analyzers.list_all()
        sys.exit(0)

    # handle active environment, if any
    env = ev.get_env(args, 'analyze')

    # Get an disambiguate spec (we should only have one)
    specs = spack.cmd.parse_specs(args.spec)
    if not specs:
        tty.die("You must provide one or more specs to analyze.")
    spec = spack.cmd.disambiguate_spec(specs[0], env)

    # The user wants to monitor builds using github.com/spack/spack-monitor
    monitor = None
    if args.use_monitor:
        monitor = spack.monitor.get_client(
            host=args.monitor_host,
            prefix=args.monitor_prefix,
            disable_auth=args.monitor_disable_auth,
        )

    # Run the analysis
    analyze_spec(spec, args.analyzers, args.outdir, monitor)
