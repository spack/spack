# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
import sys
import textwrap

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.build_environment
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.fetch_strategy
import spack.monitor
import spack.paths
import spack.report
from spack.error import SpackError
from spack.installer import PackageInstaller


description = "build and install packages"
section = "build"
level = "short"


def update_kwargs_from_args(args, kwargs):
    """Parse cli arguments and construct a dictionary
    that will be passed to the package installer."""

    kwargs.update({
        'fail_fast': args.fail_fast,
        'keep_prefix': args.keep_prefix,
        'keep_stage': args.keep_stage,
        'restage': not args.dont_restage,
        'install_source': args.install_source,
        'verbose': args.verbose,
        'fake': args.fake,
        'dirty': args.dirty,
        'use_cache': args.use_cache,
        'cache_only': args.cache_only,
        'include_build_deps': args.include_build_deps,
        'explicit': True,  # Always true for install command
        'stop_at': args.until,
        'unsigned': args.unsigned,
        'full_hash_match': args.full_hash_match,
    })

    kwargs.update({
        'install_deps': ('dependencies' in args.things_to_install),
        'install_package': ('package' in args.things_to_install)
    })

    if hasattr(args, 'setup'):
        setups = set()
        for arglist_s in args.setup:
            for arg in [x.strip() for x in arglist_s.split(',')]:
                setups.add(arg)
        kwargs['setup'] = setups
        tty.msg('Setup={0}'.format(kwargs['setup']))


def setup_parser(subparser):
    subparser.add_argument(
        '--only',
        default='package,dependencies',
        dest='things_to_install',
        choices=['package', 'dependencies'],
        help="""select the mode of installation.
the default is to install the package along with all its dependencies.
alternatively one can decide to install only the package or only
the dependencies"""
    )
    subparser.add_argument(
        '-u', '--until', type=str, dest='until', default=None,
        help="phase to stop after when installing (default None)")
    arguments.add_common_arguments(subparser, ['jobs'])
    subparser.add_argument(
        '--overwrite', action='store_true',
        help="reinstall an existing spec, even if it has dependents")
    subparser.add_argument(
        '--fail-fast', action='store_true',
        help="stop all builds if any build fails (default is best effort)")
    subparser.add_argument(
        '--keep-prefix', action='store_true',
        help="don't remove the install prefix if installation fails")
    subparser.add_argument(
        '--keep-stage', action='store_true',
        help="don't remove the build stage if installation succeeds")
    subparser.add_argument(
        '--dont-restage', action='store_true',
        help="if a partial install is detected, don't delete prior state")

    cache_group = subparser.add_mutually_exclusive_group()
    cache_group.add_argument(
        '--use-cache', action='store_true', dest='use_cache', default=True,
        help="check for pre-built Spack packages in mirrors (default)")
    cache_group.add_argument(
        '--no-cache', action='store_false', dest='use_cache', default=True,
        help="do not check for pre-built Spack packages in mirrors")
    cache_group.add_argument(
        '--cache-only', action='store_true', dest='cache_only', default=False,
        help="only install package from binary mirrors")

    monitor_group = spack.monitor.get_monitor_group(subparser)  # noqa

    subparser.add_argument(
        '--include-build-deps', action='store_true', dest='include_build_deps',
        default=False, help="""include build deps when installing from cache,
which is useful for CI pipeline troubleshooting""")

    subparser.add_argument(
        '--no-check-signature', action='store_true',
        dest='unsigned', default=False,
        help="do not check signatures of binary packages")
    subparser.add_argument(
        '--require-full-hash-match', action='store_true',
        dest='full_hash_match', default=False, help="""when installing from
binary mirrors, do not install binary package unless the full hash of the
remote spec matches that of the local spec""")
    subparser.add_argument(
        '--show-log-on-error', action='store_true',
        help="print full build log to stderr if build fails")
    subparser.add_argument(
        '--source', action='store_true', dest='install_source',
        help="install source files in prefix")
    arguments.add_common_arguments(subparser, ['no_checksum', 'deprecated'])
    subparser.add_argument(
        '-v', '--verbose', action='store_true',
        help="display verbose build output while installing")
    subparser.add_argument(
        '--fake', action='store_true',
        help="fake install for debug purposes.")
    subparser.add_argument(
        '--only-concrete', action='store_true', default=False,
        help='(with environment) only install already concretized specs')
    subparser.add_argument(
        '--no-add', action='store_true', default=False,
        help="""(with environment) only install specs provided as argument
if they are already in the concretized environment""")
    subparser.add_argument(
        '-f', '--file', action='append', default=[],
        dest='specfiles', metavar='SPEC_YAML_FILE',
        help="install from file. Read specs to install from .yaml files")

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])

    testing = subparser.add_mutually_exclusive_group()
    testing.add_argument(
        '--test', default=None,
        choices=['root', 'all'],
        help="""If 'root' is chosen, run package tests during
installation for top-level packages (but skip tests for dependencies).
if 'all' is chosen, run package tests during installation for all
packages. If neither are chosen, don't run tests for any packages."""
    )
    testing.add_argument(
        '--run-tests', action='store_true',
        help='run package tests during installation (same as --test=all)'
    )
    subparser.add_argument(
        '--log-format',
        default=None,
        choices=spack.report.valid_formats,
        help="format to be used for log files"
    )
    subparser.add_argument(
        '--log-file',
        default=None,
        help="filename for the log file. if not passed a default will be used"
    )
    subparser.add_argument(
        '--help-cdash',
        action='store_true',
        help="Show usage instructions for CDash reporting"
    )
    arguments.add_cdash_args(subparser, False)
    arguments.add_common_arguments(subparser, ['yes_to_all', 'spec'])
    subparser.epilog = (
        'Statuses: {s.POS_GLYPH} - installed, '
        '{s.NEG_GLYPH} - not installed, \n'
        '          {s.UPSTREAM_GLYPH} - upstream, '
        '{s.ERR_GLYPH} - install missing/error\n'
        '          {s.EXTERNAL_GLYPH} - external'
        .format(s=spack.spec.Spec))


