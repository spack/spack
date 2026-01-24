# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import functools
from typing import Any, Callable, Dict, List, Set, Tuple, Type, Union

import spack.error
import spack.repo
import spack.spec
from spack.llnl.util.lang import dedupe

#: Names of possible directives. This list is mostly populated using the @directive decorator.
#: Some directives leverage others and in that case are not automatically added.
directive_names = ["build_system"]

SPEC_CACHE: Dict[str, spack.spec.Spec] = {}


def get_spec(spec_str: str) -> spack.spec.Spec:
    """Get a spec from the cache, or create it if not present."""
    if spec_str not in SPEC_CACHE:
        SPEC_CACHE[spec_str] = spack.spec._ImmutableSpec(spec_str)
    return SPEC_CACHE[spec_str]


class DirectiveMeta(type):
    """Flushes the directives that were temporarily stored in the staging
    area into the package.
    """

    #: Registry of {directive_name: [list_of_dicts_it_modifies]} populated by @directive
    _directive_to_dicts: Dict[str, Tuple[str, ...]] = {}
    #: Inverted index of {dict_name: [list_of_directives_modifying_it]}
    _dict_to_directives: Dict[str, List[str]] = collections.defaultdict(list)
    #: Maps dictionary name to its descriptor instance
    _descriptor_cache: Dict[str, "DirectiveDictDescriptor"] = {}
    #: Set of all known directive dictionary names from `@directive(dicts=...)`
    _directive_dict_names: Set[str] = set()
    #: Lists of directives to be executed for the class being defined, grouped by directive
    #: function name (e.g. "depends_on", "version", etc.)
    _directives_to_be_executed: Dict[str, List[Callable]] = collections.defaultdict(list)
    #: Stack of when constraints from `with when(...)` context managers
    _when_constraints_stack: List[str] = []
    #: Stack of default args from `with default_args(...)` context managers
    _default_args_stack: List[dict] = []
    #: This property is set *automatically* during class definition as directives are invoked,
    #: if any ``depends_on`` or ``extends`` calls include patches for dependencies. This flag can
    #: be used as an optimization to detect whether a package provides patches for dependencies,
    #: without triggering the expensive deferred execution of those directives (without populating
    #: the ``dependencies`` dictionary).
    _patches_dependencies: bool = False

    def __new__(
        cls: Type["DirectiveMeta"], name: str, bases: tuple, attr_dict: dict
    ) -> "DirectiveMeta":
        attr_dict["_patches_dependencies"] = DirectiveMeta._patches_dependencies
        # Initialize the attribute containing the list of directives to be executed. Here we go
        # reversed because we want to execute commands in the order they were defined, following
        # the MRO.
        merged: Dict[str, List[Callable]] = {}
        sources = [getattr(b, "_directives_to_be_executed", None) or {} for b in reversed(bases)]
        for source in sources:
            for key, directive_list in source.items():
                merged.setdefault(key, []).extend(directive_list)

        merged = {key: list(dedupe(directive_list)) for key, directive_list in merged.items()}

        # Add current class's directives (no deduplication needed here)
        for key, directive_list in DirectiveMeta._directives_to_be_executed.items():
            merged.setdefault(key, []).extend(directive_list)

        attr_dict["_directives_to_be_executed"] = merged

        DirectiveMeta._directives_to_be_executed.clear()
        DirectiveMeta._patches_dependencies = False

        # Add descriptors for all known directive dictionaries
        for dict_name in DirectiveMeta._directive_dict_names:
            # Where the actual data will be stored
            attr_dict[f"_{dict_name}"] = None
            # Descriptor to lazily initialize and populate the dictionary
            attr_dict[dict_name] = DirectiveMeta._get_descriptor(dict_name)

        return super(DirectiveMeta, cls).__new__(cls, name, bases, attr_dict)

    def __init__(cls: "DirectiveMeta", name: str, bases: tuple, attr_dict: dict):
        if spack.repo.is_package_module(cls.__module__):
            # Historically, maintainers was not a directive. They were simply set as class
            # attributes `maintainers = ["alice", "bob"]`. Therefore, we execute these directives
            # eagerly.
            for directive in cls._directives_to_be_executed.get("maintainers", ()):
                directive(cls)
        super(DirectiveMeta, cls).__init__(name, bases, attr_dict)

    @staticmethod
    def register_directive(name: str, dicts: Tuple[str, ...]) -> None:
        """Called by @directive to register relationships."""
        DirectiveMeta._directive_to_dicts[name] = dicts
        for d in dicts:
            DirectiveMeta._dict_to_directives[d].append(name)

    @staticmethod
    def _get_descriptor(name: str) -> "DirectiveDictDescriptor":
        """Returns a singleton descriptor for the given dictionary name."""
        if name not in DirectiveMeta._descriptor_cache:
            DirectiveMeta._descriptor_cache[name] = DirectiveDictDescriptor(name)
        return DirectiveMeta._descriptor_cache[name]

    @staticmethod
    def push_when_constraint(when_spec: str) -> None:
        """Add a spec to the context constraints."""
        DirectiveMeta._when_constraints_stack.append(when_spec)

    @staticmethod
    def pop_when_constraint() -> str:
        """Pop the last constraint from the context"""
        return DirectiveMeta._when_constraints_stack.pop()

    @staticmethod
    def push_default_args(default_args: Dict[str, Any]) -> None:
        """Push default arguments"""
        DirectiveMeta._default_args_stack.append(default_args)

    @staticmethod
    def pop_default_args() -> dict:
        """Pop default arguments"""
        return DirectiveMeta._default_args_stack.pop()

    @staticmethod
    def _remove_kwarg_value_directives_from_queue(value) -> None:
        """Remove directives found in a kwarg value from the execution queue."""
        # Certain keyword argument values of directives may themselves be (lists of) directives. An
        # example of this is ``depends_on(..., patches=[patch(...), ...])``. In that case, we
        # should not execute those directives as part of the current package, but let the called
        # directive handle them. This function removes such directives from the execution queue.
        if isinstance(value, (list, tuple)):
            for item in value:
                DirectiveMeta._remove_kwarg_value_directives_from_queue(item)
        elif callable(value):  # directives are always callable
            # Remove directives args from the exec queue
            for lst in DirectiveMeta._directives_to_be_executed.values():
                for directive in lst:
                    if value is directive:
                        lst.remove(directive)  # iterations ends, so mutation is fine
                        break

    @staticmethod
    def _get_execution_plan(target_dict: str) -> Tuple[List[str], List[str]]:
        """Calculates the closure of dicts and directives needed to populate target_dict."""
        dicts_involved = {target_dict}
        directives_involved = set()
        stack = [target_dict]

        while stack:
            current_dict = stack.pop()

            for directive_name in DirectiveMeta._dict_to_directives.get(current_dict, ()):
                if directive_name in directives_involved:
                    continue

                directives_involved.add(directive_name)

                for other_dict in DirectiveMeta._directive_to_dicts[directive_name]:
                    if other_dict not in dicts_involved:
                        dicts_involved.add(other_dict)
                        stack.append(other_dict)

        return sorted(dicts_involved), sorted(directives_involved)


