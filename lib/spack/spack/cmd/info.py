# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import textwrap

from six.moves import zip_longest

import llnl.util.tty as tty
import llnl.util.tty.color as color
from llnl.util.tty.colify import colify

import spack.cmd.common.arguments as arguments
import spack.fetch_strategy as fs
import spack.repo
import spack.spec

description = 'get detailed information on a particular package'
section = 'basic'
level = 'short'

header_color = '@*b'
plain_format = '@.'


def padder(str_list, extra=0):
    """Return a function to pad elements of a list."""
    length = max(len(str(s)) for s in str_list) + extra

    def pad(string):
        string = str(string)
        padding = max(0, length - len(string))
        return string + (padding * ' ')
    return pad


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['package'])


def section_title(s):
    return header_color + s + plain_format


def version(s):
    return spack.spec.version_color + s + plain_format


def variant(s):
    return spack.spec.enabled_variant_color + s + plain_format


class VariantFormatter(object):
    def __init__(self, variants):
        self.variants = variants
        self.headers = ('Name [Default]', 'Allowed values', 'Description')

        # Formats
        fmt_name = '{0} [{1}]'

        # Initialize column widths with the length of the
        # corresponding headers, as they cannot be shorter
        # than that
        self.column_widths = [len(x) for x in self.headers]

        # Expand columns based on max line lengths
        for k, v in variants.items():
            candidate_max_widths = (
                len(fmt_name.format(k, self.default(v))),  # Name [Default]
                len(v.allowed_values),  # Allowed values
                len(v.description)  # Description
            )

            self.column_widths = (
                max(self.column_widths[0], candidate_max_widths[0]),
                max(self.column_widths[1], candidate_max_widths[1]),
                max(self.column_widths[2], candidate_max_widths[2])
            )

        # Don't let name or possible values be less than max widths
        _, cols = tty.terminal_size()
        max_name = min(self.column_widths[0], 30)
        max_vals = min(self.column_widths[1], 20)

        # allow the description column to extend as wide as the terminal.
        max_description = min(
            self.column_widths[2],
            # min width 70 cols, 14 cols of margins and column spacing
            max(cols, 70) - max_name - max_vals - 14,
        )
        self.column_widths = (max_name, max_vals, max_description)

        # Compute the format
        self.fmt = "%%-%ss%%-%ss%%s" % (
            self.column_widths[0] + 4,
            self.column_widths[1] + 4
        )

    def default(self, v):
        s = 'on' if v.default is True else 'off'
        if not isinstance(v.default, bool):
            s = v.default
        return s

    @property
    def lines(self):
        if not self.variants:
            yield '    None'
        else:
            yield '    ' + self.fmt % self.headers
            underline = tuple([w * "=" for w in self.column_widths])
            yield '    ' + self.fmt % underline
            yield ''
            for k, v in sorted(self.variants.items()):
                name = textwrap.wrap(
                    '{0} [{1}]'.format(k, self.default(v)),
                    width=self.column_widths[0]
                )
                allowed = v.allowed_values.replace('True, False', 'on, off')
                allowed = textwrap.wrap(allowed, width=self.column_widths[1])
                description = []
                for d_line in v.description.split('\n'):
                    description += textwrap.wrap(
                        d_line,
                        width=self.column_widths[2]
                    )
                for t in zip_longest(
                        name, allowed, description, fillvalue=''
                ):
                    yield "    " + self.fmt % t


