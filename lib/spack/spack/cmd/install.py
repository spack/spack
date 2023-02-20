# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
import sys
from typing import List

import llnl.util.filesystem as fs
from llnl.util import lang, tty

import spack.build_environment
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.config
import spack.environment as ev
import spack.fetch_strategy
import spack.package_base
import spack.paths
import spack.report
import spack.spec
import spack.store
from spack.error import SpackError
from spack.installer import PackageInstaller

description = "build and install packages"
section = "build"
level = "short"


# Determine value of cache flag
def cache_opt(default_opt, use_buildcache):
    if use_buildcache == "auto":
        return default_opt
    elif use_buildcache == "only":
        return True
    elif use_buildcache == "never":
        return False


def install_kwargs_from_args(args):
    """Translate command line arguments into a dictionary that will be passed
    to the package installer.
    """
    pkg_use_bc, dep_use_bc = args.use_buildcache

    return {
        "fail_fast": args.fail_fast,
        "keep_prefix": args.keep_prefix,
        "keep_stage": args.keep_stage,
        "restage": not args.dont_restage,
        "install_source": args.install_source,
        "verbose": args.verbose or args.install_verbose,
        "fake": args.fake,
        "dirty": args.dirty,
        "package_use_cache": cache_opt(args.use_cache, pkg_use_bc),
        "package_cache_only": cache_opt(args.cache_only, pkg_use_bc),
        "dependencies_use_cache": cache_opt(args.use_cache, dep_use_bc),
        "dependencies_cache_only": cache_opt(args.cache_only, dep_use_bc),
        "include_build_deps": args.include_build_deps,
        "explicit": True,  # Use true as a default for install command
        "stop_at": args.until,
        "unsigned": args.unsigned,
        "install_deps": ("dependencies" in args.things_to_install),
        "install_package": ("package" in args.things_to_install),
    }