class DirectiveDictDescriptor:
    """A descriptor that lazily executes directives on first access."""

    def __init__(self, name: str):
        self.name = name
        self.private_name = f"_{name}"
        self.dicts_to_init, self.directives_to_run = DirectiveMeta._get_execution_plan(name)

    def __get__(self, obj, objtype=None):
        val = getattr(objtype, self.private_name)
        if val is not None:
            return val

        # The None value is a sentinel for "not yet initialized".
        for dictionary in self.dicts_to_init:
            if getattr(objtype, f"_{dictionary}") is None:
                setattr(objtype, f"_{dictionary}", {})

        # Populate these dictionaries by running all directives that modify them
        for directive_name in self.directives_to_run:
            directives = objtype._directives_to_be_executed.get(directive_name)
            if directives:
                for directive in directives:
                    directive(objtype)

        return getattr(objtype, self.private_name)


class directive:
    def __init__(
        self,
        dicts: Union[Tuple[str, ...], str] = (),
        supports_when: bool = True,
        can_patch_dependencies: bool = False,
    ) -> None:
        """Decorator for Spack directives.

        Spack directives allow you to modify a package while it is being defined, e.g. to add
        version or dependency information.  Directives are one of the key pieces of Spack's
        package "language", which is embedded in python.

        Here's an example directive::

            @directive(dicts="versions")
            def version(pkg, ...):
                ...

        This directive allows you write::

            class Foo(Package):
                version(...)

        The ``@directive`` decorator handles a couple things for you:

        1. Adds the class scope (pkg) as an initial parameter when called, like a class method
           would. This allows you to modify a package from within a directive, while the package is
           still being defined.

        2. It automatically adds a dictionary called ``versions`` to the package so that you can
           refer to pkg.versions.

        Arguments:
            dicts: A tuple of names of dictionaries to add to the package class if they don't
                already exist.
            supports_when: If True, the directive can be used within a ``with when(...)`` context
                manager. (To be removed when all directives support ``when=`` arguments.)
            can_patch_dependencies: If True, the directive can patch dependencies. This is used to
                identify nested directives so they can be removed from the execution queue, and to
                mark the package as patching dependencies.
        """

        if isinstance(dicts, str):
            dicts = (dicts,)

        # Add the dictionary names if not already there
        DirectiveMeta._directive_dict_names.update(dicts)

        self.supports_when = supports_when
        self.can_patch_dependencies = can_patch_dependencies
        self.dicts = tuple(dicts)

    def __call__(self, decorated_function: Callable) -> Callable:
        directive_names.append(decorated_function.__name__)
        DirectiveMeta.register_directive(decorated_function.__name__, self.dicts)

        @functools.wraps(decorated_function)
        def _wrapper(*args, **_kwargs):
            # First merge default args with kwargs
            if DirectiveMeta._default_args_stack:
                kwargs = {}
                for default_args in DirectiveMeta._default_args_stack:
                    kwargs.update(default_args)
                kwargs.update(_kwargs)
            else:
                kwargs = _kwargs

            # Inject when arguments from the `with when(...)` stack.
            if DirectiveMeta._when_constraints_stack:
                if not self.supports_when:
                    raise DirectiveError(
                        f'directive "{decorated_function.__name__}" cannot be used within a '
                        '"when" context since it does not support a "when=" argument'
                    )
                if "when" in kwargs:
                    kwargs["when"] = (*DirectiveMeta._when_constraints_stack, kwargs["when"])
                else:
                    kwargs["when"] = tuple(DirectiveMeta._when_constraints_stack)

            # Remove directives passed as arguments, so they are not executed as part of this
            # class's directive execution, but handled by the called directive instead
            if self.can_patch_dependencies and "patches" in kwargs:
                DirectiveMeta._remove_kwarg_value_directives_from_queue(kwargs["patches"])
                DirectiveMeta._patches_dependencies = True

            result = decorated_function(*args, **kwargs)

            DirectiveMeta._directives_to_be_executed[decorated_function.__name__].append(result)

            # wrapped function returns same result as original so that we can nest directives
            return result

        return _wrapper


class DirectiveError(spack.error.SpackError):
    """This is raised when something is wrong with a package directive."""
