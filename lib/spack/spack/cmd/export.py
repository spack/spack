# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
import ruamel.yaml as yaml

import llnl.util.tty as tty
import llnl.util.lang

import spack.repo
import spack.cmd.common.arguments as arguments
from spack.cmd import display_specs
from spack.filesystem_view import filter_exclude

from spack.build_systems.python import PythonPackage

import spack.util.spack_yaml as syaml
from spack.util.spack_yaml import syaml_dict, syaml_list

description = "create a package.yaml from installed packages"
section = "administration"
level = "long"


class PackagesDumper(syaml.OrderedLineDumper):
    """Customization to match common packages.yaml style
    """

    def represent_list(self, seq, flow_style=None):
        """Impose an arbitrary length limit up to flow lists
        """
        res = super(PackagesDumper, self).represent_list(seq)
        tot_len = sum(len(e.value) for e in res.value)
        res.flow_style = tot_len < 60
        return res


PackagesDumper.add_representer(syaml_list, PackagesDumper.represent_list)


def setup_parser(sp):
    scopes = spack.config.scopes()
    sp.add_argument('-f', '--format',
                    help="specify format for path/module keys",
                    metavar="FMT", default='$_$@')
    sp.add_argument('-d', '--dependencies',
                    help="add selected dependencies to the specs",
                    action='store_true')
    sp.add_argument('-m', '--module',
                    choices=spack.modules.module_types.keys(),
                    default=None,
                    help="point to modules generated for MOD",
                    metavar="MOD")
    sp.add_argument("--scope", choices=scopes,
                    default=spack.config.default_modify_scope(),
                    help="configuration scope to modify.")
    sp.add_argument("-v", "--variants", choices=('all', 'changed'),
                    default='all',
                    help="which variant flags to store: only changed ones or all (default)")
    arguments.add_common_arguments(sp, ['tags', 'constraint'])
    sp.add_argument('--unbuildable', default=[], nargs='+',
                    help='mark packages as unbuildable')
    sp.add_argument('--exclude', action='append', default=[],
                    help="exclude packages with names matching the given regex pattern")
    sp.add_argument('--explicit',
                    help='export specs that were installed explicitly',
                    default=None,
                    action='store_true')


def _to_key(spec, fmt, variants):
    """Convert the provided `spec` to a simple, identifiable string, using
    the spec format given by `fmt`, and using all variants if `variants` is
    set to ``"all"``, otherwise only the ones changed from the default
    value.
    """
    key = spec.format(fmt)
    sflags = []
    bflags = []
    for k, v in spec.variants.items():
        default = None
        if k in spec.package.variants:
            default = spec.package.variants[k][0].default
        if v.value != default or variants == 'all':
            if v.value in (True, False):
                bflags.append(v)
            elif v.name != 'patches':
                sflags.append(v)

    sflags = ' '.join(str(f) for f in sorted(sflags))
    bflags = ''.join(str(f) for f in sorted(bflags))
    key = ' '.join([e for e in (key, sflags, bflags) if len(e) > 0])
    return str(key)


def export(parser, args):
    q_args = {"explicit": True if args.explicit else any}
    specs = args.specs(**q_args)

    # Exit early if no package matches the constraint
    if not args.specs and args.constraint:
        msg = "No package matches the query: {0}"
        msg = msg.format(' '.join(args.constraint))
        tty.msg(msg)
        return

    packages = spack.config.get('packages', scope=args.scope)

    # If tags have been specified on the command line, filter by tags
    if args.tags:
        packages_with_tags = spack.repo.path.packages_with_tags(*args.tags)
        specs = [x for x in specs if x.name in packages_with_tags]

    if args.exclude:
        specs = set(filter_exclude(specs, args.exclude))

    cls = None
    if args.module:
        cls = spack.modules.module_types[args.module]

    # Add all selected specs to the external packages
    new_packages = {}
    for spec in specs:
        pkg_toplevel = new_packages.setdefault(spec.name, {})
        pkg_externals = pkg_toplevel.setdefault("externals", [])
        pkg_versions = pkg_toplevel.setdefault("version", syaml_list())

        key = _to_key(spec, args.format, args.variants)
        externality = dict(spec=key, prefix=str(spec.prefix))

        if key in [ext["spec"] for ext in pkg_externals]:
            tty.warn("spec already present, skipping: {0}".format(key))
            continue

        mod = cls(spec, 'default') if cls else None
        if mod and not mod.conf.blacklisted:
            if os.path.exists(mod.layout.filename):
                externality["modules"] = [str(mod.layout.use_name)]
            else:
                msg = "module not present for {0}"
                msg = msg.format(spec.format("$_$@"))
                tty.warn(msg)

        version = str(spec.version)
        if version not in pkg_versions:
            pkg_versions.append(version)
        pkg_externals.append(externality)

    spack.config.merge_yaml(packages, new_packages)

    # Restore ordering
    packages = syaml_dict(sorted((k, v) for (k, v) in packages.items() if len(v) > 0))
    for pkg in args.unbuildable:
        packages.setdefault(pkg, {})['buildable'] = False
    if 'all' in packages:
        packages['all'] = packages.pop('all')
    yaml.dump({'packages': packages},
              stream=sys.stdout,
              default_flow_style=False,
              Dumper=PackagesDumper)
