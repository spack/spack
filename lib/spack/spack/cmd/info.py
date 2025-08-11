# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# mypy: disallow-untyped-defs

import argparse
import shutil
import sys
import textwrap
from argparse import Namespace
from typing import Any, Callable, Dict, Iterable, Optional, TextIO, TypeVar

import spack.builder
import spack.dependency
import spack.deptypes as dt
import spack.fetch_strategy as fs
import spack.install_test
import spack.llnl.util.tty.color as color
import spack.package_base
import spack.repo
import spack.spec
import spack.variant
import spack.version
from spack.cmd.common import arguments
from spack.llnl.util.tty.colify import colify
from spack.package_base import PackageBase
from spack.util.typing import SupportsRichComparison

description = "get detailed information on a particular package"
section = "basic"
level = "short"

header_color = "@*b"
plain_format = "@."


class Formatter:
    """Generic formatter for elements displayed by `spack info`.

    Elements have four parts: name, values, when condition, and description. They can
    be formatted two ways (shown here for variants)::

    Grouped by when (default)::

        when +cuda
          cuda_arch [none]                            none, 10, 100, 100a, 101,
                                                      101a, 11, 12, 120, 120a, 13
              CUDA architecture

    Or, by name (each name has a when nested under it)::

        cuda_arch [none]                              none, 10, 100, 100a, 101,
                                                      101a, 11, 12, 120, 120a, 13
          when +cuda
            CUDA architecture

    The values and description will be wrapped if needed. the name (and any additional info)
    will not (so they should be kept short).

    Subclasses are responsible for generating colorized text, but not wrapping,
    indentation, or other formatting, for the name, values, and description.

    """

    def format_name(self, element: Any) -> str:
        return str(element)

    def format_values(self, element: Any) -> str:
        return ""

    def format_description(self, element: Any) -> str:
        return ""


def padder(str_list: Iterable, extra: int = 0) -> Callable:
    """Return a function to pad elements of a list."""
    length = max(len(str(s)) for s in str_list) + extra

    def pad(string: str) -> str:
        string = str(string)
        padding = max(0, length - len(string))
        return string + (padding * " ")

    return pad


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "-a", "--all", action="store_true", default=False, help="output all package information"
    )

    options = [
        ("--by-name", "list variants in strict name order; don't group by condition"),
        ("--detectable", print_detectable.__doc__),
        ("--maintainers", print_maintainers.__doc__),
        ("--namespace", print_namespace.__doc__),
        ("--no-dependencies", f"do not {print_dependencies.__doc__}"),
        ("--no-variants", f"do not {print_variants.__doc__}"),
        ("--no-versions", f"do not {print_versions.__doc__}"),
        ("--phases", print_phases.__doc__),
        ("--tags", print_tags.__doc__),
        ("--tests", print_tests.__doc__),
        ("--virtuals", print_virtuals.__doc__),
    ]
    for opt, help_comment in options:
        subparser.add_argument(opt, action="store_true", help=help_comment)

    # deprecated for the more generic --by-name, but still here until we can remove it
    subparser.add_argument(
        "--variants-by-name", dest="by_name", action="store_true", help=argparse.SUPPRESS
    )
    arguments.add_common_arguments(subparser, ["package"])


def section_title(s: str) -> str:
    return header_color + s + plain_format


def version(s: str) -> str:
    return spack.spec.VERSION_COLOR + s + plain_format


def format_deptype(depflag: int) -> str:
    color_flags = zip("gcbm", dt.ALL_FLAGS)
    return ", ".join(
        color.colorize(f"@{c}{{{dt.flag_to_string(depflag & flag)}}}")
        for c, flag in color_flags
        if depflag & flag
    )


class DependencyFormatter(Formatter):
    def format_name(self, dep: spack.dependency.Dependency) -> str:
        return dep.spec.format(color=color.get_color_when())

    def format_values(self, dep: spack.dependency.Dependency) -> str:
        return str(format_deptype(dep.depflag))


def print_dependencies(pkg: PackageBase, args: Namespace) -> None:
    """output build, link, and run package dependencies"""
    print_definitions("Dependencies", pkg.dependencies, DependencyFormatter(), args.by_name)


