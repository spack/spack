# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
import os
import argparse
import textwrap
import fnmatch
import re
import shutil

import llnl.util.tty as tty

import spack.install_test
import spack.environment as ev
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.report
import spack.package

description = "run spack's tests for an install"
section = "administrator"
level = "long"


def first_line(docstring):
    """Return the first line of the docstring."""
    return docstring.split('\n')[0]


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='test_command')

    # Run
    run_parser = sp.add_parser('run', description=test_run.__doc__,
                               help=first_line(test_run.__doc__))

    alias_help_msg = "Provide an alias for this test-suite"
    alias_help_msg += " for subsequent access."
    run_parser.add_argument('--alias', help=alias_help_msg)

    run_parser.add_argument(
        '--fail-fast', action='store_true',
        help="Stop tests for each package after the first failure."
    )
    run_parser.add_argument(
        '--fail-first', action='store_true',
        help="Stop after the first failed package."
    )
    run_parser.add_argument(
        '--keep-stage',
        action='store_true',
        help='Keep testing directory for debugging'
    )
    run_parser.add_argument(
        '--log-format',
        default=None,
        choices=spack.report.valid_formats,
        help="format to be used for log files"
    )
    run_parser.add_argument(
        '--log-file',
        default=None,
        help="filename for the log file. if not passed a default will be used"
    )
    arguments.add_cdash_args(run_parser, False)
    run_parser.add_argument(
        '--help-cdash',
        action='store_true',
        help="Show usage instructions for CDash reporting"
    )

    length_group = run_parser.add_mutually_exclusive_group()
    length_group.add_argument(
        '--smoke', action='store_true', dest='smoke_test', default=True,
        help='run smoke tests (default)')
    length_group.add_argument(
        '--capability', action='store_false', dest='smoke_test', default=True,
        help='run full capability tests using pavilion')

    cd_group = run_parser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])

    arguments.add_common_arguments(run_parser, ['installed_specs'])

    # List
    list_parser = sp.add_parser('list', description=test_list.__doc__,
                                help=first_line(test_list.__doc__))
    list_parser.add_argument(
        'filter', nargs=argparse.REMAINDER,
        help='optional case-insensitive glob patterns to filter results.')

    # Find
    find_parser = sp.add_parser('find', description=test_find.__doc__,
                                help=first_line(test_find.__doc__))
    find_parser.add_argument(
        'filter', nargs=argparse.REMAINDER,
        help='optional case-insensitive glob patterns to filter results.')

    # Status
    status_parser = sp.add_parser('status', description=test_status.__doc__,
                                  help=first_line(test_status.__doc__))
    status_parser.add_argument(
        'names', nargs=argparse.REMAINDER,
        help="Test suites for which to print status")

    # Results
    results_parser = sp.add_parser('results', description=test_results.__doc__,
                                   help=first_line(test_results.__doc__))
    results_parser.add_argument(
        'names', nargs=argparse.REMAINDER,
        help="Test suites for which to print results")

    # Remove
    remove_parser = sp.add_parser('remove', description=test_remove.__doc__,
                                  help=first_line(test_remove.__doc__))
    arguments.add_common_arguments(remove_parser, ['yes_to_all'])
    remove_parser.add_argument(
        'names', nargs=argparse.REMAINDER,
        help="Test suites to remove from test stage")


def test_run(args):
    """Run tests for the specified installed packages.

    If no specs are listed, run tests for all packages in the current
    environment or all installed packages if there is no active environment.
    """
    # cdash help option
    if args.help_cdash:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''\
