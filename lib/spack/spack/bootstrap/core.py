# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Bootstrap Spack core dependencies.

Core dependencies are installed by the regular installer into the bootstrap store, from the first
configured source that provides them. They are recorded in an environment per interpreter, whose
lockfile is written without the concretizer, since clingo may be among the software to install:

1. From a buildcache source, the lockfile holds a spec from the index of the mirror. Its nodes
   are installed from binaries that are verified by the sha256 sums of the source metadata, while
   the externals of the build host (python, libc) are spliced for those of this host.
2. From a source that builds from sources, the spec is concretized from a prototype (clingo), or
   by the concretizer.
"""

import copy
import functools
import os
import sys
import uuid
from typing import Any, Callable, Dict, Generic, List, Optional, Sequence, Type, TypeVar

import spack.binary_distribution
import spack.compilers.libraries
import spack.concretize
import spack.config
import spack.deptypes as dt
import spack.detection
import spack.environment
import spack.error
import spack.mirrors.mirror
import spack.repo
import spack.spec
import spack.store
import spack.user_environment
import spack.util.executable
import spack.util.gpg
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
from .clingo import ClingoBootstrapConcretizer, host_externals
from .config import interpreter_dirname, root_path, spec_for_current_python

#: Name of the file containing metadata about the bootstrapping source
METADATA_YAML_FILENAME = "metadata.yaml"

#: Whether the current platform is Windows
IS_WINDOWS = sys.platform == "win32"

ConfigDictionary = Dict[str, Any]

#: Whatever a bootstrapper's store probe returns on success
ResultT = TypeVar("ResultT")

_SOURCE_ONLY = {"root_policy": "source_only", "dependencies_policy": "source_only"}


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
        probe: Callable[[spack.spec.Spec], Optional[ResultT]],
        installer_args: Dict[str, Any],
        concretize: Callable[[spack.spec.Spec], spack.spec.Spec],
    ) -> None:
        #: Spec to be installed to satisfy this request
        self.abstract_spec = abstract_spec
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
            probe=functools.partial(_try_import_from_store, module),
            installer_args=_SOURCE_ONLY,
            concretize=concretize or spack.concretize.concretize_one,
        )

    @classmethod
    def for_executables(
        cls, executables: Sequence[str], abstract_spec_str: str
    ) -> "BootstrapRequest[ExecutableInfo]":
        """Return a request for executables to be found in the PATH."""
        return BootstrapRequest(
            abstract_spec=spack.spec.Spec(abstract_spec_str),
            probe=functools.partial(_executables_in_store, executables),
            installer_args={},
            concretize=spack.concretize.concretize_one,
        )


def _mirror_scope(source: ConfigDictionary) -> spack.config.InternalConfigScope:
    """Return a configuration scope to install from a bootstrapping source, whose mirror is the
    only one"""
    url = source["info"]["url"]
    # A relative path is relative to the metadata directory
    if spack.util.url.is_path_instead_of_url(url) and not os.path.isabs(url):
        url = os.path.join(spack.config.canonicalize_path(source["metadata"]), url)
    data: Dict[str, Any] = {
        "mirrors:": {source["name"]: spack.mirrors.mirror.Mirror(url).fetch_url}
    }
    if source["type"] == "buildcache":
        # Pinned binaries can be of versions that were deprecated after they were built
        allow = [{"labels": ["version_deprecated"]}]
        data["packages"] = {"all": {"deprecation": {"allow": allow}}}
    return spack.config.InternalConfigScope(f"bootstrap-{source['name']}-{uuid.uuid4()}", data)


def _python_venv(prototype: spack.spec.Spec, python: spack.spec.Spec) -> spack.spec.Spec:
    """Return a concrete python-venv like the prototype, for another interpreter"""
    venv = prototype.copy(deps=False)
    venv._mark_concrete(False)
    venv.architecture = python.architecture
    edge = prototype.edges_to_dependencies("python")[0]
    venv.add_dependency_edge(python, depflag=edge.depflag, virtuals=edge.virtuals)
    spack.spec.assign_hashes([venv], repo=spack.repo.PATH)
    return venv


def _pinned_binary(abstract_spec: spack.spec.Spec, sha256: Dict[str, str]) -> spack.spec.Spec:
    """Return a spec from the index of the configured mirror that provides the abstract spec.

    Every node of the spec is pinned by a sha256 sum, except for the externals of the build host,
    which are spliced for those of this host, and a venv, which is created anew for the python of
    this host.

    Args:
        abstract_spec: spec to be bootstrapped
        sha256: expected sha256 sum of the binary of each pinned node, by DAG hash
    """
    host = {s.name: s for s in host_externals()}
    index = spack.binary_distribution.update_cache_and_get_specs(config=spack.config.CONFIG)
    candidates = [s for s in index if s.dag_hash() in sha256 and s.satisfies(abstract_spec)]
    for candidate in sorted(candidates, key=lambda s: s.version, reverse=True):
        result = candidate
        for node in candidate.traverse(root=False, deptype=dt.LINK | dt.RUN):
            if node.name == "python-venv" and "python" in host:
                result = result.splice(_python_venv(node, host["python"]), transitive=True)
            elif node.external and node.name in host:
                # The abstract spec selects the version of python, libc must be at least as recent
                if node.name != "python" and host[node.name].version < node.version:
                    break
                result = result.splice(host[node.name], transitive=False)
            elif node.external or node.dag_hash() not in sha256:
                break
        else:
            return result
    raise RuntimeError(f'no pinned binary provides "{abstract_spec}"')


def _core_environment() -> spack.environment.Environment:
    """Return the environment recording the core dependencies installed for this interpreter"""
    path = os.path.join(root_path(), "environments", f"core-{interpreter_dirname()}")
    if os.path.exists(os.path.join(path, spack.environment.manifest_name)):
        return spack.environment.Environment(path)
    return spack.environment.create_in_dir(path, with_view=False)


def _install_from_source(
    request: BootstrapRequest[ResultT], source: ConfigDictionary
) -> Optional[ResultT]:
    """Try to make the requested software available from a bootstrapping source.

    Return:
        What the probe of the request returned, or None if the software is not usable
    """
    tty.debug(f"Bootstrapping {request.abstract_spec.name} from {source['name']}")
    with spack.config.CONFIG.override(_mirror_scope(source)):
        if source["type"] == "buildcache":
            sha256 = source["sha256"]
            concrete_spec = _pinned_binary(request.abstract_spec, sha256)
            # Nodes without a pinned binary, like a venv for the python of this host, come first
            from_sources = [
                s
                for s in concrete_spec.traverse(root=False, deptype=dt.LINK | dt.RUN)
                if not s.external and s.build_spec.dag_hash() not in sha256
            ]
            cache_only = {"root_policy": "cache_only", "dependencies_policy": "cache_only"}
            installs = [
                (from_sources, _SOURCE_ONLY),
                ([concrete_spec], {**cache_only, "binary_checksums": sha256}),
            ]
        else:
            # If we compile code from sources detecting a few build tools
            # might reduce compilation time by a fair amount
            _add_externals_if_missing()
            concrete_spec = request.concretize(request.abstract_spec)
            installs = [([concrete_spec], request.installer_args)]

        env = _core_environment()
        with env.write_transaction():
            if any(x.root == request.abstract_spec for x in env.concretized_roots):
                env.deconcretize_by_user_spec(request.abstract_spec)
            env.add_concrete_spec(request.abstract_spec, concrete_spec)
            env.write(regenerate=False)
            for specs, installer_args in installs:
                if specs:
                    env.install_specs(specs, fail_fast=True, **installer_args)

    return request.probe(concrete_spec)


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

    # Fail before extracting the tarball if the database cannot be modified.
    spack.store.STORE.db.ensure_latest_db_version()

    if sources is None:
        sources = enabled_bootstrapping_sources()

    exception_handler = GroupedExceptionHandler()

    for current_config in sources:
        with exception_handler.forward(current_config["name"], Exception):
            result = _install_from_source(request, current_config)
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
    path: Optional[List[str]] = None,
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
        path: directories to search instead of PATH. Defaults to PATH.

    Raises:
        RuntimeError: if the executables cannot be ensured to be in PATH

    Return:
        Executable object
    """
    cmd = spack.util.executable.which(*executables, path=path)
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
    externals = spack.detection.by_path(search_list, repo=spack.repo.PATH)
    # System git is typically deprecated, so mark as non-buildable to force it as external
    non_buildable_externals = {k: externals.pop(k) for k in ("git",) if k in externals}
    spack.detection.update_configuration(
        externals, config=spack.config.CONFIG, scope="bootstrap", buildable=True
    )
    spack.detection.update_configuration(
        non_buildable_externals, config=spack.config.CONFIG, scope="bootstrap", buildable=False
    )


def clingo_root_spec(platform: Optional[str] = None, target: Optional[str] = None) -> str:
    """Return the root spec used to bootstrap clingo.

    Args:
        platform: platform the binary will run on. Defaults to the host platform.
        target: target family the binary will run on. Defaults to the host target family.
    """
    return _root_spec("clingo-bootstrap@spack+python", platform=platform, target=target)


def _concretize_clingo(abstract_spec: spack.spec.Spec) -> spack.spec.Spec:
    """Return the clingo spec to be built, edited from a prototype.

    The ``abstract_spec`` argument is discarded, so a change to ``clingo_root_spec()`` has
    no effect on what is built from sources.
    """
    return ClingoBootstrapConcretizer(
        spack.config.CONFIG,
        repo=spack.repo.PATH,
        compiler_cache=spack.compilers.libraries.COMPILER_CACHE,
    ).concretize()


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
        executables=["gpg2", "gpg"],
        abstract_spec=gnupg_root_spec(),
        path=spack.util.gpg.search_path(),
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
    externals = spack.detection.by_path(["win-sdk", "wgl"], repo=spack.repo.PATH, max_workers=1)
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
    spack.detection.update_configuration(externals, config=spack.config.CONFIG, buildable=False)


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
