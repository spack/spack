# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
import textwrap
from argparse import ArgumentParser
from typing import cast

from spack.vendor.ruamel.yaml.compat import ordereddict

import spack.config
import spack.llnl.util.tty as tty
import spack.paths
import spack.schema.include
import spack.util.spack_yaml as syaml

description = "isolate the current spack instance from the home directory"
section = "config"
level = "long"

INCLUDE_PATH = os.path.join(spack.paths.etc_path, "include.yaml")
PRESERVED_INCLUDE_PATH = os.path.join(spack.paths.etc_path, ".isolate.include.yaml")
ISOLATE_SCOPE_PATH = os.path.join(spack.paths.etc_path, "isolate")


def _get_scope_indices(included_scopes):
    user_index = None
    site_index = None
    system_index = None
    iso_index = None
    for i, entry in enumerate(included_scopes):
        if entry["name"] == "user":
            user_index = i
        elif entry["name"] == "site":
            site_index = i
        elif entry["name"] == "system":
            system_index = i
        elif entry["name"] == "isolate":
            iso_index = i
    return user_index, site_index, system_index, iso_index


def _isolate_bootstrap_config(new_user_path):
    bootstrap_yaml = {"bootstrap": {"root": os.path.join(new_user_path, "bootstrap")}}
    with open(os.path.join(ISOLATE_SCOPE_PATH, "bootstrap.yaml"), "w", encoding="utf-8") as f:
        syaml.dump(bootstrap_yaml, f)


def _isolate_config_config(new_user_path):
    build_stage_dirs = ["$tempdir/$user/spack-stage", os.path.join(new_user_path, "stage")]
    test_stage_dir = os.path.join(new_user_path, "test-stage")
    misc_cache_dir = os.path.join(new_user_path, "cache")
    config_yaml = {
        "config": {
            "build_stage:": build_stage_dirs,
            "test_stage:": test_stage_dir,
            "misc_cache:": misc_cache_dir,
        }
    }
    with open(os.path.join(ISOLATE_SCOPE_PATH, "config.yaml"), "w", encoding="utf-8") as f:
        syaml.dump(config_yaml, f)


def _isolate_repos_config(new_user_path):
    current_repos_config = spack.config.get("repos")
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


def _setup_isolate_scope(new_user_path, overwrite: bool):
    if os.path.exists(ISOLATE_SCOPE_PATH):
        if overwrite:
            shutil.rmtree(ISOLATE_SCOPE_PATH)
        else:
            raise Exception("An isolation already exists for this Spack instance")
    os.mkdir(ISOLATE_SCOPE_PATH)
    isolate_dict = {}
    isolate_dict["name"] = "isolate"
    isolate_dict["path"] = ISOLATE_SCOPE_PATH
    _isolate_bootstrap_config(new_user_path)
    _isolate_config_config(new_user_path)
    _isolate_repos_config(new_user_path)
    return isolate_dict


def _get_new_user_scope(new_user_path):
    return {
        "name": "user",
        "path": new_user_path,
        "optional": True,
        "prefer_modify": True,
        "when": '"SPACK_DISABLE_LOCAL_CONFIG" not in env',
    }


def _ensure_destination_setup(destination: str, overwrite: bool):
    if os.path.exists(destination):
        if overwrite:
            shutil.rmtree(destination)
        else:
            raise Exception(f"Isolation destination: {destination} already exists")
    os.mkdir(destination)
    return os.path.abspath(destination)


def _preserve_and_extract_include():
    if not os.path.exists(PRESERVED_INCLUDE_PATH):
        shutil.copy(INCLUDE_PATH, PRESERVED_INCLUDE_PATH)
    include_config = cast(
        ordereddict, spack.config.read_config_file(INCLUDE_PATH, spack.schema.include.schema)
    )
    return include_config["include"]


def setup_parser(subparser: ArgumentParser):
    isolate_group = subparser.add_mutually_exclusive_group()
    isolate_group.add_argument(
        "--path", dest="path", type=str, help="path to data isolation directory"
    )
    isolate_group.add_argument(
        "--self",
        dest="path",
        action="store_const",
        const=spack.paths.prefix,
        help="use spack's own prefix as isolation directory",
    )
    isolate_group.add_argument(
        "--undo", action="store_true", help="undo the result of calling isolate"
    )
    subparser.add_argument(
        "--overwrite", action="store_true", help="overwrite existing isolation if necessary"
    )


def _do_isolate(args):
    destination = _ensure_destination_setup(args.path, args.overwrite)
    include_config: list = _preserve_and_extract_include()
    user_index, site_index, system_index, old_isolate_index = _get_scope_indices(include_config)
    isolate_scope = _setup_isolate_scope(destination, args.overwrite)
    # insert the isolate scope above the below user and site but above system
    if old_isolate_index is not None:  # first try the old isolate index (--overwrite)
        include_config[old_isolate_index] = isolate_scope
    elif site_index is not None:  # otherwise put it below the site scope
        include_config.insert(site_index + 1, isolate_scope)
    elif system_index is not None:  # if there is no site scope, put it above the system scope
        include_config.insert(system_index, isolate_scope)
    elif user_index is not None:  # if there is no system scope, put it below the user scope
        include_config.insert(user_index + 1, isolate_scope)
    else:  # Strange changes have been made if there is no site, system, or user scope
        include_config.append(isolate_scope)

    new_user_scope = _get_new_user_scope(destination)
    if user_index is not None:
        include_config[user_index] = new_user_scope
    else:
        include_config.insert(0, new_user_scope)

    with open(INCLUDE_PATH, "w", encoding="utf-8") as f:
        syaml.dump({"include": include_config}, f)


def _undo_isolate():
    if not os.path.exists(ISOLATE_SCOPE_PATH):
        raise RuntimeError("Cannot find isolation to undo")
    if not os.path.exists(PRESERVED_INCLUDE_PATH):
        raise RuntimeError("Cannot find pre-isolate include.yaml")
    shutil.rmtree(ISOLATE_SCOPE_PATH)
    shutil.copy(PRESERVED_INCLUDE_PATH, INCLUDE_PATH)


def isolate(parser, args):
    if args.undo:
        _undo_isolate()
    elif args.path is None:
        tty.die("Must provide one of --path, --self, or --undo")
    else:
        _do_isolate(args)
        tty.warn(
            "\n".join(
                textwrap.wrap(
                    "Due to current limitations in Spack's configuration, adding repos without an"
                    " explicit destination will default to $SPACK_USER_CACHE_PATH or ~/.spack."
                    " This behavior will be fixed with shared spack in v1.3."
                )
            )
        )
