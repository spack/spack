# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import contextlib
import os
import shlex
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

import spack.cmd
import spack.cmd.common
import spack.cmd.common.arguments
import spack.cmd.modules
import spack.config
import spack.enums
import spack.environment as ev
import spack.environment.environment
import spack.environment.shell
import spack.error
import spack.spec
import spack.spec_diff
import spack.tengine
import spack.util.filesystem as fs
import spack.util.spack_json as sjson
import spack.variant
from spack.active_environment import active_environment
from spack.cmd.common import arguments
from spack.environment import depfile
from spack.environment import diff as env_diff_core
from spack.traverse import traverse_nodes
from spack.util import string, tty
from spack.util.environment import EnvironmentModifications
from spack.util.filesystem import islink, symlink
from spack.util.tty.colify import colify, render_blocks, terminal_columns
from spack.util.tty.color import cescape, clen, colorize

description = "manage environments"
section = "environments"
level = "short"


#: List of subcommands of ``spack env``
subcommands: List[Tuple[str, ...]] = [
    ("activate",),
    ("deactivate",),
    ("create",),
    ("remove", "rm"),
    ("rename", "mv"),
    ("list", "ls"),
    ("status", "st"),
    ("diff",),
    ("loads",),
    ("view",),
    ("update",),
    ("revert",),
    ("depfile",),
    ("track",),
    ("untrack",),
]


#
# env create
#
def env_create_setup_parser(subparser):
    """\
    create a new environment

    create a new environment or, optionally, copy an existing environment

    a manifest file results in a new abstract environment while a lock file
    creates a new concrete environment
    """
    subparser.add_argument(
        "env_name", metavar="env", help="name or directory of the new environment"
    )
    subparser.add_argument(
        "-d", "--dir", action="store_true", help="create an environment in a specific directory"
    )
    subparser.add_argument(
        "--keep-relative",
        action="store_true",
        help="copy envfile's relative develop paths verbatim",
    )
    view_opts = subparser.add_mutually_exclusive_group()
    view_opts.add_argument(
        "--without-view", action="store_true", help="do not maintain a view for this environment"
    )
    view_opts.add_argument(
        "--with-view", help="maintain view at WITH_VIEW (vs. environment's directory)"
    )
    subparser.add_argument(
        "envfile",
        nargs="?",
        default=None,
        help="manifest or lock file (ends with '.json' or '.lock') or an environment name or path",
    )
    subparser.add_argument(
        "--include-concrete",
        action="append",
        help="copy concrete specs from INCLUDE_CONCRETE's environment",
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

    include_concrete = None
    if hasattr(args, "include_concrete"):
        include_concrete = args.include_concrete

    env = _env_create(
        args.env_name,
        init_file=args.envfile,
        dir=args.dir or os.path.sep in args.env_name or args.env_name in (".", ".."),
        with_view=with_view,
        keep_relative=args.keep_relative,
        include_concrete=include_concrete,
    )

    # Generate views, only really useful for environments created from spack.lock files.
    if args.envfile:
        env.regenerate_views()


def _env_create(
    name_or_path: str,
    *,
    init_file: Optional[str] = None,
    dir: bool = False,
    with_view: Optional[Union[bool, str]] = None,
    keep_relative: bool = False,
    include_concrete: Optional[List[str]] = None,
):
    """Create a new environment, with an optional yaml description.

    Arguments:
        name_or_path: name of the environment to create, or path to it
        init_file: optional initialization file -- can be a JSON lockfile
            (*.lock, *.json), YAML manifest file, or env dir
        dir: if True, create an environment in a directory instead of a named
            environment
        keep_relative: if True, develop paths are copied verbatim into the new
            environment file, otherwise they may be made absolute if the new
            environment is in a different location
        include_concrete: list of the included concrete environments
    """
    if not dir:
        env = ev.create(
            name_or_path,
            init_file=init_file,
            with_view=with_view,
            keep_relative=keep_relative,
            include_concrete=include_concrete,
        )
        tty.msg(
            colorize(
                f"Created environment @c{{{cescape(name_or_path)}}} in: @c{{{cescape(env.path)}}}"
            )
        )
    else:
        env = ev.create_in_dir(
            name_or_path,
            init_file=init_file,
            with_view=with_view,
            keep_relative=keep_relative,
            include_concrete=include_concrete,
        )
        tty.msg(colorize(f"Created independent environment in: @c{{{cescape(env.path)}}}"))
    tty.msg(f"Activate with: {colorize(f'@c{{spack env activate {cescape(name_or_path)}}}')}")
    return env


#
# env activate
#
def env_activate_setup_parser(subparser):
    """set the active environment"""
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
        "-v",
        "--with-view",
        metavar="name",
        help="set runtime environment variables for the named view",
    )
    view_options.add_argument(
        "-V",
        "--without-view",
        action="store_true",
        help="do not set runtime environment variables for any view",
    )

    subparser.add_argument(
        "-p",
        "--prompt",
        action="store_true",
        default=False,
        help="add the active environment to the command line prompt",
    )

    subparser.add_argument(
        "--temp",
        action="store_true",
        default=False,
        help="create and activate in a temporary directory",
    )
    subparser.add_argument(
        "--create",
        action="store_true",
        default=False,
        help="create and activate the environment if it doesn't exist",
    )
    subparser.add_argument(
        "--envfile",
        nargs="?",
        default=None,
        help="manifest or lock file (ends with '.json' or '.lock')",
    )
    subparser.add_argument(
        "--keep-relative",
        action="store_true",
        help="copy envfile's relative develop paths verbatim when create",
    )
    subparser.add_argument(
        "-d",
        "--dir",
        default=False,
        action="store_true",
        help="activate environment based on the directory supplied",
    )
    subparser.add_argument(
        metavar="env",
        dest="env_name",
        nargs="?",
        default=None,
        help=("name or directory of the environment being activated"),
    )