def print_detectable(pkg: PackageBase, args: Namespace) -> None:
    """output information on external detection"""

    color.cprint("")
    color.cprint(section_title("Externally Detectable: "))

    # If the package has an 'executables' of 'libraries' field, it
    # can detect an installation
    if hasattr(pkg, "executables") or hasattr(pkg, "libraries"):
        find_attributes = []
        if hasattr(pkg, "determine_version"):
            find_attributes.append("version")

        if hasattr(pkg, "determine_variants"):
            find_attributes.append("variants")

        # If the package does not define 'determine_version' nor
        # 'determine_variants', then it must use some custom detection
        # mechanism. In this case, just inform the user it's detectable somehow.
        color.cprint(
            "    True{0}".format(
                " (" + ", ".join(find_attributes) + ")" if find_attributes else ""
            )
        )
    else:
        color.cprint("    False")


def print_maintainers(pkg: PackageBase, args: Namespace) -> None:
    """output package maintainers"""

    if len(pkg.maintainers) > 0:
        mnt = " ".join(["@@" + m for m in pkg.maintainers])
        color.cprint("")
        color.cprint(section_title("Maintainers: ") + mnt)


def print_namespace(pkg: PackageBase, args: Namespace) -> None:
    """output package namespace"""

    repo = spack.repo.PATH.get_repo(pkg.namespace)
    color.cprint("")
    color.cprint(section_title("Namespace:"))
    color.cprint(f"    @c{{{repo.namespace}}} at {repo.root}")


def print_phases(pkg: PackageBase, args: Namespace) -> None:
    """output installation phases"""

    builder = spack.builder.create(pkg)

    if hasattr(builder, "phases") and builder.phases:
        color.cprint("")
        color.cprint(section_title("Installation Phases:"))
        phase_str = ""
        for phase in builder.phases:
            phase_str += "    {0}".format(phase)
        color.cprint(phase_str)


def print_tags(pkg: PackageBase, args: Namespace) -> None:
    """output package tags"""

    color.cprint("")
    color.cprint(section_title("Tags: "))
    if hasattr(pkg, "tags"):
        tags = sorted(pkg.tags)
        colify(tags, indent=4)
    else:
        color.cprint("    None")


def print_tests(pkg: PackageBase, args: Namespace) -> None:
    """output relevant build-time and stand-alone tests"""

    # Some built-in base packages (e.g., Autotools) define callback (e.g.,
    # check) inherited by descendant packages. These checks may not result
    # in build-time testing if the package's build does not implement the
    # expected functionality (e.g., a 'check' or 'test' targets).
    #
    # So the presence of a callback in Spack does not necessarily correspond
    # to the actual presence of built-time tests for a package.
    for callbacks, phase in [
        (getattr(pkg, "build_time_test_callbacks", None), "Build"),
        (getattr(pkg, "install_time_test_callbacks", None), "Install"),
    ]:
        color.cprint("")
        color.cprint(section_title("Available {0} Phase Test Methods:".format(phase)))
        names = []
        if callbacks:
            for name in callbacks:
                if getattr(pkg, name, False):
                    names.append(name)

        if names:
            colify(sorted(names), indent=4)
        else:
            color.cprint("    None")

    # PackageBase defines an empty install/smoke test but we want to know
    # if it has been overridden and, therefore, assumed to be implemented.
    color.cprint("")
    color.cprint(section_title("Stand-Alone/Smoke Test Methods:"))
    names = spack.install_test.test_function_names(pkg, add_virtuals=True)
    if names:
        colify(sorted(names), indent=4)
    else:
        color.cprint("    None")


def _fmt_when(when: "spack.spec.Spec", indent: int) -> str:
    return color.colorize(
        f"{indent * ' '}@B{{when}} {color.cescape(when.format(color=color.get_color_when()))}"
    )


def _fmt_variant_value(v: Any) -> str:
    return str(v).lower() if v is None or isinstance(v, bool) else str(v)


