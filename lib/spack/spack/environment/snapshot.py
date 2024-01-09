# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Manage snapshots of environments"""
import datetime
import io
import os.path
import pathlib
import shutil
from typing import List, NamedTuple

from llnl.util.tty import colify, color

from .environment import Environment, SpackEnvironmentError, lockfile_name, manifest_name


class Snapshot(NamedTuple):
    time: datetime.datetime
    spack_yaml: pathlib.Path
    spack_lock: pathlib.Path


class SnapshotSaver:
    """Saves a snapshot of a Spack environment"""

    def __init__(self, env: Environment) -> None:
        self.environment = env

    def save(self, snapshot_dir: pathlib.Path) -> Snapshot:
        if not os.path.exists(self.environment.lock_path):
            raise SpackEnvironmentError(
                f"cannot take a snapshot of the environment in '{self.environment.path}', "
                f"because it has no lock file."
            )

        snapshot_time = datetime.datetime.now(tz=datetime.timezone.utc)
        root_dir = snapshot_dir / str(snapshot_time.timestamp())
        # TODO: Ensure the root specs in the lockfile are in sync with the manifest
        snapshot = Snapshot(
            time=snapshot_time,
            spack_yaml=root_dir / manifest_name,
            spack_lock=root_dir / lockfile_name,
        )
        root_dir.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy(self.environment.manifest_path, snapshot.spack_yaml)
            shutil.copy(self.environment.lock_path, snapshot.spack_lock)
        except OSError as e:
            shutil.rmtree(root_dir)
            msg = f"cannot take a snapshot of the environment: {e}"
            raise SpackEnvironmentError(msg) from e

        return snapshot


class SnapshotLoader:
    """Loads a snapshot of a Spack environment"""

    def __init__(self, snapshot: Snapshot):
        self.snapshot = snapshot

    def load(self, environment_dir: pathlib.Path) -> Environment:
        try:
            shutil.copy(self.snapshot.spack_yaml, environment_dir / manifest_name)
            shutil.copy(self.snapshot.spack_lock, environment_dir / lockfile_name)
        except OSError as e:
            msg = f"cannot restore the environment in {environment_dir}: {str(e)}"
            raise RuntimeError(msg) from e

        env = Environment(manifest_dir=environment_dir)
        env.regenerate_views()
        return env


class SnapshotPrompter:
    def __init__(self, env: Environment, stream: io.IOBase) -> None:
        self.environment = env
        self.snapshots: List[Snapshot] = []
        self._update_snapshots()
        self.stream = stream

    def _update_snapshots(self):
        self.snapshots = [
            snapshot_from_dir(x)
            for x in pathlib.Path(self.environment.snapshots_path).iterdir()
            if x.is_dir()
        ]
        self.snapshots.sort(key=lambda x: x.time)

    def prompt(self) -> None:
        while True:
            self.show_available_snapshots()
            command = self.ask_user()
            if command == "q":
                break
            elif command == "s":
                snapshot = SnapshotSaver(self.environment).save(
                    snapshot_dir=pathlib.Path(self.environment.snapshots_path)
                )
                self.stream.write(f"\nSnapshot taken at {snapshot.time}\n\n")
                self._update_snapshots()

            elif command == "d":
                self.ask_what_to_delete()

            elif command == "r":
                self.ask_what_to_restore()

            else:
                self.stream.write(f"\nInvalid command: {command}\n\n")

    def show_available_snapshots(self):
        header = "Available snapshots:\n\n" if self.snapshots else "No snapshots available.\n\n"
        self.stream.write(header)
        for ii, snapshot in enumerate(self.snapshots):
            self.stream.write(f"{ii}.    Date: {str(snapshot.time)}\n")
        self.stream.write("\n")

    def ask_user(self):
        self.stream.write(color.colorize("Enter the @*{action} to take:\n"))
        commands = ("@*b{[s]ave}", "@*b{[r]estore}", "@*b{[d]elete}", "@*b{[q]}uit")
        colify.colify(list(map(color.colorize, commands)), indent=4)
        try:
            command = input(color.colorize("@*g{action>} ")).strip().lower()
        except EOFError:
            print()
            command = "q"
        return command

    def ask_what_to_restore(self):
        self.stream.write(color.colorize("Enter the @*{number} of the snapshot to restore:\n"))
        try:
            idx = input(color.colorize("@*g{number>} ")).strip().lower()
            idx = int(idx)
        except EOFError:
            return

        if idx >= len(self.snapshots):
            return

        SnapshotLoader(self.snapshots[idx]).load(pathlib.Path(self.environment.path))
        self.stream.write(f"\nRestored environment from {self.snapshots[idx].time}\n\n")

    def ask_what_to_delete(self):
        self.stream.write(color.colorize("Enter the @*{number} of the snapshot to delete:\n"))
        try:
            idx = input(color.colorize("@*g{number>} ")).strip().lower()
            idx = int(idx)
        except EOFError:
            return

        if idx >= len(self.snapshots):
            return

        shutil.rmtree(self.snapshots[idx].spack_yaml.parent)
        self._update_snapshots()


def snapshot_from_dir(snapshot_dir: pathlib.Path) -> Snapshot:
    """Returns a snapshot object, given the directory where the data is stored"""
    time = datetime.datetime.fromtimestamp(float(snapshot_dir.name), tz=datetime.timezone.utc)
    return Snapshot(
        time=time, spack_yaml=snapshot_dir / manifest_name, spack_lock=snapshot_dir / lockfile_name
    )
