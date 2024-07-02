# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
Interface for bootstrapping needed resources for running of Spack;
unlike bootstrap.py (the typical pathway) this does not refer to
utilities with Specs, but rather by an ID that refers to the needed binary.

This is currently only needed on Windows.
"""

import os
import pathlib
import shutil

from llnl.util import tty

import spack.paths
import spack.util.path as sup

BINARY_RESOURCE_SUBDIR = "binary-resources"


def binary_resource_root() -> pathlib.Path:
    """Returns the root of the Windows resources required for bootstrapping"""
    return pathlib.Path(spack.paths.user_cache_path) / BINARY_RESOURCE_SUBDIR


def win_insert_resource_into_environment(name):
    resource_root = binary_resource_root() / name
    env = spack.util.environment.EnvironmentModifications()
    env.append_path("PATH", str(resource_root / "bin"))
    env.apply_modifications()


class BinaryResource:
    """Represents a resource required by Spack to run, fetched as part
    of the bootstrapping operation

    More or less identical to package based resources but exposes additional logic related
    to bootstrapping/ resource visibility.

    Composes a name and a fetch strategy
    """

    def __init__(self, name, conf):
        """
        Args:
            name (str): Name of resource to be fetched
            conf (dict): Dictionary representing resource endpoint layout
        """
        self._name = name
        fetcher = spack.fetch_strategy.URLFetchStrategy(
            url=sup.substitute_path_variables(conf["endpoint"]), checksum=conf["sha256"]
        )
        self.stage = spack.stage.Stage(fetcher)

    def acquire_resource(self):
        "fetches, expands, and 'installs' resource"
        with self.stage as s:
            s.fetch()
            s.expand_archive()
            shutil.move(
                s.source_path,
                binary_resource_root() / self._name,
            )
        return True


def win_ensure_or_acquire_resource(name):
    """Acquires resource from configured sources"""
    path = os.environ.get("PATH", "")
    path = os.pathsep.join([str(binary_resource_root() / name / "bin"), path])
    cmd = spack.util.executable.which(name, path=path)
    if cmd:
        tty.debug(f"Resource {name} already available on system path at: {cmd.path}")
        win_insert_resource_into_environment(name)
    else:
        if not spack.config.get("bootstrap_resource:enable"):
            raise RuntimeError(
                f"Cannot fetch bootstrap resource {name} as it is disabled, and \
{name} is not available on the PATH"
            )
        resources = spack.config.get("bootstrap_resource:resources")
        providers = resources.get(name)["providers"]
        for provider in providers:
            if BinaryResource(name, provider).acquire_resource():
                win_insert_resource_into_environment(name)
                return
        # if we reach this point, and no other error was raised, there must be no providers given
        raise RuntimeError(
            f"Failed to fetch bootstrap resource {name} as no provider was specified"
        )
