# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Here we consolidate the logic for creating an abstract description
of the information that module systems need.

This information maps **a single spec** to:

* a unique module filename
* the module file content

and is divided among four classes:

* a configuration class that provides a convenient interface to query
  details about the configuration for the spec under consideration.
* a layout class that provides the information associated with module
  file names and directories
* a context class that provides the dictionary used by the template engine
  to generate the module file
* a writer that collects and uses the information above to either write
  or remove the module file

Each of the four classes needs to be sub-classed when implementing a new
module type.
"""

import collections
import contextlib
import copy
import datetime
import itertools
import os
import pathlib
import re
import string
import warnings
from typing import IO, ClassVar, Dict, Iterator, List, NamedTuple, Optional, Tuple, Type, Union

import spack.vendor.jinja2

import spack.build_environment
import spack.compilers
import spack.compilers.config
import spack.config
import spack.deptypes as dt
import spack.environment
import spack.error
import spack.llnl.util.filesystem as fs
import spack.llnl.util.tty as tty
import spack.paths
import spack.projections as proj
import spack.schema
import spack.schema.environment
import spack.spec
import spack.store
import spack.tengine as tengine
import spack.user_environment
import spack.util.environment
import spack.util.file_permissions as fp
import spack.util.path
import spack.util.spack_yaml as syaml
from spack.aliases import BUILTIN_TO_LEGACY_COMPILER
from spack.enums import Context
from spack.llnl.util.lang import Singleton, dedupe, memoized

#: Valid tokens for naming scheme and env variable names
_valid_tokens = (
    "name",
    "version",
    "compiler",
    "compiler.name",
    "compiler.version",
    "architecture",
    # tokens from old-style format strings
    "package",
    "compilername",
    "compilerver",
)


_FORMAT_STRING_RE = re.compile(r"({[^}]*})")


def _format_env_var_name(spec: spack.spec.Spec, var_name_fmt: str) -> str:
    """Format the variable name, but uppercase any formatted fields."""
    fmt_parts = _FORMAT_STRING_RE.split(var_name_fmt)
    return "".join(
        spec.format(part).upper() if _FORMAT_STRING_RE.match(part) else part for part in fmt_parts
    )


def _check_tokens_are_valid(format_string: str, error_message: str) -> None:
    """Checks that the tokens used in the format string are valid.

    Args:
        format_string: template string for ``Spec.format`` that will be checked
        error_message: error message if invalid tokens are found
    """
    named_tokens = re.findall(r"{(\w*)}", format_string)
    invalid_tokens = [x for x in named_tokens if x.lower() not in _valid_tokens]
    if invalid_tokens:
        raise RuntimeError(
            f"{error_message} [{', '.join(invalid_tokens)}]. "
            f"Did you check your 'modules.yaml' configuration?"
        )


def update_dictionary_extending_lists(target: dict, update: dict) -> None:
    """Updates a dictionary, but extends lists instead of overriding them."""
    for key in update:
        value = target.get(key, None)
        if isinstance(value, list):
            target[key].extend(update[key])
        elif isinstance(value, dict):
            update_dictionary_extending_lists(target[key], update[key])
        else:
            target[key] = update[key]


def dependencies(spec: spack.spec.Spec, request: str = "all") -> List[spack.spec.Spec]:
    """Returns the list of dependencies for a given spec.

    Args:
        spec: spec to be analyzed
        request: one of ``"none"``, ``"run"``, ``"direct"``, ``"all"``
    """
    if request == "none":
        return []
    elif request == "run":
        return spec.dependencies(deptype=dt.RUN)
    elif request == "direct":
        return spec.dependencies(deptype=dt.RUN | dt.LINK)
    elif request == "all":
        return list(spec.traverse(order="topo", deptype=dt.LINK | dt.RUN, root=False))

    raise ValueError(f'request "{request}" is not one of "none", "direct", "run", "all"')


def _has_system_driver(compiler: spack.spec.Spec) -> bool:
    """Returns True if any of the compiler's C, C++, or Fortran drivers lives in a system dir."""
    for attr in ("cc", "cxx", "fc"):
        try:
            path = getattr(compiler.package, attr)
        except (KeyError, TypeError, AttributeError):
            continue
        if path and str(pathlib.Path(path).parent) in spack.util.environment.SYSTEM_DIRS:
            return True
    return False


def _store_core_compilers(
    module_set: str, module_system: str, core_compilers: List[spack.spec.Spec]
) -> None:
    """Writes a list of core compilers to the modules.yaml configuration file."""
    default_scope = spack.config.default_modify_scope()
    modules_cfg = spack.config.get(f"modules:{module_set}", {}, scope=default_scope)
    modules_cfg.setdefault(module_system, {})["core_compilers"] = [str(x) for x in core_compilers]
    spack.config.set(f"modules:{module_set}", modules_cfg, scope=default_scope)


def merge_config_rules(configuration: dict, spec: spack.spec.Spec) -> dict:
    """Parses the module specific part of a configuration and returns a dictionary containing the
    actions to be performed on the spec passed as an argument.

    Args:
        configuration: module specific configuration (e.g. entries under the top-level 'tcl' key)
        spec: spec for which we need to generate a module file
    """
    # The keyword 'all' is always evaluated first, all the others are evaluated in order of
    # appearance in the module file
    spec_configuration = copy.deepcopy(configuration.get("all", {}))
    for constraint, action in configuration.items():
        if spec.satisfies(constraint):
            if hasattr(constraint, "override") and constraint.override:
                spec_configuration = {}
            update_dictionary_extending_lists(spec_configuration, copy.deepcopy(action))

    for key, default in (("autoload", "direct"), ("prerequisites", "none")):
        dep_request = spec_configuration.get(key, default)
        spec_configuration[key] = dependencies(spec, request=dep_request)

    for key, default in (("hash_length", 7), ("verbose", False), ("defaults", [])):
        spec_configuration[key] = configuration.get(key, default)

    return spec_configuration