def default_log_file(spec):
    """Computes the default filename for the log file and creates
    the corresponding directory if not present
    """
    fmt = 'test-{x.name}-{x.version}-{hash}.xml'
    basename = fmt.format(x=spec, hash=spec.dag_hash())
    dirname = fs.os.path.join(spack.paths.reports_path, 'junit')
    fs.mkdirp(dirname)
    return fs.os.path.join(dirname, basename)


def install_specs(cli_args, kwargs, specs):
    """Do the actual installation.

    Args:
        cli_args (Namespace): argparse namespace with command arguments
        kwargs (dict):  keyword arguments
        specs (list of tuples):  list of (abstract, concrete) spec tuples
    """

    # handle active environment, if any
    env = ev.get_env(cli_args, 'install')

    try:
        if env:
            specs_to_install = []
            specs_to_add = []
            for abstract, concrete in specs:
                # This won't find specs added to the env since last
                # concretize, therefore should we consider enforcing
                # concretization of the env before allowing to install
                # specs?
                m_spec = env.matching_spec(abstract)

                # If there is any ambiguity in the above call to matching_spec
                # (i.e. if more than one spec in the environment matches), then
                # SpackEnvironmentError is rasied, with a message listing the
                # the matches.  Getting to this point means there were either
                # no matches or exactly one match.

                if not m_spec:
                    tty.debug('{0} matched nothing in the env'.format(
                        abstract.name))
                    # no matches in the env
                    if cli_args.no_add:
                        msg = ('You asked to install {0} without adding it ' +
                               '(--no-add), but no such spec exists in ' +
                               'environment').format(abstract.name)
                        tty.die(msg)
                    else:
                        tty.debug('adding {0} as a root'.format(abstract.name))
                        specs_to_add.append((abstract, concrete))

                    continue

                tty.debug('exactly one match for {0} in env -> {1}'.format(
                    m_spec.name, m_spec.dag_hash()))

                if m_spec in env.roots() or cli_args.no_add:
                    # either the single match is a root spec (and --no-add is
                    # the default for roots) or --no-add was stated explictly
                    tty.debug('just install {0}'.format(m_spec.name))
                    specs_to_install.append(m_spec)
                else:
                    # the single match is not a root (i.e. it's a dependency),
                    # and --no-add was not specified, so we'll add it as a
                    # root before installing
                    tty.debug('add {0} then install it'.format(m_spec.name))
                    specs_to_add.append((abstract, concrete))

            if specs_to_add:
                tty.debug('Adding the following specs as roots:')
                for abstract, concrete in specs_to_add:
                    tty.debug('  {0}'.format(abstract.name))
                    with env.write_transaction():
                        specs_to_install.append(
                            env.concretize_and_add(abstract, concrete))
                        env.write(regenerate=False)

            # Install the validated list of cli specs
            if specs_to_install:
                tty.debug('Installing the following cli specs:')
                for s in specs_to_install:
                    tty.debug('  {0}'.format(s.name))
                env.install_specs(specs_to_install, args=cli_args, **kwargs)
        else:
            installs = [(concrete.package, kwargs) for _, concrete in specs]
            builder = PackageInstaller(installs)
            builder.install()
    except spack.build_environment.InstallError as e:
        if cli_args.show_log_on_error:
            e.print_context()
            if not os.path.exists(e.pkg.build_log_path):
                tty.error("'spack install' created no log.")
            else:
                sys.stderr.write('Full build log:\n')
                with open(e.pkg.build_log_path) as log:
                    shutil.copyfileobj(log, sys.stderr)
        raise


