# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
import sys
import tempfile
from typing import Optional

import llnl.string as string
import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize

import spack.cmd
import spack.cmd.common
import spack.cmd.common.arguments
import spack.cmd.common.arguments as arguments
import spack.cmd.install
import spack.cmd.modules
import spack.cmd.uninstall
import spack.config
import spack.environment as ev
import spack.environment.depfile as depfile
import spack.environment.shell
import spack.schema.env
import spack.spec
import spack.tengine
from spack.util.environment import EnvironmentModifications

description = "manage virtual environments"
section = "environments"
level = "short"


#: List of subcommands of `spack env`
subcommands = [
    "activate",
    "deactivate",
    "create",
    ["remove", "rm"],
    ["list", "ls"],
    ["status", "st"],
    "loads",
    "view",
    "update",
    "revert",
    "depfile",
]


#
# env activate
#
def env_activate_setup_parser(subparser):
    """set the current environment"""
    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        "--sh",
        action="store_const",
        dest="shell",
        const="sh",
        help="print sh commands to activate the environment",
    )
    shells.add_argument(
        "--csh",
        action="store_const",
        dest="shell",
        const="csh",
        help="print csh commands to activate the environment",
    )
    shells.add_argument(
        "--fish",
        action="store_const",
        dest="shell",
        const="fish",
        help="print fish commands to activate the environment",
    )
    shells.add_argument(
        "--bat",
        action="store_const",
        dest="shell",
        const="bat",
        help="print bat commands to activate the environment",
    )
    shells.add_argument(
        "--pwsh",
        action="store_const",
        dest="shell",
        const="pwsh",
        help="print powershell commands to activate environment",
    )

    view_options = subparser.add_mutually_exclusive_group()
    view_options.add_argument(
        "--with-view",
        "-v",
        metavar="name",
        help="set runtime environment variables for specific view",
    )
    view_options.add_argument(
        "--without-view",
        "-V",
        action="store_true",
        help="do not set runtime environment variables for any view",
    )

    subparser.add_argument(
        "-p",
        "--prompt",
        action="store_true",
        default=False,
        help="decorate the command line prompt when activating",
    )

    env_options = subparser.add_mutually_exclusive_group()
    env_options.add_argument(
        "--temp",
        action="store_true",
        default=False,
        help="create and activate an environment in a temporary directory",
    )
    env_options.add_argument(
        "-d", "--dir", default=None, help="activate the environment in this directory"
    )
    env_options.add_argument(
        metavar="env",
        dest="activate_env",
        nargs="?",
        default=None,
        help="name of environment to activate",
    )


def create_temp_env_directory():
    """
    Returns the path of a temporary directory in which to
    create an environment
    """
    return tempfile.mkdtemp(prefix="spack-")


def env_activate(args):
    if not args.activate_env and not args.dir and not args.temp:
        tty.die("spack env activate requires an environment name, directory, or --temp")

    if not args.shell:
        spack.cmd.common.shell_init_instructions(
            "spack env activate", "    eval `spack env activate {sh_arg} [...]`"
        )
        return 1

    # Error out when -e, -E, -D flags are given, cause they are ambiguous.
    if args.env or args.no_env or args.env_dir:
        tty.die("Calling spack env activate with --env, --env-dir and --no-env is ambiguous")

    env_name_or_dir = args.activate_env or args.dir

    # Temporary environment
    if args.temp:
        env = create_temp_env_directory()
        env_path = os.path.abspath(env)
        short_name = os.path.basename(env_path)
        ev.create_in_dir(env).write(regenerate=False)

    # Managed environment
    elif ev.exists(env_name_or_dir) and not args.dir:
        env_path = ev.root(env_name_or_dir)
        short_name = env_name_or_dir

    # Environment directory
    elif ev.is_env_dir(env_name_or_dir):
        env_path = os.path.abspath(env_name_or_dir)
        short_name = os.path.basename(env_path)

    else:
        tty.die("No such environment: '%s'" % env_name_or_dir)

    env_prompt = "[%s]" % short_name

    # We only support one active environment at a time, so deactivate the current one.
    if ev.active_environment() is None:
        cmds = ""
        env_mods = EnvironmentModifications()
    else:
        cmds = spack.environment.shell.deactivate_header(shell=args.shell)
        env_mods = spack.environment.shell.deactivate()

    # Activate new environment
    active_env = ev.Environment(env_path)

    # Check if runtime environment variables are requested, and if so, for what view.
    view: Optional[str] = None
    if args.with_view:
        view = args.with_view
        if not active_env.has_view(view):
            tty.die(f"The environment does not have a view named '{view}'")
    elif not args.without_view and active_env.has_view(ev.default_view_name):
        view = ev.default_view_name

    cmds += spack.environment.shell.activate_header(
        env=active_env, shell=args.shell, prompt=env_prompt if args.prompt else None, view=view
    )
    env_mods.extend(spack.environment.shell.activate(env=active_env, view=view))
    cmds += env_mods.shell_modifications(args.shell)
    sys.stdout.write(cmds)