def root_path(module_type: str, module_set: str) -> str:
    """Returns the root folder for module file installation.

    Args:
        module_type: module type to be used
        module_set: name of the set of module configs to use
    """
    dir_name = "modules" if module_type == "tcl" else module_type
    fallback = os.path.join(spack.paths.share_path, dir_name)
    configured = spack.config.get(f"modules:{module_set}:roots", {})
    return spack.config.canonicalize_path(configured.get(module_type, fallback))


def generate_module_index(
    root: str, modules: List["BaseModuleFileWriter"], overwrite: bool = False
) -> None:
    entries = {}
    index_path = os.path.join(root, "module-index.yaml")
    if not overwrite and os.path.exists(index_path):
        with open(index_path, encoding="utf-8") as index_file:
            entries = syaml.load(index_file)["module_index"]

    for m in modules:
        entries[m.spec.dag_hash()] = {"path": m.layout.filename, "use_name": m.layout.use_name}

    fs.mkdirp(root)
    with open(index_path, "w", encoding="utf-8") as index_file:
        syaml.dump({"module_index": entries}, default_flow_style=False, stream=index_file)


def _generate_upstream_module_index() -> "UpstreamModuleIndex":
    module_indices = read_module_indices()
    return UpstreamModuleIndex(spack.store.STORE.db, module_indices)


upstream_module_index = Singleton(_generate_upstream_module_index)


class ModuleIndexEntry(NamedTuple):
    path: str
    use_name: str


def read_module_index(root: str) -> Dict[str, ModuleIndexEntry]:
    index_path = os.path.join(root, "module-index.yaml")
    if not os.path.exists(index_path):
        return {}
    with open(index_path, encoding="utf-8") as index_file:
        return _read_module_index(index_file)


def _read_module_index(str_or_file: IO[str]) -> Dict[str, ModuleIndexEntry]:
    """Read in the mapping of spec hash to module location/name. For a given
    Spack installation there is assumed to be (at most) one such mapping
    per module type."""
    yaml_content = syaml.load(str_or_file)
    index = {}
    yaml_index = yaml_content["module_index"]
    for dag_hash, module_properties in yaml_index.items():
        index[dag_hash] = ModuleIndexEntry(
            module_properties["path"], module_properties["use_name"]
        )
    return index


def read_module_indices() -> List[Dict[str, Dict[str, ModuleIndexEntry]]]:
    other_spack_instances = spack.config.get("upstreams") or {}

    module_indices = []

    for install_properties in other_spack_instances.values():
        module_type_to_index = {}
        module_type_to_root = install_properties.get("modules", {})
        for module_type, root in module_type_to_root.items():
            module_type_to_index[module_type] = read_module_index(root)
        module_indices.append(module_type_to_index)

    return module_indices


class UpstreamModuleIndex:
    """This is responsible for taking the individual module indices of all
    upstream Spack installations and locating the module for a given spec
    based on which upstream install it is located in."""

    def __init__(self, local_db, module_indices):
        self.local_db = local_db
        self.upstream_dbs = local_db.upstream_dbs
        self.module_indices = module_indices

    def upstream_module(
        self, spec: spack.spec.Spec, module_type: str
    ) -> Optional[ModuleIndexEntry]:
        db_for_spec = self.local_db.db_for_spec_hash(spec.dag_hash())
        if db_for_spec in self.upstream_dbs:
            db_index = self.upstream_dbs.index(db_for_spec)
        elif db_for_spec:
            raise spack.error.SpackError(f"Unexpected: {spec} is installed locally")
        else:
            raise spack.error.SpackError(f"Unexpected: no install DB found for {spec}")
        module_index = self.module_indices[db_index]
        module_type_index = module_index.get(module_type, {})
        if not module_type_index:
            tty.debug(
                f"No {module_type} modules associated with the Spack instance "
                f"where {spec} is installed"
            )
            return None
        if spec.dag_hash() in module_type_index:
            return module_type_index[spec.dag_hash()]
        else:
            tty.debug(f"No module is available for upstream package {spec}")
            return None


