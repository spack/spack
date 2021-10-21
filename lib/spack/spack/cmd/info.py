# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import textwrap
from datetime import date

from six.moves import zip_longest

import llnl.util.tty as tty
import llnl.util.tty.color as color
from llnl.util.tty.colify import colify

import spack.environment as ev
import spack.fetch_strategy as fs
import spack.repo
import spack.spec
from spack.package import preferred_version

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
    subparser.add_argument(
        'pkg_spec',
        nargs=argparse.REMAINDER,
        help='Package name or, with --installed, spec')

    subparser.add_argument(
        '-i', '--installed',
        action='store_true',
        help='Show installation details for the provided spec')


def section_title(s):
    return header_color + s + plain_format


def version(s):
    return spack.spec.version_color + s + plain_format


def variant(s):
    return spack.spec.enabled_variant_color + s + plain_format


class VariantFormatter(object):
    def __init__(self, variants):
        self.variants = variants
        self.headers = ('Name [Default]', 'When', 'Allowed values', 'Description')

        # Formats
        fmt_name = '{0} [{1}]'

        # Initialize column widths with the length of the
        # corresponding headers, as they cannot be shorter
        # than that
        self.column_widths = [len(x) for x in self.headers]

        # Expand columns based on max line lengths
        for k, e in variants.items():
            v, w = e
            candidate_max_widths = (
                len(fmt_name.format(k, self.default(v))),  # Name [Default]
                len(str(w)),
                len(v.allowed_values),  # Allowed values
                len(v.description)  # Description
            )

            self.column_widths = (
                max(self.column_widths[0], candidate_max_widths[0]),
                max(self.column_widths[1], candidate_max_widths[1]),
                max(self.column_widths[2], candidate_max_widths[2]),
                max(self.column_widths[3], candidate_max_widths[3])
            )

        # Don't let name or possible values be less than max widths
        _, cols = tty.terminal_size()
        max_name = min(self.column_widths[0], 30)
        max_when = min(self.column_widths[1], 30)
        max_vals = min(self.column_widths[2], 20)

        # allow the description column to extend as wide as the terminal.
        max_description = min(
            self.column_widths[3],
            # min width 70 cols, 14 cols of margins and column spacing
            max(cols, 70) - max_name - max_vals - 14,
        )
        self.column_widths = (max_name, max_when, max_vals, max_description)

        # Compute the format
        self.fmt = "%%-%ss%%-%ss%%-%ss%%s" % (
            self.column_widths[0] + 4,
            self.column_widths[1] + 4,
            self.column_widths[2] + 4
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
            for k, e in sorted(self.variants.items()):
                v, w = e
                name = textwrap.wrap(
                    '{0} [{1}]'.format(k, self.default(v)),
                    width=self.column_widths[0]
                )
                if len(w) == 1:
                    w = w[0]
                    if w == spack.spec.Spec():
                        w = '--'
                when = textwrap.wrap(str(w), width=self.column_widths[1])
                allowed = v.allowed_values.replace('True, False', 'on, off')
                allowed = textwrap.wrap(allowed, width=self.column_widths[2])
                description = []
                for d_line in v.description.split('\n'):
                    description += textwrap.wrap(
                        d_line,
                        width=self.column_widths[3]
                    )
                for t in zip_longest(
                        name, when, allowed, description, fillvalue=''
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

        preferred = preferred_version(pkg)
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
        color.cprint(color.cescape(line))

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


def print_deps(title, name, dep_dict, filter_name=False):
    deps = dep_dict.items()
    if not deps:
        return

    color.cprint('')
    color.cprint(section_title('Recorded {0}:'.format(title)))
    for _, value in deps:
        dep_str = str(value).replace(name, '') if filter_name else str(value)
        dep_str = dep_str.replace('-->', ' dependencies on')
        color.cprint("    {0}".format(dep_str.strip()))


def print_installed_info(args):
    # Provide installation details for the installed spec
    env = ev.active_environment()
    specs = [spack.cmd.disambiguate_spec(spec, env)
             for spec in spack.cmd.parse_specs(args.pkg_spec)]
    if len(specs) != 1:
        # Make sure to terminate if disambiguate doesn't do so
        tty.die("Can only support one spec")

    spec = specs[0]
    dag = spec.dag_hash()
    _, record = spack.store.db.query_by_spec_hash(dag)

    pkg_vers = version('{0}@@{1}'.format(spec.name, spec.versions[0]))
    header = section_title(
        '{0}:   '
    ).format(spec.package.build_system_class) + pkg_vers
    color.cprint(header)

    color.cprint('')
    color.cprint(section_title('Hashes:'))
    color.cprint("    DAG  = {0}".format(dag))
    color.cprint("    full = {0}".format(spec.full_hash()))

    color.cprint('')
    how = 'Explicitly' if record.explicit else 'as Dependency'
    installation = 'Installed {0}:   '.format(how)
    when = date.fromtimestamp(record.installation_time).strftime("%A %d %B %Y")
    color.cprint(section_title(installation) + when)
    color.cprint("    architecture = {0}".format(spec.architecture))
    color.cprint("    prefix       = {0}".format(record.path))

    if spec.external:
        color.cprint('')
        color.cprint(section_title('External:'))
        color.cprint("    path             = {0}".format(spec.external_path))
        color.cprint("    module           = {0}".format(spec.external_modules))
        color.cprint("    extra_attributes = {0}".format(spec.extra_attributes))

    color.cprint('')
    compiler = '{0}@@{1}'.format(spec.compiler.name, spec.compiler.versions[0])
    color.cprint(section_title('Compiler:   ') + version(compiler))
    for flag, value in spec.compiler_flags.items():
        color.cprint("    {0} = {1}".format(flag, value))

    color.cprint('')
    color.cprint(section_title('Variant Settings:'))
    variants = spec.variants.items()
    if len(variants) > 1:
        for _, value in variants:
            color.cprint("    {0}".format(value))
    else:
        color.cprint("    None")

    print_deps('Dependencies', spec.name, spec.dependencies_dict(), True)
    print_deps('Dependents', spec.name, spec.dependents_dict(), False)


def info(parser, args):
    if len(args.pkg_spec) != 1:
        parser.subparsers.choices['info'].print_help()
        tty.die("Only one package or spec is allowed")

    if args.installed:
        print_installed_info(args)
        return

    # Print the static package info
    pkg = spack.repo.get(args.pkg_spec[0])
    print_text_info(pkg)