#
# env deactivate
#
def env_deactivate_setup_parser(subparser):
    """deactivate any active environment in the shell"""
    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        "--sh",
        action="store_const",
        dest="shell",
        const="sh",
        help="print sh commands to deactivate the environment",
    )
    shells.add_argument(
        "--csh",
        action="store_const",
        dest="shell",
        const="csh",
        help="print csh commands to deactivate the environment",
    )
    shells.add_argument(
        "--fish",
        action="store_const",
        dest="shell",
        const="fish",
        help="print fish commands to activate the environment",
    )
    shells.add_argument(
        "--bat",
        action="store_const",
        dest="shell",
        const="bat",
        help="print bat commands to activate the environment",
    )
    shells.add_argument(
        "--pwsh",
        action="store_const",
        dest="shell",
        const="pwsh",
        help="print pwsh commands to activate the environment",
    )


def env_deactivate(args):
    if not args.shell:
        spack.cmd.common.shell_init_instructions(
            "spack env deactivate", "    eval `spack env deactivate {sh_arg}`"
        )
        return 1

    # Error out when -e, -E, -D flags are given, cause they are ambiguous.
    if args.env or args.no_env or args.env_dir:
        tty.die("Calling spack env deactivate with --env, --env-dir and --no-env is ambiguous")

    if ev.active_environment() is None:
        tty.die("No environment is currently active.")

    cmds = spack.environment.shell.deactivate_header(args.shell)
    env_mods = spack.environment.shell.deactivate()
    cmds += env_mods.shell_modifications(args.shell)
    sys.stdout.write(cmds)


#
# env create
#
def env_create_setup_parser(subparser):
    """create a new environment"""
    subparser.add_argument("create_env", metavar="env", help="name of environment to create")
    subparser.add_argument(
        "-d", "--dir", action="store_true", help="create an environment in a specific directory"
    )
    subparser.add_argument(
        "--keep-relative",
        action="store_true",
        help="copy relative develop paths verbatim into the new environment"
        " when initializing from envfile",
    )
    view_opts = subparser.add_mutually_exclusive_group()
    view_opts.add_argument(
        "--without-view", action="store_true", help="do not maintain a view for this environment"
    )
    view_opts.add_argument(
        "--with-view",
        help="specify that this environment should maintain a view at the"
        " specified path (by default the view is maintained in the"
        " environment directory)",
    )
    subparser.add_argument(
        "envfile",
        nargs="?",
        default=None,
        help="either a lockfile (must end with '.json' or '.lock') or a manifest file",
    )


