# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
import sys
from typing import List, Tuple

import spack.config
import spack.migrate
import spack.paths
from spack.util import tty

description = "manage migration of Spack resources"
section = "config"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="migrate_command")

    undo = sp.add_parser(
        "undo",
        help="point all resources back at their legacy locations under $spack",
        description=(
            "Update the layout scope so that environments, GPG data and licenses are read"
            " from their legacy locations under $spack again. Nothing is moved or deleted;"
            " copies made in the new locations are left in place."
        ),
    )
    cleanup = sp.add_parser(
        "cleanup-old",
        help="permanently delete ~/.spack",
        description=(
            "Permanently delete ~/.spack. Reports its contents and any references to it in"
            " the active configuration, then asks for confirmation. Refuses, even with"
            " --yes, while the install tree or active user config point inside ~/.spack."
            " Uninstalling packages does not lift this; the install tree must be moved."
        ),
    )
    cleanup.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help=(
            "do not prompt for confirmation. Still refuses to delete ~/.spack if"
            " config:install_tree:root points inside it"
        ),
    )

    new = sp.add_parser(
        "use-new-layout",
        help="remove the layout scope and migrate $spack resources again",
        description=(
            "Remove the layout scope and re-run the migration of $spack-internal resources,"
            " for example after declining the prompt on the first run."
        ),
    )

    for parser in (undo, cleanup, new):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="show what would be done without actually doing it",
        )

    subparser.epilog = (
        "WARNING:\n"
        "  undo and use-new-layout hold the migration lock, so spack commands that start\n"
        "  while they run wait for the result. Commands already running for the same Spack\n"
        "  instance have loaded their configuration and do not see the change."
    )


def _under_old_dotspack(path: str) -> bool:
    old_path = os.path.realpath(os.path.expanduser("~/.spack"))
    try:
        return (
            os.path.commonpath([old_path, os.path.realpath(os.path.expanduser(path))]) == old_path
        )
    except ValueError:
        return False


