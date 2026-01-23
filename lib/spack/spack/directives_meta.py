# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import functools
import itertools
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

import spack.error
import spack.llnl.util.lang
import spack.repo
import spack.spec

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

    #: Set of all known directive dictionary names from `@directive(dicts=...)`
    _directive_dict_names: Set[str] = set()
    #: List of directives to be executed at class initialization time
    _directives_to_be_executed: List[Callable] = []
    #: Stack of when constraints from `with when(...)` context managers
    _when_constraints_stack: List[spack.spec.Spec] = []
    #: Stack of default args from `with default_args(...)` context managers
    _default_args_stack: List[dict] = []

    def __new__(
        cls: Type["DirectiveMeta"], name: str, bases: tuple, attr_dict: dict
    ) -> "DirectiveMeta":
        # Initialize the attribute containing the list of directives
        # to be executed. Here we go reversed because we want to execute
        # commands:
        # 1. in the order they were defined
        # 2. following the MRO
        attr_dict["_directives_to_be_executed"] = []
        for base in reversed(bases):
            try:
                directive_from_base = base._directives_to_be_executed
                attr_dict["_directives_to_be_executed"].extend(directive_from_base)
            except AttributeError:
                # The base class didn't have the required attribute.
                # Continue searching
                pass

        # De-duplicates directives from base classes
        attr_dict["_directives_to_be_executed"] = [
            x for x in spack.llnl.util.lang.dedupe(attr_dict["_directives_to_be_executed"])
        ]

        # Move things to be executed from module scope (where they
        # are collected first) to class scope
        if DirectiveMeta._directives_to_be_executed:
            attr_dict["_directives_to_be_executed"].extend(
                DirectiveMeta._directives_to_be_executed
            )
            DirectiveMeta._directives_to_be_executed = []

        return super(DirectiveMeta, cls).__new__(cls, name, bases, attr_dict)

    def __init__(cls: "DirectiveMeta", name: str, bases: tuple, attr_dict: dict):
        # The instance is being initialized: if it is a package we must ensure
        # that the directives are called to set it up.

        if spack.repo.is_package_module(cls.__module__):
            # Ensure the presence of the dictionaries associated with the directives.
            # All dictionaries are defaultdicts that create lists for missing keys.
            for d in DirectiveMeta._directive_dict_names:
                setattr(cls, d, {})

            # Lazily execute directives
            for directive in cls._directives_to_be_executed:
                directive(cls)

            # Ignore any directives executed *within* top-level
            # directives by clearing out the queue they're appended to
            DirectiveMeta._directives_to_be_executed = []

        super(DirectiveMeta, cls).__init__(name, bases, attr_dict)

    @staticmethod
    def push_when_constraint(when_spec: spack.spec.Spec) -> None:
        """Add a spec to the context constraints."""
        DirectiveMeta._when_constraints_stack.append(when_spec)

    @staticmethod
    def pop_when_constraint() -> spack.spec.Spec:
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
    def _remove_directives(args):
        # If any of the arguments are executors returned by a directive passed as an argument,
        # don't execute them lazily. Instead, let the called directive handle them. This allows
        # nested directive calls in packages.  The caller can return the directive if it should be
        # queued. Nasty, but it's the best way I can think of to avoid side effects if directive
        # results are passed as args
        directives = DirectiveMeta._directives_to_be_executed
        for arg in args:
            if isinstance(arg, (list, tuple)):
                # Descend into args that are lists or tuples
                DirectiveMeta._remove_directives(arg)
            elif callable(arg):  # directives are always callable, and very rare
                # Remove directives args from the exec queue
                for directive in directives:
                    if arg is directive:
                        directives.remove(directive)  # iterations ends, so mutation is fine
                        break


def _combine_when(
    when: Optional[str] = None,
    when_stack: List[spack.spec.Spec] = DirectiveMeta._when_constraints_stack,
) -> spack.spec.Spec:
    """Compute the combined when constraints from the context and the directive keyword argument.

    Arguments:
        when: The when constraint from the directive's keyword argument as a raw string (if any).
        when_stack: The stack of parsed when constraints from ``with when(...)`` context managers.
    """
    # In the following case
    #     with when("+foo"):     # single constraint on the stack
    #         depends_on("foo")  # unconditional directive
    # avoid creating a new spec and just return the one from the stack
    if len(when_stack) == 1 and not when:
        return when_stack[0]

    # Otherwise, combine all when constraints by mutating a new spec
    when_spec = spack.spec.Spec(when)
    for current in when_stack:
        when_spec._constrain_symbolically(current, deps=True)
    return when_spec


class directive:
    def __init__(
        self, dicts: Union[Tuple[str, ...], str] = (), supports_when: bool = True
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
            dicts: A list of names of dictionaries to add to the package class if they don't
                already exist.
            supports_when: If True, the directive can be used within a ``with when(...)`` context
                manager. (To be removed when all directives support ``when=`` arguments.)
        """

        if isinstance(dicts, str):
            dicts = (dicts,)

        # Add the dictionary names if not already there
        DirectiveMeta._directive_dict_names.update(dicts)

        self.supports_when = supports_when

    def __call__(self, decorated_function: Callable) -> Callable:
        directive_names.append(decorated_function.__name__)

        # Do not capture `self` in the wrapper
        supports_when = self.supports_when

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

            # Inject when arguments from the context
            if DirectiveMeta._when_constraints_stack:
                if not supports_when:
                    raise DirectiveError(
                        f'directive "{decorated_function.__name__}" cannot be used within a '
                        '"when" context since it does not support a "when=" argument'
                    )
                kwargs["when"] = _combine_when(kwargs.get("when"))

            # Remove directives passed as arguments, so they are not executed as part of this
            # class's directive execution, but handled by the called directive instead
            DirectiveMeta._remove_directives(itertools.chain(args, kwargs.values()))

            result = decorated_function(*args, **kwargs)

            DirectiveMeta._directives_to_be_executed.append(result)

            # wrapped function returns same result as original so that we can nest directives
            return result

        return _wrapper


class DirectiveError(spack.error.SpackError):
    """This is raised when something is wrong with a package directive."""