def _print_definition(
    name_field: str,
    values_field: str,
    description: str,
    max_name_len: int,
    indent: int,
    when: Optional[spack.spec.Spec] = None,
    out: Optional[TextIO] = None,
) -> None:
    """Print a definition entry for `spack info` output.

    Arguments:
        name_field: name and optional info, e.g. a default; should be short.
        values_field: possible values for the entry; Wrapped if long.
        description: description of the field (wrapped if overly long)
        max_name_len:
        indent: size of leading indent for entry
        when: optional when condition
        out: stream to print to
    """
    out = out or sys.stdout
    cols = shutil.get_terminal_size().columns

    name_len = color.clen(name_field)

    pad = 4  # min padding between name and values
    value_indent = (indent + max_name_len + pad) * " "  # left edge of values

    formatted_name_and_values = f"{indent * ' '}{name_field}"
    if values_field:
        formatted_values = "\n".join(
            textwrap.wrap(
                values_field,
                width=cols - 2,
                initial_indent=value_indent,
                subsequent_indent=value_indent,
            )
        )
        # trim initial indentation
        formatted_values = formatted_values[indent + name_len + pad :]

        # e.g,. name [default]   value1, value2, value3, ...
        formatted_name_and_values += f"{pad * ' '}{formatted_values}"

    out.write(f"{formatted_name_and_values}\n")

    # when <spec>
    description_indent = indent + 4
    if when is not None and when != spack.spec.Spec():
        out.write(_fmt_when(when, description_indent - 2))
        out.write("\n")

    # description, preserving explicit line breaks from the way it's written in the
    # package file, but still wrapoing long lines for small terminals. This allows
    # descriptions to provide detailed help in descriptions (see, e.g., gasnet's variants).
    if description:
        formatted_description = "\n".join(
            textwrap.fill(
                line,
                width=cols - 2,
                initial_indent=description_indent * " ",
                subsequent_indent=description_indent * " ",
            )
            for line in description.split("\n")
        )
        out.write(formatted_description)
        out.write("\n")


K = TypeVar("K", bound=SupportsRichComparison)
V = TypeVar("V")


def print_header(header: str, when_indexed_dictionary: Dict, formatter: Formatter) -> bool:
    color.cprint("")
    color.cprint(section_title(f"{header}:"))

    if not when_indexed_dictionary:
        print("    None")
        return False
    return True


def max_name_length(when_indexed_dictionary: Dict, formatter: Formatter) -> int:
    # Calculate the max length of the first field of the definition. Lets us know how
    # much to pad other fields on the first line.
    return max(
        color.clen(formatter.format_name(definition))
        for subkey in spack.package_base._subkeys(when_indexed_dictionary)
        for _, definition in spack.package_base._definitions(when_indexed_dictionary, subkey)
    )


def print_grouped_by_when(
    header: str, when_indexed_dictionary: Dict, formatter: Formatter
) -> None:
    """Generic method to print metadata grouped by when conditions."""
    if not print_header(header, when_indexed_dictionary, formatter):
        return

    max_name_len = max_name_length(when_indexed_dictionary, formatter)

    # ensure that items without conditions come first
    unconditional_first = lambda item: (item[0] != spack.spec.Spec(), item)

    indent = 4
    for when, by_name in sorted(when_indexed_dictionary.items(), key=unconditional_first):
        start_indent = indent
        values_indent = max_name_len + 4

        if when != spack.spec.Spec():
            sys.stdout.write("\n")
            sys.stdout.write(_fmt_when(when, indent))
            sys.stdout.write("\n")

            # indent names slightly inside 'when', but line up values
            start_indent += 2
            values_indent -= 2

        for subkey, definition in sorted(by_name.items()):
            _print_definition(
                formatter.format_name(definition),
                formatter.format_values(definition),
                formatter.format_description(definition),
                values_indent,
                start_indent,
                when=None,
                out=sys.stdout,
            )


def print_by_name(header: str, when_indexed_dictionary: Dict, formatter: Formatter) -> None:
    if not print_header(header, when_indexed_dictionary, formatter):
        return

    max_name_len = max_name_length(when_indexed_dictionary, formatter)
    max_name_len += 4

    indent = 4

    for subkey in spack.package_base._subkeys(when_indexed_dictionary):
        for when, definition in spack.package_base._definitions(when_indexed_dictionary, subkey):
            _print_definition(
                formatter.format_name(definition),
                formatter.format_values(definition),
                formatter.format_description(definition),
                max_name_len,
                indent,
                when=when,
                out=sys.stdout,
            )
            sys.stdout.write("\n")


def print_definitions(
    header: str, when_indexed_dictionary: Dict, formatter: Formatter, by_name: bool
) -> None:
    # convert simple dictionaries to dicts of dicts before formatting.
    # subkeys are ignored in formatting, so use stringified numbers.
    values = when_indexed_dictionary.values()
    if when_indexed_dictionary and not isinstance(next(iter(values)), dict):
        when_indexed_dictionary = {
            when: {str(i): element}
            for i, (when, element) in enumerate(when_indexed_dictionary.items())
        }

    if by_name:
        print_by_name(header, when_indexed_dictionary, formatter)
    else:
        print_grouped_by_when(header, when_indexed_dictionary, formatter)


