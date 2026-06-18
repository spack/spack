# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
import textwrap
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

import spack.config
import spack.extensions
import spack.llnl.util.lang
from spack.util.path import canonicalize_path

if TYPE_CHECKING:
    import spack.vendor.jinja2


class ContextMeta(type):
    """Metaclass for Context. It helps reduce the boilerplate in client code."""

    #: Keeps track of the context properties that have been added
    #: by the class that is being defined
    _new_context_properties: List[str] = []

    def __new__(cls, name, bases, attr_dict):
        # Merge all the context properties that are coming from base classes
        # into a list without duplicates.
        context_properties = list(cls._new_context_properties)
        for x in bases:
            try:
                context_properties.extend(x.context_properties)
            except AttributeError:
                pass
        context_properties = list(spack.llnl.util.lang.dedupe(context_properties))

        # Flush the list
        cls._new_context_properties = []

        # Attach the list to the class being created
        attr_dict["context_properties"] = context_properties

        return super(ContextMeta, cls).__new__(cls, name, bases, attr_dict)

    @classmethod
    def context_property(cls, func):
        """Decorator that adds a function name to the list of new context
        properties, and then returns a property.
        """
        name = func.__name__
        cls._new_context_properties.append(name)
        return property(func)


#: A saner way to use the decorator
context_property = ContextMeta.context_property


class Context(metaclass=ContextMeta):
    """Base class for context classes that are used with the template engine."""

    context_properties: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary containing all the context properties."""
        return {name: getattr(self, name) for name in self.context_properties}


def make_environment(dirs: Optional[Tuple[str, ...]] = None) -> "spack.vendor.jinja2.Environment":
    """Returns a configured environment for template rendering."""
    if dirs is None:
        # Default directories where to search for templates
        dirs = default_template_dirs(spack.config.CONFIG)

    return make_environment_from_dirs(dirs)


@spack.llnl.util.lang.memoized
def make_environment_from_dirs(dirs: Tuple[str, ...]) -> "spack.vendor.jinja2.Environment":
    # Import at this scope to avoid slowing Spack startup down
    import spack.vendor.jinja2

    # Loader for the templates
    loader = spack.vendor.jinja2.FileSystemLoader(dirs)
    # Environment of the template engine
    env = spack.vendor.jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    # Custom filters
    _set_filters(env)
    return env


def default_template_dirs(configuration: spack.config.Configuration) -> Tuple[str, ...]:
    config_yaml = configuration.get_config("config")
    builtins = config_yaml.get("template_dirs", ["$spack/share/spack/templates"])
    extensions = spack.extensions.get_template_dirs()
    return tuple(canonicalize_path(d) for d in itertools.chain(builtins, extensions))


# Extra filters for the template engine environment


def prepend_to_line(text, token):
    """Prepends a token to each line in text"""
    return [token + line for line in text]


def quote(text):
    """Quotes each line in text"""
    return ['"{0}"'.format(line) for line in text]


def curly_quote(text):
    """Encloses each line of text in curly braces"""
    return ["{{{0}}}".format(line) for line in text]


def _set_filters(env):
    """Sets custom filters to the template engine environment"""
    env.filters["textwrap"] = textwrap.wrap
    env.filters["prepend_to_line"] = prepend_to_line
    env.filters["join"] = "\n".join
    env.filters["quote"] = quote
    env.filters["curly_quote"] = curly_quote
