# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import json
import sys
import textwrap
from argparse import ArgumentParser, Namespace
from typing import Any, Dict, List, Optional, Tuple, Union

import llnl.util.tty as tty
import llnl.util.tty.color as color
from llnl.util.tty.colify import colify

import spack.deptypes as dt
import spack.fetch_strategy as fs
import spack.install_test
import spack.repo
import spack.spec
import spack.version
from spack.cmd.common import arguments
from spack.package_base import preferred_version, PackageBase

description = "get detailed information on a particular package"
section = "basic"
level = "short"

header_color = "@*b"
plain_format = "@."

isatty = sys.stdout.isatty()

OutputList = List[Tuple[str, str]]


def padder(str_list: List[str], extra: int = 0) -> str:
    """Return a function to pad elements of a list."""
    length = max(len(str(s)) for s in str_list) + extra

    def pad(string):
        string = str(string)
        padding = max(0, length - len(string))
        return string + (padding * " ")

    return pad


def setup_parser(subparser: ArgumentParser) -> None:
    subparser.add_argument(
        "-a", "--all", action="store_true", default=False, help="output all package information"
    )

    options = [
        ("--detectable", detectable.__doc__),
        ("--maintainers", maintainers.__doc__),
        ("--no-dependencies", "do not " + dependencies.__doc__),
        ("--no-variants", "do not " + variants.__doc__),
        ("--no-versions", "do not " + versions.__doc__),
        ("--phases", phases.__doc__),
        ("--tags", tags.__doc__),
        ("--tests", tests.__doc__),
        ("--virtuals", virtuals.__doc__),
        ("--variants-by-name", "list variants in strict name order; don't group by condition"),
    ]
    for opt, help_comment in options:
        subparser.add_argument(opt, action="store_true", help=help_comment)

    subparser.add_argument(
        "-j", "--json", action="store_true", default=False, dest="json", help="print as JSON"
    )

    arguments.add_common_arguments(subparser, ["package"])


def section_title(s: str) -> str:
    return header_color + s + plain_format


def version(s: str) -> str:
    return spack.spec.VERSION_COLOR + s + plain_format


def license(s: str) -> str:
    return spack.spec.VERSION_COLOR + s + plain_format


def _dump(args: Namespace, data: Optional[Any], separator: Optional[str] = None) -> str:
    """format the data for output"""
    if args.json:
        return json.dumps(data)

    if isinstance(data, (str, bool, type(None))):
        return _fmt_value(data)

    if isinstance(data, (list, tuple)):
        if separator is None:
            buffer = io.StringIO()
            colify(data, output=buffer, tty=isatty, indent=4)
            values = buffer.getvalue()
        else:
            values = separator.join([d for d in data])
        return values

    raise RuntimeError(f"Unsupported type ({type(data)}) for {data}")


def _heading(args: Namespace, text: str) -> str:
    return (f'"{text.lower()}"').replace(" ", "_") if args.json else section_title(f"{text}:  ")


def dependencies(pkg: type[PackageBase], args: Namespace) -> OutputList:
    """output build, link, and run package dependencies"""
    output = []
    for deptype in ("build", "link", "run"):
        heading = _heading(args, f"{deptype.capitalize()} Dependencies")
        deps = sorted(pkg.dependencies_of_type(dt.flag_from_string(deptype)))

        output.extend(_add_section(args, heading, deps, blank=False))

    return output


def externally_detectable(pkg: type[PackageBase]) -> Tuple[bool, List[str]]:
    """returns external detection information"""
    can_detect = False
    find_attributes = []

    # If the package has an 'executables' or 'libraries' field, it
    # can detect an installation.
    if hasattr(pkg, "executables") or hasattr(pkg, "libraries"):
        find_attributes = []
        if hasattr(pkg, "determine_version"):
            find_attributes.append("version")

        if hasattr(pkg, "determine_variants"):
            find_attributes.append("variants")

        # If the package does not define 'determine_version' nor
        # 'determine_variants', then it must use some custom detection
        # mechanism. In this case, just inform the user it's detectable somehow.
        can_detect = True

    return can_detect, find_attributes