class VariantFormatter(Formatter):
    def format_name(self, variant: spack.variant.Variant) -> str:
        return color.colorize(
            f"@c{{{variant.name}}} @C{{[{_fmt_variant_value(variant.default)}]}}"
        )

    def format_values(self, variant: spack.variant.Variant) -> str:
        values = (
            [variant.values]
            if not isinstance(variant.values, (tuple, list, spack.variant.DisjointSetsOfValues))
            else variant.values
        )

        # put 'none' first, sort the rest by value
        sorted_values = sorted(values, key=lambda v: (v != "none", v))

        return color.colorize(f"@c{{{', '.join(_fmt_variant_value(v) for v in sorted_values)}}}")

    def format_description(self, variant: spack.variant.Variant) -> str:
        return variant.description


def print_variants(pkg: PackageBase, args: Namespace) -> None:
    """output variants"""
    print_definitions("Variants", pkg.variants, VariantFormatter(), args.by_name)


def print_licenses(pkg: PackageBase, args: Namespace) -> None:
    """Output the licenses of the project."""
    print_definitions("Licenses", pkg.licenses, Formatter(), args.by_name)


def print_versions(pkg: PackageBase, args: Namespace) -> None:
    """output versions"""

    color.cprint("")
    color.cprint(section_title("Preferred version:  "))

    if not pkg.versions:
        color.cprint(version("    None"))
        color.cprint("")
        color.cprint(section_title("Safe versions:  "))
        color.cprint(version("    None"))
        color.cprint("")
        color.cprint(section_title("Deprecated versions:  "))
        color.cprint(version("    None"))
    else:
        pad = padder(pkg.versions, 4)

        preferred = spack.package_base.preferred_version(pkg)

        def get_url(version: spack.version.VersionType) -> str:
            try:
                return str(fs.for_package_version(pkg, version))
            except spack.fetch_strategy.InvalidArgsError:
                return "No URL"

        url = get_url(preferred) if pkg.has_code else ""
        line = version("    {0}".format(pad(preferred))) + color.cescape(str(url))
        color.cwrite(line)

        print()

        safe = []
        deprecated = []
        for v in reversed(sorted(pkg.versions)):
            if pkg.has_code:
                url = get_url(v)
            if pkg.versions[v].get("deprecated", False):
                deprecated.append((v, url))
            else:
                safe.append((v, url))

        for title, vers in [("Safe", safe), ("Deprecated", deprecated)]:
            color.cprint("")
            color.cprint(section_title("{0} versions:  ".format(title)))
            if not vers:
                color.cprint(version("    None"))
                continue

            for v, url in vers:
                line = version("    {0}".format(pad(v))) + color.cescape(str(url))
                color.cprint(line)


def print_virtuals(pkg: PackageBase, args: Namespace) -> None:
    """output virtual packages"""

    color.cprint("")
    color.cprint(section_title("Virtual Packages: "))
    if pkg.provided:
        for when, specs in reversed(sorted(pkg.provided.items())):
            line = "    %s provides %s" % (when.cformat(), ", ".join(s.cformat() for s in specs))
            print(line)

    else:
        color.cprint("    None")


def info(parser: argparse.ArgumentParser, args: Namespace) -> None:
    spec = spack.spec.Spec(args.package)
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.fullname)
    pkg = pkg_cls(spec)

    # Output core package information
    header = section_title("{0}:   ").format(pkg.build_system_class) + pkg.name
    color.cprint(header)

    color.cprint("")
    color.cprint(section_title("Description:"))
    if pkg.__doc__:
        color.cprint(color.cescape(pkg.format_doc(indent=4)))
    else:
        color.cprint("    None")

    if getattr(pkg, "homepage"):
        color.cprint(section_title("Homepage: ") + str(pkg.homepage))

    # Now output optional information in expected order
    sections = [
        (args.all or args.maintainers, print_maintainers),
        (args.all or args.namespace, print_namespace),
        (args.all or args.detectable, print_detectable),
        (args.all or args.tags, print_tags),
        (args.all or not args.no_versions, print_versions),
        (args.all or not args.no_variants, print_variants),
        (args.all or args.phases, print_phases),
        (args.all or not args.no_dependencies, print_dependencies),
        (args.all or args.virtuals, print_virtuals),
        (args.all or args.tests, print_tests),
        (args.all or True, print_licenses),
    ]
    for print_it, func in sections:
        if print_it:
            func(pkg, args)

    color.cprint("")