def print_text_info(pkg):
    """Print out a plain text description of a package."""

    header = section_title(
        '{0}:   '
    ).format(pkg.build_system_class) + pkg.name
    color.cprint(header)

    color.cprint('')
    color.cprint(section_title('Description:'))
    if pkg.__doc__:
        color.cprint(color.cescape(pkg.format_doc(indent=4)))
    else:
        color.cprint("    None")

    color.cprint(section_title('Homepage: ') + pkg.homepage)

    if len(pkg.maintainers) > 0:
        mnt = " ".join(['@@' + m for m in pkg.maintainers])
        color.cprint('')
        color.cprint(section_title('Maintainers: ') + mnt)

    color.cprint('')
    color.cprint(section_title('Externally Detectable: '))

    # If the package has an 'executables' field, it can detect an installation
    if hasattr(pkg, 'executables'):
        find_attributes = []
        if hasattr(pkg, 'determine_version'):
            find_attributes.append('version')

        if hasattr(pkg, 'determine_variants'):
            find_attributes.append('variants')

        # If the package does not define 'determine_version' nor
        # 'determine_variants', then it must use some custom detection
        # mechanism. In this case, just inform the user it's detectable somehow.
        color.cprint('    True{0}'.format(
            ' (' + ', '.join(find_attributes) + ')' if find_attributes else ''))
    else:
        color.cprint('    False')

    color.cprint('')
    color.cprint(section_title("Tags: "))
    if hasattr(pkg, 'tags'):
        tags = sorted(pkg.tags)
        colify(tags, indent=4)
    else:
        color.cprint("    None")

    color.cprint('')
    color.cprint(section_title('Preferred version:  '))

    if not pkg.versions:
        color.cprint(version('    None'))
        color.cprint('')
        color.cprint(section_title('Safe versions:  '))
        color.cprint(version('    None'))
        color.cprint('')
        color.cprint(section_title('Deprecated versions:  '))
        color.cprint(version('    None'))
    else:
        pad = padder(pkg.versions, 4)

        # Here we sort first on the fact that a version is marked
        # as preferred in the package, then on the fact that the
        # version is not develop, then lexicographically
        key_fn = lambda v: (pkg.versions[v].get('preferred', False),
                            not v.isdevelop(),
                            v)
        preferred = sorted(pkg.versions, key=key_fn).pop()
        url = ''
        if pkg.has_code:
            url = fs.for_package_version(pkg, preferred)

        line = version('    {0}'.format(pad(preferred))) + color.cescape(url)
        color.cprint(line)

        safe = []
        deprecated = []
        for v in reversed(sorted(pkg.versions)):
            if pkg.has_code:
                url = fs.for_package_version(pkg, v)
            if pkg.versions[v].get('deprecated', False):
                deprecated.append((v, url))
            else:
                safe.append((v, url))

        for title, vers in [('Safe', safe), ('Deprecated', deprecated)]:
            color.cprint('')
            color.cprint(section_title('{0} versions:  '.format(title)))
            if not vers:
                color.cprint(version('    None'))
                continue

            for v, url in vers:
                line = version('    {0}'.format(pad(v))) + color.cescape(url)
                color.cprint(line)

    color.cprint('')
    color.cprint(section_title('Variants:'))

    formatter = VariantFormatter(pkg.variants)
    for line in formatter.lines:
        color.cprint(line)

    if hasattr(pkg, 'phases') and pkg.phases:
        color.cprint('')
        color.cprint(section_title('Installation Phases:'))
        phase_str = ''
        for phase in pkg.phases:
            phase_str += "    {0}".format(phase)
        color.cprint(phase_str)

    for deptype in ('build', 'link', 'run'):
        color.cprint('')
        color.cprint(section_title('%s Dependencies:' % deptype.capitalize()))
        deps = sorted(pkg.dependencies_of_type(deptype))
        if deps:
            colify(deps, indent=4)
        else:
            color.cprint('    None')

    color.cprint('')
    color.cprint(section_title('Virtual Packages: '))
    if pkg.provided:
        inverse_map = {}
        for spec, whens in pkg.provided.items():
            for when in whens:
                if when not in inverse_map:
                    inverse_map[when] = set()
                inverse_map[when].add(spec)
        for when, specs in reversed(sorted(inverse_map.items())):
            line = "    %s provides %s" % (
                when.colorized(), ', '.join(s.colorized() for s in specs)
            )
            print(line)

    else:
        color.cprint("    None")

    color.cprint('')


def info(parser, args):
    pkg = spack.repo.get(args.package)
    print_text_info(pkg)