def env_create(args):
    if args.with_view:
        # Expand relative paths provided on the command line to the current working directory
        # This way we interpret `spack env create --with-view ./view --dir ./env` as
        # a view in $PWD/view, not $PWD/env/view. This is different from specifying a relative
        # path in the manifest, which is resolved relative to the manifest file's location.
        with_view = os.path.abspath(args.with_view)
    elif args.without_view:
        with_view = False
    else:
        # Note that 'None' means unspecified, in which case the Environment
        # object could choose to enable a view by default. False means that
        # the environment should not include a view.
        with_view = None

    env = _env_create(
        args.create_env,
        init_file=args.envfile,
        dir=args.dir,
        with_view=with_view,
        keep_relative=args.keep_relative,
    )

    # Generate views, only really useful for environments created from spack.lock files.
    env.regenerate_views()


def _env_create(name_or_path, *, init_file=None, dir=False, with_view=None, keep_relative=False):
    """Create a new environment, with an optional yaml description.

    Arguments:
        name_or_path (str): name of the environment to create, or path to it
        init_file (str or file): optional initialization file -- can be
            a JSON lockfile (*.lock, *.json) or YAML manifest file
        dir (bool): if True, create an environment in a directory instead
            of a named environment
        keep_relative (bool): if True, develop paths are copied verbatim into
            the new environment file, otherwise they may be made absolute if the
            new environment is in a different location
    """
    if not dir:
        env = ev.create(
            name_or_path, init_file=init_file, with_view=with_view, keep_relative=keep_relative
        )
        tty.msg("Created environment '%s' in %s" % (name_or_path, env.path))
        tty.msg("You can activate this environment with:")
        tty.msg("  spack env activate %s" % (name_or_path))
        return env

    env = ev.create_in_dir(
        name_or_path, init_file=init_file, with_view=with_view, keep_relative=keep_relative
    )
    tty.msg("Created environment in %s" % env.path)
    tty.msg("You can activate this environment with:")
    tty.msg("  spack env activate %s" % env.path)
    return env


#
# env remove
#
def env_remove_setup_parser(subparser):
    """remove an existing environment"""
    subparser.add_argument("rm_env", metavar="env", nargs="+", help="environment(s) to remove")
    arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_remove(args):
    """Remove a *named* environment.

    This removes an environment managed by Spack. Directory environments
    and manifests embedded in repositories should be removed manually.
    """
    read_envs = []
    bad_envs = []
    for env_name in args.rm_env:
        try:
            env = ev.read(env_name)
            read_envs.append(env)
        except spack.config.ConfigFormatError:
            bad_envs.append(env_name)

    if not args.yes_to_all:
        environments = string.plural(len(args.rm_env), "environment", show_n=False)
        envs = string.comma_and(args.rm_env)
        answer = tty.get_yes_or_no(f"Really remove {environments} {envs}?", default=False)
        if not answer:
            tty.die("Will not remove any environments")

    for env in read_envs:
        name = env.name
        if env.active:
            tty.die(f"Environment {name} can't be removed while activated.")
        env.destroy()
        tty.msg(f"Successfully removed environment '{name}'")

    for bad_env_name in bad_envs:
        shutil.rmtree(
            spack.environment.environment.environment_dir_from_name(bad_env_name, exists_ok=True)
        )
        tty.msg(f"Successfully removed environment '{bad_env_name}'")


#
# env list
#
def env_list_setup_parser(subparser):
    """list available environments"""


def env_list(args):
    names = ev.all_environment_names()

    color_names = []
    for name in names:
        if ev.active(name):
            name = colorize("@*g{%s}" % name)
        color_names.append(name)

    # say how many there are if writing to a tty
    if sys.stdout.isatty():
        if not names:
            tty.msg("No environments")
        else:
            tty.msg("%d environments" % len(names))

    colify(color_names, indent=4)


class ViewAction:
    regenerate = "regenerate"
    enable = "enable"
    disable = "disable"

    @staticmethod
    def actions():
        return [ViewAction.regenerate, ViewAction.enable, ViewAction.disable]


#
# env view
#
def env_view_setup_parser(subparser):
    """manage a view associated with the environment"""
    subparser.add_argument(
        "action", choices=ViewAction.actions(), help="action to take for the environment's view"
    )
    subparser.add_argument(
        "view_path", nargs="?", help="when enabling a view, optionally set the path manually"
    )


