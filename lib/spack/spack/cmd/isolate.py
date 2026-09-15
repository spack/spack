# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
import sys
import textwrap
from argparse import ArgumentParser

import spack.config
import spack.paths
import spack.schema.include
import spack.util.spack_yaml as syaml
from spack.util import tty

description = "isolate the current spack instance from the home directory"
section = "config"
level = "long"

ISOLATE_SCOPE_PATH = os.path.join(spack.paths.etc_path, "isolate")


# _get_scope_indices no longer needed - we don't modify etc/spack/include.yaml


def _isolate_bootstrap_config(new_user_path):
    bootstrap_yaml = {"bootstrap": {"root": os.path.join(new_user_path, "bootstrap")}}
    with open(os.path.join(ISOLATE_SCOPE_PATH, "bootstrap.yaml"), "w", encoding="utf-8") as f:
        syaml.dump(bootstrap_yaml, f)


def _isolate_config_config(new_user_path, config_path):
    build_stage_dirs = ["$tempdir/$user/spack-stage", os.path.join(new_user_path, "stage")]
    test_stage_dir = os.path.join(new_user_path, "test-stage")
    misc_cache_dir = os.path.join(new_user_path, "cache")
    config_yaml = {
        "config": {
            "build_stage:": build_stage_dirs,
            "test_stage:": test_stage_dir,
            "misc_cache:": misc_cache_dir,
            "locations": spack.config._isolate_locations_config(new_user_path),
        }
    }
    with open(config_path, "w", encoding="utf-8") as f:
        syaml.dump(config_yaml, f)


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
        "when": '"SPACK_DISABLE_LOCAL_CONFIG" not in env',
    }

    # Create the include list with just the user scope
    # (site and system will still come from the default include.yaml)
    include_list = [user_scope_dict]

    # Create a syaml_str with override marker for the key
    include_key = syaml.syaml_str("include")
    include_key.override = True  # type: ignore[attr-defined]

    # Create the dict with the marked key
    include_data = syaml.syaml_dict([(include_key, include_list)])

    # Write to isolate scope's include.yaml
    include_yaml_path = os.path.join(ISOLATE_SCOPE_PATH, "include.yaml")
    with open(include_yaml_path, "w", encoding="utf-8") as f:
        syaml.dump_config(include_data, f)


def _setup_isolate_scope(new_user_path, overwrite: bool, target_config_existed: bool) -> str:
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
        else:
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

    # Write configuration files into isolate scope.  Preserve a pre-existing
    # target config and put generated resource overrides in the layout scope.
    _isolate_bootstrap_config(new_user_path)
    config_path = (
        os.path.join(spack.config._layout_scope_path(), "config.yaml")
        if target_config_existed
        else os.path.join(new_user_path, "config.yaml")
    )
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    if not target_config_existed:
        _isolate_config_config(new_user_path, config_path)
    _isolate_repos_config(new_user_path)

    # Write include.yaml with include:: override to redirect user scope
    # For --self, this points to user-redirect/
    # For --path, this points to the external path
    _isolate_include_config(final_user_path)
    return config_path


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


def _do_isolate(args):
    target_config_existed = os.path.isfile(os.path.join(args.path, "config.yaml"))
    destination = _ensure_destination_setup(args.path, args.overwrite)
    config_path = _setup_isolate_scope(destination, args.overwrite, target_config_existed)
    # No need to modify etc/spack/include.yaml anymore - the isolate scope's
    # include.yaml with include:: override handles the redirection

    # Record old resources in the layout scope, but never relocate them while
    # isolating.  The isolate scope controls new data; the layout scope keeps
    # existing data reachable from its original locations.
    if (
        not spack.config._has_layout_scope()
        and spack.config._is_spack_writable()
        and any(spack.config._detect_old_resources().values())
    ):
        spack.config._do_migrate(
            is_isolate_command=True,
            config_path=config_path,
            isolate_target=destination,
        )
        # No need to reload CONFIG here: this process exits immediately, and
        # the generated scopes are loaded by the next Spack invocation.


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
    tty.warn(
        "\n".join(
            textwrap.wrap(
                "Due to current limitations in Spack's configuration, adding repos without an"
                " explicit destination will default to $SPACK_USER_CACHE_PATH or ~/.spack."
                " This behavior will be fixed with shared spack in v1.3."
            )
        )
    )
    if "SPACK_DISABLE_LOCAL_CONFIG" in os.environ:
        tty.warn(
            "\n".join(
                textwrap.wrap(
                    "SPACK_DISABLE_LOCAL_CONFIG is present in the current shell environment,"
                    " which disables the user scope. spack isolate uses this scope for"
                    " isolation. In order for future configuration changes to be added"
                    " to the isolated scope, you will need to unset SPACK_DISABLE_LOCAL_CONFIG."
                )
            )
        )
        pass