def detectable(pkg: type[PackageBase], args: Namespace) -> OutputList:
    """output information on external detection"""

    can_detect, find_attributes = externally_detectable(pkg)
    heading = _heading(args, "Externally Detectable")
    values = find_attributes if can_detect else False

    if args.json:
        return [(heading, _dump(args, values))]

    output = [("", ""), (heading, "")]
    if isinstance(values, list):
        values = "True{0}".format(
            " (" + ", ".join(find_attributes) + ")" if find_attributes else ""
        )
    else:
        values = str(values).capitalize()
    output.append(("    ", _dump(args, values)))
    return output


def maintainers(pkg: type[PackageBase], args: Namespace) -> OutputList:
    """output package maintainers"""
    output = []
    if len(pkg.maintainers) > 0:
        heading = _heading(args, "Maintainers")
        mnt = pkg.maintainers if args.json else " ".join(["@@" + m for m in pkg.maintainers])
        output.extend([("", ""), (heading, _dump(args, mnt))])

    return output


def phases(pkg: type[PackageBase], args: Namespace) -> OutputList:
    """output installation phases"""

    output = []
    if hasattr(pkg.builder, "phases") and pkg.builder.phases:
        heading = _heading(args, "Installation Phases")
        output.extend(_add_section(args, heading, pkg.builder.phases, blank=False))
    return output


def tags(pkg: type[PackageBase], args: Namespace) -> OutputList:
    """output package tags"""
    heading = _heading(args, "Tags")
    none = None if args.json else "    None"
    tags = sorted(pkg.tags) if hasattr(pkg, "tags") else none
    return _add_section(args, heading, tags)


def tests(pkg: type[PackageBase], args: Namespace) -> OutputList:
    """output relevant build-time and stand-alone tests"""
    output = []
    none = None if args.json else "    None"

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
        heading = _heading(args, f"{phase.capitalize()} Phase Test Methods")
        names = []
        if callbacks:
            for name in callbacks:
                if getattr(pkg, name, False):
                    names.append(name)

        names = sorted(names) if names else none
        output.extend(_add_section(args, heading, names))

    blank = len(names) == 0

    # PackageBase defines an empty install/smoke test but we want to know
    # if it has been overridden and, therefore, assumed to be implemented.
    heading = _heading(args, "Stand-Alone Test Methods")
    tests = spack.install_test.test_function_names(pkg, add_virtuals=True)
    output.extend(_add_section(args, heading, tests, blank=blank))

    return output


def _fmt_value(v: Any) -> str:
    if v is None or isinstance(v, bool):
        return str(v).lower()
    else:
        return str(v)


def _fmt_name_and_default(variant: "spack.variant.Variant") -> str:
    """Print colorized name [default] for a variant."""
    # TODO/TLD: Resolve @ format issue
    # return color.colorize(f"@c{{{variant.name}}} @C{{[{_fmt_value(variant.default)}]}}")
    return color.colorize(f"@@c{{{variant.name}}} @@C{{[{_fmt_value(variant.default)}]}}")


def _fmt_when(when: "spack.spec.Spec", indent: int) -> str:
    # TODO/TLD: Resolve @ format issue
    return color.colorize(f"{indent * ' '}@B{{when}} {color.cescape(str(when))}")


def _fmt_variant_description(variant: "spack.variant.Variant", width: int, indent: int) -> str:
    """Format a variant's description, preserving explicit line breaks."""
    # TODO/TLD: shouldn't this be separate lines?
    return "\n".join(
        textwrap.fill(
            line, width=width, initial_indent=indent * " ", subsequent_indent=indent * " "
        )
        for line in variant.description.split("\n")
    )