def create_temp_env_directory():
    """
    Returns the path of a temporary directory in which to
    create an environment
    """
    return tempfile.mkdtemp(prefix="spack-")


def _tty_info(msg):
    """tty.info like function that prints the equivalent printf statement for eval."""
    decorated = f"{colorize('@*b{==>}')} {msg}\n"
    executor = "echo" if sys.platform == "win32" else "printf"
    print(f"{executor} {shlex.quote(decorated)};")


def env_activate(args):
    if not args.shell:
        spack.cmd.common.shell_init_instructions(
            "spack env activate", "    eval `spack env activate {sh_arg} [...]`"
        )
        return 1

    # Error out when -e, -E, -D flags are given, cause they are ambiguous.
    if args.env or args.no_env or args.env_dir:
        tty.die("Calling spack env activate with --env, --env-dir and --no-env is ambiguous")

    # special parser error handling relative to the --temp flag
    temp_conflicts = iter([args.keep_relative, args.dir, args.env_name, args.with_view])
    if args.temp and any(temp_conflicts):
        tty.die(
            "spack env activate --temp cannot be combined with managed environments, --with-view,"
            " --keep-relative, or --dir."
        )

    # When executing `spack env activate` without further arguments, activate
    # the default environment. It's created when it doesn't exist yet.
    if not args.env_name and not args.temp:
        short_name = "default"
        if not ev.exists(short_name):
            ev.create(short_name)
            action = "Created and activated"
        else:
            action = "Activated"
        env_path = ev.root(short_name)
        _tty_info(f"{action} default environment in {env_path}")

    # Temporary environment
    elif args.temp:
        env = create_temp_env_directory()
        env_path = os.path.abspath(env)
        short_name = os.path.basename(env_path)
        view = not args.without_view
        ev.create_in_dir(env, with_view=view).write(regenerate=False)
        _tty_info(f"Created and activated temporary environment in {env_path}")

    # Managed environment
    elif ev.exists(args.env_name) and not args.dir:
        env_path = ev.root(args.env_name)
        short_name = args.env_name

    # Environment directory
    elif ev.is_env_dir(args.env_name):
        env_path = os.path.abspath(args.env_name)
        short_name = os.path.basename(env_path)

    # create if user requested, and then recall recursively
    elif args.create:
        tty.set_msg_enabled(False)
        env_create(args)
        tty.set_msg_enabled(True)
        env_activate(args)
        return

    else:
        tty.die("No such environment: '%s'" % args.env_name)

    env_prompt = "[%s]" % short_name

    # We only support one active environment at a time, so deactivate the current one.
    if active_environment() is None:
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
    """deactivate the active environment"""
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

    if active_environment() is None:
        tty.die("No environment is currently active.")

    cmds = spack.environment.shell.deactivate_header(args.shell)
    env_mods = spack.environment.shell.deactivate()
    cmds += env_mods.shell_modifications(args.shell)
    sys.stdout.write(cmds)


#
# env track
#
def env_track_setup_parser(subparser):
    """track an environment from a directory in Spack"""
    subparser.add_argument("-n", "--name", help="custom environment name")
    subparser.add_argument("dir", help="path to environment")
    arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_track(args):
    src_path = os.path.abspath(args.dir)
    if not ev.is_env_dir(src_path):
        tty.die("Cannot track environment. Path doesn't contain an environment")

    if args.name:
        name = args.name
    else:
        name = os.path.basename(src_path)

    try:
        dst_path = ev.environment_dir_from_name(name, exists_ok=False)
    except ev.SpackEnvironmentError:
        tty.die(
            f"An environment named {name} already exists. Set a name with:"
            "\n\n"
            f"        spack env track --name NAME {src_path}\n"
        )

    symlink(src_path, dst_path)

    tty.msg(f"Tracking environment in {src_path}")
    tty.msg(
        "You can now activate this environment with the following command:\n\n"
        f"        spack env activate {name}\n"
    )


#
# env remove & untrack helpers
#
def filter_managed_env_names(env_names: Set[str]) -> Set[str]:
    tracked_env_names = {e for e in env_names if islink(ev.environment_dir_from_name(e))}
    managed_env_names = env_names - set(tracked_env_names)

    num_managed_envs = len(managed_env_names)
    managed_envs_str = " ".join(managed_env_names)
    if num_managed_envs >= 2:
        tty.error(
            f"The following are not tracked environments. "
            "To remove them completely run,"
            "\n\n"
            f"        spack env rm {managed_envs_str}\n"
        )

    elif num_managed_envs > 0:
        tty.error(
            f"'{managed_envs_str}' is not a tracked env. "
            "To remove it completely run,"
            "\n\n"
            f"        spack env rm {managed_envs_str}\n"
        )

    return tracked_env_names