def setup_parser(subparser):
    subparser.add_argument(
        "--only",
        default="package,dependencies",
        dest="things_to_install",
        choices=["package", "dependencies"],
        help="""select the mode of installation.
the default is to install the package along with all its dependencies.
alternatively one can decide to install only the package or only
the dependencies""",
    )
    subparser.add_argument(
        "-u",
        "--until",
        type=str,
        dest="until",
        default=None,
        help="phase to stop after when installing (default None)",
    )
    arguments.add_common_arguments(subparser, ["jobs"])
    subparser.add_argument(
        "--overwrite",
        action="store_true",
        help="reinstall an existing spec, even if it has dependents",
    )
    subparser.add_argument(
        "--fail-fast",
        action="store_true",
        help="stop all builds if any build fails (default is best effort)",
    )
    subparser.add_argument(
        "--keep-prefix",
        action="store_true",
        help="don't remove the install prefix if installation fails",
    )
    subparser.add_argument(
        "--keep-stage",
        action="store_true",
        help="don't remove the build stage if installation succeeds",
    )
    subparser.add_argument(
        "--dont-restage",
        action="store_true",
        help="if a partial install is detected, don't delete prior state",
    )

    cache_group = subparser.add_mutually_exclusive_group()
    cache_group.add_argument(
        "--use-cache",
        action="store_true",
        dest="use_cache",
        default=True,
        help="check for pre-built Spack packages in mirrors (default)",
    )
    cache_group.add_argument(
        "--no-cache",
        action="store_false",
        dest="use_cache",
        default=True,
        help="do not check for pre-built Spack packages in mirrors",
    )
    cache_group.add_argument(
        "--cache-only",
        action="store_true",
        dest="cache_only",
        default=False,
        help="only install package from binary mirrors",
    )
    cache_group.add_argument(
        "--use-buildcache",
        dest="use_buildcache",
        type=arguments.use_buildcache,
        default="package:auto,dependencies:auto",
        metavar="[{auto,only,never},][package:{auto,only,never},][dependencies:{auto,only,never}]",
        help="""select the mode of buildcache for the 'package' and 'dependencies'.
Default: package:auto,dependencies:auto
- `auto` behaves like --use-cache
- `only` behaves like --cache-only
- `never` behaves like --no-cache
""",
    )

    subparser.add_argument(
        "--include-build-deps",
        action="store_true",
        dest="include_build_deps",
        default=False,
        help="""include build deps when installing from cache,
which is useful for CI pipeline troubleshooting""",
    )

    subparser.add_argument(
        "--no-check-signature",
        action="store_true",
        dest="unsigned",
        default=False,
        help="do not check signatures of binary packages",
    )
    subparser.add_argument(
        "--show-log-on-error",
        action="store_true",
        help="print full build log to stderr if build fails",
    )
    subparser.add_argument(
        "--source",
        action="store_true",
        dest="install_source",
        help="install source files in prefix",
    )
    arguments.add_common_arguments(subparser, ["no_checksum", "deprecated"])
    subparser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="install_verbose",
        help="display verbose build output while installing",
    )
    subparser.add_argument("--fake", action="store_true", help="fake install for debug purposes.")
    subparser.add_argument(
        "--only-concrete",
        action="store_true",
        default=False,
        help="(with environment) only install already concretized specs",
    )

    updateenv_group = subparser.add_mutually_exclusive_group()
    updateenv_group.add_argument(
        "--add",
        action="store_true",
        default=False,
        help="""(with environment) add spec to the environment as a root.""",
    )
    updateenv_group.add_argument(
        "--no-add",
        action="store_false",
        dest="add",
        help="""(with environment) do not add spec to the environment as a
root (the default behavior).""",
    )

    subparser.add_argument(
        "-f",
        "--file",
        action="append",
        default=[],
        dest="specfiles",
        metavar="SPEC_YAML_FILE",
        help="install from file. Read specs to install from .yaml files",
    )

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ["clean", "dirty"])

    testing = subparser.add_mutually_exclusive_group()
    testing.add_argument(
        "--test",
        default=None,
        choices=["root", "all"],
        help="""If 'root' is chosen, run package tests during
installation for top-level packages (but skip tests for dependencies).
if 'all' is chosen, run package tests during installation for all
packages. If neither are chosen, don't run tests for any packages.""",
    )
    arguments.add_common_arguments(subparser, ["log_format"])
    subparser.add_argument(
        "--log-file",
        default=None,
        help="filename for the log file. if not passed a default will be used",
    )
    subparser.add_argument(
        "--help-cdash", action="store_true", help="Show usage instructions for CDash reporting"
    )
    arguments.add_cdash_args(subparser, False)
    arguments.add_common_arguments(subparser, ["yes_to_all", "spec"])
    arguments.add_concretizer_args(subparser)


def default_log_file(spec):
    """Computes the default filename for the log file and creates
    the corresponding directory if not present
    """
    fmt = "test-{x.name}-{x.version}-{hash}.xml"
    basename = fmt.format(x=spec, hash=spec.dag_hash())
    dirname = fs.os.path.join(spack.paths.reports_path, "junit")
    fs.mkdirp(dirname)
    return fs.os.path.join(dirname, basename)


def report_filename(args: argparse.Namespace, specs: List[spack.spec.Spec]) -> str:
    """Return the filename to be used for reporting to JUnit or CDash format."""
    result = args.log_file or default_log_file(specs[0])
    return result


def install_specs(specs, install_kwargs, cli_args):
    try:
        if ev.active_environment():
            install_specs_inside_environment(specs, install_kwargs, cli_args)
        else:
            install_specs_outside_environment(specs, install_kwargs)
    except spack.build_environment.InstallError as e:
        if cli_args.show_log_on_error:
            e.print_context()
            assert e.pkg, "Expected InstallError to include the associated package"
            if not os.path.exists(e.pkg.build_log_path):
                tty.error("'spack install' created no log.")
            else:
                sys.stderr.write("Full build log:\n")
                with open(e.pkg.build_log_path) as log:
                    shutil.copyfileobj(log, sys.stderr)
        raise