def env_view(args):
    env = ev.active_environment()

    if not env:
        tty.msg("No active environment")
        return

    if args.action == ViewAction.regenerate:
        env.regenerate_views()
    elif args.action == ViewAction.enable:
        if args.view_path:
            view_path = args.view_path
        else:
            view_path = env.view_path_default
        env.update_default_view(view_path)
        env.write()
    elif args.action == ViewAction.disable:
        env.update_default_view(path_or_bool=False)
        env.write()


#
# env status
#
def env_status_setup_parser(subparser):
    """print whether there is an active environment"""


def env_status(args):
    env = ev.active_environment()
    if env:
        if env.path == os.getcwd():
            tty.msg("Using %s in current directory: %s" % (ev.manifest_name, env.path))
        else:
            tty.msg("In environment %s" % env.name)

        # Check if environment views can be safely activated
        env.check_views()
    else:
        tty.msg("No active environment")


#
# env loads
#
def env_loads_setup_parser(subparser):
    """list modules for an installed environment '(see spack module loads)'"""
    subparser.add_argument(
        "-n",
        "--module-set-name",
        default="default",
        help="module set for which to generate load operations",
    )
    subparser.add_argument(
        "-m",
        "--module-type",
        choices=("tcl", "lmod"),
        help="type of module system to generate loads for",
    )
    spack.cmd.modules.add_loads_arguments(subparser)


def env_loads(args):
    env = spack.cmd.require_active_env(cmd_name="env loads")

    # Set the module types that have been selected
    module_type = args.module_type
    if module_type is None:
        # If no selection has been made select all of them
        module_type = "tcl"

    recurse_dependencies = args.recurse_dependencies
    args.recurse_dependencies = False

    loads_file = fs.join_path(env.path, "loads")
    with open(loads_file, "w") as f:
        specs = env._get_environment_specs(recurse_dependencies=recurse_dependencies)

        spack.cmd.modules.loads(module_type, specs, args, f)

    print("To load this environment, type:")
    print("   source %s" % loads_file)