def get_valid_envs(env_names: Set[str]) -> Set[ev.Environment]:
    valid_envs = set()
    for env_name in env_names:
        try:
            env = ev.read(env_name)
            valid_envs.add(env)

        except (spack.config.ConfigFormatError, ev.SpackEnvironmentConfigError):
            pass

    return valid_envs


def _env_untrack_or_remove(
    env_names: List[str], remove: bool = False, force: bool = False, yes_to_all: bool = False
):
    all_env_names = set(ev.all_environment_names())
    known_env_names = set(env_names).intersection(all_env_names)
    unknown_env_names = set(env_names) - known_env_names

    # print error for unknown environments
    for env_name in unknown_env_names:
        tty.error(f"Environment '{env_name}' does not exist")

    # if only unlinking is allowed, remove all environments
    # which do not point internally at symlinks
    if not remove:
        env_names_to_remove = filter_managed_env_names(known_env_names)
    else:
        env_names_to_remove = known_env_names

    # initialize all environments with valid spack.yaml configs
    all_valid_envs = get_valid_envs(all_env_names)

    # build a task list of environments and bad env names to remove
    envs_to_remove = [e for e in all_valid_envs if e.name in env_names_to_remove]
    bad_env_names_to_remove = env_names_to_remove - {e.name for e in envs_to_remove}
    for remove_env in envs_to_remove:
        for env in all_valid_envs:
            # don't check if an environment is included to itself
            if env.name == remove_env.name:
                continue

            # check if an environment is included in another
            if remove_env.path in env.included_concrete_env_root_dirs:
                msg = f"Environment '{remove_env.name}' is used by environment '{env.name}'"
                if force:
                    tty.warn(msg)
                else:
                    tty.error(msg)
                    envs_to_remove.remove(remove_env)

    # ask the user if they really want to remove the known environments
    # force should do the same as yes to all here following the semantics of rm
    if not (yes_to_all or force) and (envs_to_remove or bad_env_names_to_remove):
        environments = string.plural(len(env_names_to_remove), "environment", show_n=False)
        envs = string.comma_and(list(env_names_to_remove))
        answer = tty.get_yes_or_no(
            f"Really {'remove' if remove else 'untrack'} {environments} {envs}?", default=False
        )
        if not answer:
            tty.msg(f"Will not remove environment(s) {envs}")
            return

    # keep track of the environments we remove for later printing the exit code
    removed_env_names = []
    for env in envs_to_remove:
        name = env.name
        if not force and env.active:
            tty.error(
                f"Environment '{name}' can't be "
                f"{'removed' if remove else 'untracked'} while activated."
            )
            continue
        # Get path to check if environment is a tracked / symlinked environment
        if islink(env.path):
            real_env_path = os.path.realpath(env.path)
            os.unlink(env.path)
            tty.msg(
                f"Successfully untracked environment '{name}', "
                "but it can still be found at:\n\n"
                f"        {real_env_path}\n"
            )
        else:
            env.destroy()
            tty.msg(f"Successfully removed environment '{name}'")

        removed_env_names.append(env.name)

    for bad_env_name in bad_env_names_to_remove:
        shutil.rmtree(
            spack.environment.environment.environment_dir_from_name(bad_env_name, exists_ok=True)
        )
        tty.msg(f"Successfully removed environment '{bad_env_name}'")
        removed_env_names.append(bad_env_name)

    # Following the design of linux rm we should exit with a status of 1
    # anytime we cannot delete every environment the user asks for.
    # However, we should still process all the environments we know about
    # and delete them instead of failing on the first unknown environment.
    if len(removed_env_names) < len(known_env_names):
        sys.exit(1)


#
# env untrack
#
def env_untrack_setup_parser(subparser):
    """untrack an environment from a directory in Spack"""
    subparser.add_argument("env", nargs="+", help="tracked environment name")
    subparser.add_argument(
        "-f", "--force", action="store_true", help="force unlink even when environment is active"
    )
    arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_untrack(args):
    _env_untrack_or_remove(
        env_names=args.env, force=args.force, yes_to_all=args.yes_to_all, remove=False
    )


#
# env remove
#
def env_remove_setup_parser(subparser):
    """\
    remove managed environment(s)

    remove existing environment(s) managed by Spack

    directory environments and manifests embedded in repositories must be
    removed manually
    """
    subparser.add_argument(
        "rm_env", metavar="env", nargs="+", help="name(s) of the environment(s) being removed"
    )
    arguments.add_common_arguments(subparser, ["yes_to_all"])
    subparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="force removal even when included in other environment(s)",
    )


def env_remove(args):
    """remove existing environment(s)"""
    _env_untrack_or_remove(
        env_names=args.rm_env, remove=True, force=args.force, yes_to_all=args.yes_to_all
    )


#
# env rename
#
def env_rename_setup_parser(subparser):
    """\
    rename an existing environment

    rename a managed environment or move an independent/directory environment

    operation cannot be performed to or from an active environment
    """
    subparser.add_argument(
        "mv_from", metavar="from", help="current name or directory of the environment"
    )
    subparser.add_argument("mv_to", metavar="to", help="new name or directory for the environment")
    subparser.add_argument(
        "-d",
        "--dir",
        action="store_true",
        help="positional arguments are environment directory paths",
    )
    subparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="force renaming even if overwriting an existing environment",
    )


