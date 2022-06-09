# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import inspect
import textwrap

from six.moves import zip_longest

import llnl.util.tty as tty
import llnl.util.tty.color as color
from llnl.util.tty.colify import colify

import spack.cmd.common.arguments as arguments
import spack.fetch_strategy as fs
import spack.repo
import spack.spec
from spack.package import has_test_method, preferred_version

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
        '-a', '--all', action='store_true', default=False,
        help="output all package information"
    )

    options = [
        ('--detectable', print_detectable.__doc__),
        ('--maintainers', print_maintainers.__doc__),
        ('--no-dependencies', 'do not ' + print_dependencies.__doc__),
        ('--no-variants', 'do not ' + print_variants.__doc__),
        ('--no-versions', 'do not ' + print_versions.__doc__),
        ('--phases', print_phases.__doc__),
        ('--tags', print_tags.__doc__),
        ('--tests', print_tests.__doc__),
        ('--virtuals', print_virtuals.__doc__),
    ]
    for opt, help_comment in options:
        subparser.add_argument(opt, action='store_true', help=help_comment)

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


def print_dependencies(pkg):
    """output build, link, and run package dependencies"""

    for deptype in ('build', 'link', 'run'):
        color.cprint('')
        color.cprint(section_title('%s Dependencies:' % deptype.capitalize()))
        deps = sorted(pkg.dependencies_of_type(deptype))
        if deps:
            colify(deps, indent=4)
        else:
            color.cprint('    None')


def print_detectable(pkg):
    """output information on external detection"""

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


def print_maintainers(pkg):
    """output package maintainers"""

    if len(pkg.maintainers) > 0:
        mnt = " ".join(['@@' + m for m in pkg.maintainers])
        color.cprint('')
        color.cprint(section_title('Maintainers: ') + mnt)


def print_phases(pkg):
    """output installation phases"""

    if hasattr(pkg, 'phases') and pkg.phases:
        color.cprint('')
        color.cprint(section_title('Installation Phases:'))
        phase_str = ''
        for phase in pkg.phases:
            phase_str += "    {0}".format(phase)
        color.cprint(phase_str)


def print_tags(pkg):
    """output package tags"""

    color.cprint('')
    color.cprint(section_title("Tags: "))
    if hasattr(pkg, 'tags'):
        tags = sorted(pkg.tags)
        colify(tags, indent=4)
    else:
        color.cprint("    None")


def print_tests(pkg):
    """output relevant build-time and stand-alone tests"""

    # Some built-in base packages (e.g., Autotools) define callback (e.g.,
    # check) inherited by descendant packages. These checks may not result
    # in build-time testing if the package's build does not implement the
    # expected functionality (e.g., a 'check' or 'test' targets).
    #
    # So the presence of a callback in Spack does not necessarily correspond
    # to the actual presence of built-time tests for a package.
    for callbacks, phase in [(pkg.build_time_test_callbacks, 'Build'),
                             (pkg.install_time_test_callbacks, 'Install')]:
        color.cprint('')
        color.cprint(section_title('Available {0} Phase Test Methods:'
                                   .format(phase)))
        names = []
        if callbacks:
            for name in callbacks:
                if getattr(pkg, name, False):
                    names.append(name)

        if names:
            colify(sorted(names), indent=4)
        else:
            color.cprint('    None')

    # PackageBase defines an empty install/smoke test but we want to know
    # if it has been overridden and, therefore, assumed to be implemented.
    color.cprint('')
    color.cprint(section_title('Stand-Alone/Smoke Test Methods:'))
    names = []
    pkg_cls = pkg if inspect.isclass(pkg) else pkg.__class__
    if has_test_method(pkg_cls):
        pkg_base = spack.package.PackageBase
        test_pkgs = [str(cls.test) for cls in inspect.getmro(pkg_cls) if
                     issubclass(cls, pkg_base) and cls.test != pkg_base.test]
        test_pkgs = list(set(test_pkgs))
        names.extend([(test.split()[1]).lower() for test in test_pkgs])

    # TODO Refactor START
    # Use code from package.py's test_process IF this functionality is
    # accepted.
    v_names = list(set([vspec.name for vspec in pkg.virtuals_provided]))

    # hack for compilers that are not dependencies (yet)
    # TODO: this all eventually goes away
    c_names = ('gcc', 'intel', 'intel-parallel-studio', 'pgi')
    if pkg.name in c_names:
        v_names.extend(['c', 'cxx', 'fortran'])
    if pkg.spec.satisfies('llvm+clang'):
        v_names.extend(['c', 'cxx'])
    # TODO Refactor END

    v_specs = [spack.spec.Spec(v_name) for v_name in v_names]
    for v_spec in v_specs:
        try:
            pkg = v_spec.package
            pkg_cls = pkg if inspect.isclass(pkg) else pkg.__class__
            if has_test_method(pkg_cls):
                names.append('{0}.test'.format(pkg.name.lower()))
        except spack.repo.UnknownPackageError:
            pass

    if names:
        colify(sorted(names), indent=4)
    else:
        color.cprint('    None')


def print_variants(pkg):
    """output variants"""

    color.cprint('')
    color.cprint(section_title('Variants:'))

    formatter = VariantFormatter(pkg.variants)
    for line in formatter.lines:
        color.cprint(color.cescape(line))


def print_versions(pkg):
    """output versions"""

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


def print_virtuals(pkg):
    """output virtual packages"""

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


def info(parser, args):
    pkg = spack.repo.get(args.package)

    # Output core package information
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

    # Now output optional information in expected order
    sections = [
        (args.all or args.maintainers, print_maintainers),
        (args.all or args.detectable, print_detectable),
        (args.all or args.tags, print_tags),
        (args.all or not args.no_versions, print_versions),
        (args.all or not args.no_variants, print_variants),
        (args.all or args.phases, print_phases),
        (args.all or not args.no_dependencies, print_dependencies),
        (args.all or args.virtuals, print_virtuals),
        (args.all or args.tests, print_tests),
    ]
    for print_it, func in sections:
        if print_it:
            func(pkg)

    color.cprint('')