def env_update_setup_parser(subparser):
    """update environments to the latest format"""
    subparser.add_argument(
        metavar="env", dest="update_env", help="name or directory of the environment to activate"
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_update(args):
    manifest_file = ev.manifest_file(args.update_env)
    backup_file = manifest_file + ".bkp"
    needs_update = not ev.is_latest_format(manifest_file)

    if not needs_update:
        tty.msg('No update needed for the environment "{0}"'.format(args.update_env))
        return

    proceed = True
    if not args.yes_to_all:
        msg = (
            'The environment "{0}" is going to be updated to the latest '
            "schema format.\nIf the environment is updated, versions of "
            "Spack that are older than this version may not be able to "
            "read it. Spack stores backups of the updated environment "
            'which can be retrieved with "spack env revert"'
        )
        tty.msg(msg.format(args.update_env))
        proceed = tty.get_yes_or_no("Do you want to proceed?", default=False)

    if not proceed:
        tty.die("Operation aborted.")

    ev.update_yaml(manifest_file, backup_file=backup_file)
    msg = 'Environment "{0}" has been updated [backup={1}]'
    tty.msg(msg.format(args.update_env, backup_file))


def env_revert_setup_parser(subparser):
    """restore environments to their state before update"""
    subparser.add_argument(
        metavar="env", dest="revert_env", help="name or directory of the environment to activate"
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_revert(args):
    manifest_file = ev.manifest_file(args.revert_env)
    backup_file = manifest_file + ".bkp"

    # Check that both the spack.yaml and the backup exist, the inform user
    # on what is going to happen and ask for confirmation
    if not os.path.exists(manifest_file):
        msg = "cannot find the manifest file of the environment [file={0}]"
        tty.die(msg.format(manifest_file))
    if not os.path.exists(backup_file):
        msg = "cannot find the old manifest file to be restored [file={0}]"
        tty.die(msg.format(backup_file))

    proceed = True
    if not args.yes_to_all:
        msg = (
            "Spack is going to overwrite the current manifest file"
            " with a backup copy [manifest={0}, backup={1}]"
        )
        tty.msg(msg.format(manifest_file, backup_file))
        proceed = tty.get_yes_or_no("Do you want to proceed?", default=False)

    if not proceed:
        tty.die("Operation aborted.")

    shutil.copy(backup_file, manifest_file)
    os.remove(backup_file)
    msg = 'Environment "{0}" reverted to old state'
    tty.msg(msg.format(manifest_file))


def env_depfile_setup_parser(subparser):
    """generate a depfile from the concrete environment specs"""
    subparser.add_argument(
        "--make-prefix",
        "--make-target-prefix",
        default=None,
        metavar="TARGET",
        help="prefix Makefile targets (and variables) with <TARGET>/<name>\n\nby default "
        "the absolute path to the directory makedeps under the environment metadata dir is "
        "used. can be set to an empty string --make-prefix ''",
    )
    subparser.add_argument(
        "--make-disable-jobserver",
        default=True,
        action="store_false",
        dest="jobserver",
        help="disable POSIX jobserver support",
    )
    subparser.add_argument(
        "--use-buildcache",
        dest="use_buildcache",
        type=arguments.use_buildcache,
        default="package:auto,dependencies:auto",
        metavar="[{auto,only,never},][package:{auto,only,never},][dependencies:{auto,only,never}]",
        help="when using `only`, redundant build dependencies are pruned from the DAG\n\n"
        "this flag is passed on to the generated spack install commands",
    )
    subparser.add_argument(
        "-o",
        "--output",
        default=None,
        metavar="FILE",
        help="write the depfile to FILE rather than to stdout",
    )
    subparser.add_argument(
        "-G",
        "--generator",
        default="make",
        choices=("make",),
        help="specify the depfile type\n\ncurrently only make is supported",
    )
    subparser.add_argument(
        metavar="specs",
        dest="specs",
        nargs=argparse.REMAINDER,
        default=None,
        help="generate a depfile only for matching specs in the environment",
    )


def env_depfile(args):
    # Currently only make is supported.
    spack.cmd.require_active_env(cmd_name="env depfile")

    # What things do we build when running make? By default, we build the
    # root specs. If specific specs are provided as input, we build those.
    filter_specs = spack.cmd.parse_specs(args.specs) if args.specs else None
    template = spack.tengine.make_environment().get_template(os.path.join("depfile", "Makefile"))
    model = depfile.MakefileModel.from_env(
        ev.active_environment(),
        filter_specs=filter_specs,
        pkg_buildcache=depfile.UseBuildCache.from_string(args.use_buildcache[0]),
        dep_buildcache=depfile.UseBuildCache.from_string(args.use_buildcache[1]),
        make_prefix=args.make_prefix,
        jobserver=args.jobserver,
    )
    makefile = template.render(model.to_dict())

    # Finally write to stdout/file.
    if args.output:
        with open(args.output, "w") as f:
            f.write(makefile)
    else:
        sys.stdout.write(makefile)


#: Dictionary mapping subcommand names and aliases to functions
subcommand_functions = {}


#
# spack env
#
def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="env_command")

    for name in subcommands:
        if isinstance(name, (list, tuple)):
            name, aliases = name[0], name[1:]
        else:
            aliases = []

        # add commands to subcommands dict
        function_name = "env_%s" % name
        function = globals()[function_name]
        for alias in [name] + aliases:
            subcommand_functions[alias] = function

        # make a subparser and run the command's setup function on it
        setup_parser_cmd_name = "env_%s_setup_parser" % name
        setup_parser_cmd = globals()[setup_parser_cmd_name]

        subsubparser = sp.add_parser(name, aliases=aliases, help=setup_parser_cmd.__doc__)
        setup_parser_cmd(subsubparser)


def env(parser, args):
    """Look for a function called environment_<name> and call it."""
    action = subcommand_functions[args.env_command]
    action(args)