def env_rename(args):
    """rename or move an existing environment"""

    # Directory option has been specified
    if args.dir:
        if not ev.is_env_dir(args.mv_from):
            tty.die("The specified path does not correspond to a valid spack environment")
        from_path = Path(args.mv_from)
        if not args.force:
            if ev.is_env_dir(args.mv_to):
                tty.die(
                    "The new path corresponds to an existing environment;"
                    " specify the --force flag to overwrite it."
                )
            if Path(args.mv_to).exists():
                tty.die("The new path already exists; specify the --force flag to overwrite it.")
        to_path = Path(args.mv_to)

    # Name option being used
    elif ev.exists(args.mv_from):
        from_path = ev.environment.environment_dir_from_name(args.mv_from)
        if not args.force and ev.exists(args.mv_to):
            tty.die(
                "The new name corresponds to an existing environment;"
                " specify the --force flag to overwrite it."
            )
        to_path = ev.environment.root(args.mv_to)

    # Neither
    else:
        tty.die("The specified name does not correspond to a managed spack environment")

    # Guard against renaming from or to an active environment
    active_env = active_environment()
    if active_env:
        from_env = ev.Environment(from_path)
        if from_env.path == active_env.path:
            tty.die("Cannot rename active environment")
        if to_path == active_env.path:
            tty.die(f"{args.mv_to} is an active environment")

    shutil.rmtree(to_path, ignore_errors=True)
    fs.rename(from_path, to_path)
    tty.msg(f"Successfully renamed environment {args.mv_from} to {args.mv_to}")


#
# env list
#
def env_list_setup_parser(subparser):
    """list all managed environments"""


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
    """\
    manage the environment's view

    provide the path when enabling a view with a non-default path
    """
    subparser.add_argument(
        "action", choices=ViewAction.actions(), help="action to take for the environment's view"
    )
    subparser.add_argument("view_path", nargs="?", help="view's non-default path when enabling it")


def env_view(args):
    env = active_environment()

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
    """print active environment status"""


def env_status(args):
    env = active_environment()
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
    env = spack.cmd.require_active_env(args.subparser)

    # Set the module types that have been selected
    module_type = args.module_type
    if module_type is None:
        # If no selection has been made select all of them
        module_type = "tcl"

    recurse_dependencies = args.recurse_dependencies
    args.recurse_dependencies = False

    loads_file = fs.join_path(env.path, "loads")
    with open(loads_file, "w", encoding="utf-8") as f:
        if not recurse_dependencies:
            specs = [env.specs_by_hash[x.hash] for x in env.concretized_roots]
        else:
            specs = list(traverse_nodes(env.concrete_roots(), deptype=("link", "run")))
        spack.cmd.modules.loads(module_type, specs, args, f)

    print("To load this environment, type:")
    print("   source %s" % loads_file)