def _pretty_size(nbytes: int) -> str:
    size = float(nbytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def _scan_dot_spack(old_path: str) -> Tuple[List[Tuple[str, int, int]], int, int]:
    """Summarize the top-level contents of ``~/.spack``.

    Returns: ``(entries, total_bytes, total_files)`` where each entry is
        ``(name, bytes, files)``. Symlinks are counted but not followed.
    """
    entries = []
    total_bytes = total_files = 0
    for item in sorted(os.listdir(old_path)):
        item_path = os.path.join(old_path, item)
        nbytes = nfiles = 0
        if os.path.islink(item_path) or not os.path.isdir(item_path):
            nfiles = 1
            try:
                nbytes = os.lstat(item_path).st_size
            except OSError:
                pass
        else:
            for root, _, files in os.walk(item_path):
                for name in files:
                    nfiles += 1
                    try:
                        nbytes += os.lstat(os.path.join(root, name)).st_size
                    except OSError:
                        pass
        entries.append((item, nbytes, nfiles))
        total_bytes += nbytes
        total_files += nfiles
    return entries, total_bytes, total_files


def _dot_spack_references() -> Tuple[List[str], List[str]]:
    """Find values in the active configuration that resolve under ``~/.spack``.

    Returns: ``(fatal, other)``. ``fatal`` references are ones whose deletion loses data
        that cannot be regenerated (the install tree). ``other`` references are reported
        for the user to judge. Both are ``"<config path> = <value>"`` strings.

    Only the active configuration is inspected: inactive environments, conditional scopes,
    other Spack instances, and anything outside Spack's configuration are not seen.
    """
    fatal: List[str] = []
    other: List[str] = []

    # The install tree is the one reference we refuse to delete through
    root = spack.config.CONFIG.get("config:install_tree:root")
    if root and _under_old_dotspack(spack.config.canonicalize_path(root)):
        fatal.append(f"config:install_tree:root = {root}")

    # The next sections are paths that are only known with some non-config resolution for
    # environment variable overrides: The user scope, gpghome, and locations:*
    user_scope = spack.config.CONFIG.scopes.get("user")
    user_path = getattr(user_scope, "path", None)
    if user_path and _under_old_dotspack(user_path):
        fatal.append(f"user configuration scope = {user_path}")

    gnupghome = os.getenv("SPACK_GNUPGHOME")
    if gnupghome and _under_old_dotspack(gnupghome):
        other.append(f"SPACK_GNUPGHOME = {gnupghome}")

    for kind in ("data", "state", "cache"):
        resolved = spack.config._resolve_location_var(kind)
        if _under_old_dotspack(resolved):
            other.append(f"config:locations:{kind} = {resolved}")

    # Any string in the merged configuration that resolves under ~/.spack. This
    # over-reports (a non-path string could look like one) but that is harmless for an
    # informational list and avoids maintaining a per-key allow list.
    for section in spack.config.SECTION_SCHEMAS:
        data = spack.config.CONFIG.get(section)
        if not data:
            continue
        for key_path, value in _walk_strings(data):
            if not _looks_like_dot_spack_path(value):
                continue
            key = ":".join(
                str(k) if not isinstance(k, spack.migrate.Index) else f"[{k.idx}]"
                for k in [section] + key_path
            )
            other.append(f"{key} = {value}")

    return fatal, other


def _walk_strings(data, key_path=None):
    """Yield ``(key_path, value)`` for every string in a YAML data structure."""
    key_path = key_path or []
    if isinstance(data, dict):
        for key, value in data.items():
            yield from _walk_strings(value, key_path + [key])
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            yield from _walk_strings(item, key_path + [spack.migrate.Index(idx)])
    elif isinstance(data, str):
        yield key_path, data


def _looks_like_dot_spack_path(value: str) -> bool:
    """Whether a config string resolves under ``~/.spack``, as a path or a ``file://`` URL."""
    if value.startswith("file://"):
        value = value[len("file://") :]

    # Resolved path expands user as well
    resolved = spack.config.substitute_path_variables(value)
    if not os.path.isabs(resolved):
        return False
    return _under_old_dotspack(resolved)


def _cleanup_old(args) -> None:
    old_path = os.path.expanduser("~/.spack")

    if os.path.islink(old_path):
        tty.die(
            f"{old_path} is a symbolic link; refusing to remove it. Remove the link "
            "or its target yourself once you are sure nothing uses it."
        )
    if not os.path.isdir(old_path):
        tty.msg(f"No old user directory found at {old_path}")
        return

    entries, total_bytes, total_files = _scan_dot_spack(old_path)
    fatal, other = _dot_spack_references()

    # ---- report ----
    size = _pretty_size(total_bytes)
    lines = [f"This will permanently delete {old_path} ({size}, {total_files} files)."]
    if entries:
        lines.append("")
        lines.append("  Contents:")
        width = max(len(name) for name, _, _ in entries)
        for name, nbytes, nfiles in entries:
            lines.append(f"    {name:<{width}}  {_pretty_size(nbytes):>9}  {nfiles:>6} files")
    if fatal or other:
        lines.append("")
        lines.append("  The active configuration still refers to it:")
        for ref in fatal + other:
            lines.append(f"    {ref}")
    lines.append("")
    lines.append(
        "  Not checked: inactive environments, conditional config scopes, other Spack"
        " instances, and anything outside Spack configuration (scripts, cron jobs)."
    )
    tty.msg(*lines)

    # ---- hard stop: the install tree cannot be regenerated ----
    if fatal:
        tty.die(
            "Refusing to remove ~/.spack: it holds the current install tree or the active user"
            " configuration.",
            *[f"  - {r}" for r in fatal],
            "Point the setting(s) above at another directory, or remove ~/.spack manually.",
        )

    if args.dry_run:
        tty.msg(f"Dry run: would remove {old_path}")
        return

    # ---- confirmation ----
    if not args.yes:
        if not sys.stdin.isatty():
            tty.die("Not removing ~/.spack: no terminal to confirm on. Pass --yes to proceed.")
        if not tty.get_yes_or_no("Proceed?", default=False):
            tty.msg("Not removing ~/.spack.")
            return

    # ---- remove, reporting anything that could not be removed ----
    failures: List[str] = []

    def on_error(func, path, exc_info):
        failures.append(f"{path}: {exc_info[1]}")

    shutil.rmtree(old_path, onerror=on_error)
    if failures:
        shown = failures[:10]
        more = f"  ... and {len(failures) - 10} more" if len(failures) > 10 else None
        tty.die(
            f"Could not completely remove {old_path}:",
            *[f"  {f}" for f in shown],
            *([more] if more else []),
        )
    tty.msg(f"Removed old user directory: {old_path}")


def _use_new_layout(args):
    """Remove layout scope and trigger migration to new XDG locations."""
    layout_scope_path = spack.paths.layout_scope_path
    marker_path = spack.migrate.migration_done_marker_path()

    # The copies would go to the home directory, outside the isolation, and the isolate
    # scope would keep pointing at the legacy locations (see perform_migration).
    if os.path.exists(os.path.join(spack.paths.isolate_scope_path, "include.yaml")):
        tty.die(
            "This Spack instance is isolated; an isolated instance keeps its legacy resources"
            " where they are. Run `spack isolate --undo` first if you want to migrate them."
        )

    old_resources = spack.migrate.detect_old_resources()

    if not any(old_resources.values()):
        tty.msg("No old resources: nothing to migrate")
        return

    if args.dry_run:
        if os.path.exists(layout_scope_path) or os.path.exists(marker_path):
            tty.msg(f"Would remove layout scope: {layout_scope_path}")
        tty.msg("Would trigger migration to new XDG layout")
        return

    # Hold the migration lock across removing the decision and making the new one, so that
    # a command started meanwhile waits for the result rather than deciding for itself
    # (see perform_migration).
    with spack.migrate.migration_lock():
        if spack.migrate.detect_old_resources() != old_resources:
            tty.die(
                "Another process migrated while this process waited for the migration lock."
                " Re-run if still desired"
            )
        if os.path.exists(layout_scope_path):
            tty.msg(f"Removing layout scope: {layout_scope_path}")
            shutil.rmtree(layout_scope_path)
            tty.msg("  Layout scope removed")
        if os.path.exists(marker_path):
            os.remove(marker_path)

        spack.migrate.migrate_spack_prefix(old_resources)


def _undo(args):
    """Undo migration by pointing all resources back to their old locations."""

    old_resources = spack.migrate.detect_old_resources()

    if not any(old_resources.values()):
        tty.die(
            "Nothing to do: this spack instance has no old resources, and would not have "
            "been migrated."
        )

    if args.dry_run:
        tty.msg("Would perform the following operations:")
        if old_resources.get("licenses"):
            tty.msg(f"  - Point license_dir back to {spack.paths.old_licenses_path}")
        if old_resources.get("environments"):
            tty.msg(f"  - Point environments_root back to {spack.paths.old_envs_path}")
        if old_resources.get("gpg_keys"):
            tty.msg(f"  - Point gpg_path back to {spack.paths.old_gpg_path}")
            tty.msg(f"  - Point gpg_keys_path back to {spack.paths.old_gpg_keys_path}")
        # Installs are never migrated, so don't need to mention that
        tty.msg("  - Update layout scope to use old locations")
        return

    with spack.migrate.migration_lock():
        if spack.migrate.detect_old_resources() != old_resources:
            tty.die(
                "Another process migrated while this process waited for the migration lock."
                " Re-run if still desired"
            )

        tty.msg("Undoing migration...")
        spack.migrate.force_old_layout(old_resources, print_message=False)

    tty.msg("  Updated layout scope to point to old locations")

    tty.msg("\nUndo complete!")
    tty.msg(
        "\nNOTE: Old resources remain at their original locations. New locations may be\n"
        "left in place for other Spack instances to use, or manually removed if desired."
    )


def migrate(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    action = {"undo": _undo, "cleanup-old": _cleanup_old, "use-new-layout": _use_new_layout}
    action[args.migrate_command](args)