class BaseConfiguration:
    """Manipulates the information needed to generate a module file to make
    querying easier. It needs to be sub-classed for specific module types.
    """

    default_projections: Dict[str, str]

    compiler: Optional[spack.spec.Spec]

    #: Name of the module system (must be set by each subclass)
    module_system: str

    #: Default for the ``hierarchical`` config key when it is absent. Subclasses may override.
    _default_hierarchical: bool = False

    #: Per-subclass cache: must be assigned as ClassVar[Dict] = {} in each concrete subclass
    _registry: ClassVar[Dict[Tuple[str, str, bool], "BaseConfiguration"]]

    #: Layout class must be set on each concrete subclass
    layout_class: ClassVar[Type["BaseFileLayout"]]
    #: Context class must be set on each concrete subclass
    context_class: ClassVar[Type["BaseContext"]]

    @classmethod
    def configuration(cls, module_set_name: str) -> dict:
        """Returns the raw configuration dict for this module system."""
        return spack.config.get(f"modules:{module_set_name}:{cls.module_system}", {})

    @classmethod
    def make_configuration(
        cls, spec: spack.spec.Spec, module_set_name: str, explicit: Optional[bool] = None
    ) -> "BaseConfiguration":
        """Returns the cached configuration object for spec."""
        explicit = bool(spec._installed_explicitly()) if explicit is None else explicit
        key = (spec.dag_hash(), module_set_name, explicit)
        try:
            return cls._registry[key]
        except KeyError:
            return cls._registry.setdefault(key, cls(spec, module_set_name, explicit))

    @classmethod
    def make_layout(
        cls, spec: spack.spec.Spec, module_set_name: str, explicit: Optional[bool] = None
    ) -> "BaseFileLayout":
        return cls.layout_class(cls.make_configuration(spec, module_set_name, explicit))

    @classmethod
    def make_context(
        cls,
        spec: spack.spec.Spec,
        module_set_name: str,
        *,
        explicit: Optional[bool] = None,
        layout: "BaseFileLayout",
    ) -> "BaseContext":
        return cls.context_class(cls.make_configuration(spec, module_set_name, explicit), layout)

    def __init__(self, spec: spack.spec.Spec, module_set_name: str, explicit: bool) -> None:
        # Spec for which we want to generate a module file
        self.spec = spec
        self.name = module_set_name
        self.explicit = explicit
        # Cache once — configuration() traverses all config scopes on every call
        self._config = self.configuration(self.name)
        self.hierarchical: bool = self._config.get("hierarchical", self._default_hierarchical)
        # Dictionary of configuration options that should be applied to the spec
        self.conf = merge_config_rules(self._config, self.spec)

        self.default_projections = {"all": "{name}/{version}-{compiler.name}-{compiler.version}"}
        if self.hierarchical:
            self.default_projections = {"all": "{name}/{version}"}

        self.compiler = None
        self._core_compilers: Optional[List[spack.spec.Spec]] = None
        if self.hierarchical:
            candidates = collections.defaultdict(list)
            language_virtuals = ("c", "cxx", "fortran")

            for node in spec.traverse(deptype=("link", "run")):
                for language in language_virtuals:
                    candidates[language].extend(node.dependencies(virtuals=(language,)))

            for language in language_virtuals:
                if candidates[language]:
                    self.compiler = candidates[language][0]
                    if len(set(candidates[language])) > 1:
                        warnings.warn(
                            f"{spec.short_spec} uses more than one compiler, and might not fit "
                            f"the module hierarchy. Using {self.compiler.short_spec} as the "
                            "compiler."
                        )
                    break

    @property
    def projections(self) -> Dict[str, str]:
        """Projection from specs to module names"""
        # backwards compatibility for naming_scheme key
        conf = self._config
        if "naming_scheme" in conf:
            default = {"all": conf["naming_scheme"]}
        else:
            default = self.default_projections
        projections = conf.get("projections", default)

        # Ensure the named tokens we are expanding are allowed, see
        # issue #2884 for reference
        msg = "some tokens cannot be part of the module naming scheme"
        for projection in projections.values():
            _check_tokens_are_valid(projection, error_message=msg)

        return projections

    @property
    def template(self) -> Optional[str]:
        """Returns the name of the template to use for the module file
        or None if not specified in the configuration.
        """
        return self.conf.get("template", None)

    @property
    def defaults(self) -> List[str]:
        """Returns the specs configured as defaults or []."""
        return self.conf.get("defaults", [])

    @property
    def env(self) -> spack.util.environment.EnvironmentModifications:
        """List of environment modifications that should be done in the
        module.
        """
        return spack.schema.environment.parse(self.conf.get("environment", {}))

    @property
    def suffixes(self) -> List[str]:
        """List of suffixes that should be appended to the module
        file name.
        """
        suffixes = []
        for constraint, suffix in self.conf.get("suffixes", {}).items():
            if constraint in self.spec:
                suffixes.append(suffix)
        suffixes = list(dedupe(suffixes))
        # For hidden modules we can always add a fixed length hash as suffix, since it guards
        # against file name clashes, and the module is not exposed to the user anyways.
        if self.hidden:
            suffixes.append(self.spec.dag_hash(length=7))
        elif self.hash:
            suffixes.append(self.hash)
        return suffixes

    @property
    def hash(self) -> Optional[str]:
        """Hash tag for the module or None"""
        hash_length = self.conf.get("hash_length", 7)
        if hash_length != 0:
            return self.spec.dag_hash(length=hash_length)
        return None

    @property
    def conflicts(self) -> List[str]:
        """Conflicts for this module file"""
        return self.conf.get("conflict", [])

    @property
    def excluded(self) -> bool:
        """Returns True if the module has been excluded, False otherwise."""

        # A few variables for convenience of writing the method
        spec = self.spec
        conf = self._config

        # Compute the list of matching include / exclude rules, and whether excluded as implicit
        include_matches = [x for x in conf.get("include", []) if spec.satisfies(x)]
        exclude_matches = [x for x in conf.get("exclude", []) if spec.satisfies(x)]
        excluded_as_implicit = not self.explicit and conf.get("exclude_implicits", False)

        def debug_info(line_header: str, match_list: List[str]) -> None:
            if match_list:
                tty.debug(f"\t{line_header} : {spec.cshort_spec}")
                for rule in match_list:
                    tty.debug(f"\t\tmatches rule: {rule}")

        debug_info("INCLUDE", include_matches)
        debug_info("EXCLUDE", exclude_matches)

        if excluded_as_implicit:
            tty.debug(f"\tEXCLUDED_AS_IMPLICIT : {spec.cshort_spec}")

        return bool(not include_matches and (exclude_matches or excluded_as_implicit))

    @property
    def hidden(self) -> bool:
        """Returns True if the module has been hidden, False otherwise."""

        if self.hierarchical:
            # Never hide a module that opens a hierarchy
            if any(
                self.spec.name == x or self.spec.package.provides(x) for x in self.hierarchy_tokens
            ):
                return False

        conf = self._config

        hidden_as_implicit = not self.explicit and conf.get("hide_implicits", False)

        if hidden_as_implicit:
            tty.debug(f"\tHIDDEN_AS_IMPLICIT : {self.spec.cshort_spec}")

        return hidden_as_implicit

    @property
    def context(self) -> dict:
        return self.conf.get("context", {})

    @property
    def specs_to_load(self) -> List[spack.spec.Spec]:
        """List of specs that should be loaded in the module file."""
        return self._create_list_for("autoload")

    @property
    def literals_to_load(self) -> List[str]:
        """List of literal modules to be loaded."""
        return self.conf.get("load", [])

    @property
    def specs_to_prereq(self) -> List[spack.spec.Spec]:
        """List of specs that should be prerequisite of the module file."""
        return self._create_list_for("prerequisites")

    @property
    def exclude_env_vars(self) -> List[str]:
        """List of variables that should be left unmodified."""
        filter_subsection = self.conf.get("filter", {})
        return filter_subsection.get("exclude_env_vars", [])

    def _create_list_for(self, what: str) -> List[spack.spec.Spec]:
        include = []
        for item in self.conf[what]:
            if not self.make_configuration(item, self.name).excluded:
                include.append(item)
        return include

    @property
    def verbose(self) -> Optional[bool]:
        """Returns True if the module file needs to be verbose, False
        otherwise
        """
        return self.conf.get("verbose")

    @property
    def core_compilers(self) -> List[spack.spec.Spec]:
        """Returns the list of "Core" compilers

        Raises:
            CoreCompilersNotFoundError: if the key was not specified in the configuration file or
                the sequence is empty
        """
        if self._core_compilers is not None:
            return self._core_compilers

        compilers = []
        for c in self._config.get("core_compilers", []):
            compilers.extend(spack.spec.Spec(f"%{c}").dependencies())

        if not compilers:
            all_compilers = spack.compilers.config.all_compilers(init_config=False)
            compilers = [c for c in all_compilers if _has_system_driver(c)]
            if compilers:
                _store_core_compilers(self.name, self.module_system, compilers)

        if not compilers:
            msg = 'the key "core_compilers" must be set in modules.yaml'
            raise CoreCompilersNotFoundError(msg)

        self._core_compilers = compilers
        return self._core_compilers

    @property
    def core_specs(self) -> List[str]:
        """Returns the list of "Core" specs"""
        return self._config.get("core_specs", [])

    @property
    def filter_hierarchy_specs(self) -> Dict[str, List[str]]:
        """Returns the dict of specs with modified hierarchies"""
        return self._config.get("filter_hierarchy_specs", {})

    @property
    @memoized
    def hierarchy_tokens(self) -> List[str]:
        """Returns the list of tokens that are part of the modulefile
        hierarchy. ``compiler`` is always present.
        """
        configured = self._config.get("hierarchy", [])
        return list(dedupe(itertools.chain(configured, ["compiler"])))

    @property
    @memoized
    def requires(self) -> Dict[str, spack.spec.Spec]:
        """Returns a dictionary mapping all the requirements of this spec to the actual provider.

        The ``compiler`` key is always present among the requirements.

        Returns an empty dictionary if hierarchical mode is disabled.
        """
        if not self.hierarchical:
            return {}

        # If it's a core_spec, lie and say it requires a core compiler
        if any(self.spec.satisfies(core_spec) for core_spec in self.core_specs):
            return {"compiler": self.core_compilers[0]}

        hierarchy_filter_list = []
        for spec, filter_list in self.filter_hierarchy_specs.items():
            if self.spec.satisfies(spec):
                hierarchy_filter_list = filter_list
                break

        # Keep track of the requirements that this package has in terms
        # of virtual packages that participate in the hierarchical structure
        requirements = {"compiler": self.compiler or self.core_compilers[0]}

        # For each dependency in the hierarchy
        for x in self.hierarchy_tokens:
            # Skip anything filtered for this spec
            if x in hierarchy_filter_list:
                continue

            # If I depend on it
            if x in self.spec and not (self.spec.name == x or self.spec.package.provides(x)):
                requirements[x] = self.spec[x]  # record the actual provider
        return requirements

    @property
    def provides(self) -> Dict[str, spack.spec.Spec]:
        """Returns a dictionary mapping all the services provided by this
        spec to the spec itself.

        Returns an empty dictionary if hierarchical mode is disabled.
        """
        if not self.hierarchical:
            return {}

        provides = {}

        # Treat the 'compiler' case in a special way, as compilers are not
        # virtual dependencies in spack

        # If it is in the list of supported compilers family -> compiler
        if self.spec.name in spack.compilers.config.supported_compilers():
            provides["compiler"] = spack.spec.Spec(self.spec.format("{name}{@versions}"))
        elif self.spec.name in BUILTIN_TO_LEGACY_COMPILER:
            # If it is the package for a supported compiler, but of a different name
            cname = BUILTIN_TO_LEGACY_COMPILER[self.spec.name]
            provides["compiler"] = spack.spec.Spec(f"{cname}@{self.spec.versions}")

        # All the other tokens in the hierarchy must be virtual dependencies
        for x in self.hierarchy_tokens:
            if self.spec.name == x or self.spec.package.provides(x):
                provides[x] = self.spec
        return provides

    @property
    def available(self) -> Dict[str, spack.spec.Spec]:
        """Returns a dictionary of the services that are currently
        available.
        """
        available = {}
        # What is available is what I require plus what I provide.
        # 'compiler' is the only key that may be overridden.
        available.update(self.requires)
        available.update(self.provides)
        return available

    @property
    @memoized
    def missing(self) -> List[str]:
        """Returns the list of tokens that are not available."""
        return [x for x in self.hierarchy_tokens if x not in self.available]