def env_update_setup_parser(subparser):
    """\
    update the environment manifest to the latest schema format

    update the environment to the latest schema format, which may not be
    readable by older versions of spack

    a backup copy of the manifest is retained in case there is a need to revert
    this operation
    """
    subparser.add_argument(
        metavar="env", dest="update_env", help="name or directory of the environment"
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_update(args):
    """update the manifest to the latest format"""
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
    """\
    restore the environment manifest to its previous format

    revert the environment's manifest to the schema format from its last
    'spack env update'

    the current manifest will be overwritten by the backup copy and the backup
    copy will be removed
    """
    subparser.add_argument(
        metavar="env", dest="revert_env", help="name or directory of the environment"
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ["yes_to_all"])


def env_revert(args):
    """restore the environment manifest to its previous format"""
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
    """\
    generate a depfile to exploit parallel builds across specs

    requires the active environment to be concrete
    """
    subparser.add_argument(
        "--make-prefix",
        "--make-target-prefix",
        default=None,
        metavar="TARGET",
        help="prefix Makefile targets/variables with <TARGET>/<name>,\n"
        "which can be an empty string (--make-prefix '')\n"
        "defaults to the absolute path of the environment's makedeps\n"
        "environment metadata dir\n",
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
        help="use `only` to prune redundant build dependencies\n"
        "option is also passed to generated spack install commands",
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
        help="specify the depfile type (only supports `make`)",
    )
    subparser.add_argument(
        metavar="specs",
        dest="specs",
        nargs=argparse.REMAINDER,
        default=None,
        help="limit the generated file to matching specs",
    )


def env_depfile(args):
    # Currently only make is supported.
    spack.cmd.require_active_env(args.subparser)

    env = active_environment()

    # What things do we build when running make? By default, we build the
    # root specs. If specific specs are provided as input, we build those.
    filter_specs = spack.cmd.parse_specs(args.specs) if args.specs else None
    template = spack.tengine.make_environment().get_template(os.path.join("depfile", "Makefile"))
    model = depfile.MakefileModel.from_env(
        env,
        filter_specs=filter_specs,
        pkg_buildcache=depfile.UseBuildCache.from_string(args.use_buildcache[0]),
        dep_buildcache=depfile.UseBuildCache.from_string(args.use_buildcache[1]),
        make_prefix=args.make_prefix,
        jobserver=args.jobserver,
    )

    # Warn in case we're generating a depfile for an empty environment. We don't automatically
    # concretize; the user should do that explicitly. Could be changed in the future if requested.
    if model.empty:
        if not env.user_specs:
            tty.warn("no specs in the environment")
        elif filter_specs is not None:
            tty.warn("no concrete matching specs found in environment")
        else:
            tty.warn("environment is not concretized. Run `spack concretize` first")

    makefile = template.render(model.to_dict())

    # Finally write to stdout/file.
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(makefile)
    else:
        sys.stdout.write(makefile)


#: Short identifiers for the two environments being compared, used across the whole diff output.
#: They are directional, unlike the comparison itself: the second environment is taken to be the
#: later state of the first, which is the assumption `_attribute_style` judges a change against.
_ENV_BEFORE = "before"
_ENV_AFTER = "after"

#: Above this many input specs reaching the same divergent node, report a count instead of a list
_MAX_LISTED_INPUTS = 3

#: Indentation of every section header and of the entries under it
_BAND_INDENT = 2

#: Width assumed for section headers when the output is not going to a terminal
_DEFAULT_WIDTH = 80

#: Shortest rule drawn after a section header, when its content is narrower than its label
_MIN_RULE = 6

#: Columns `tty.band` spends on its own decoration, i.e. the leading "-- " and the trailing space
_BAND_DECORATION = 4

#: Categories with no spec syntax to be rendered in, reported on a line of their own instead
_ANNOTATED_CATEGORIES = (spack.spec_diff.DiffCategory.EXTERNAL, spack.spec_diff.DiffCategory.OTHER)


def env_diff_setup_parser(subparser):
    """compare two concrete environments

    Report the input specs unique to each environment, and for common input specs the
    first node in each concrete DAG whose configuration differs

    Either side can be a full environment, or just a lockfile.

    The second environment is taken to be the later state of the first: a difference that a
    re-concretization would explain, like a newer version or a variant at its default, is
    reported normally, and only the other kinds are highlighted
    """
    subparser.add_argument(
        "before", help="environment to compare from: a name, a directory, or a lockfile"
    )
    subparser.add_argument(
        "after",
        help="environment to compare to, the later state: a name, a directory, or a lockfile",
    )
    subparser.add_argument(
        "--no-prune",
        action="store_false",
        default=True,
        dest="prune",
        help="report every differing node, instead of reporting the node where a difference "
        "first appears and skipping the subgraph below it",
    )
    subparser.add_argument(
        "--json",
        action="store_true",
        default=False,
        dest="dump_json",
        help="dump json output instead of pretty printing",
    )


def _is_lockfile(path: str) -> bool:
    """Whether a file is a Spack lockfile, decided by its content rather than by its name.

    Only used to word an error, so the cost of reading the file again does not matter here.
    """
    try:
        with open(path, "r", encoding="utf-8") as stream:
            data = sjson.load(stream)
    except (OSError, ValueError):
        return False
    meta = data.get("_meta") if isinstance(data, dict) else None
    return isinstance(meta, dict) and meta.get("file-type") == "spack-lockfile"


def _open_environment_to_diff(
    stack: contextlib.ExitStack, argument: str
) -> Tuple[ev.Environment, Dict[str, Optional[str]]]:
    """Resolve one command-line argument to an environment, and to the identity to report for it.

    A name or an environment directory is opened where it is. A lockfile is materialized as a
    throwaway environment, which lives until the stack is closed, so that comparing two lockfiles
    does not require creating an environment for each of them first.

    Raises:
        spack.environment.environment.SpackEnvironmentError: if the argument is a file that is
            not a lockfile
    """
    path = spack.config.substitute_path_variables(argument)
    if os.path.isfile(path):
        root = stack.enter_context(tempfile.TemporaryDirectory(prefix="spack-env-diff-"))
        # A lockfile is told from a manifest by suffix, so only one that is not named like a
        # lockfile has to be staged under a canonical name; create_in_dir copies it either way
        init_file = path
        if not path.endswith((".lock", ".json")):
            init_file = os.path.join(root, ev.lockfile_name)
            shutil.copy(path, init_file)
        try:
            env = ev.create_in_dir(os.path.join(root, "env"), init_file=init_file)
        except ev.SpackEnvironmentError as e:
            # Checking what the file is only once materializing it failed keeps the success
            # path from parsing a lockfile that is about to be parsed again anyway
            if _is_lockfile(path):
                raise
            hint = f"pass an environment name, a directory, or a '{ev.lockfile_name}' file"
            if os.path.basename(path) == ev.manifest_name:
                directory = os.path.dirname(argument) or "."
                hint = f"to compare the environment it describes, pass '{directory}'"
            raise ev.SpackEnvironmentError(f"'{argument}' is not a Spack lockfile", hint) from e
        # The temporary directory is an implementation detail, so the lockfile is what the
        # comparison reports as this side's identity. It has no name of its own.
        return env, {"name": None, "path": os.path.abspath(path)}

    env = ev.environment_from_name_or_dir(argument)
    return env, {"name": env.name, "path": env.path}


def env_diff(args):
    with contextlib.ExitStack() as stack:
        env_before, identity_before = _open_environment_to_diff(stack, args.before)
        env_after, identity_after = _open_environment_to_diff(stack, args.after)

        result = env_diff_core.diff_environments(
            env_before, env_after, prune=args.prune, label_a=args.before, label_b=args.after
        )

        if args.dump_json:
            # The environment identities are the command's, added on top of the core's
            # serialization: the core knows what was compared, not what the user called it. They
            # go in a block of their own, so that no identity key can collide with a key of the
            # comparison. What was typed on the command line is recorded resolved, since a
            # consumer needs the environment rather than the string that named it.
            #
            # The keys stay positional, unlike the labels of the pretty output: the comparison is
            # symmetric, and only the way it is rendered assumes a direction, so a consumer is
            # left free to read the two sides in whichever order it means to.
            identities = {"a": identity_before, "b": identity_after}
            print(sjson.dumps({**result.as_dict(), "environments": identities}))
            return

        EnvironmentDiffRenderer(result, args.before, args.after).render()


def _variant_default(node: spack.spec.Spec, key: str) -> Optional[spack.variant.VariantValue]:
    """Returns the default value of a variant for a node, or None if it cannot be determined.

    An environment can have been concretized against a package repository that no longer knows
    this package, or no longer defines this variant, so the lookup is allowed to come up empty.
    """
    try:
        # get_variant already picks the highest precedence definition whose `when` the node
        # satisfies, and make_default turns the raw default into a value of the right type.
        return node.package.get_variant(key).make_default()
    except (spack.error.SpackError, ValueError):
        return None


def _attribute_style(
    divergence: spack.spec_diff.NodeDivergence, attribute: spack.spec_diff.AttributeDiff
) -> spack.enums.PartStyle:
    """Returns how prominently one difference of a divergent node should be rendered.

    A difference that is what one would expect from a re-concretization is rendered normally, and
    only a suspicious one is highlighted. Expectedness is a property of the change rather than of
    either side, so both rendered specs use the style returned here.

    This is the one place where the two environments are not interchangeable: the second is taken
    to be the later state of the first, which is what makes a version that does not go up worth
    pointing at. The comparison itself, and its serialization, stay symmetric.

    Only versions and variants have a notion of an expected direction. Anything else has no
    default to be judged against, and stays highlighted rather than blending in unclassified.
    """
    if attribute.category is spack.spec_diff.DiffCategory.VERSION:
        try:
            newer = divergence.node_b.version > divergence.node_a.version
        except TypeError:  # two versions that cannot be ordered say nothing about direction
            newer = False
        return spack.enums.PartStyle.NORMAL if newer else spack.enums.PartStyle.HIGHLIGHT

    if attribute.category is spack.spec_diff.DiffCategory.VARIANT:
        # What matters is the value the diff lands on. A variant dropped on the second side is
        # judged on the value it had on the first one, which is the only value there is.
        node = divergence.node_b
        if attribute.key not in node.variants:
            node = divergence.node_a
        value = node.variants.get(attribute.key)
        default = _variant_default(node, attribute.key) if value is not None else None
        if default is not None and set(value.values) == set(default.values):
            return spack.enums.PartStyle.NORMAL
        return spack.enums.PartStyle.HIGHLIGHT

    return spack.enums.PartStyle.HIGHLIGHT


#: How prominently each differing (category, key) of a node should be rendered
_StyleMap = Dict[Tuple[spack.spec_diff.DiffCategory, str], spack.enums.PartStyle]


def _node_styles(divergence: spack.spec_diff.NodeDivergence) -> _StyleMap:
    """Judge every difference of a node once, so both sides can be rendered from one pass."""
    return {
        (attribute.category, attribute.key): _attribute_style(divergence, attribute)
        for attribute in divergence.attributes
    }


def _format_divergent_node(
    divergence: spack.spec_diff.NodeDivergence, *, first: bool, styles: Optional[_StyleMap] = None
) -> str:
    """Render one side of a divergent node as an abstract spec holding only the differences.

    Every part that is equal on both sides is hidden, so the result is a valid abstract spec
    naming exactly what changed on that node. Of what is left, an expected change (a newer
    version, a variant sitting at its default) keeps the color it has in any spec, and only a
    suspicious one (a version regression, a non-default variant value) is highlighted.

    Args:
        divergence: the node where the two DAGs diverge
        first: render the node from the first environment, otherwise the one from the second
        styles: styles from :func:`_node_styles`, computed here when the caller has none to share
    """
    if styles is None:
        styles = _node_styles(divergence)
    categories = {attribute.category for attribute in divergence.attributes}
    node = divergence.node_a if first else divergence.node_b

    def style(category: spack.spec_diff.DiffCategory, key: str = "") -> spack.enums.PartStyle:
        return styles.get((category, key), spack.enums.PartStyle.HIDDEN)

    # Version, variants and architecture parts are hidden through the style callbacks below.
    # Flags and namespace have no callback, so they are dropped from the format string instead;
    # this means all flags of the node are shown, not only the ones that differ.
    format_string = "{name}{@version}"
    if spack.spec_diff.DiffCategory.FLAGS in categories:
        format_string += "{compiler_flags}"
    format_string += "{variants}"
    if spack.spec_diff.DiffCategory.NAMESPACE in categories:
        format_string += "{ namespace=namespace}"
    # The hash identifies the node and keeps the line usable with e.g. `spack find`. It must be
    # rendered before the dependency sigils appended below, or it would bind to a dependency.
    format_string += (
        "{ platform=architecture.platform}{ os=architecture.os}{ target=architecture.target}"
        "{/hash:7}"
    )

    rendered = node.format(
        format_string,
        color=None,
        version_style_fn=lambda n: style(spack.spec_diff.DiffCategory.VERSION),
        variant_style_fn=lambda n, key: style(spack.spec_diff.DiffCategory.VARIANT, key),
        architecture_style_fn=lambda n, part: style(
            spack.spec_diff.DiffCategory.ARCHITECTURE, part
        ),
    )

    # Dependencies are edges, so they are not part of the node format string and are appended
    # here with the direct dependency sigil, which is what the traversal compares.
    edges = []
    for attribute in divergence.attributes:
        if attribute.category is not spack.spec_diff.DiffCategory.DEPENDENCY:
            continue
        own = attribute.value_a if first else attribute.value_b
        if not own:
            continue  # the edge only exists on the other side
        other = attribute.value_b if first else attribute.value_a
        # Both sides depend on this name, but the edge differs: show the edge attributes.
        # Otherwise the dependency itself is what is unique to this side.
        edges.append(f"%[{own}]{attribute.key}" if other else f"%{attribute.key}")

    if edges:
        rendered += " " + colorize("@_R{%s}" % cescape(" ".join(edges)))

    return rendered


#: A divergence and the input specs that reach it
_Entry = Tuple[spack.spec_diff.NodeDivergence, List[ev.UserSpecId]]


def _format_root(root: ev.UserSpecId, *, with_group: bool = True) -> str:
    """Render an input spec, naming its group only when it is not the default one."""
    if not with_group or root.group == spack.environment.environment.DEFAULT_USER_SPEC_GROUP:
        return str(root.spec)
    return f"{root.spec} (group: {root.group})"


def _is_recipe_change(node: spack.spec_diff.NodeDivergence) -> bool:
    """Whether a divergence reports a changed recipe rather than a configuration difference."""
    return any(
        attribute.category is spack.spec_diff.DiffCategory.RECIPE for attribute in node.attributes
    )


def _annotations(node: spack.spec_diff.NodeDivergence) -> List[str]:
    """Render the differences that a spec literal has no room for, one per line.

    Where an external lives, and the node state the catch-all reports, have no spec syntax to be
    written in. Putting them on their own line keeps the two rendered specs above parseable.
    """
    lines = []
    for attribute in node.attributes:
        if attribute.category not in _ANNOTATED_CATEGORIES:
            continue
        key = f" {attribute.key}" if attribute.key else ""
        lines.append(
            colorize(
                f"    {attribute.category.value}{key}: "
                f"@R{{{cescape(attribute.value_a or '(none)')}}} -> "
                f"@G{{{cescape(attribute.value_b or '(none)')}}}"
            )
        )
    return lines


def _group_divergences(
    divergences: List[env_diff_core.UserSpecDivergence],
) -> Tuple[Dict[str, List[_Entry]], List[_Entry]]:
    """Split divergences into configuration differences per group, and recipe changes.

    A single divergence is typically reached from many input specs, and reporting it once per
    input spec makes the output grow with the size of the environment rather than with the number
    of differences. Findings are therefore reported once, against the input specs reaching them.

    Configuration differences are keyed by node, within the group of the input spec reaching them,
    since a group exists precisely to build the same specs under a different configuration. Recipe
    changes are instead a property of a package file: they span groups, and are keyed by package.
    Keying those by node, or even by package hash, would repeat one fact once per instance, since
    a package hash is taken over the canonical source *filtered for its own spec*, so a single
    edit to a package file yields a different pair of package hashes for every differently
    configured instance of it.

    """
    config: Dict[str, Dict[Tuple[str, str], _Entry]] = {}  # group -> (hash of a, hash of b)
    recipes: Dict[Tuple[str, str], _Entry] = {}  # (namespace, name)

    for input_divergence in divergences:
        root = input_divergence.root
        for node in input_divergence.nodes:
            if _is_recipe_change(node):
                key = (node.node_a.namespace, node.node_a.name)
                recipes.setdefault(key, (node, []))[1].append(root)
            else:
                node_key = (node.node_a.dag_hash(), node.node_b.dag_hash())
                config.setdefault(root.group, {}).setdefault(node_key, (node, []))[1].append(root)

    # The default group comes first, as it does when the environment is concretized, and the
    # entries of a group follow their nodes.
    default = spack.environment.environment.DEFAULT_USER_SPEC_GROUP
    by_group = {
        group: [
            (node, env_diff_core.sorted_roots(roots))
            for node, roots in sorted(
                config[group].values(), key=lambda x: spack.spec_diff.node_sort_key(x[0])
            )
        ]
        for group in sorted(config, key=lambda x: (x != default, x))
    }

    return by_group, [
        (recipes[key][0], env_diff_core.sorted_roots(recipes[key][1])) for key in sorted(recipes)
    ]


def _reached_from(roots: List[ev.UserSpecId], *, with_group: bool = True) -> str:
    """Describe which input specs reach a divergent node, without listing an unbounded number."""
    if len(roots) > _MAX_LISTED_INPUTS:
        return f"from {len(roots)} input specs"
    return "from " + ", ".join(_format_root(root, with_group=with_group) for root in roots)


class EnvironmentDiffRenderer:
    """Renders an ``EnvironmentDiff`` to the terminal, for the two named environments.

    The comparison itself carries no identity for the two environments (that is the caller's),
    so a renderer bundles the diff with the names needed to present it.
    """

    def __init__(
        self, result: env_diff_core.EnvironmentDiff, name_before: str, name_after: str
    ) -> None:
        self.result = result
        self.name_before = name_before
        self.name_after = name_after
        # Environment names can be long paths, so they are spelled out once at the top and the
        # short identifiers used from there on. Their colors match the two sides throughout.
        self.label_before = colorize(f"@R{{{_ENV_BEFORE}}}")
        self.label_after = colorize(f"@G{{{_ENV_AFTER}}}")
        # The two sides are always printed one above the other, so what follows the identifier is
        # padded to a common width to keep them aligned. The labels themselves stay unpadded,
        # since a section header ends with one.
        width = max(len(_ENV_BEFORE), len(_ENV_AFTER))
        self.tag_before = f"{self.label_before}:{' ' * (width - len(_ENV_BEFORE) + 1)}"
        self.tag_after = f"{self.label_after}:{' ' * (width - len(_ENV_AFTER) + 1)}"
        # Zero when the output is not a terminal, which keeps the blocks in a single column
        self.columns = terminal_columns()
        #: Set by _section, so that render can tell whether it found anything to report
        self.printed = False

    def _section(self, label: str, blocks: List[List[str]]) -> None:
        """Print a section header followed by its blocks.

        Like the criteria of `spack spec --show=opt`, the header spans its own content rather than
        the console, so that a short section does not get a rule running off to the right.
        """
        self.printed = True
        text = colorize(label)
        lines = render_blocks(blocks, self.columns, indent=_BAND_INDENT)
        content = max((clen(line) for line in lines), default=0)
        rule = clen(text) + _BAND_INDENT + _BAND_DECORATION + _MIN_RULE
        # rule wins over a narrow terminal, so the header is never shorter than its own label
        width = max(rule, min(content, self.columns or _DEFAULT_WIDTH))
        print(tty.band(text, width, indent=_BAND_INDENT))
        for line in lines:
            print(line)
        print()

    def _node_block(
        self, node: spack.spec_diff.NodeDivergence, roots: List[ev.UserSpecId]
    ) -> List[str]:
        """Render one divergent node as a block: a header, the two sides, then its annotations."""
        styles = _node_styles(node)
        return [
            f"{node.node_a.name}  ({_reached_from(roots, with_group=False)})",
            f"    {self.tag_before}{_format_divergent_node(node, first=True, styles=styles)}",
            f"    {self.tag_after}{_format_divergent_node(node, first=False, styles=styles)}",
        ] + _annotations(node)

    def render(self) -> None:
        print()
        print(f"{' ' * _BAND_INDENT}{self.tag_before}{self.name_before}")
        print(f"{' ' * _BAND_INDENT}{self.tag_after}{self.name_after}")
        print()

        sides = (
            (self.label_before, self.result.inputs.only_in_a),
            (self.label_after, self.result.inputs.only_in_b),
        )
        for label, only in sides:
            if only:
                self._section(
                    f"@*{{Input specs only in}} {label}",
                    [[_format_root(root)] for root in env_diff_core.sorted_roots(only)],
                )

        config_by_group, recipes = _group_divergences(self.result.divergences)

        # A section header already qualifies every entry under it, so the group is not repeated on
        # each input spec. With nothing but the default group there is nothing to qualify.
        default = spack.environment.environment.DEFAULT_USER_SPEC_GROUP
        show_groups = list(config_by_group) != [default]

        for group, entries in config_by_group.items():
            self._section(
                f"@*{{Group: {cescape(group)}}}" if show_groups else "@*{Node differences}",
                [self._node_block(node, roots) for node, roots in entries],
            )

        # Recipe changes come last: they are the least actionable finding, and unlike a
        # configuration difference there is no pair of specs to show, since the two configurations
        # are identical.
        if recipes:
            self._section(
                "@*{Packages whose recipe differs}",
                [[f"{node.node_a.name}  ({_reached_from(roots)})"] for node, roots in recipes],
            )

        if self.result.unresolved:
            self._section(
                "@*{Common input specs with no difference to point at}",
                [[_format_root(r)] for r in env_diff_core.sorted_roots(self.result.unresolved)],
            )

        if not self.printed:
            print(f"{' ' * _BAND_INDENT}the two environments are equivalent")
            print()


#: Dictionary mapping subcommand names and aliases to functions
subcommand_functions = {}


#
# spack env
#
def setup_parser(subparser: argparse.ArgumentParser) -> None:
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="env_command")

    _globals = globals()

    for name_and_aliases in subcommands:
        name, aliases = name_and_aliases[0], name_and_aliases[1:]

        # add commands to subcommands dict
        for alias in name_and_aliases:
            subcommand_functions[alias] = _globals[f"env_{name}"]

        # make a subparser and run the command's setup function on it
        setup_parser_cmd = _globals[f"env_{name}_setup_parser"]

        subsubparser = sp.add_parser(
            name,
            aliases=aliases,
            description=spack.cmd.doc_dedented(setup_parser_cmd),
            help=spack.cmd.doc_first_line(setup_parser_cmd),
        )
        subsubparser.set_defaults(subparser=subsubparser)
        setup_parser_cmd(subsubparser)


def env(parser, args):
    """Look for a function called environment_<name> and call it."""
    action = subcommand_functions[args.env_command]
    action(args)