def _fmt_variant(
    variant: Any, max_name_default_len: int, indent: int, when: Optional["spack.spec.Spec"] = None
) -> List[str]:
    lines = []

    _, cols = tty.terminal_size()

    name_and_default = _fmt_name_and_default(variant)
    name_default_len = color.clen(name_and_default)

    values = variant.values
    if not isinstance(variant.values, (tuple, list, spack.variant.DisjointSetsOfValues)):
        values = [variant.values]

    # put 'none' first, sort the rest by value
    sorted_values = sorted(values, key=lambda v: (v != "none", v))

    pad = 4  # min padding between 'name [default]' and values
    value_indent = (indent + max_name_default_len + pad) * " "  # left edge of values

    # This preserves any formatting (i.e., newlines) from how the description was
    # written in package.py, but still wraps long lines for small terminals.
    # This allows some packages to provide detailed help on their variants (see, e.g., gasnet).
    # TLD/TODO: fix this .. should be adding one line at a time
    formatted_values = "\n".join(
        textwrap.wrap(
            f"{', '.join(_fmt_value(v) for v in sorted_values)}",
            width=cols - 2,
            initial_indent=value_indent,
            subsequent_indent=value_indent,
        )
    )
    formatted_values = formatted_values[indent + name_default_len + pad :]

    # name [default]   value1, value2, value3, ...
    padding = pad * " "
    lines.append(f"{indent * ' '}{name_and_default}{padding}@c{{{formatted_values}}}")

    # when <spec>
    description_indent = indent + 4
    if when is not None and when != spack.spec.Spec():
        lines.append(_fmt_when(when, description_indent - 2))

    # description, preserving explicit line breaks from the way it's written in the package file
    # TODO/TLD: shouldn't this be an extension of separate lines?
    lines.append(_fmt_variant_description(variant, cols - 2, description_indent))
    return lines


def _variants_by_name_when(pkg: type[PackageBase]) -> Dict[str, Any]:
    """Adaptor to get variants keyed by { name: { when: { [Variant...] } }."""
    # TODO: replace with pkg.variants_by_name(when=True) when unified directive dicts are merged.
    variants = {}
    for name, (variant, whens) in sorted(pkg.variants.items()):
        for when in whens:
            variants.setdefault(name, {}).setdefault(when, []).append(variant)
    return variants


def _variants_by_when_name(pkg: type[PackageBase]) -> Dict[str, Any]:
    """Adaptor to get variants keyed by { when: { name: Variant } }"""
    # TODO: replace with pkg.variants when unified directive dicts are merged.
    variants = {}
    for name, (variant, whens) in pkg.variants.items():
        for when in whens:
            variants.setdefault(when, {})[name] = variant
    return variants


def variants_default_heading_len(pkg: type[PackageBase]) -> Tuple[Dict[str, Any], int]:
    """Retrieves variants by name and calculate max length of the 'name [default]' output

    Args:
        pkg: package being queried

    Returns: (variants_by_name, max_name_length)
    """
    variants_by_name = _variants_by_name_when(pkg)

    # Calculate the max length of the "name [default]" part of the variant display
    # This lets us know where to print variant values.
    max_name_default_len = max(
        color.clen(_fmt_name_and_default(variant))
        for name, when_variants in variants_by_name.items()
        for variants in when_variants.values()
        for variant in variants
    )

    return variants_by_name, max_name_default_len


def _unconstrained_ver_first(item):
    """sort key that puts specs with open version ranges first"""
    spec, _ = item
    return (spack.version.any_version not in spec.versions, spec)


class VariantInfo:
    """Essentially a data class for variant info so json reports the property"""

    def __init__(self, when: str, name: str, default: str):
        self.when = when
        self.name = name
        self.default = default


