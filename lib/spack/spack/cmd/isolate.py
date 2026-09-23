# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
import sys
from argparse import ArgumentParser
from typing import Tuple

import spack.config
import spack.paths
import spack.util.spack_yaml as syaml
from spack.util import tty

description = "isolate the current spack instance from the home directory"
section = "config"
level = "long"

ISOLATE_SCOPE_PATH = os.path.join(spack.paths.etc_path, "isolate")


def _isolate_repos_config(new_user_path):
    current_repos_config = spack.config.CONFIG.get("repos")
    new_repos_config = {}
    for key, value in current_repos_config.items():
        if isinstance(value, str):
            new_repos_config[key] = value
        if isinstance(value, dict):
            if "destination" not in value:
                value["destination"] = os.path.join(new_user_path, "repos", key)
                new_repos_config[key] = value

    with open(os.path.join(ISOLATE_SCOPE_PATH, "repos.yaml"), "w", encoding="utf-8") as f:
        syaml.dump({"repos": new_repos_config}, f)


def _isolate_include_config(new_user_path):
    """Write include.yaml with include:: override to redirect user scope."""
    user_scope_dict = {
        "name": "user",
        "path": new_user_path,
        "optional": True,
        "prefer_modify": True,
    }

    # The override replaces the standard_scopes include list. Keep the layout
    # scope visible because it contains old-resource redirects and may be
    # updated later by commands such as `spack migrate undo`.
    include_list = [
        user_scope_dict,
        {"name": "layout", "path": "$spack/etc/spack/layout", "optional": True},
    ]

    # Create a syaml_str with override marker for the key
    include_key = syaml.syaml_str("include")
    include_key.override = True  # type: ignore[attr-defined]

    # Create the dict with the marked key
    include_data = syaml.syaml_dict([(include_key, include_list)])

    # Write to isolate scope's include.yaml
    include_yaml_path = os.path.join(ISOLATE_SCOPE_PATH, "include.yaml")
    with open(include_yaml_path, "w", encoding="utf-8") as f:
        syaml.dump_config(include_data, f)


def _setup_isolate_scope(
    new_user_path, overwrite: bool, target_config_existed: bool, reuse_old: bool
) -> Tuple[str, str]:
    """Set up the isolate scope directories and include.yaml.

    Returns:
        (config_path, final_user_path) - where to write config, and the user redirect path
    """
    # Check if this is --self (isolate scope IS the user path)
    is_self = os.path.exists(ISOLATE_SCOPE_PATH) and os.path.samefile(
        new_user_path, ISOLATE_SCOPE_PATH
    )

    # Bypass overwriting/pre-existing when using --self
    if os.path.exists(ISOLATE_SCOPE_PATH):
        if is_self:
            pass
        elif overwrite:
            shutil.rmtree(ISOLATE_SCOPE_PATH)
            os.makedirs(ISOLATE_SCOPE_PATH)
        elif not reuse_old:
            raise Exception("An isolation already exists for this Spack instance")
    else:
        os.makedirs(ISOLATE_SCOPE_PATH, exist_ok=True)

    # For --self, create a user-redirect subdirectory for user config additions
    # The isolate scope's config files point to isolate/bootstrap, isolate/cache, etc.
    # But user additions go to isolate/user-redirect
    if is_self:
        user_redirect_path = os.path.join(ISOLATE_SCOPE_PATH, "user-redirect")
        os.makedirs(user_redirect_path, exist_ok=True)
        final_user_path = user_redirect_path
    else:
        final_user_path = new_user_path

    # Determine where to write generated config (isolation locations + old resources)
    # If reusing an existing target config, write to layout scope to avoid overwriting it
    # Otherwise, write to the isolate target's config.yaml
    config_path = (
        os.path.join(spack.config._layout_scope_path(), "config.yaml")
        if target_config_existed and reuse_old
        else os.path.join(new_user_path, "config.yaml")
    )

    # Write include.yaml with include:: override to redirect user scope
    # For --self, this points to user-redirect/
    # For --path, this points to the external path
    _isolate_include_config(final_user_path)

    return config_path, final_user_path


# _get_new_user_scope no longer needed - moved into _isolate_include_config


def _ensure_destination_setup(destination: str, overwrite: bool):
    if os.path.exists(destination):
        if overwrite:
            shutil.rmtree(destination)
        else:
            raise Exception(f"Isolation destination: {destination} already exists")
    os.mkdir(destination)
    return os.path.abspath(destination)


