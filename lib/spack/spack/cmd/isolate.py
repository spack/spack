# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
import sys
from argparse import ArgumentParser
from typing import Dict, List

import spack.config
import spack.paths
import spack.util.spack_yaml as syaml
from spack.util import tty

description = "isolate the current spack instance from the home directory"
section = "config"
level = "long"


def _isolate_include_config(new_user_path):
    """Write include.yaml with include:: override to redirect user scope."""
    include_list = [
        {"name": "user", "path": new_user_path, "optional": True, "prefer_modify": True},
        {
            "name": "layout",
            "path": os.path.join(spack.paths.isolate_scope_path, "layout"),
            "optional": True,
        },
    ]

    include_key = syaml.syaml_str("include")
    # The override replaces the standard_scopes include list.
    include_key.override = True  # type: ignore[attr-defined]
    include_data = syaml.syaml_dict([(include_key, include_list)])

    include_yaml_path = os.path.join(spack.paths.isolate_scope_path, "include.yaml")
    with open(include_yaml_path, "w", encoding="utf-8") as f:
        syaml.dump_config(include_data, f)


def _isolate_locations_config(isolate_target: str) -> Dict[str, List[str]]:
    """Return location settings for data created by an isolated Spack."""
    return {"data": [isolate_target], "state": [isolate_target], "cache": [isolate_target]}


def _setup_isolate_scope(new_user_path, overwrite: bool, reuse_old: bool) -> str:
    """Set up the isolate scope directories and include.yaml.

    Returns:
        final_user_path - the user redirect path
    """
    # Check if this is --self (isolate scope IS the user path)
    is_self = os.path.exists(spack.paths.isolate_scope_path) and os.path.samefile(
        new_user_path, spack.paths.isolate_scope_path
    )

    # Bypass overwriting/pre-existing when using --self
    if os.path.exists(spack.paths.isolate_scope_path):
        if is_self:
            pass
        elif overwrite:
            shutil.rmtree(spack.paths.isolate_scope_path)
            os.makedirs(spack.paths.isolate_scope_path)
        elif not reuse_old:
            tty.die(
                "An isolation already exists for this Spack instance:"
                " see --help for --overwrite/--reuse-old options"
            )
    else:
        os.makedirs(spack.paths.isolate_scope_path, exist_ok=True)

    # For --self, create a redirected user subdirectory for user config additions
    # The isolate scope's config files point to isolate/bootstrap, isolate/cache, etc.
    # But user additions go to isolate/user-redirect
    if is_self:
        user_redirect_path = os.path.join(spack.paths.isolate_scope_path, "user")
        os.makedirs(user_redirect_path, exist_ok=True)
        final_user_path = user_redirect_path
    else:
        final_user_path = new_user_path

    # Write include.yaml with include:: override to redirect user scope
    # For --self, this points to user-redirect/
    # For --path, this points to the external path
    _isolate_include_config(final_user_path)

    return final_user_path


def _ensure_destination_setup(destination: str, overwrite: bool):
    if os.path.exists(destination):
        if overwrite:
            shutil.rmtree(destination)
        else:
            tty.die(f"Isolation destination: {destination} already exists")
    os.mkdir(destination)
    return os.path.abspath(destination)


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
        "--overwrite",
        action="store_true",
        help="overwrite (delete and replace) existing isolation",
    )
    subparser.add_argument(
        "--reuse-old",
        action="store_true",
        help=(
            "reuse an existing isolation target without overwriting its configuration"
            " (this is generally for Spack instances that used `spack isolate` before"
            " 1.3 and then upgraded to 1.3)"
        ),
    )


def _do_isolate(args):
    if args.overwrite and args.reuse_old:
        tty.die("Cannot combine --overwrite and --reuse-old")

    # Validate that path is (or can be) a directory
    if os.path.exists(args.path) and not os.path.isdir(args.path):
        tty.die(f"Isolation path {args.path} exists but is not a directory")

    # Check write permissions if directory exists, or create it if it doesn't
    if os.path.exists(args.path):
        test_file = os.path.join(args.path, ".spack-write-test")
        try:
            with open(test_file, "w", encoding="utf-8") as f:
                pass
            os.remove(test_file)
        except (OSError, PermissionError) as e:
            tty.die(f"Isolation path {args.path} is not writable: {e}")
    else:
        # Try creating the directory to verify we have permissions
        try:
            os.makedirs(args.path)
        except (OSError, PermissionError) as e:
            tty.die(f"Cannot create isolation path {args.path}: {e}")

    target_config_existed = os.path.isfile(os.path.join(args.path, "config.yaml"))
    if os.path.exists(args.path):
        if args.overwrite:
            destination = _ensure_destination_setup(args.path, overwrite=True)
        elif args.reuse_old:
            destination = os.path.abspath(args.path)
        else:
            tty.die(
                f"Isolation destination: {args.path} already exists:"
                " see --help for --overwrite/--reuse-old options"
            )
    else:
        destination = _ensure_destination_setup(args.path, overwrite=False)

    final_user_path = _setup_isolate_scope(destination, args.overwrite, args.reuse_old)

    # Build config with isolation locations
    scope_config = {
        "config": {
            "build_stage:": ["$tempdir/$user/spack-stage", os.path.join(destination, "stage")],
            "test_stage:": os.path.join(destination, "test-stage"),
            "locations": _isolate_locations_config(destination),
        }
    }

    old_resources = spack.config._detect_old_resources()

    if any(old_resources.values()):
        spack.config.generate_old_layout_config(old_resources, scope_config)
        config_path = os.path.join(spack.paths.isolate_scope_path, "layout", "config.yaml")
    elif target_config_existed:
        config_path = os.path.join(spack.paths.isolate_scope_path, "layout", "config.yaml")
    else:
        config_path = os.path.join(final_user_path, "config.yaml")

    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        syaml.dump(scope_config, f)


def _undo_isolate():
    if not os.path.exists(spack.paths.isolate_scope_path):
        tty.die("Cannot find isolation to undo")

    shutil.rmtree(spack.paths.isolate_scope_path)
    tty.msg(f"Removed isolate scope: {spack.paths.isolate_scope_path}")

    spack.config._perform_migration()


def isolate(parser, args):
    if args.undo:
        _undo_isolate()
        sys.exit(0)
    elif args.use_self:
        if args.path is not None:
            tty.die("Cannot provide both --self and --path")
        else:
            args.path = spack.paths.isolate_scope_path
    elif args.path is None:
        tty.die("Must provide one of --path, --self, or --undo")
    _do_isolate(args)