def variants_grouped_by_when(
    pkg: type[PackageBase], args: Namespace
) -> List[Union["VariantInfo", str]]:
    """return variants grouped by when"""
    variants = _variants_by_when_name(pkg)

    if args.json:
        data = []
        for when, variants_by_name in sorted(variants.items(), key=_unconstrained_ver_first):
            for name, variant in sorted(variants_by_name.items()):
                assert name == variant.name
                data.append(VariantInfo(str(when), name, _fmt_value(variant.default)))
        return data

    lines = []
    _, max_name_len = variants_default_heading_len(pkg)
    indent = 4
    for when, variants_by_name in sorted(variants.items(), key=_unconstrained_ver_first):
        padded_values = max_name_len + 4
        start_indent = indent

        if when != spack.spec.Spec():
            lines.append("")
            lines.append(_fmt_when(when, indent))
            lines.append("")

            # indent names slightly inside 'when', but line up values
            padded_values -= 2
            start_indent += 2

        for name, variant in sorted(variants_by_name.items()):
            lines.extend(_fmt_variant(variant, padded_values, start_indent, None))

    return lines


def variants_by_name(pkg: type[PackageBase], args: Namespace) -> List[str]:
    """output variants already sorted by name"""
    variants, max_name_len = variants_default_heading_len(pkg)

    if args.json:
        return variants

    indent = 4
    lines = []
    for name, when_variants in variants.items():
        for when, variants in sorted(when_variants.items(), key=_unconstrained_ver_first):
            for variant in variants:
                lines.append(_fmt_variant(variant, max_name_len, indent, when))
                # lines.append("")
    return lines


def variants(pkg: type[PackageBase], args: Namespace) -> OutputList:
    """output variants"""
    heading = _heading(args, "Variants")
    none = None if args.json else "    None"

    if not pkg.variants:
        return [(heading, _dump(args, none))]

    output = []
    if not args.json:
        output.extend([("", ""), (heading, "")])

    if args.variants_by_name:
        variants = variants_by_name(pkg, args)
    else:
        variants = variants_grouped_by_when(pkg, args)

    if args.json:
        output.append((heading, _dump(args, variants)))
    else:
        for info in variants:
            output.append(("", info))

    return output


def _add_section(args, heading: str, values, blank: bool = True):
    """Add section output for a single set of values that can be output together.

    Args:
        heading: heading, formatted appropriately if on its own line
        values: values that can be output together (json dump or on the line following the heading)
        blank: add a blank line to non-JSON output only if ``True``


    Returns: a list of tuples representing (heading, values) lines
    """
    output = []
    if args.json:
        output.append((heading, _dump(args, values)))
    else:
        if blank:
            output.append(("", ""))
        output.extend([(heading, ""), ("", _dump(args, values))])
    return output


class VersionInfo:
    """Essentially a data class for version info so json reports the property"""

    def __init__(self, version: str, url: str):
        self.version = version
        self.url = url


def versions(pkg: type[PackageBase], args: Namespace) -> OutputList:
    """output versions"""
    output = []

    headings = [
        _heading(args, "Preferred version(s)"),
        _heading(args, "Safe versions"),
        _heading(args, "Deprecated versions"),
    ]

    none = None if args.json else version("    None")
    if not pkg.versions:
        for heading in headings:
            output.extend(_add_section(args, heading, none))
        return output

    pad = padder(pkg.versions, 4)

    def get_url(version):
        try:
            return fs.for_package_version(pkg, version)
        except spack.fetch_strategy.InvalidArgsError:
            return "No URL"

    calc_preferred = preferred_version(pkg)
    calc_url = get_url(calc_preferred) if pkg.has_code else ""

    safe = []
    deprecated = []
    preferred = []
    for v in reversed(sorted(pkg.versions)):
        if pkg.has_code:
            url = get_url(v)
        if pkg.versions[v].get("deprecated", False):
            deprecated.append((v, url))
        elif pkg.versions[v].get("preferred", False):
            preferred.append((v, url))
        else:
            safe.append((v, url))

    if len(preferred) == 0:
        preferred.append((calc_preferred, calc_url))

    for i, vers in enumerate([preferred, safe, deprecated]):
        if not vers:
            output.extend(_add_section(args, headings[i], none))
            continue

        if args.json:
            data = []
            for v, url in vers:
                data.append(VersionInfo(str(v), str(url)))
            output.extend(_add_section(args, headings[i], data))
            continue

        if i > 0:
            output.append(("", ""))
        output.append((headings[i], ""))

        for v, url in vers:
            output.append(("", "    " + version(pad(v)) + color.cescape(str(url))))

    return output


