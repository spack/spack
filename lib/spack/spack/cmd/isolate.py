# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
from argparse import ArgumentParser
from typing import cast

from spack.vendor.ruamel.yaml.compat import ordereddict

import spack.concretize
import spack.config
import spack.paths
import spack.schema.include
import spack.util.spack_yaml as syaml

description = "isolate the current spack instance from the home directory"
section = "config"
level = "long"

INCLUDE_PATH = os.path.join(spack.paths.etc_path, "include.yaml")
ISOLATE_PATH = os.path.join(spack.paths.etc_path, "isolate")


def _get_scope_indices(included_scopes, destination):
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
    with open(os.path.join(ISOLATE_PATH, "bootstrap.yaml"), "w", encoding="utf-8") as f:
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
    with open(os.path.join(ISOLATE_PATH, "config.yaml"), "w", encoding="utf-8") as f:
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
    with open(os.path.join(ISOLATE_PATH, "repos.yaml"), "w", encoding="utf-8") as f:
        syaml.dump({"repos": new_repos_config}, f)


def _setup_isolate_scope(new_user_path, overwrite: bool):
    if os.path.exists(ISOLATE_PATH):
        if overwrite:
            shutil.rmtree(ISOLATE_PATH)
        else:
            raise Exception("An isolation already exists for this Spack instance")
    os.mkdir(ISOLATE_PATH)
    isolate_dict = {}
    isolate_dict["name"] = "isolate"
    isolate_dict["path"] = ISOLATE_PATH
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


def setup_parser(subparser: ArgumentParser):
    subparser.add_argument("destination", type=str, help="Path to data isolation directory")
    subparser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing isolation if necessary"
    )
    subparser.add_argument(
        "--bootstrap",
        action="store_true",
        help="Bootstrap clingo, repos, and compiler config after isolation",
    )


def _ensure_destination_setup(destination: str, overwrite: bool):
    if os.path.exists(destination):
        if overwrite:
            shutil.rmtree(destination)
        else:
            raise Exception("Isolation destination already exists")
    os.mkdir(destination)
    return os.path.abspath(destination)


def _preserve_and_extract_include():
    include_config = cast(
        ordereddict, spack.config.read_config_file(INCLUDE_PATH, spack.schema.include.schema)
    )
    return include_config["include"]


def isolate(parser, args):
    destination = _ensure_destination_setup(args.destination, args.overwrite)
    include_config: list = _preserve_and_extract_include()
    user_index, site_index, system_index, old_isolate_index = _get_scope_indices(
        include_config, destination
    )
    isolate_scope = _setup_isolate_scope(destination, args.overwrite)
    # insert the isolate scope above the below user and site but above system
    if old_isolate_index is not None:
        include_config.insert(old_isolate_index, isolate_scope)
    elif site_index is not None:
        include_config.insert(site_index + 1, isolate_scope)
    elif system_index is not None:
        include_config.insert(system_index - 1, isolate_scope)
    elif user_index is not None:
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

    if args.bootstrap:
        del spack.config.CONFIG
        spack.config.CONFIG = spack.config.create()
        spack.concretize.concretize_one("zlib")
