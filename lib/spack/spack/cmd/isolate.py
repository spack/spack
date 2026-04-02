# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
from pathlib import Path

import spack
import spack.config
import spack.llnl.util.tty as tty
import spack.paths_base
import spack.util.path
import spack.util.spack_yaml as syaml
from spack.cmd.common import arguments

description = "force spack to only use/write data from/to an isolated prefix"
section = "config"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "--force-scopes", action="store_true", help="remove all config scopes in ~"
    )
    subparser.add_argument(
        "--force-home", action="store_true", help="override home even if user setting is detected"
    )
    subparser.add_argument("--force-all", action="store_true", help="set all 'force' options")
    # TODO: add an --undo option: delete config:locations:home and restore
    # default config scopes in the include: section of the spack scope
    arguments.add_common_arguments(subparser, ["specs"])


class Force:

    SCOPES = 1
    HOME = 2

    options = {SCOPES: "--force-scopes", HOME: "--force-home"}

    def __init__(self, args):
        self.all = args.force_all
        self.active = {Force.SCOPES: args.force_scopes, Force.HOME: args.force_home}

    def go_ahead(self, category, context):
        do_it = self.all or self.active[category]
        if do_it:
            tty.debug(f"{context}\nOverriding because{Force.options[category]} is set")
        else:
            tty.warn(f"{context}\nYou can override with {Force.options[category]}")
        return do_it


def isolate(parser, args):
    # TODO: warn if installed specs are detected? If we move config:locations:home
    # then these will be "lost"

    force = Force(args)

    spack_root = Path(spack.paths_base.locations.prefix)

    def is_in_spack_prefix(path):
        resolved = Path(spack.util.path.canonicalize_path(path)).resolve()
        return path == spack_root or spack_root in resolved.parents

    def same_path(x, y):
        return Path(x).resolve(strict=False) == Path(y).resolve(strict=False)

    current_install_root = spack.config.get("config:install_tree:root")
    current_env_root = spack.config.get("config:environments_root")

    if current_install_root and current_install_root != "$default_install_root":
        tty.warn(
            f"config:install_tree:root is set to {current_install_root},"
            " the install tree will not be relocated because this setting"
            " has precedence."
        )

    if current_env_root and current_env_root != "$default_envs_root":
        tty.warn(
            f"config:environments_root is set to {current_env_root}, "
            " environments will not be relocated because this setting"
            " has precedence."
        )

    current_home = spack.config.get("config:locations:home")
    change_home = True
    if current_home:
        if is_in_spack_prefix(current_home):
            change_home = False
            tty.debug(f"config:locations:home is inside $spack: {current_home}\nkeeping it")
        else:
            msg = f"config:locations:home is outside of $spack: {current_home}"
            if not force.go_ahead(Force.HOME, msg):
                # By default for a new clone of Spack, config:locations:home is not
                # set. So if we're here, it implies we will be changing something
                # that was set by the user.
                change_home = False

    # else: home is unset (typical) - we will set it to relocate everything
    # except for config (and then redirect config)

    if change_home:
        config_spack = spack.config.get("config", scope="spack")
        locations = config_spack.setdefault("locations", {})
        locations["home"] = "$spack/all-data"

    include_spack = spack.config.get("include", scope="spack") or []

    # Take included scopes defined in the "spack" scope and remove the
    # user/system scopes. Look for other scopes defined here that exist
    # outside the spack prefix; --force will remove those scopes but
    # otherwise this command will just print a warning
    visited = set()
    new_include_spack = syaml.syaml_list()
    for scope_def in include_spack:
        scope_name = scope_def.get("name", None)
        path = scope_def.get("path")
        if scope_name:
            scope_id = f"{scope_name} - {path}"
        else:
            scope_id = f"(unnamed) - {path}"

        if scope_name == "user":
            path = spack.util.path.canonicalize_path(path)
            if same_path(path, spack.util.path.canonicalize_path("~/.config/spack")):
                tty.debug("Removing default user scope")
            elif not force.go_ahead(Force.SCOPES, "user scope is not in default path"):
                new_include_spack.append(scope_def)
            visited.add("user")
        elif scope_name == "system":
            if same_path(path, "/etc/spack"):
                tty.debug("Removing default system scope")
            elif not force.go_ahead(Force.SCOPES, "system scope is not in default path"):
                new_include_spack.append(scope_def)
            visited.add("system")
        else:
            if not is_in_spack_prefix(path):
                if not force.go_ahead(
                    Force.SCOPES, f"User-defined scope is not in spack prefix: {scope_id}"
                ):
                    new_include_spack.append(scope_def)
            else:
                new_include_spack.append(scope_def)

    for expect_remove in ["user", "system"]:
        if expect_remove not in visited:
            tty.warn(
                f"Expected to find (and remove): {expect_remove}"
                "\nbut it wasn't present (suggests prior run of `spack isolate`, or)"
                " manual editing)"
            )

    if change_home:
        spack.config.set("config", config_spack, scope="spack")
    # TODO: the "spack" config scope is version-controlled in the
    # spack repo, so this change can be dropped or committed by
    # accident (e.g. if the user runs `git checkout` or
    # `git commit -a` without being aware of the effects of this
    # command.
    spack.config.set("include", new_include_spack, scope="spack")