def install_specs_inside_environment(specs, install_kwargs, cli_args):
    specs_to_install, specs_to_add = [], []
    env = ev.active_environment()
    for abstract, concrete in specs:
        # This won't find specs added to the env since last
        # concretize, therefore should we consider enforcing
        # concretization of the env before allowing to install
        # specs?
        m_spec = env.matching_spec(abstract)

        # If there is any ambiguity in the above call to matching_spec
        # (i.e. if more than one spec in the environment matches), then
        # SpackEnvironmentError is raised, with a message listing the
        # the matches.  Getting to this point means there were either
        # no matches or exactly one match.

        if not m_spec and not cli_args.add:
            msg = (
                "Cannot install '{0}' because it is not in the current environment."
                " You can add it to the environment with 'spack add {0}', or as part"
                " of the install command with 'spack install --add {0}'"
            ).format(str(abstract))
            tty.die(msg)

        if not m_spec:
            tty.debug("adding {0} as a root".format(abstract.name))
            specs_to_add.append((abstract, concrete))
            continue

        tty.debug("exactly one match for {0} in env -> {1}".format(m_spec.name, m_spec.dag_hash()))

        if m_spec in env.roots() or not cli_args.add:
            # either the single match is a root spec (in which case
            # the spec is not added to the env again), or the user did
            # not specify --add (in which case it is assumed we are
            # installing already-concretized specs in the env)
            tty.debug("just install {0}".format(m_spec.name))
            specs_to_install.append(m_spec)
        else:
            # the single match is not a root (i.e. it's a dependency),
            # and --add was specified, so we'll add it as a
            # root before installing
            tty.debug("add {0} then install it".format(m_spec.name))
            specs_to_add.append((abstract, concrete))
    if specs_to_add:
        tty.debug("Adding the following specs as roots:")
        for abstract, concrete in specs_to_add:
            tty.debug("  {0}".format(abstract.name))
            with env.write_transaction():
                specs_to_install.append(env.concretize_and_add(abstract, concrete))
                env.write(regenerate=False)
    # Install the validated list of cli specs
    if specs_to_install:
        tty.debug("Installing the following cli specs:")
        for s in specs_to_install:
            tty.debug("  {0}".format(s.name))
        env.install_specs(specs_to_install, **install_kwargs)


def install_specs_outside_environment(specs, install_kwargs):
    installs = [(concrete.package, install_kwargs) for _, concrete in specs]
    builder = PackageInstaller(installs)
    builder.install()


def install_all_specs_from_active_environment(
    install_kwargs, only_concrete, cli_test_arg, reporter_factory
):
    """Install all specs from the active environment

    Args:
        install_kwargs (dict): dictionary of options to be passed to the installer
        only_concrete (bool): if true don't concretize the environment, but install
            only the specs that are already concrete
        cli_test_arg (bool or str): command line argument to select which test to run
        reporter: reporter object for the installations
    """
    env = ev.active_environment()
    if not env:
        msg = "install requires a package argument or active environment"
        if "spack.yaml" in os.listdir(os.getcwd()):
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

    install_kwargs["tests"] = compute_tests_install_kwargs(env.user_specs, cli_test_arg)
    if not only_concrete:
        with env.write_transaction():
            concretized_specs = env.concretize(tests=install_kwargs["tests"])
            ev.display_specs(concretized_specs)

            # save view regeneration for later, so that we only do it
            # once, as it can be slow.
            env.write(regenerate=False)

    specs = env.all_specs()
    if not specs:
        msg = "{0} environment has no specs to install".format(env.name)
        tty.msg(msg)
        return

    reporter = reporter_factory(specs) or lang.nullcontext()

    tty.msg("Installing environment {0}".format(env.name))
    with reporter:
        env.install_all(**install_kwargs)

    tty.debug("Regenerating environment views for {0}".format(env.name))
    with env.write_transaction():
        # write env to trigger view generation and modulefile
        # generation
        env.write()


def compute_tests_install_kwargs(specs, cli_test_arg):
    """Translate the test cli argument into the proper install argument"""
    if cli_test_arg == "all":
        return True
    elif cli_test_arg == "root":
        return [spec.name for spec in specs]
    return False


