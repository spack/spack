# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Bootstrap Spack core dependencies from binaries.

This module contains logic to bootstrap software required by Spack from binaries served in the
bootstrapping mirrors. The logic is quite different from an installation done from a Spack user,
because of the following reasons:

1. The binaries are all compiled on the same OS for a given platform (e.g. they are compiled on
   ``centos7`` on ``linux``), but they will be installed and used on the host OS. They are also
   targeted at the most generic architecture possible. That makes the binaries difficult to reuse
   with other specs in an environment without ad-hoc logic.
2. Bootstrapping has a fallback procedure where we try to install software by default from the
   most recent binaries, and proceed to older versions of the mirror, until we try building from
   sources as a last resort. This allows us not to be blocked on architectures where we don't
   have binaries readily available, but is also not compatible with the working of environments
   (they don't have fallback procedures).
3. Among the binaries we have clingo, so we can't concretize that with clingo :-)
4. clingo, GnuPG and patchelf binaries need to be verified by sha256 sum (all the other binaries
   we might add on top of that in principle can be verified with GPG signatures).
"""

import copy
import functools
import json
import os
import sys
import uuid
from typing import Any, Callable, Dict, Generic, List, Optional, Sequence, Type, TypeVar

import spack.binary_distribution
import spack.concretize
import spack.config
import spack.detection
import spack.error
import spack.installer_dispatch
import spack.mirrors.mirror
import spack.spec
import spack.store
import spack.user_environment
import spack.util.executable
import spack.util.spack_yaml
import spack.util.url
import spack.version
from spack.util import tty
from spack.util.lang import GroupedExceptionHandler

from ._common import (
    ExecutableInfo,
    _executables_in_store,
    _python_import,
    _root_spec,
    _try_import_from_store,
)
from .clingo import ClingoBootstrapConcretizer
from .config import spec_for_current_python

#: Name of the file containing metadata about the bootstrapping source
METADATA_YAML_FILENAME = "metadata.yaml"

#: Whether the current platform is Windows
IS_WINDOWS = sys.platform == "win32"

ConfigDictionary = Dict[str, Any]

#: Whatever a bootstrapper's store probe returns on success
ResultT = TypeVar("ResultT")


class BootstrapRequest(Generic[ResultT]):
    """Software to be made available in the bootstrap store, and how to check for it.

    The two kinds of request, a Python module and a set of executables, differ only in the
    spec to be installed, in the probe that tests whether the software can be used, in the
    arguments to be passed to the installer when building from sources, and in how the spec
    is concretized.
    """

    def __init__(
        self,
        abstract_spec: spack.spec.Spec,
        metadata_name: str,
        probe: Callable[[spack.spec.Spec], Optional[ResultT]],
        installer_args: Dict[str, Any],
        concretize: Callable[[spack.spec.Spec], spack.spec.Spec],
    ) -> None:
        #: Spec to be installed to satisfy this request
        self.abstract_spec = abstract_spec
        #: Name of the buildcache metadata file for this software
        self.metadata_name = metadata_name
        #: Returns the software from the store, or None if it is not usable from there
        self.probe = probe
        #: Extra arguments for the installer, when building from sources
        self.installer_args = installer_args
        #: Turns the abstract spec into the concrete one to be built from sources
        self.concretize = concretize

    @classmethod
    def for_module(
        cls,
        module: str,
        abstract_spec_str: str,
        concretize: Optional[Callable[[spack.spec.Spec], spack.spec.Spec]] = None,
    ) -> "BootstrapRequest[bool]":
        """Return a request for a module importable in the interpreter running Spack.

        Args:
            module: module to be imported in the interpreter running Spack
            abstract_spec_str: abstract spec that provides the module
            concretize: how to concretize the spec, when building from sources. Defaults to
                the regular concretizer.
        """
        return BootstrapRequest(
            abstract_spec=spack.spec.Spec(abstract_spec_str + " ^" + spec_for_current_python()),
            metadata_name=module,
            probe=functools.partial(_try_import_from_store, module),
            installer_args={
                "fail_fast": True,
                "root_policy": "source_only",
                "dependencies_policy": "source_only",
            },
            concretize=concretize or spack.concretize.concretize_one,
        )

    @classmethod
    def for_executables(
        cls, executables: Sequence[str], abstract_spec_str: str
    ) -> "BootstrapRequest[ExecutableInfo]":
        """Return a request for executables to be found in the PATH."""
        abstract_spec = spack.spec.Spec(abstract_spec_str)
        return BootstrapRequest(
            abstract_spec=abstract_spec,
            metadata_name=abstract_spec.name,
            probe=functools.partial(_executables_in_store, executables),
            installer_args={},
            concretize=spack.concretize.concretize_one,
        )


class Bootstrapper:
    """Interface for "core" software bootstrappers"""

    def __init__(self, conf: ConfigDictionary) -> None:
        self.name = conf["name"]
        self.metadata_dir = spack.config.canonicalize_path(conf["metadata"])

        # Check for relative paths, and turn them into absolute paths
        # root is the metadata_dir
        maybe_url = conf["info"]["url"]
        if spack.util.url.is_path_instead_of_url(maybe_url) and not os.path.isabs(maybe_url):
            maybe_url = os.path.join(self.metadata_dir, maybe_url)
        self.url = spack.mirrors.mirror.Mirror(maybe_url).fetch_url

        #: Mirror scope to be pushed onto the bootstrapping configuration when using
        #: this bootstrapper
        self.mirror_scope = spack.config.InternalConfigScope(
            f"bootstrap-{self.name}-{uuid.uuid4()}", {"mirrors:": {self.name: self.url}}
        )

    def try_to_bootstrap(self, request: BootstrapRequest[ResultT]) -> Optional[ResultT]:
        """Try to make the requested software available, from this source.

        Args:
            request: software to be bootstrapped, and the probe that tests for it

        Return:
            What the probe of the request returned, or None if bootstrapping failed
        """
        raise NotImplementedError("subclasses must implement try_to_bootstrap")


def _matching_entries(bincache_data, abstract_spec: spack.spec.Spec) -> List[Any]:
    """Return the metadata entries whose spec provides the abstract spec, in metadata order.

    Args:
        bincache_data: content of a buildcache metadata file
        abstract_spec: spec to be bootstrapped
    """
    return [
        entry
        for entry in bincache_data["verified"]
        if spack.spec.Spec(entry["spec"]).satisfies(abstract_spec)
    ]


class BuildcacheBootstrapper(Bootstrapper):
    """Install the software needed during bootstrapping from a buildcache."""

    def _read_metadata(self, package_name: str) -> Any:
        """Return metadata about the given package."""
        json_filename = f"{package_name}.json"
        json_dir = self.metadata_dir
        json_path = os.path.join(json_dir, json_filename)
        with open(json_path, encoding="utf-8") as stream:
            data = json.load(stream)
        return data

    def _install_by_hash(self, pkg_hash: str, pkg_sha256: str) -> None:
        # The caller is inside ensure_bootstrap_configuration, which already selects the platform
        query = spack.binary_distribution.BinaryCacheQuery(all_architectures=True)
        for match in spack.store.find([f"/{pkg_hash}"], multiple=False, query_fn=query):
            spack.binary_distribution.install_root_node(
                # allow_missing is true since when bootstrapping clingo we truncate runtime
                # deps such as gcc-runtime, since we link libstdc++ statically, and the other
                # further runtime deps are loaded by the Python interpreter. This just silences
                # warnings about missing dependencies.
                match,
                unsigned=True,
                force=True,
                sha256=pkg_sha256,
                allow_missing=True,
            )

    def _install_and_test(
        self, request: BootstrapRequest[ResultT], bincache_data
    ) -> Optional[ResultT]:
        # Ensure we see only the buildcache being used to bootstrap
        with spack.config.CONFIG.override(self.mirror_scope):
            # This index is currently needed to get the compiler used to build some
            # specs that we know by dag hash.
            spack.binary_distribution.BINARY_INDEX.regenerate_spec_cache()
            index = spack.binary_distribution.update_cache_and_get_specs()

            if not index:
                raise RuntimeError("The binary index is empty")

            for item in _matching_entries(bincache_data, request.abstract_spec):
                for _, pkg_hash, pkg_sha256 in item["binaries"]:
                    self._install_by_hash(pkg_hash, pkg_sha256)

                result = request.probe(request.abstract_spec)
                if result:
                    return result
        return None

    def try_to_bootstrap(self, request: BootstrapRequest[ResultT]) -> Optional[ResultT]:
        tty.debug(f"Bootstrapping {request.metadata_name} from pre-built binaries")
        return self._install_and_test(request, self._read_metadata(request.metadata_name))


class SourceBootstrapper(Bootstrapper):
    """Install the software needed during bootstrapping from sources."""

    def try_to_bootstrap(self, request: BootstrapRequest[ResultT]) -> Optional[ResultT]:
        tty.debug(f"Bootstrapping {request.metadata_name} from sources")

        # If we compile code from sources detecting a few build tools
        # might reduce compilation time by a fair amount
        _add_externals_if_missing()

        # Try to build and install from sources
        concrete_spec = request.concretize(request.abstract_spec)

        tty.debug(f"[BOOTSTRAP] Try installing '{request.abstract_spec}' from sources")
        with spack.config.CONFIG.override(self.mirror_scope):
            spack.installer_dispatch.create_installer(
                [concrete_spec.package], **request.installer_args
            ).install()

        return request.probe(concrete_spec)


#: Map a bootstrapper type to the corresponding class
_bootstrap_methods: Dict[str, Type[Bootstrapper]] = {
    "buildcache": BuildcacheBootstrapper,
    "install": SourceBootstrapper,
}


def create_bootstrapper(conf: ConfigDictionary) -> Bootstrapper:
    """Return a bootstrap object built according to the configuration argument"""
    return _bootstrap_methods[conf["type"]](conf)


def source_is_enabled(conf: ConfigDictionary) -> bool:
    """Returns True if the source is enabled for bootstrapping, False otherwise"""
    return spack.config.CONFIG.get("bootstrap:trusted").get(conf["name"], False)


def _cannot_bootstrap_message(
    what: str,
    abstract_spec: spack.spec.Spec,
    exception_handler: GroupedExceptionHandler,
    sources_tried: int,
) -> str:
    """Return the error message to report when no bootstrapping source succeeded.

    Args:
        what: description of what could not be bootstrapped
        abstract_spec: spec that was searched for
        exception_handler: handler that collected the failure of each source
        sources_tried: number of sources that were tried
    """
    msg = f'cannot bootstrap {what} from spec "{abstract_spec}"'
    if not sources_tried:
        msg += ": no bootstrapping sources are enabled"
    elif not exception_handler:
        msg += ": no bootstrapping source could provide it"
    elif spack.error.debug or spack.error.SHOW_BACKTRACE:
        msg += " " + exception_handler.grouped_message(with_tracebacks=True)
    else:
        msg += " " + exception_handler.grouped_message(with_tracebacks=False)
        msg += "\nRun `spack --backtrace ...` for more detailed errors"
    return msg


def enabled_bootstrapping_sources() -> List[ConfigDictionary]:
    """Return the configured bootstrapping sources that are enabled, in order."""
    return [x for x in bootstrapping_sources() if source_is_enabled(x)]


def _bootstrap_or_raise(
    request: BootstrapRequest[ResultT],
    what: str,
    error_type: Type[Exception],
    sources: Optional[Sequence[ConfigDictionary]] = None,
) -> ResultT:
    """Make the requested software available in the bootstrap store, or raise.

    The sources are tried in order, and the function exits on the first success.

    Args:
        request: software to be bootstrapped, and the probe that tests for it
        what: description of the software, to be used in the error message
        error_type: exception to be raised if no source succeeds
        sources: sources to be tried. Defaults to the enabled ones from configuration.

    Raises:
        error_type: if the software could not be bootstrapped
    """
    # Every source installs into the same store, so check it once for all of them
    result = request.probe(request.abstract_spec)
    if result:
        return result

    if sources is None:
        sources = enabled_bootstrapping_sources()

    exception_handler = GroupedExceptionHandler()

    for current_config in sources:
        with exception_handler.forward(current_config["name"], Exception):
            result = create_bootstrapper(current_config).try_to_bootstrap(request)
            if result:
                return result

    raise error_type(
        _cannot_bootstrap_message(what, request.abstract_spec, exception_handler, len(sources))
    )


def ensure_module_importable_or_raise(
    module: str,
    abstract_spec: Optional[str] = None,
    concretize: Optional[Callable[[spack.spec.Spec], spack.spec.Spec]] = None,
):
    """Make the requested module available for import, or raise.

    This function tries to import a Python module in the current interpreter
    using, in order, the methods configured in bootstrap.yaml.

    If none of the methods succeed, an exception is raised. The function exits
    on first success.

    Args:
        module: module to be imported in the current interpreter
        abstract_spec: abstract spec that might provide the module. If not
            given it defaults to "module"
        concretize: how to concretize the spec, when building from sources. Defaults to
            the regular concretizer.

    Raises:
        ImportError: if the module couldn't be imported
    """
    # If we can import it already, that's great
    tty.debug(f"[BOOTSTRAP MODULE {module}] Try importing from Python")
    if _python_import(module):
        return

    abstract_spec = abstract_spec or module
    _bootstrap_or_raise(
        BootstrapRequest.for_module(module, abstract_spec, concretize=concretize),
        what=f'the "{module}" Python module',
        error_type=ImportError,
    )


def ensure_executables_in_path_or_raise(
    executables: Sequence[str],
    abstract_spec: str,
    cmd_check: Optional[Callable[[spack.util.executable.Executable], bool]] = None,
) -> spack.util.executable.Executable:
    """Ensure that some executables are in path or raise.

    Args:
        executables: executables to be searched in the PATH, in order. The function
            exits on the first one found.
        abstract_spec: abstract spec that provides the executables
        cmd_check: callable predicate that takes a ``spack.util.executable.Executable``
            command and validates it. Should return ``True`` if the executable is
            acceptable, ``False`` otherwise. Can be used to, e.g., ensure a suitable
            version of the command before accepting for bootstrapping.

    Raises:
        RuntimeError: if the executables cannot be ensured to be in PATH

    Return:
        Executable object
    """
    cmd = spack.util.executable.which(*executables)
    if cmd:
        if not cmd_check or cmd_check(cmd):
            return cmd

    found = _bootstrap_or_raise(
        BootstrapRequest.for_executables(executables, abstract_spec),
        what=f"any of the {', '.join(executables)} executables",
        error_type=RuntimeError,
    )
    # Additional environment variables needed to run the command
    found.command.add_default_envmod(
        spack.user_environment.environment_modifications_for_specs(
            found.spec, set_package_py_globals=False
        )
    )
    return found.command


def _add_externals_if_missing() -> None:
    search_list = [
        # clingo
        "cmake",
        "bison",
        # GnuPG
        "gawk",
        # develop deps
        "git",
    ]
    if IS_WINDOWS:
        search_list.append("winbison")
    externals = spack.detection.by_path(search_list)
    # System git is typically deprecated, so mark as non-buildable to force it as external
    non_buildable_externals = {k: externals.pop(k) for k in ("git",) if k in externals}
    spack.detection.update_configuration(externals, scope="bootstrap", buildable=True)
    spack.detection.update_configuration(
        non_buildable_externals, scope="bootstrap", buildable=False
    )


def clingo_root_spec() -> str:
    """Return the root spec used to bootstrap clingo"""
    return _root_spec("clingo-bootstrap@spack+python")


def _concretize_clingo(abstract_spec: spack.spec.Spec) -> spack.spec.Spec:
    """Return the clingo spec to be built, edited from a prototype.

    The ``abstract_spec`` argument is discarded, so a change to ``clingo_root_spec()`` has
    no effect on what is built from sources.
    """
    return ClingoBootstrapConcretizer(configuration=spack.config.CONFIG).concretize()


def ensure_clingo_importable_or_raise() -> None:
    """Ensure that the clingo module is available for import."""
    ensure_module_importable_or_raise(
        module="clingo", abstract_spec=clingo_root_spec(), concretize=_concretize_clingo
    )


def gnupg_root_spec() -> str:
    """Return the root spec used to bootstrap GnuPG"""
    root_spec_name = "win-gpg" if IS_WINDOWS else "gnupg"
    return _root_spec(f"{root_spec_name}@2.3:")


def ensure_gpg_in_path_or_raise() -> spack.util.executable.Executable:
    """Ensure gpg or gpg2 are in the PATH or raise."""
    return ensure_executables_in_path_or_raise(
        executables=["gpg2", "gpg"], abstract_spec=gnupg_root_spec()
    )


def patchelf_root_spec() -> str:
    """Return the root spec used to bootstrap patchelf"""
    # 0.13.1 is the last version not to require C++17.
    return _root_spec("patchelf@0.13.1:")


def verify_patchelf(patchelf: "spack.util.executable.Executable") -> bool:
    """Older patchelf versions can produce broken binaries, so we
    verify the version here.

    Arguments:

        patchelf: patchelf executable
    """
    out = patchelf("--version", output=str, error=os.devnull, fail_on_error=False).strip()
    if patchelf.returncode != 0:
        return False
    parts = out.split(" ")
    if len(parts) < 2:
        return False
    try:
        version = spack.version.Version(parts[1])
    except ValueError:
        return False
    return version >= spack.version.Version("0.13.1")


def ensure_patchelf_in_path_or_raise() -> spack.util.executable.Executable:
    """Ensure patchelf is in the PATH or raise."""
    # If the latest patchelf cannot be provided, e.g. because the compiler doesn't
    # support C++17, retry with the newest version that does not require it.
    try:
        return ensure_executables_in_path_or_raise(
            executables=["patchelf"], abstract_spec=patchelf_root_spec(), cmd_check=verify_patchelf
        )
    except RuntimeError:
        return ensure_executables_in_path_or_raise(
            executables=["patchelf"],
            abstract_spec=_root_spec("patchelf@0.13.1:0.13"),
            cmd_check=verify_patchelf,
        )


def ensure_winsdk_external_or_raise() -> None:
    """Ensure the Windows SDK + WGL are available on system
    If both of these package are found, the Spack user or bootstrap
    configuration (depending on where Spack is running)
    will be updated to include all versions and variants detected.
    If either the WDK or WSDK are not found, this method will raise
    a RuntimeError.

    **NOTE:** This modifies the Spack config in the current scope,
    either user or environment depending on the calling context.
    This is different from all other current bootstrap dependency
    checks.
    """
    if set(["win-sdk", "wgl"]).issubset(spack.config.CONFIG.get("packages").keys()):
        return
    tty.debug("Detecting Windows SDK and WGL installations")
    # find the externals sequentially to avoid subprocesses being spawned
    externals = spack.detection.by_path(["win-sdk", "wgl"], max_workers=1)
    if not set(["win-sdk", "wgl"]) == externals.keys():
        missing_packages_lst = []
        if "wgl" not in externals:
            missing_packages_lst.append("wgl")
        if "win-sdk" not in externals:
            missing_packages_lst.append("win-sdk")
        missing_packages = " & ".join(missing_packages_lst)
        raise RuntimeError(
            f"Unable to find the {missing_packages}, please install these packages via the Visual "
            "Studio installer before proceeding with Spack or provide the path to a non standard "
            "install with 'spack external find --path'"
        )
    # wgl/sdk are not required for bootstrapping Spack, but
    # are required for building anything non trivial
    # add to user config so they can be used by subsequent Spack ops
    spack.detection.update_configuration(externals, buildable=False)


def ensure_core_dependencies() -> None:
    """Ensure the presence of all the core dependencies."""
    if sys.platform.lower() == "linux":
        ensure_patchelf_in_path_or_raise()
    ensure_gpg_in_path_or_raise()
    ensure_clingo_importable_or_raise()


def all_core_root_specs() -> List[str]:
    """Return a list of all the core root specs that may be used to bootstrap Spack"""
    return [clingo_root_spec(), gnupg_root_spec(), patchelf_root_spec()]


def bootstrapping_sources(scope: Optional[str] = None):
    """Return the list of configured sources of software for bootstrapping Spack

    Args:
        scope: if a valid configuration scope is given, return the
            list only from that scope
    """
    source_configs = spack.config.CONFIG.get("bootstrap:sources", default=None, scope=scope)
    source_configs = source_configs or []
    list_of_sources = []
    for entry in source_configs:
        current = copy.copy(entry)
        metadata_dir = spack.config.canonicalize_path(entry["metadata"])
        metadata_yaml = os.path.join(metadata_dir, METADATA_YAML_FILENAME)
        try:
            with open(metadata_yaml, encoding="utf-8") as stream:
                current.update(spack.util.spack_yaml.load(stream))
            list_of_sources.append(current)
        except OSError:
            pass
    return list_of_sources
