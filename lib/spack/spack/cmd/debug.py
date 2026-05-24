# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import platform
import re
from typing import Optional

import spack
import spack.config
import spack.paths
import spack.platforms
import spack.repo
import spack.spec
import spack.util.git
import spack.util.path

description = "debugging commands for troubleshooting Spack"
section = "developer"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="debug_command")
    sp.add_parser("report", help="print information useful for bug reports")
    sp.add_parser(
        "paths",
        help="show how each Spack data path was resolved (active layout scheme, "
        "config keys, env-var overrides)",
    )


def _format_repo_info(source, commit):
    if source.endswith(".git"):
        return f"{source[:-4]}/commit/{commit}"

    return f"{source} ({commit[:7]})"


def _get_builtin_repo_info() -> Optional[str]:
    """Get the builtin package repository git commit sha."""
    # Get builtin from config
    descriptors = spack.repo.RepoDescriptors.from_config(
        spack.repo.package_repository_lock(), spack.config.CONFIG
    )
    if "builtin" not in descriptors:
        return None

    builtin = descriptors["builtin"]

    source = None
    if isinstance(builtin, spack.repo.RemoteRepoDescriptor) and builtin.fetched():
        destination = builtin.destination
        source = builtin.repository
    elif isinstance(builtin, spack.repo.LocalRepoDescriptor):
        destination = builtin.path
        source = builtin.path
    else:
        return None  # no git info

    git = spack.util.git.git(required=False)
    if not git:
        return None

    rev = git(
        "-C", destination, "rev-parse", "HEAD", output=str, error=os.devnull, fail_on_error=False
    )
    if git.returncode != 0:
        return None

    match = re.match(r"[a-f\d]{7,}$", rev)
    return _format_repo_info(source, match.group(0)) if match else None


def _get_spack_repo_info() -> str:
    """Get the spack package repository git info."""
    commit = spack.get_spack_commit()
    if not commit:
        return spack.spack_version

    repo_info = _format_repo_info("https://github.com/spack/spack.git", commit)
    return f"{spack.spack_version} ({repo_info})"


def report(args):
    host_platform = spack.platforms.host()
    host_os = host_platform.default_operating_system()
    host_target = host_platform.default_target()
    architecture = spack.spec.ArchSpec((str(host_platform), str(host_os), str(host_target)))
    print("* **Spack:**", _get_spack_repo_info())
    print("* **Builtin repo:**", _get_builtin_repo_info() or "not available")
    print("* **Python:**", platform.python_version())
    print("* **Platform:**", architecture)


def _row(label, value, source):
    return f"  {label:<22} {value}\n    {source}"


def _resolved_home(spack_var, config_var):
    """Return (value, source) for state/data/cache home."""
    disable_env = spack.config.get("config:locations:disable_env", False)
    if not disable_env and spack_var in os.environ:
        return os.path.expanduser(os.environ[spack_var]), f"env: {spack_var}"
    if not disable_env and "SPACK_HOME" in os.environ:
        # The actual value is computed by SpackPaths._resolve_home;
        # we just report SPACK_HOME as the source.
        return getattr(spack.paths.locations, f"{config_var}_home"), "env: SPACK_HOME"
    cfg = spack.config.get(f"config:locations:{config_var}", None)
    if cfg:
        scope = _scope_that_set(f"config:locations:{config_var}")
        return spack.util.path.canonicalize_path(cfg), f"config:locations:{config_var} ({scope})"
    return getattr(spack.paths.locations, f"{config_var}_home"), "default (no source set)"


def _scope_that_set(config_path):
    """Walk scopes high-to-low and return the name of the first one with this key."""
    section, _, key = config_path.partition(":")
    for scope in reversed(list(spack.config.CONFIG.scopes.values())):
        data = scope.get_section(section) or {}
        # Walk nested keys.
        node = data.get(section, {})
        for part in key.split(":") if key else ():
            if not isinstance(node, dict) or part not in node:
                node = None
                break
            node = node[part]
        if node not in (None, {}):
            return f"scope: {scope.name}"
    return "scope: (not set)"


def paths(args):
    p = spack.paths.locations

    # Active layout scheme
    if p.old_layout_detected:
        env_forces_new = any(
            v in os.environ
            for v in ("SPACK_DATA_HOME", "SPACK_STATE_HOME", "SPACK_CACHE_HOME", "SPACK_HOME")
        )
        if env_forces_new:
            scheme = "xdg (forced by SPACK_*_HOME env var; old-layout markers also present)"
        else:
            scheme = "old ($spack-local layout markers detected)"
    else:
        scheme = "xdg (no legacy $spack-local data)"
    print(f"layout scheme: {scheme}\n")

    print("homes:")
    for spack_var, cfg_var in (
        ("SPACK_DATA_HOME", "data"),
        ("SPACK_STATE_HOME", "state"),
        ("SPACK_CACHE_HOME", "cache"),
    ):
        value, source = _resolved_home(spack_var, cfg_var)
        print(_row(f"${cfg_var}_home", value, source))
    print(_row("$spack_home", p.spack_home, _spack_home_source()))
    print()

    # Paths that are read out of config (with substitutions resolved).
    print("config-driven paths:")
    for key in (
        "config:install_tree:root",
        "config:environments_root",
        "config:license_dir",
        "config:source_cache",
        "config:misc_cache",
        "config:test_stage",
        "config:gpg_path",
        "config:gpg_keys_path",
    ):
        raw = spack.config.get(key, None)
        if raw is None:
            print(_row(key, "(unset)", ""))
            continue
        resolved = spack.util.path.canonicalize_path(raw)
        scope = _scope_that_set(key)
        print(_row(key, resolved, f"{raw}  [{scope}]"))


def _spack_home_source():
    if "SPACK_HOME" in os.environ and not spack.config.get("config:locations:disable_env", False):
        return "env: SPACK_HOME"
    if spack.config.get("config:locations:home", None):
        return f"config:locations:home ({_scope_that_set('config:locations:home')})"
    return "default (~)"


def debug(parser, args):
    if args.debug_command == "report":
        report(args)
    elif args.debug_command == "paths":
        paths(args)
