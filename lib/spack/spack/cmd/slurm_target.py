# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Select a CPU target compatible with an entire Slurm node selection."""

import argparse
import shlex
import subprocess
import tempfile

import spack.paths
from spack.util.slurm_target import SlurmTargetError, discover, resolve, write_scope

description = "detect Slurm-compatible CPU targets for package builds"
section = "config"
level = "long"


def setup_parser(parser: argparse.ArgumentParser) -> None:
    subs = parser.add_subparsers(dest="action", metavar="ACTION")
    subs.required = True
    for action in ("detect", "sync", "spec", "install"):
        sub = subs.add_parser(
            action,
            help={
                "detect": "print the compatible target without modifying Spack configuration",
                "sync": "write a standalone strict config scope for spack -C",
                "spec": "detect target and inspect a concretized package spec",
                "install": "detect target and install packages using the strict target scope",
            }[action],
        )
        sub.add_argument(
            "--partition", help="comma-separated Slurm partitions; default: all visible"
        )
        sub.add_argument(
            "--source",
            choices=("features", "auto", "probe", "file"),
            default="features",
            help="auto/probe can run bounded srun jobs",
        )
        sub.add_argument(
            "--inventory", help="offline JSON node->Archspec target map (file source)"
        )
        sub.add_argument(
            "--mode",
            choices=("common", "generic"),
            default="common",
            help="common chooses a specific compatible microarchitecture",
        )
        sub.add_argument(
            "--max-probes",
            type=int,
            default=32,
            help="maximum compute-node srun allocations (default 32)",
        )
        sub.add_argument("--account", help="Slurm account used for explicit node probes")
        sub.add_argument("--qos", help="Slurm QoS used for explicit node probes")
        sub.add_argument("--verbose-nodes", action="store_true", help="print all node targets")
        if action == "detect":
            sub.add_argument(
                "--target-only", action="store_true", help="print only the target name"
            )
        if action == "sync":
            sub.add_argument("--scope", required=True, help="config scope directory to create")
        if action in ("spec", "install"):
            sub.add_argument(
                "spack_args",
                nargs=argparse.REMAINDER,
                help="arguments after -- passed verbatim to Spack",
            )


def slurm_target(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.action in ("install", "spec"):
        forwarded = list(args.spack_args)
        if forwarded and forwarded[0] == "--":
            forwarded.pop(0)
        if not forwarded:
            parser.error("provide Spack arguments after '--' (e.g. -- zlib)")
    else:
        forwarded = []

    if args.source == "file" and not args.inventory:
        parser.error("--source file requires --inventory PATH")
    if args.max_probes < 0:
        parser.error("--max-probes must be >= 0")

    try:
        nodes = discover(
            partition=args.partition,
            source=args.source,
            inventory=args.inventory,
            account=args.account,
            qos=args.qos,
            max_probes=args.max_probes,
            spack_executable=spack.paths.spack_script,
        )
        result = resolve(nodes, mode=args.mode)
        if args.action == "detect" and args.target_only:
            print(result.target)
            return
        print(f"Slurm target: {result.target} ({result.strategy})", flush=True)
        print(f"Nodes: {len(nodes)} | generic fallback: {result.generic}", flush=True)
        if args.source == "file":
            print("NOTE: offline inventory was not checked against live Slurm nodes", flush=True)
        if args.verbose_nodes:
            for node, target in sorted(nodes.items()):
                print(f"  {node}: {target}", flush=True)
        if result.strategy == "ambiguous-generic-fallback":
            print("Incomparable common ancestors: " + ", ".join(result.candidates), flush=True)
        if args.action == "detect":
            return
        if args.action == "sync":
            path = write_scope(
                args.scope,
                result,
                nodes,
                partition=args.partition,
                source=args.source,
                mode=args.mode,
            )
            print(f"Wrote config scope: {path}", flush=True)
            print("Use: spack -C " + shlex.quote(str(path)) + " spec zlib", flush=True)
            return
        # An ephemeral scope is not installed in the user's global config.
        with tempfile.TemporaryDirectory(prefix="spack-slurm-target-") as directory:
            write_scope(
                directory,
                result,
                nodes,
                partition=args.partition,
                source=args.source,
                mode=args.mode,
            )
            command = [spack.paths.spack_script, "-C", directory, args.action, *forwarded]
            completed = subprocess.run(command, check=False)
            if completed.returncode:
                raise SystemExit(completed.returncode)
    except SlurmTargetError as e:
        parser.error(str(e))