# _preserve_and_extract_include no longer needed - we don't modify etc/spack/include.yaml


def setup_parser(subparser: ArgumentParser):
    isolate_group = subparser.add_mutually_exclusive_group()
    isolate_group.add_argument(
        "--path", dest="path", type=str, help="path to data isolation directory"
    )
    isolate_group.add_argument(
        "--self",
        dest="use_self",
        action="store_true",
        help="store isolation directory in Spack's prefix",
    )
    isolate_group.add_argument(
        "--undo", action="store_true", help="undo the result of calling isolate"
    )
    subparser.add_argument(
        "--overwrite", action="store_true", help="overwrite existing isolation if necessary"
    )
    subparser.add_argument(
        "--reuse-old",
        action="store_true",
        help="reuse an existing isolation target without overwriting its configuration",
    )


def _do_isolate(args):
    if args.overwrite and args.reuse_old:
        tty.die("Cannot combine --overwrite and --reuse-old")

    target_config_existed = os.path.isfile(os.path.join(args.path, "config.yaml"))
    if os.path.exists(args.path):
        if args.overwrite:
            destination = _ensure_destination_setup(args.path, overwrite=True)
        elif args.reuse_old:
            destination = os.path.abspath(args.path)
        else:
            raise Exception(f"Isolation destination: {args.path} already exists")
    else:
        destination = _ensure_destination_setup(args.path, overwrite=False)

    config_path, final_user_path = _setup_isolate_scope(
        destination, args.overwrite, target_config_existed, args.reuse_old
    )

    # If writing to layout scope (because we're reusing existing target config),
    # ensure layout scope doesn't already exist to avoid conflicts
    layout_config = os.path.join(spack.config._layout_scope_path(), "config.yaml")
    if config_path == layout_config and os.path.exists(config_path):
        raise Exception(
            f"Layout scope config already exists at {config_path}. "
            "Cannot write isolation config without overwriting it."
        )

    # Build config with isolation locations
    scope_config = {
        "config": {
            "build_stage:": ["$tempdir/$user/spack-stage", os.path.join(destination, "stage")],
            "test_stage:": os.path.join(destination, "test-stage"),
            "misc_cache:": os.path.join(destination, "cache"),
            "locations": spack.config._isolate_locations_config(destination),
        }
    }

    # Add old resource pointers if they exist
    old_resources = spack.config._detect_old_resources()

    if old_resources["installs"]:
        scope_config["config"]["install_tree"] = {
            "root": os.path.join(spack.paths.prefix, "opt", "spack")
        }
        tty.debug(f"Keeping existing installs in {spack.paths.prefix}/opt/spack")

    if old_resources["gpg_keys"]:
        old_gpg_home = spack.paths.old_gpg_path
        old_gpg_keys = spack.paths.old_gpg_keys_path
        scope_config["config"]["gpg_path"] = old_gpg_home
        scope_config["config"]["gpg_keys_path"] = old_gpg_keys
        tty.debug(f"Keeping GPG data in {old_gpg_home} and {old_gpg_keys}")

    if old_resources["licenses"]:
        scope_config["config"]["license_dir"] = spack.paths.old_licenses_path
        tty.debug(f"Keeping licenses in {spack.paths.old_licenses_path}")

    if old_resources["environments"]:
        scope_config["config"]["environments_root"] = spack.paths.old_envs_path
        tty.debug(f"Keeping environments in {spack.paths.old_envs_path}")

    # Write the config file
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        syaml.dump(scope_config, f)


def _undo_isolate():
    if not os.path.exists(ISOLATE_SCOPE_PATH):
        raise RuntimeError("Cannot find isolation to undo")
    # Simply remove the isolate scope directory
    # No need to restore include.yaml since we never modified it
    shutil.rmtree(ISOLATE_SCOPE_PATH)


def isolate(parser, args):
    if args.undo:
        _undo_isolate()
        sys.exit(0)
    elif args.use_self:
        if args.path is not None:
            tty.die("Cannot provide both --self and --path")
        else:
            args.path = ISOLATE_SCOPE_PATH
    elif args.path is None:
        tty.die("Must provide one of --path, --self, or --undo")
    _do_isolate(args)