def virtuals(pkg: type[PackageBase], args: Namespace) -> OutputList:
    """output virtual packages"""

    heading = _heading(args, "Virtual Packages")
    if not pkg.provided or len(pkg.provided) == 0:
        none = None if args.json else "    None"
        return _add_section(args, heading, none, blank=False)

    if args.json:
        provides = []
        for when, specs in reversed(sorted(pkg.provided.items())):
            fspecs = ",".join(s for s in specs)
            provides.append(f"{when} provides {fspecs}")
        return [(heading, _dump(args, provides))]

    provides = []
    for when, specs in provides:
        fspecs = ", ".join(s.cformat() for s in specs)
        provides.append(f"{when.cformat()} provides {fspecs}")

    output = [("", ""), (heading, "")]
    for p in provides:
        output.append(("    ", p))
    return output


def licenses(pkg: type[PackageBase], args: Namespace) -> OutputList:
    """output project licenses."""

    heading = _heading(args, "Licenses")
    if not pkg.licenses:
        return [(heading, _dump(args, None))]

    lics = []
    for when_spec in pkg.licenses:
        lics.append((pkg.licenses[when_spec], when_spec))

    if args.json:
        return [(heading, _dump(args, lics))]

    pad = padder(pkg.licenses, 4)
    output = [(heading, "")]
    for license_id, when_spec in lics:
        output.append(("", license(f"    {pad(license_id)}{color.cescape(str(when_spec))}")))

    return output


def _description(pkg) -> str:
    """The description of the package or `None`"""
    return color.cescape(pkg.format_doc(indent=4)) if pkg.__doc__ else "None"


def content(pkg: type[PackageBase], args: Namespace) -> OutputList:
    """Extract the relevant info content to be output.

    Args:
        pkg: the package whose info is being returned
        args: parsed command line arguments

    Returns:
        list of (key, value(s)) content
    """
    output = []

    if args.json:
        output.extend(
            [('"name"', f'"{pkg.name}"'), ('"build_system"', f'"{pkg.build_system_class}"')]
        )
    else:
        # Text output ties the build system (as heading) to the package name.
        # Also want to output the potentially multi-line description.
        output.extend(
            [
                (_heading(args, pkg.build_system_class), pkg.name),
                ("", ""),  # a blank line between title/package and description
                (_heading(args, "Description"), ""),
                ("", _description(pkg)),
            ]
        )

    if getattr(pkg, "homepage"):
        output.extend([(_heading(args, "Homepage"), _dump(args, pkg.homepage))])

    sections = [
        (args.all or args.maintainers, maintainers),
        (args.all or args.detectable, detectable),
        (args.all or args.tags, tags),
        (args.all or not args.no_versions, versions),
        (args.all or not args.no_variants, variants),
        (args.all or args.phases, phases),
        (args.all or not args.no_dependencies, dependencies),
        (args.all or args.virtuals, virtuals),
        (args.all or args.tests, tests),
        (args.all or True, licenses),
    ]
    for show, func in sections:
        if show:
            output.extend(func(pkg, args))

    return output


def print_text(content) -> None:
    for heading, value in content:
        # TBD/TLD: What is the *right* way to work around the colorize problem?
        line = f"{heading}{value}"
        if "when" in value:
            print(line)
        else:
            color.cprint(line)
    print("")


def print_json(content) -> None:
    sys.stdout.write("[\n {\n")

    # Output core package information
    for heading, value in content:
        # skip blank line tuples
        if len(heading) > 0 and len(value) > 0:
            sys.stdout.write(f" {heading}: {value},\n")

    sys.stdout.write(" }\n]\n")


def info(parser, args: Namespace) -> None:
    # Get the package class
    spec = spack.spec.Spec(args.package)
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    pkg = pkg_cls(spec)

    data = content(pkg, args)

    # Print the formatted information
    if args.json:
        print_json(data)
    else:
        print_text(data)
