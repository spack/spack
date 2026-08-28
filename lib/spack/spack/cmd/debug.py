# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import platform
import re
from typing import Optional

import spack
import spack.cmd
import spack.config
import spack.debug_source
import spack.environment as ev
import spack.platforms
import spack.repo
import spack.spec
import spack.util.git
from spack.llnl.util import tty

description = "debugging commands for troubleshooting Spack"
section = "developer"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="debug_command")
    sp.add_parser("report", help="print information useful for bug reports")

    stage_source_parser = sp.add_parser(
        "stage-source",
        help="fetch pristine source for an installed package into the debug-source cache "
        "(fallback for packages installed without 'spack install --debug-source')",
    )
    stage_source_parser.add_argument("spec", help="installed spec to stage source for")
    stage_source_parser.add_argument(
        "--force", action="store_true", help="re-stage even if already staged"
    )

    split_symbols_parser = sp.add_parser(
        "split-symbols",
        help="split debug symbols for an installed package into the debug-source cache "
        "(fallback for packages installed without 'spack install --debug-symbols')",
    )
    split_symbols_parser.add_argument("spec", help="installed spec to split symbols for")
    split_symbols_parser.add_argument(
        "--force", action="store_true", help="re-split even if already split"
    )

    fetch_parser = sp.add_parser(
        "fetch",
        help="fetch previously-pushed debug source/symbols for an installed spec "
        "from configured OCI mirrors",
    )
    fetch_parser.add_argument("spec", nargs="?", help="installed spec to fetch debug info for")
    fetch_parser.add_argument("--build-id", help="fetch a single specific build-id instead")
    fetch_parser.add_argument("--mirror", help="mirror name to fetch from (default: all configured OCI mirrors)")

    serve_parser = sp.add_parser(
        "serve",
        help="run a local debuginfod-compatible server backed by configured OCI mirrors "
        "(resolves GDB's DEBUGINFOD_URLS requests via OCI, redirecting to the registry "
        "for the actual payload rather than proxying it)",
    )
    serve_parser.add_argument("--mirror", help="mirror name to search (default: all configured OCI mirrors)")
    serve_parser.add_argument("--host", default="127.0.0.1", help="listen address (default: 127.0.0.1)")
    serve_parser.add_argument("--port", type=int, default=8002, help="listen port (default: 8002)")
    daemon_group = serve_parser.add_mutually_exclusive_group()
    daemon_group.add_argument(
        "--start-daemon", action="store_true",
        help="start the server detached in the background and return immediately"
    )
    daemon_group.add_argument(
        "--stop-daemon", action="store_true",
        help="stop a previously-started background server for the given --host/--port"
    )
    serve_parser.add_argument(
        "--status", action="store_true",
        help="report whether a background server is running for the given --host/--port, then exit"
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


def stage_source(args):
    specs = spack.cmd.parse_specs(args.spec, concretize=False)
    if len(specs) != 1:
        tty.die("'spack debug stage-source' requires exactly one spec")

    env = ev.active_environment()
    spec = spack.cmd.disambiguate_spec(specs[0], env)
    pkg = spec.package
    spack.debug_source.stage_source(pkg, force=args.force)


def split_symbols(args):
    specs = spack.cmd.parse_specs(args.spec, concretize=False)
    if len(specs) != 1:
        tty.die("'spack debug split-symbols' requires exactly one spec")

    env = ev.active_environment()
    spec = spack.cmd.disambiguate_spec(specs[0], env)
    pkg = spec.package
    spack.debug_source.split_symbols(pkg, force=args.force)

def fetch(args):
    if not args.spec and not args.build_id:
        tty.die("'spack debug fetch' requires a spec or --build-id")

    mirror = None
    if args.mirror:
        mirror = spack.mirrors.mirror.MirrorCollection(binary=True).get(args.mirror)
        if mirror is None:
            tty.die(f"No configured mirror named '{args.mirror}'")

    if args.build_id and not args.spec:
        tty.die("--build-id alone (without a spec) is not yet supported -- "
                 "spack.debug_source.debug_source_dir() needs a Spec to key the cache")
        # (a build-id-only fetch would need a different, unkeyed destination --
        #  worth a separate design decision if this case matters in practice)

    specs = spack.cmd.parse_specs(args.spec, concretize=False)
    if len(specs) != 1:
        tty.die("'spack debug fetch' requires exactly one spec")
    env = ev.active_environment()
    spec = spack.cmd.disambiguate_spec(specs[0], env)

    spack.debug_source.fetch_debug_artifacts(spec, build_id=args.build_id, mirror=mirror)

def serve(args):
    mirror = None
    if args.mirror:
        mirror = spack.mirrors.mirror.MirrorCollection(binary=True).get(args.mirror)
        if mirror is None:
            tty.die(f"No configured mirror named '{args.mirror}'")

    if args.status:
        pid = spack.debug_source.daemon_status(host=args.host, port=args.port)
        if pid is None:
            tty.msg(f"no debuginfod daemon running for {args.host}:{args.port}")
        else:
            tty.msg(f"debuginfod daemon running for {args.host}:{args.port} (pid {pid})")
        return

    if args.stop_daemon:
        stopped = spack.debug_source.stop_debuginfod_daemon(host=args.host, port=args.port)
        if stopped:
            tty.msg(f"stopped debuginfod daemon for {args.host}:{args.port}")
        else:
            tty.msg(f"no debuginfod daemon was running for {args.host}:{args.port}")
        return

    if args.start_daemon:
        pid = spack.debug_source.start_debuginfod_daemon(host=args.host, port=args.port, mirror=mirror)
        tty.msg(f"debuginfod daemon running for {args.host}:{args.port} (pid {pid})")
        tty.msg(f"set DEBUGINFOD_URLS=http://{args.host}:{args.port} to use it")
        return
            
    spack.debug_source.serve_debuginfod(host=args.host, port=args.port, mirror=mirror)

def debug(parser, args):
    if args.debug_command == "report":
        report(args)
    elif args.debug_command == "stage-source":
        stage_source(args)
    elif args.debug_command == "split-symbols":
        split_symbols(args)
    elif args.debug_command == "fetch":
        fetch(args)
    elif args.debug_command == "serve":
        serve(args)