environment variables:
  SPACK_CDASH_AUTH_TOKEN
                        authentication token to present to CDash
                        '''))
        arguments.add_cdash_args(parser, True)
        parser.print_help()
        return

    # set config option for fail-fast
    if args.fail_fast:
        spack.config.set('config:fail_fast', True, scope='command_line')

    # Get specs to test
    env = ev.get_env(args, 'test')
    hashes = env.all_hashes() if env else None

    specs = spack.cmd.parse_specs(args.specs) if args.specs else [None]
    specs_to_test = []
    for spec in specs:
        matching = spack.store.db.query_local(spec, hashes=hashes)
        if spec and not matching:
            tty.warn("No installed packages match spec %s" % spec)
        specs_to_test.extend(matching)

    # test_stage_dir
    test_suite = spack.install_test.TestSuite(specs_to_test, args.alias)
    test_suite.ensure_stage()
    tty.msg("Spack test %s" % test_suite.name)

    # Set up reporter
    setattr(args, 'package', [s.format() for s in test_suite.specs])
    reporter = spack.report.collect_info(
        spack.package.PackageBase, 'do_test', args.log_format, args)
    if not reporter.filename:
        if args.log_file:
            if os.path.isabs(args.log_file):
                log_file = args.log_file
            else:
                log_dir = os.getcwd()
                log_file = os.path.join(log_dir, args.log_file)
        else:
            log_file = os.path.join(
                os.getcwd(),
                'test-%s' % test_suite.name)
        reporter.filename = log_file
    reporter.specs = specs_to_test

    with reporter('test', test_suite.stage):
        if args.smoke_test:
            test_suite(remove_directory=not args.keep_stage,
                       dirty=args.dirty,
                       fail_first=args.fail_first)
        else:
            raise NotImplementedError


def test_list(args):
    """List all installed packages with available tests."""
    raise NotImplementedError


def test_find(args):  # TODO: merge with status (noargs)
    """Find tests that are running or have available results.

    Displays aliases for tests that have them, otherwise test suite content
    hashes."""
    test_suites = spack.install_test.get_all_test_suites()

    # Filter tests by filter argument
    if args.filter:
        def create_filter(f):
            raw = fnmatch.translate('f' if '*' in f or '?' in f
                                    else '*' + f + '*')
            return re.compile(raw, flags=re.IGNORECASE)
        filters = [create_filter(f) for f in args.filter]

        def match(t, f):
            return f.match(t)
        test_suites = [t for t in test_suites
                       if any(match(t.alias, f) for f in filters) and
                       os.path.isdir(t.stage)]

    names = [t.name for t in test_suites]

    if names:
        # TODO: Make these specify results vs active
        msg = "Spack test results available for the following tests:\n"
        msg += "        %s\n" % ' '.join(names)
        msg += "    Run `spack test remove` to remove all tests"
        tty.msg(msg)
    else:
        msg = "No test results match the query\n"
        msg += "        Tests may have been removed using `spack test remove`"
        tty.msg(msg)


def test_status(args):
    """Get the current status for the specified Spack test suite(s)."""
    if args.names:
        test_suites = []
        for name in args.names:
            test_suite = spack.install_test.get_test_suite(name)
            if test_suite:
                test_suites.append(test_suite)
            else:
                tty.msg("No test suite %s found in test stage" % name)
    else:
        test_suites = spack.install_test.get_all_test_suites()
        if not test_suites:
            tty.msg("No test suites with status to report")

    for test_suite in test_suites:
        # TODO: Make this handle capability tests too
        # TODO: Make this handle tests running in another process
        tty.msg("Test suite %s completed" % test_suite.name)


def test_results(args):
    """Get the results from Spack test suite(s) (default all)."""
    if args.names:
        test_suites = []
        for name in args.names:
            test_suite = spack.install_test.get_test_suite(name)
            if test_suite:
                test_suites.append(test_suite)
            else:
                tty.msg("No test suite %s found in test stage" % name)
    else:
        test_suites = spack.install_test.get_all_test_suites()
        if not test_suites:
            tty.msg("No test suites with results to report")

    # TODO: Make this handle capability tests too
    # The results file may turn out to be a placeholder for future work
    for test_suite in test_suites:
        results_file = test_suite.results_file
        if os.path.exists(results_file):
            msg = "Results for test suite %s: \n" % test_suite.name
            with open(results_file, 'r') as f:
                lines = f.readlines()
            for line in lines:
                msg += "        %s" % line
            tty.msg(msg)
        else:
            msg = "Test %s has no results.\n" % test_suite.name
            msg += "        Check if it is running with "
            msg += "`spack test status %s`" % test_suite.name
            tty.msg(msg)


def test_remove(args):
    """Remove results from Spack test suite(s) (default all).

    If no test suite is listed, remove results for all suites.

    Removed tests can no longer be accessed for results or status, and will not
    appear in `spack test list` results."""
    if args.names:
        test_suites = []
        for name in args.names:
            test_suite = spack.install_test.get_test_suite(name)
            if test_suite:
                test_suites.append(test_suite)
            else:
                tty.msg("No test suite %s found in test stage" % name)
    else:
        test_suites = spack.install_test.get_all_test_suites()

    if not test_suites:
        tty.msg("No test suites to remove")
        return

    if not args.yes_to_all:
        msg = 'The following test suites will be removed:\n\n'
        msg += '    ' + '   '.join(test.name for test in test_suites) + '\n'
        tty.msg(msg)
        answer = tty.get_yes_or_no('Do you want to proceed?', default=False)
        if not answer:
            tty.msg('Aborting removal of test suites')
            return

    for test_suite in test_suites:
        shutil.rmtree(test_suite.stage)


def test(parser, args):
    globals()['test_%s' % args.test_command](args)
