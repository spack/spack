# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module handles transmission of Spack state to child processes started
using the ``"spawn"`` start method. Notably, installations are performed in a
subprocess and require transmitting the Package object (in such a way
that the repository is available for importing when it is deserialized);
installations performed in Spack unit tests may include additional
modifications to global state in memory that must be replicated in the
child process.
"""
import importlib
import io
import multiprocessing
import multiprocessing.context
import pickle
from types import ModuleType
from typing import TYPE_CHECKING, Optional

import spack.config
import spack.paths
import spack.platforms
import spack.repo
import spack.store

if TYPE_CHECKING:
    import spack.package_base

#: Used in tests to track monkeypatches that need to be restored in child processes
MONKEYPATCHES: list = []


def serialize(pkg: "spack.package_base.PackageBase") -> io.BytesIO:
    serialized_pkg = io.BytesIO()
    pickle.dump(pkg, serialized_pkg)
    serialized_pkg.seek(0)
    return serialized_pkg


def deserialize(serialized_pkg: io.BytesIO) -> "spack.package_base.PackageBase":
    pkg = pickle.load(serialized_pkg)
    pkg.spec._package = pkg
    # ensure overwritten package class attributes get applied
    spack.repo.PATH.get_pkg_class(pkg.spec.name)
    return pkg


class SpackTestProcess:
    def __init__(self, fn):
        self.fn = fn

    def _restore_and_run(self, fn, test_state):
        test_state.restore()
        fn()

    def create(self):
        test_state = GlobalStateMarshaler()
        return multiprocessing.Process(target=self._restore_and_run, args=(self.fn, test_state))


class PackageInstallContext:
    """Captures the in-memory process state of a package installation that needs to be transmitted
    to a child process."""

    def __init__(
        self,
        pkg: "spack.package_base.PackageBase",
        *,
        ctx: Optional[multiprocessing.context.BaseContext] = None,
    ):
        ctx = ctx or multiprocessing.get_context()
        self.global_state = GlobalStateMarshaler(ctx=ctx)
        self.pkg = pkg if ctx.get_start_method() == "fork" else serialize(pkg)
        self.spack_working_dir = spack.paths.spack_working_dir

    def restore(self) -> "spack.package_base.PackageBase":
        spack.paths.spack_working_dir = self.spack_working_dir
        self.global_state.restore()
        return deserialize(self.pkg) if isinstance(self.pkg, io.BytesIO) else self.pkg


class GlobalStateMarshaler:
    """Class to serialize and restore global state for child processes if needed.

    Spack may modify state that is normally read from disk or command line in memory;
    this object is responsible for properly serializing that state to be applied to a subprocess.
    """

    def __init__(
        self, *, ctx: Optional[Optional[multiprocessing.context.BaseContext]] = None
    ) -> None:
        ctx = ctx or multiprocessing.get_context()
        self.is_forked = ctx.get_start_method() == "fork"
        if self.is_forked:
            return

        from spack.environment import active_environment

        self.config = spack.config.CONFIG.ensure_unwrapped()
        self.platform = spack.platforms.host
        self.store = spack.store.STORE
        self.test_patches = TestPatches.create()
        self.env = active_environment()

    def restore(self):
        if self.is_forked:
            return
        spack.config.CONFIG = self.config
        spack.repo.enable_repo(spack.repo.RepoPath.from_config(self.config))
        spack.platforms.host = self.platform
        spack.store.STORE = self.store
        self.test_patches.restore()
        if self.env:
            from spack.environment import activate

            activate(self.env)


class TestPatches:
    def __init__(self, module_patches, class_patches):
        self.module_patches = [(x, y, serialize(z)) for (x, y, z) in module_patches]
        self.class_patches = [(x, y, serialize(z)) for (x, y, z) in class_patches]

    def restore(self):
        if not self.module_patches and not self.class_patches:
            return
        # this code path is only followed in tests, so use inline imports
        from pydoc import locate

        for module_name, attr_name, value in self.module_patches:
            value = pickle.load(value)
            module = importlib.import_module(module_name)
            setattr(module, attr_name, value)
        for class_fqn, attr_name, value in self.class_patches:
            value = pickle.load(value)
            cls = locate(class_fqn)
            setattr(cls, attr_name, value)

    @staticmethod
    def create():
        module_patches = []
        class_patches = []
        for target, name in MONKEYPATCHES:
            if isinstance(target, ModuleType):
                new_val = getattr(target, name)
                module_name = target.__name__
                module_patches.append((module_name, name, new_val))
            elif isinstance(target, type):
                new_val = getattr(target, name)
                class_fqn = ".".join([target.__module__, target.__name__])
                class_patches.append((class_fqn, name, new_val))

        return TestPatches(module_patches, class_patches)