class BaseFileLayout:
    """Provides information on the layout of module files. Needs to be
    sub-classed for specific module types.
    """

    #: This needs to be redefined
    extension: Optional[str] = None

    def __init__(self, configuration):
        self.conf = configuration

    @property
    def modulerc(self) -> str:
        raise NotImplementedError

    @property
    def spec(self) -> spack.spec.Spec:
        """Spec under consideration"""
        return self.conf.spec

    def dirname(self) -> str:
        """Root folder for module files of this type."""
        return root_path(self.conf.module_system, self.conf.name)

    @property
    def use_name(self) -> str:
        """Returns the 'use' name of the module i.e. the name you have to type
        to console to use it. This implementation fits the needs of most
        non-hierarchical layouts.
        """
        projection = proj.get_projection(self.conf.projections, self.spec)
        if not projection:
            projection = self.conf.default_projections["all"]

        name = self.spec.format_path(projection)
        # Not everybody is working on linux...
        parts = name.split("/")
        name = os.path.join(*parts)
        # Add optional suffixes based on constraints
        path_elements = [name]
        path_elements.extend(map(self.spec.format, self.conf.suffixes))
        return "-".join(path_elements)

    @property
    def arch_dirname(self) -> str:
        """Returns the root folder for THIS architecture"""
        # Architecture sub-folder
        arch_folder_conf = spack.config.get("modules:%s:arch_folder" % self.conf.name, True)
        if arch_folder_conf:
            # include an arch specific folder between root and filename
            if self.conf.hierarchical:
                arch_folder = "-".join(
                    [str(self.spec.platform), str(self.spec.os), str(self.spec.target.family)]
                )
            else:
                arch_folder = str(self.spec.architecture)
            return os.path.join(self.dirname(), arch_folder)
        return self.dirname()

    @property
    def filename(self) -> str:
        """Name of the module file for the current spec."""
        # Just the name of the file
        filename = self.use_name
        if self.extension:
            filename = f"{self.use_name}.{self.extension}"

        if self.conf.hierarchical:
            # Get the list of requirements and build an **ordered**
            # list of the path parts
            requires = self.conf.requires
            hierarchy = self.conf.hierarchy_tokens
            path_parts = lambda x: self.token_to_path(x, requires[x])
            parts = [path_parts(x) for x in hierarchy if x in requires]

            if not parts:
                raise ModulesError(
                    f"{self.spec.short_spec}: hierarchical module has no resolved requirements; "
                    "cannot construct the module file path"
                )
            filename = os.path.join(*parts, filename)

        # Return the absolute path
        return os.path.join(self.arch_dirname, filename)

    def token_to_path(self, name: str, value: spack.spec.Spec) -> str:
        """Transforms a hierarchy token into the corresponding path part.

        Args:
            name (str): name of the service in the hierarchy
            value: actual provider of the service

        Returns:
            str: part of the path associated with the service
        """

        # General format for the path part
        def path_part_fmt(token: spack.spec.Spec) -> str:
            return fs.polite_path([f"{token.name}", f"{token.version}"])

        # If we are dealing with a core compiler, return 'Core'
        core_compilers = self.conf.core_compilers
        if name == "compiler" and any(value.satisfies(c) for c in core_compilers):
            return "Core"

        # Spec does not have a hash, as we are not allowed to
        # use different flavors of the same compiler
        if name == "compiler":
            return path_part_fmt(token=value)

        # In case the hierarchy token refers to a virtual provider
        # we need to append a hash to the version to distinguish
        # among flavors of the same library (e.g. openblas~openmp vs.
        # openblas+openmp)
        return f"{path_part_fmt(token=value)}-{value.dag_hash(length=7)}"

    @property
    def available_path_parts(self) -> List[str]:
        """List of path parts that are currently available. Needed to
        construct the file name.
        """
        available = self.conf.available
        requires = self.conf.requires
        provides = self.conf.provides
        hierarchy = self.conf.hierarchy_tokens
        parts = []
        for x in hierarchy:
            if x not in available:
                continue
            # A spec that provides hierarchy token X (e.g. a compiler) is placed in the directory
            # corresponding to what it *requires* for X, not what it provides.
            # For instance gcc@12 built with a core compiler belongs in Core/, not Compiler/gcc/12/
            if x in provides and x in requires:
                parts.append(self.token_to_path(x, requires[x]))
            else:
                parts.append(self.token_to_path(x, available[x]))
        return parts

    @property
    @memoized
    def unlocked_paths(self) -> Dict[Optional[Tuple[str, ...]], List[Tuple[str, ...]]]:
        """Returns a dictionary mapping conditions to a list of unlocked
        paths.

        The paths that are unconditionally unlocked are under the
        key 'None'. The other keys represent the list of services you need
        loaded to unlock the corresponding paths.
        """

        unlocked: Dict[Optional[Tuple[str, ...]], List[Tuple[str, ...]]] = collections.defaultdict(
            list
        )

        # Get the list of services we require and we provide
        requires_key = list(self.conf.requires)
        provides_key = list(self.conf.provides)

        # A compiler is always required. To avoid duplication pop the
        # 'compiler' item from required if we also **provide** one
        if "compiler" in provides_key:
            requires_key.remove("compiler")

        # Compute the unique combinations of the services we provide
        combinations: List[Tuple[str, ...]] = []
        for ii in range(len(provides_key)):
            combinations += itertools.combinations(provides_key, ii + 1)

        # Attach the services required to each combination
        to_be_processed = [x + tuple(requires_key) for x in combinations]

        # Compute the paths that are unconditionally added
        # and append them to the dictionary (key = None)
        available_combination = []
        for item in to_be_processed:
            hierarchy = self.conf.hierarchy_tokens
            available = self.conf.available
            ac = [x for x in hierarchy if x in item]
            available_combination.append(tuple(ac))
            parts = [self.token_to_path(x, available[x]) for x in ac]
            unlocked[None].append(tuple([self.arch_dirname] + parts))

        # Deduplicate the list
        unlocked[None] = list(dedupe(unlocked[None]))

        # Compute the combination of missing requirements: this will lead to
        # paths that are unlocked conditionally
        missing = self.conf.missing

        missing_combinations: List[Tuple[str, ...]] = []
        for ii in range(len(missing)):
            missing_combinations += itertools.combinations(missing, ii + 1)

        # Attach the services required to each combination
        for m in missing_combinations:
            to_be_processed = [m + x for x in available_combination]
            for item in to_be_processed:
                hierarchy = self.conf.hierarchy_tokens
                available = self.conf.available
                token2path = lambda x: self.token_to_path(x, available[x])
                parts = []
                for x in hierarchy:
                    if x not in item:
                        continue
                    value = token2path(x) if x in available else x
                    parts.append(value)
                unlocked[m].append(tuple([self.arch_dirname] + parts))
            # Deduplicate the list
            unlocked[m] = list(dedupe(unlocked[m]))
        return unlocked