def specs_from_cli(args, install_kwargs):
    """Return abstract and concrete spec parsed from the command line."""
    abstract_specs = spack.cmd.parse_specs(args.spec)
    install_kwargs["tests"] = compute_tests_install_kwargs(abstract_specs, args.test)
    try:
        concrete_specs = spack.cmd.parse_specs(
            args.spec, concretize=True, tests=install_kwargs["tests"]
        )
    except SpackError as e:
        tty.debug(e)
        if args.log_format is not None:
            reporter = args.reporter()
            reporter.concretization_report(report_filename(args, abstract_specs), e.message)
        raise
    return abstract_specs, concrete_specs


def concrete_specs_from_file(args):
    """Return the list of concrete specs read from files."""
    result = []
    for file in args.specfiles:
        with open(file, "r") as f:
            if file.endswith("yaml") or file.endswith("yml"):
                s = spack.spec.Spec.from_yaml(f)
            else:
                s = spack.spec.Spec.from_json(f)

        concretized = s.concretized()
        if concretized.dag_hash() != s.dag_hash():
            msg = 'skipped invalid file "{0}". '
            msg += "The file does not contain a concrete spec."
            tty.warn(msg.format(file))
            continue
        result.append(concretized)
    return result


def require_user_confirmation_for_overwrite(concrete_specs, args):
    if args.yes_to_all:
        return

    installed = list(filter(lambda x: x, map(spack.store.db.query_one, concrete_specs)))
    display_args = {"long": True, "show_flags": True, "variants": True}

    if installed:
        tty.msg("The following package specs will be " "reinstalled:\n")
        spack.cmd.display_specs(installed, **display_args)

    not_installed = list(filter(lambda x: x not in installed, concrete_specs))
    if not_installed:
        tty.msg(
            "The following package specs are not installed and"
            " the --overwrite flag was given. The package spec"
            " will be newly installed:\n"
        )
        spack.cmd.display_specs(not_installed, **display_args)

    # We have some specs, so one of the above must have been true
    answer = tty.get_yes_or_no("Do you want to proceed?", default=False)
    if not answer:
        tty.die("Reinstallation aborted.")


def install(parser, args):
    # TODO: unify args.verbose?
    tty.set_verbose(args.verbose or args.install_verbose)

    if args.help_cdash:
        spack.cmd.common.arguments.print_cdash_help()
        return

    if args.no_checksum:
        spack.config.set("config:checksum", False, scope="command_line")

    if args.deprecated:
        spack.config.set("config:deprecated", True, scope="command_line")

    spack.cmd.common.arguments.sanitize_reporter_options(args)

    def reporter_factory(specs):
        if args.log_format is None:
            return None

        context_manager = spack.report.build_context_manager(
            reporter=args.reporter(), filename=report_filename(args, specs=specs), specs=specs
        )
        return context_manager

    install_kwargs = install_kwargs_from_args(args)

    if not args.spec and not args.specfiles:
        # If there are no args but an active environment then install the packages from it.
        install_all_specs_from_active_environment(
            install_kwargs=install_kwargs,
            only_concrete=args.only_concrete,
            cli_test_arg=args.test,
            reporter_factory=reporter_factory,
        )
        return

    # Specs from CLI
    abstract_specs, concrete_specs = specs_from_cli(args, install_kwargs)

    # Concrete specs from YAML or JSON files
    specs_from_file = concrete_specs_from_file(args)
    abstract_specs.extend(specs_from_file)
    concrete_specs.extend(specs_from_file)

    if len(concrete_specs) == 0:
        tty.die("The `spack install` command requires a spec to install.")

    reporter = reporter_factory(concrete_specs) or lang.nullcontext()
    with reporter:
        if args.overwrite:
            require_user_confirmation_for_overwrite(concrete_specs, args)
            install_kwargs["overwrite"] = [spec.dag_hash() for spec in concrete_specs]
        install_specs(zip(abstract_specs, concrete_specs), install_kwargs, args)
