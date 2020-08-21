# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
import os
import argparse
import textwrap
import datetime
import fnmatch
import re
import shutil

import llnl.util.tty as tty
import llnl.util.filesystem as fs

import spack.environment as ev
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.report
import spack.package

description = "run spack's tests for an install"
section = "administrator"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='test_command')

    # Run
    run_parser = sp.add_parser('run', help=test_run.__doc__)

    name_help_msg = "Name the test for subsequent access."
    name_help_msg += " Default is the timestamp of the run formatted"
    name_help_msg += " 'YYYY-MM-DD_HH:MM:SS'"
    run_parser.add_argument('-n', '--name', help=name_help_msg)

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
    list_parser = sp.add_parser('list', help=test_list.__doc__)
    list_parser.add_argument(
        'filter', nargs=argparse.REMAINDER,
        help='optional case-insensitive glob patterns to filter results.')

    # Status
    status_parser = sp.add_parser('status', help=test_status.__doc__)
    status_parser.add_argument('name', help="Test for which to provide status")

    # Results
    results_parser = sp.add_parser('results', help=test_results.__doc__)
    results_parser.add_argument('name', help="Test for which to print results")

    # Remove
    remove_parser = sp.add_parser('remove', help=test_remove.__doc__)
    remove_parser.add_argument(
        'name', nargs='?',
        help="Test to remove from test stage")


def test_run(args):
    """Run tests for the specified installed packages

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

    # record test time; this will be default test name
    now = datetime.datetime.now()
    test_name = args.name or now.strftime('%Y-%m-%d_%H:%M:%S')
    tty.msg("Spack test %s" % test_name)

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

    # Set up reporter
    setattr(args, 'package', [s.format() for s in specs_to_test])
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
                'test-%s' % test_name)
        reporter.filename = log_file
    reporter.specs = specs_to_test

    # test_stage_dir
    stage = get_stage(test_name)
    fs.mkdirp(stage)

    with reporter('test', stage):
        if args.smoke_test:
            for spec in specs_to_test:
                try:
                    spec.package.do_test(
                        name=test_name,
                        remove_directory=not args.keep_stage,
                        dirty=args.dirty)
                    _write_test_result(spec, test_name, 'PASSED')
                except BaseException as err:
                    if isinstance(err, SyntaxError):
                        # Create the test log file and report the error.
                        test_stage = spack.package.setup_test_stage(test_name)
                        logfile = spack.package.test_log_pathname(test_stage,
                                                                  spec)
                        msg = 'Testing package {0}\n{1}'\
                            .format(spack.package.test_pkg_id(spec), str(err))
                        _add_msg_to_file(logfile, msg)

                    _write_test_result(spec, test_name, 'FAILED')
                    if args.fail_first:
                        break
        else:
            raise NotImplementedError


def test_list(args):
    """List tests that are running or have available results."""
    stage_dir = get_stage()
    tests = os.listdir(stage_dir)

    # Filter tests by filter argument
    if args.filter:
        def create_filter(f):
            raw = fnmatch.translate('f' if '*' in f or '?' in f
                                    else '*' + f + '*')
            return re.compile(raw, flags=re.IGNORECASE)
        filters = [create_filter(f) for f in args.filter]

        def match(t, f):
            return f.match(t)
        tests = [t for t in tests if any(match(t, f) for f in filters)]

    if tests:
        # TODO: Make these specify results vs active
        msg = "Spack test results available for the following tests:\n"
        msg += "        %s\n" % ' '.join(tests)
        msg += "    Run `spack test remove` to remove all tests"
        tty.msg(msg)
    else:
        msg = "No test results match the query\n"
        msg += "        Tests may have been removed using `spack test remove`"
        tty.msg(msg)


def test_status(args):
    """Get the current status for a particular Spack test."""
    name = args.name
    stage = get_stage(name)

    if os.path.exists(stage):
        # TODO: Make this handle capability tests too
        tty.msg("Test %s completed" % name)
    else:
        tty.msg("Test %s no longer available" % name)


def test_results(args):
    """Get the results for a particular Spack test."""
    name = args.name
    stage = get_stage(name)

    # TODO: Make this handle capability tests too
    # The results file may turn out to be a placeholder for future work
    if os.path.exists(stage):
        results_file = _get_results_file(name)
        if os.path.exists(results_file):
            msg = "Results for test %s: \n" % name
            with open(results_file, 'r') as f:
                lines = f.readlines()
            for line in lines:
                msg += "        %s" % line
            tty.msg(msg)
        else:
            msg = "Test %s has no results.\n" % name
            msg += "        Check if it is active with "
            msg += "`spack test status %s`" % name
            tty.msg(msg)
    else:
        tty.msg("No test %s found in test stage" % name)


def test_remove(args):
    """Remove results for a test from the test stage.

    If no test is listed, remove all tests from the test stage.

    Removed tests can no longer be accessed for results or status, and will not
    appear in `spack test list` results."""
    stage_dir = get_stage(args.name)
    if args.name:
        shutil.rmtree(stage_dir)
    else:
        fs.remove_directory_contents(stage_dir)


def test(parser, args):
    globals()['test_%s' % args.test_command](args)


def get_stage(name=None):
    """
    Return the test stage for the named test or the overall test stage.
    """
    stage_dir = spack.util.path.canonicalize_path(
        spack.config.get('config:test_stage', '~/.spack/test'))
    return os.path.join(stage_dir, name) if name else stage_dir


def _add_msg_to_file(filename, msg):
    """Add the message to the specified file

    Args:
        filename (str): path to the file
        msg (str): message to be appended to the file
    """
    with open(filename, 'a+') as f:
        f.write('{0}\n'.format(msg))


def _get_results_file(test_name):
    """Return the results pathname for the test

    Args:
        test_name (str): name of the test

    Returns:
        (str): path to the test results file
    """
    return os.path.join(get_stage(test_name), 'results.txt')


def _write_test_result(spec, test_name, result):
    """Write the result to the test results file

    Args:
        spec (Spec): spec of the package under test
        test_name (str): name of the test
        result (str): test result (i.e., 'PASSED' or 'FAILED')
    """
    msg = "{0} {1}".format(spack.package.test_pkg_id(spec), result)
    _add_msg_to_file(_get_results_file(test_name), msg)