def install(parser, args, **kwargs):

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

    # The user wants to monitor builds using github.com/spack/spack-monitor
    if args.use_monitor:
        monitor = spack.monitor.get_client(
            host=args.monitor_host,
            prefix=args.monitor_prefix,
            disable_auth=args.monitor_disable_auth,
            tags=args.monitor_tags,
            save_local=args.monitor_save_local,
        )

    reporter = spack.report.collect_info(
        spack.package.PackageInstaller, '_install_task', args.log_format, args)
    if args.log_file:
        reporter.filename = args.log_file

    if args.run_tests:
        tty.warn("Deprecated option: --run-tests: use --test=all instead")

    def get_tests(specs):
        if args.test == 'all' or args.run_tests:
            return True
        elif args.test == 'root':
            return [spec.name for spec in specs]
        else:
            return False

    if not args.spec and not args.specfiles:
        # if there are no args but an active environment
        # then install the packages from it.
        env = ev.get_env(args, 'install')
        if env:
            tests = get_tests(env.user_specs)
            kwargs['tests'] = tests

            if not args.only_concrete:
                with env.write_transaction():
                    concretized_specs = env.concretize(tests=tests)
                    ev.display_specs(concretized_specs)

                    # save view regeneration for later, so that we only do it
                    # once, as it can be slow.
                    env.write(regenerate=False)

            specs = env.all_specs()
            if not args.log_file and not reporter.filename:
                reporter.filename = default_log_file(specs[0])
            reporter.specs = specs

            # Tell the monitor about the specs
            if args.use_monitor and specs:
                monitor.new_configuration(specs)

            tty.msg("Installing environment {0}".format(env.name))
            with reporter('build'):
                env.install_all(args, **kwargs)

            tty.debug("Regenerating environment views for {0}"
                      .format(env.name))
            with env.write_transaction():
                # write env to trigger view generation and modulefile
                # generation
                env.write()
            return
        else:
            msg = "install requires a package argument or active environment"
            if 'spack.yaml' in os.listdir(os.getcwd()):
                # There's a spack.yaml file in the working dir, the user may
                # have intended to use that
                msg += "\n\n"
                msg += "Did you mean to install using the `spack.yaml`"
                msg += " in this directory? Try: \n"
                msg += "    spack env activate .\n"
                msg += "    spack install\n"
                msg += "  OR\n"
                msg += "    spack --env . install"
            tty.die(msg)

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    if args.deprecated:
        spack.config.set('config:deprecated', True, scope='command_line')

    # Parse cli arguments and construct a dictionary
    # that will be passed to the package installer
    update_kwargs_from_args(args, kwargs)

    # 1. Abstract specs from cli
    abstract_specs = spack.cmd.parse_specs(args.spec)
    tests = get_tests(abstract_specs)
    kwargs['tests'] = tests

    try:
        specs = spack.cmd.parse_specs(
            args.spec, concretize=True, tests=tests)
    except SpackError as e:
        tty.debug(e)
        reporter.concretization_report(e.message)
        raise

    # 2. Concrete specs from yaml files
    for file in args.specfiles:
        with open(file, 'r') as f:
            s = spack.spec.Spec.from_yaml(f)

        concretized = s.concretized()
        if concretized.dag_hash() != s.dag_hash():
            msg = 'skipped invalid file "{0}". '
            msg += 'The file does not contain a concrete spec.'
            tty.warn(msg.format(file))
            continue

        abstract_specs.append(s)
        specs.append(concretized)

    if len(specs) == 0:
        tty.die('The `spack install` command requires a spec to install.')

    if not args.log_file and not reporter.filename:
        reporter.filename = default_log_file(specs[0])
    reporter.specs = specs
    with reporter('build'):
        if args.overwrite:

            installed = list(filter(lambda x: x,
                                    map(spack.store.db.query_one, specs)))
            if not args.yes_to_all:
                display_args = {
                    'long': True,
                    'show_flags': True,
                    'variants': True
                }

                if installed:
                    tty.msg('The following package specs will be '
                            'reinstalled:\n')
                    spack.cmd.display_specs(installed, **display_args)

                not_installed = list(filter(lambda x: x not in installed,
                                            specs))
                if not_installed:
                    tty.msg('The following package specs are not installed and'
                            ' the --overwrite flag was given. The package spec'
                            ' will be newly installed:\n')
                    spack.cmd.display_specs(not_installed, **display_args)

                # We have some specs, so one of the above must have been true
                answer = tty.get_yes_or_no(
                    'Do you want to proceed?', default=False
                )
                if not answer:
                    tty.die('Reinstallation aborted.')

            # overwrite all concrete explicit specs from this build
            kwargs['overwrite'] = [spec.dag_hash() for spec in specs]

        # Update install_args with the monitor args, needed for build task
        kwargs.update({
            "monitor_disable_auth": args.monitor_disable_auth,
            "monitor_keep_going": args.monitor_keep_going,
            "monitor_host": args.monitor_host,
            "use_monitor": args.use_monitor,
            "monitor_prefix": args.monitor_prefix,
        })

        # If we are using the monitor, we send configs. and create build
        # The full_hash is the main package id, the build_hash for others
        if args.use_monitor and specs:
            monitor.new_configuration(specs)
        install_specs(args, kwargs, zip(abstract_specs, specs))