class BaseContext(tengine.Context):
    """Provides the base context needed for template rendering.

    This class needs to be sub-classed for specific module types. The
    following attributes need to be implemented:

    - fields

    """

    def __init__(self, configuration, layout: "BaseFileLayout") -> None:
        self.conf = configuration
        self.layout = layout

    @tengine.context_property
    def spec(self) -> spack.spec.Spec:
        return self.conf.spec

    @tengine.context_property
    def tags(self) -> List[str]:
        if not hasattr(self.spec.package, "tags"):
            return []
        return self.spec.package.tags

    @tengine.context_property
    def timestamp(self) -> datetime.datetime:
        return datetime.datetime.now()

    @tengine.context_property
    def category(self) -> str:
        return getattr(self.spec, "category", "spack")

    @tengine.context_property
    def short_description(self) -> str:
        # If we have a valid docstring return the first paragraph.
        docstring = type(self.spec.package).__doc__
        if docstring:
            value = docstring.split("\n\n")[0]
            # Transform tabs and friends into spaces
            value = re.sub(r"\s+", " ", value)
            # Turn double quotes into single quotes (double quotes are needed
            # to start and end strings)
            value = re.sub(r'"', "'", value)
            return value
        # Otherwise the short description is just the package + version
        return self.spec.format("{name} {@version}")

    @tengine.context_property
    def long_description(self) -> Optional[str]:
        # long description is the docstring with reduced whitespace.
        if self.spec.package.__doc__:
            return re.sub(r"\s+", " ", self.spec.package.__doc__)
        return None

    @tengine.context_property
    def configure_options(self) -> Optional[str]:
        pkg = self.spec.package

        # If the spec is external Spack doesn't know its configure options
        if self.spec.external:
            msg = "unknown, software installed outside of Spack"
            return msg

        if os.path.exists(pkg.install_configure_args_path):
            with open(pkg.install_configure_args_path, encoding="utf-8") as args_file:
                return spack.util.path.padding_filter(args_file.read())

        # Returning a false-like value makes the default templates skip
        # the configure option section
        return None

    def modification_needs_formatting(
        self,
        modification: Union[
            spack.util.environment.NameModifier, spack.util.environment.NameValueModifier
        ],
    ) -> bool:
        """Returns True if environment modification entry needs to be formatted."""
        return (
            not isinstance(modification, (spack.util.environment.SetEnv)) or not modification.raw
        )

    @tengine.context_property
    @memoized
    def environment_modifications(
        self,
    ) -> List[
        Tuple[
            str,
            Union[spack.util.environment.NameModifier, spack.util.environment.NameValueModifier],
        ]
    ]:
        """List of environment modifications to be processed."""
        # Modifications guessed by inspecting the spec prefix
        prefix_inspections = syaml.syaml_dict()
        spack.schema.merge_yaml(
            prefix_inspections, spack.config.get("modules:prefix_inspections", {})
        )
        spack.schema.merge_yaml(
            prefix_inspections,
            spack.config.get(f"modules:{self.conf.name}:prefix_inspections", {}),
        )

        use_view = spack.config.get(f"modules:{self.conf.name}:use_view", False)

        assert isinstance(use_view, (bool, str))

        if use_view:
            spack_env = spack.environment.active_environment()
            if not spack_env:
                raise spack.environment.SpackEnvironmentViewError(
                    "Module generation with views requires active environment"
                )

            view_name = spack.environment.default_view_name if use_view is True else use_view

            if not spack_env.has_view(view_name):
                raise spack.environment.SpackEnvironmentViewError(
                    f"View {view_name} not found in environment {spack_env.name}"
                    " when generating modules"
                )

            view = spack_env.views[view_name]
        else:
            view = None

        env = spack.util.environment.inspect_path(
            self.spec.prefix, prefix_inspections, exclude=spack.util.environment.is_system_path
        )

        # Let the extendee/dependency modify their extensions/dependencies

        # The only thing we care about is `setup_dependent_run_environment`, but
        # for that to work, globals have to be set on the package modules, and the
        # whole chain of setup_dependent_package has to be followed from leaf to spec.
        # So: just run it here, but don't collect env mods.
        spack.build_environment.SetupContext(
            self.spec, context=Context.RUN
        ).set_all_package_py_globals()

        # Then run setup_dependent_run_environment before setup_run_environment.
        for dep in self.spec.dependencies(deptype=("link", "run")):
            dep.package.setup_dependent_run_environment(env, self.spec)
        self.spec.package.setup_run_environment(env)

        # Project the environment variables from prefix to view if needed
        if view and self.spec in view:
            spack.user_environment.project_env_mods(
                *self.spec.traverse(deptype=dt.LINK | dt.RUN), view=view, env=env
            )

        # Modifications required from modules.yaml
        env.extend(self.conf.env)

        # List of variables that are excluded in modules.yaml
        exclude = self.conf.exclude_env_vars

        # We may have tokens to substitute in environment commands
        for x in env:
            # Ensure all the tokens are valid in this context
            msg = "some tokens cannot be expanded in an environment variable name"

            _check_tokens_are_valid(x.name, error_message=msg)
            x.name = _format_env_var_name(self.spec, x.name)
            if self.modification_needs_formatting(x):
                try:
                    # Not every command has a value
                    x.value = self.spec.format(x.value)
                except AttributeError:
                    pass
            x.name = str(x.name).replace("-", "_")

        return [(type(x).__name__, x) for x in env if x.name not in exclude]

    @tengine.context_property
    def has_manpath_modifications(self) -> bool:
        """True if MANPATH environment variable is modified."""
        for modification_type, cmd in self.environment_modifications:
            if not isinstance(
                cmd, (spack.util.environment.PrependPath, spack.util.environment.AppendPath)
            ):
                continue
            if cmd.name == "MANPATH":
                return True
        else:
            return False

    @tengine.context_property
    def conflicts(self) -> List[str]:
        """List of conflicts for the module file."""
        fmts = []
        projection = proj.get_projection(self.conf.projections, self.spec)
        for item in self.conf.conflicts:
            self._verify_conflict_naming_consistency_or_raise(item, projection)
            item = self.spec.format(item)
            fmts.append(item)
        return fmts

    def _verify_conflict_naming_consistency_or_raise(self, item: str, projection: str) -> None:
        f = string.Formatter()
        errors = []
        if len([x for x in f.parse(item)]) > 1:
            for naming_dir, conflict_dir in zip(projection.split("/"), item.split("/")):
                if naming_dir != conflict_dir:
                    errors.extend(
                        [
                            f"spec={self.spec.cshort_spec}",
                            f"conflict_scheme={item}",
                            f"naming_scheme={projection}",
                        ]
                    )
        if errors:
            raise ModulesError(
                message="conflict scheme does not match naming scheme",
                long_message="\n    ".join(errors),
            )

    @tengine.context_property
    def autoload(self) -> List[str]:
        """List of modules that needs to be loaded automatically."""
        # From 'autoload' configuration option
        specs = self._create_module_list_of("specs_to_load")
        # From 'load' configuration option
        literals = self.conf.literals_to_load
        return specs + literals

    def _create_module_list_of(self, what: str) -> List[str]:
        name = self.conf.name
        return [self.conf.make_layout(x, name).use_name for x in getattr(self.conf, what)]

    @tengine.context_property
    def verbose(self) -> Optional[bool]:
        """Verbosity level."""
        return self.conf.verbose

    @tengine.context_property
    def has_modulepath_modifications(self) -> bool:
        """True if this module modifies MODULEPATH, False otherwise."""
        return bool(self.conf.provides)

    @tengine.context_property
    def has_conditional_modifications(self) -> bool:
        """True if this module modifies MODULEPATH conditionally to the
        presence of other services in the environment, False otherwise.
        """
        # In general we have conditional modifications if we have modifications
        # and we are not providing **only** a compiler
        provides = self.conf.provides
        provide_compiler_only = "compiler" in provides and len(provides) == 1
        has_modifications = self.has_modulepath_modifications
        return has_modifications and not provide_compiler_only

    @tengine.context_property
    def name_part(self) -> str:
        """Name of this provider."""
        return self.spec.name

    @tengine.context_property
    def version_part(self) -> str:
        """Version of this provider."""
        s = self.spec
        return "-".join([str(s.version), s.dag_hash(length=7)])

    @tengine.context_property
    def provides(self) -> Dict[str, spack.spec.Spec]:
        """Returns the dictionary of provided services."""
        return self.conf.provides

    @tengine.context_property
    def missing(self) -> List[str]:
        """Returns a list of missing services."""
        return self.conf.missing

    @tengine.context_property
    def unlocked_paths(self) -> List[str]:
        """Returns the list of paths that are unlocked unconditionally."""
        return [os.path.join(*parts) for parts in self.layout.unlocked_paths[None]]

    def _manipulate_path(self, token: str) -> str:
        raise NotImplementedError

    def _format_condition(self, services_needed: Tuple[str, ...]) -> str:
        raise NotImplementedError

    def _join_path(self, parts: Tuple[str, ...]) -> str:
        raise NotImplementedError

    @tengine.context_property
    def conditionally_unlocked_paths(self) -> List[Tuple[str, str]]:
        """Returns the list of paths that are unlocked conditionally.
        Each item in the list is a tuple with the structure (condition, path).
        """
        value: List[Tuple[str, str]] = []
        for services_needed, list_of_path_parts in self.layout.unlocked_paths.items():
            if services_needed is None:
                continue
            condition = self._format_condition(services_needed)
            for parts in list_of_path_parts:
                value.append((condition, self._join_path(parts)))
        return value


class ModulesError(spack.error.SpackError):
    """Base error for modules."""


class ModuleNotFoundError(ModulesError):
    """Raised when a module cannot be found for a spec"""


class DefaultTemplateNotDefined(AttributeError, ModulesError):
    """Raised if the attribute ``default_template`` has not been specified
    in the derived classes.
    """


class HideCmdFormatNotDefined(AttributeError, ModulesError):
    """Raised if the attribute ``hide_cmd_format`` has not been specified
    in the derived classes.
    """


class ModulercHeaderNotDefined(AttributeError, ModulesError):
    """Raised if the attribute ``modulerc_header`` has not been specified
    in the derived classes.
    """


class BaseModuleFileWriter:
    default_template: str
    hide_cmd_format: str
    modulerc_header: List[str]

    configuration_class: ClassVar[Type["BaseConfiguration"]]

    _required_attrs = (
        ("default_template", DefaultTemplateNotDefined),
        ("hide_cmd_format", HideCmdFormatNotDefined),
        ("modulerc_header", ModulercHeaderNotDefined),
    )

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        for attr, exc_type in BaseModuleFileWriter._required_attrs:
            if not hasattr(cls, attr):
                raise exc_type(
                    f"'{cls.__name__}' object has no attribute '{attr}'\n"
                    "Did you forget to define it in the class?"
                )

    def __init__(
        self, spec: spack.spec.Spec, module_set_name: str, explicit: Optional[bool] = None
    ) -> None:
        self.spec = spec

        # Create the triplet of configuration/layout/context
        self.conf = self.configuration_class.make_configuration(spec, module_set_name, explicit)
        self.layout = self.conf.make_layout(spec, module_set_name, explicit)
        self.context = self.conf.make_context(
            spec, module_set_name, explicit=explicit, layout=self.layout
        )

    def _get_template(self) -> str:
        """Gets the template that will be rendered for this spec."""
        # Get templates and put them in the order of importance:
        # 1. template specified in "modules.yaml"
        # 2. template specified in a package directly
        # 3. default template (must be defined, check in __init__)
        package_attribute = f"{self.conf.module_system}_template"
        for candidate in [
            self.conf.template,
            getattr(self.spec.package, package_attribute, None),
            self.default_template,  # This is always defined at this point
        ]:
            if candidate:
                return candidate
        return self.default_template

    def write(self, overwrite: bool = False) -> None:
        """Writes the module file.

        Args:
            overwrite (bool): if True it is fine to overwrite an already
                existing file. If False the operation is skipped an we print
                a warning to the user.
        """
        # Return immediately if the module is excluded
        if self.conf.excluded:
            msg = "\tNOT WRITING: {0} [EXCLUDED]"
            tty.debug(msg.format(self.spec.cshort_spec))
            return

        # Print a warning in case I am accidentally overwriting
        # a module file that is already there (name clash)
        if not overwrite and os.path.exists(self.layout.filename):
            message = "Module file {0.filename} exists and will not be overwritten"
            tty.warn(message.format(self.layout))
            return

        # If we are here it means it's ok to write the module file
        msg = "\tWRITE: {0} [{1}]"
        tty.debug(msg.format(self.spec.cshort_spec, self.layout.filename))

        # If the directory where the module should reside does not exist
        # create it
        module_dir = os.path.dirname(self.layout.filename)
        if not os.path.exists(module_dir):
            fs.mkdirp(module_dir)

        # Get the template for the module
        template_name = self._get_template()

        try:
            env = tengine.make_environment()
            template = env.get_template(template_name)
        except spack.vendor.jinja2.TemplateNotFound:
            # If the template was not found raise an exception with a little
            # more information
            msg = "template '{0}' was not found for '{1}'"
            name = type(self).__name__
            msg = msg.format(template_name, name)
            raise ModulesTemplateNotFoundError(msg)

        # Construct the context following the usual hierarchy of updates:
        # 1. start with the default context from the module writer class
        # 2. update with package specific context
        # 3. update with 'modules.yaml' specific context

        context = self.context.to_dict()

        # Attribute from package
        attr_name = f"{self.conf.module_system}_context"
        pkg_update = getattr(self.spec.package, attr_name, {})
        context.update(pkg_update)

        # Context key in modules.yaml
        conf_update = self.conf.context
        context.update(conf_update)

        # Render the template
        text = template.render(context)
        # Write it to file
        with open(self.layout.filename, "w", encoding="utf-8") as f:
            f.write(text)

        # Set the file permissions of the module to match that of the package
        if os.path.exists(self.layout.filename):
            fp.set_permissions_by_spec(self.layout.filename, self.spec)

        # Symlink defaults if needed
        self.update_module_defaults()

        # record module hiddenness if implicit
        self.update_module_hiddenness()

    def update_module_defaults(self) -> None:
        if any(self.spec.satisfies(default) for default in self.conf.defaults):
            # This spec matches a default, it needs to be symlinked to default
            # Symlink to a tmp location first and move, so that existing
            # symlinks do not cause an error.
            default_path = os.path.join(os.path.dirname(self.layout.filename), "default")
            default_tmp = os.path.join(os.path.dirname(self.layout.filename), ".tmp_spack_default")
            os.symlink(self.layout.filename, default_tmp)
            os.rename(default_tmp, default_path)

    def update_module_hiddenness(self, remove: bool = False) -> None:
        """Update modulerc file corresponding to module to add or remove
        command that hides module depending on its hidden state.

        Args:
            remove (bool): if True, hiddenness information for module is
                removed from modulerc.
        """
        modulerc_path = self.layout.modulerc
        hide_module_cmd = self.hide_cmd_format % self.layout.use_name
        hidden = self.conf.hidden and not remove
        modulerc_exists = os.path.exists(modulerc_path)
        updated = False

        if modulerc_exists:
            # retrieve modulerc content
            with open(modulerc_path, encoding="utf-8") as f:
                content = f.readlines()
                content = "".join(content).split("\n")
                # remove last empty item if any
                if len(content[-1]) == 0:
                    del content[-1]
            already_hidden = hide_module_cmd in content

            # remove hide command if module not hidden
            if already_hidden and not hidden:
                content.remove(hide_module_cmd)
                updated = True

            # add hide command if module is hidden
            elif not already_hidden and hidden:
                if len(content) == 0:
                    content = self.modulerc_header.copy()
                content.append(hide_module_cmd)
                updated = True
        else:
            content = self.modulerc_header.copy()
            if hidden:
                content.append(hide_module_cmd)
                updated = True

        # no modulerc file change if no content update
        if updated:
            is_empty = content == self.modulerc_header or len(content) == 0
            # remove existing modulerc if empty
            if modulerc_exists and is_empty:
                os.remove(modulerc_path)
            # create or update modulerc
            elif content != self.modulerc_header:
                # ensure file ends with a newline character
                content.append("")
                with open(modulerc_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(content))

    def remove(self) -> None:
        """Deletes the module file."""
        mod_file = self.layout.filename
        if os.path.exists(mod_file):
            try:
                os.remove(mod_file)  # Remove the module file
                self.remove_module_defaults()  # Remove default targeting module file
                self.update_module_hiddenness(remove=True)  # Remove hide cmd in modulerc
                os.removedirs(
                    os.path.dirname(mod_file)
                )  # Remove all the empty directories from the leaf up
            except OSError:
                # removedirs throws OSError on first non-empty directory found
                pass

    def remove_module_defaults(self) -> None:
        if not any(self.spec.satisfies(default) for default in self.conf.defaults):
            return

        # This spec matches a default, symlink needs to be removed as we remove the module
        # file it targets.
        default_symlink = os.path.join(os.path.dirname(self.layout.filename), "default")
        try:
            os.unlink(default_symlink)
        except OSError:
            pass


@contextlib.contextmanager
def disable_modules() -> Iterator[None]:
    """Disable the generation of modulefiles within the context manager."""
    data: Dict[str, object] = {"modules:": {"default": {"enable": []}}}
    disable_scope = spack.config.InternalConfigScope("disable_modules", data=data)
    with spack.config.override(disable_scope):
        yield


class ModulesTemplateNotFoundError(ModulesError, RuntimeError):
    """Raised if the template for a module file was not found."""


class CoreCompilersNotFoundError(spack.error.SpackError, KeyError):
    """Error raised if the key ``core_compilers`` has not been specified
    in the configuration file.
    """
