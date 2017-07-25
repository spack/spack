##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import argparse
import datetime
import errno
import itertools
import json
import os
import re
import shutil
import yaml

from llnl.util.filesystem import mkdirp
import llnl.util.tty as tty

import spack
import spack.cmd
from spack.util.executable import Executable
import spack.config

description = "Create RPM specs and sources for RPM installs"
section = "admin"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='rpm_command')

    # Create RPM specs
    spec_parser = sp.add_parser('spec', help=rpm_spec.__doc__)
    spec_parser.add_argument(
        '--output-dir', dest='output_dir', help="rpmbuild SOURCES directory")
    spec_parser.add_argument(
        '--universal-subspace', dest='universal_subspace',
        help="choose the subspace to use for all packages (where available)")
    spec_parser.add_argument(
        '--build-norpm-deps', dest='build_norpm_deps',
        help="""comma-separated packages which should not become rpms, but
should be built by Spack as part of creating a dependent package""")
    spec_parser.add_argument(
        '--ignore-deps', dest='ignore_deps',
        help="comma-separated packages which should not be managed by Spack")
    spec_parser.add_argument(
        '--infer-build-norpm-deps', dest='infer_build_norpm_deps',
        action="store_true",
        help="""Use package dependency types to infer whether a package should
not be an rpm""")
    spec_parser.add_argument(
        '--infer-ignore-from-rpms', dest='infer_ignore_from_rpms',
        action="store_true",
        help="track packages maintained by spack but ignored by dependencies")
    spec_parser.add_argument(
        '--specs-dir', dest='specs_dir',
        help="parse rpm config from spec files in this directory")
    spec_parser.add_argument(
        '--pkgs-dir', dest='pkgs_dir',
        help="spec templates/filters are stored here")
    spec_parser.add_argument(
        '--rpm-db-from-spec', dest='rpm_db_spec',
        help="""create rpm db from a given spec (default is to use all specs
in --specs-dir)""")
    spec_parser.add_argument(
        '--complete-specs', dest='complete_specs', action="store_true",
        help="create specs from existing properties files")
    spec_parser.add_argument(
        '--properties-only', dest='properties_only', action="store_true",
        help="only create properties files, do not create specs")
    spec_parser.add_argument(
        '--get-namespace-from-specs', dest='get_namespace_from_specs',
        action="store_true",
        help="get package namespaces from property files in spec directories")
    spec_parser.add_argument(
        '--bootstrap', dest='bootstrap', nargs=3,
        help="""<RPM name> <package name> <root dir>: create properties files
from spec for rpm which has (up to now) not been managed with Spack""")
    spec_parser.add_argument(
        '--no-redirect', dest='no_redirect', action="store_true",
        help="Spack installation in spec file will not redirect")
    spec_parser.add_argument(
        '--default-namespace', dest='default_namespace', nargs=2,
        help="""<name-scheme> <prefix-root>: use this name scheme for packages
when there is no other option""")
    spec_parser.add_argument(
        'package', nargs=argparse.REMAINDER, help="spec of package to install")

    source_parser = sp.add_parser('source', help=rpm_source.__doc__)
    source_parser.add_argument(
        'destination_path',
        help="The source archive is created under this directory")
    source_parser.add_argument(
        'spec_path',
        help="Path to an RPM spec file created by spack")
    source_parser.add_argument(
        '--no-network-build', dest='no_network_build', action="store_true",
        help="""When creating rpm source, cache packages to avoid downloading
them at build time""")


class Properties(object):
    def __init__(self, fields, **kwargs):
        """All members of 'fields' are required. keyword args which don't
           correspond to known fields are ignored."""
        self.properties = {}
        for f in fields:
            if f in kwargs:
                self.properties[f] = kwargs[f]
            else:
                raise ValueError("Missing field: " + f)

    def __getattr__(self, k):
        if k not in self.properties:
            raise TypeError("{0} is not an attribute of {1}".format(
                k, str(self.__class__.__name__)))
        return self.properties[k]

    def to_dict(self, **kwargs):
        """Input kwargs replaces properties"""
        copy = dict(self.properties)
        copy.update(kwargs)
        return copy


class RpmTemplateVars(Properties):
    PROPERTIES = set([
        'RPM_NAME', 'PROVIDES', 'VERSION', 'RELEASE', 'REQUIRES',
        'BUILD_REQUIRES', 'INSTALL', 'PACKAGE_PATH', 'CHANGE_LOG', 'SUMMARY',
        'LICENSE', 'GROUP', 'EXTRA_REQUIRES', 'EXTRA_BUILD_REQUIRES'])

    # When reading from properties files, allow for these to be unset. However
    # when the properties object is initialized in code these should be set.
    DEFAULT_PROPERTIES = {
        'EXTRA_REQUIRES': list, 'EXTRA_BUILD_REQUIRES': list}

    def __init__(self, **kwargs):
        super(RpmTemplateVars, self).__init__(
            RpmTemplateVars.PROPERTIES, **kwargs)

    def to_json(self):
        json_data = self.to_dict(CHANGE_LOG=list(self.CHANGE_LOG))
        return json.dumps(json_data, sort_keys=True, indent=4)

    @staticmethod
    def from_json(string):
        json_data = json.loads(string)
        for prop, initializer in (
                RpmTemplateVars.DEFAULT_PROPERTIES.items()):
            if prop not in json_data:
                json_data[prop] = initializer()
        return RpmTemplateVars(**json_data)


def fill_spec_template(spec_vars, spec_template):
    requires = list(itertools.chain(
        spec_vars.REQUIRES, spec_vars.EXTRA_REQUIRES))
    if requires:
        REQUIRES = 'Requires: ' + ' '.join(requires)
    else:
        REQUIRES = ''

    build_requires = list(itertools.chain(
        spec_vars.BUILD_REQUIRES, spec_vars.EXTRA_BUILD_REQUIRES))
    if build_requires:
        BUILD_REQUIRES = 'BuildRequires: ' + ' '.join(build_requires)
    else:
        BUILD_REQUIRES = ''

    if spec_vars.PROVIDES:
        PROVIDES = 'Provides: ' + spec_vars.PROVIDES
    else:
        PROVIDES = ''

    log_entries = list()
    for date, author, release_tag, comment in spec_vars.CHANGE_LOG:
        log_entries.append("* {0} {1} {2}\n- {3}".format(
            date, author, release_tag, comment))
    CHANGE_LOG = '\n\n'.join(log_entries)

    RELEASE = str(spec_vars.RELEASE)

    template_vars = spec_vars.to_dict(
        REQUIRES=REQUIRES, BUILD_REQUIRES=BUILD_REQUIRES, PROVIDES=PROVIDES,
        CHANGE_LOG=CHANGE_LOG, RELEASE=RELEASE)

    return spec_template.format(**template_vars)


class RpmSpec(object):
    """
    This does not update .spec files by parsing them, but rather keeps
    track of information that is stored in a .spec file, updates the info, and
    generates completely new files as .spec updates for an rpm package.
    """
    def __init__(self, rpm_name, summary=None, license=None, release=None,
                 change_log=None, version=None, group=None,
                 extra_requires=None, extra_build_requires=None):
        self.name = rpm_name
        # The provided change log is expected to be ordered, with the oldest
        # entry first
        self.change_log = change_log or list()
        self.release = release
        self.version = version or '1.0'
        self.group = group or 'Spack'
        self.summary = summary
        self.license = license
        self.extra_requires = extra_requires or list()
        self.extra_build_requires = extra_build_requires or list()

    @staticmethod
    def new(rpm_name, pkg_spec):
        summary = re.sub("\s+", " ", pkg_spec.package.__doc__)
        license = pkg_spec.package.license
        return RpmSpec(rpm_name, summary=summary, license=license)

    def _add_log_entry(self, author, comment):
        # Time format: weekday, month, day, year
        time = datetime.datetime.now().strftime("%a %b %d %Y")
        release_tag = "{0}-{1}".format(str(self.version), str(self.release))
        self.change_log.append((time, author, release_tag, comment))

    def new_spec_variables(self, requires, build_requires, install,
                           install_path, author=None, comment=None,
                           provides_name=None):
        if not author:
            author = "Spack"
        if not comment:
            comment = "next release"
        if not self.release:
            self.release = 1
        else:
            self.release += 1
        self._add_log_entry(author, comment)

        license = self.license or 'PLACEHOLDER'
        # When reading a spec file top-to-bottom, the newest entry should
        # appear first in the changelog
        change_log = list(reversed(self.change_log))

        return RpmTemplateVars(
            RPM_NAME=self.name, PROVIDES=provides_name, RELEASE=self.release,
            REQUIRES=requires, BUILD_REQUIRES=build_requires, INSTALL=install,
            PACKAGE_PATH=install_path, CHANGE_LOG=change_log,
            SUMMARY=self.summary, LICENSE=license, VERSION=self.version,
            GROUP=self.group, EXTRA_REQUIRES=self.extra_requires,
            EXTRA_BUILD_REQUIRES=self.extra_build_requires)


class RpmSpecParser(object):
    TAGS = set([
        'name', 'provides', 'version', 'release', 'group', 'license',
        'summary'])

    @staticmethod
    def parse(spec_contents):
        tags = {}
        clog = None
        for i, line in enumerate(spec_contents):
            m = re.match(r'([a-zA-Z]+):\s*(.*)', line)
            if m:
                tag = m.group(1)
                val = m.group(2)
                if tag.lower() in RpmSpecParser.TAGS:
                    tags[tag.lower()] = val
            if line.startswith('%changelog'):
                clog = RpmSpecParser.clogSection(spec_contents[i:])
        tags['release'] = re.match('([^%]+)', tags['release']).group(1)
        return tags, clog

    @staticmethod
    def clogSection(spec_contents):
        ids = list()
        comments = list()
        for line in spec_contents:
            if line.startswith('*'):
                tokens = line.split()[1:]
                date = ' '.join(tokens[:4])
                verrel = tokens[-1]
                auth = ' '.join(tokens[4:-1])
                ids.append((date, auth, verrel))
            elif line.startswith('-'):
                tokens = line.split()[1:]
                comments.append(' '.join(tokens))
        return list(tuple(i) + (c,) for i, c in zip(ids, comments))

    def parse_to_properties(self, spec_contents, pkg_name, root):
        tags, clog = RpmSpecParser.parse(spec_contents.split('\n'))

        # BUILDREQUIRES, REQUIRES, INSTALL, PACKAGE_PATH
        # are inferred from rpm properties, command line
        # arguments, and spec concretization
        rpm_name = tags['name']
        provides = tags.get('provides', None)
        spec_vars = RpmTemplateVars(
            RPM_NAME=rpm_name, PROVIDES=provides, RELEASE=tags['release'],
            REQUIRES=None, BUILD_REQUIRES=None, INSTALL=None,
            PACKAGE_PATH=None, CHANGE_LOG=clog, SUMMARY=tags['summary'],
            LICENSE=tags['license'], VERSION=tags['version'],
            GROUP=tags['group'], EXTRA_REQUIRES=[],
            EXTRA_BUILD_REQUIRES=[])

        # non_rpm_deps is not recorded in a spec so must be filled manually.
        # ignore_deps has the same issue. rpm_deps could be inferred from the
        # 'requires' tag but is only intended to track packages maintained by
        # Spack/rpm-install
        rpm_props = SpackRpmProperties(
            pkg_name=pkg_name, pkg_spec=None, path=None,
            rpm_deps=[], non_rpm_deps=[], ignore_deps=[],
            non_rpm_dep_specs=[], root=root,
            name_spec=rpm_name, provides_spec=provides)

        return spec_vars, rpm_props


def read_rpms_transitive(cfg_store, rpm_name, rpm_db):
    if rpm_name in rpm_db:
        return rpm_db[rpm_name].rpm

    specProps = cfg_store.get_spec_properties(rpm_name)
    rpm_props = cfg_store.get_rpm_properties(rpm_name)

    rpm_deps = set(
        read_rpms_transitive(cfg_store, dep, rpm_db)
        for dep in rpm_props.rpm_deps)

    rpm = Rpm(
        rpm_name, rpm_props.pkg_name, rpm_props.pkg_spec, rpm_props.path,
        rpm_deps, non_rpm_deps=rpm_props.non_rpm_deps,
        ignore_deps=rpm_props.ignore_deps, provides_name=specProps.PROVIDES,
        root=rpm_props.root, name_spec=rpm_props.name_spec,
        provides_spec=rpm_props.provides_spec)

    rpm_spec = RpmSpec(
        rpm_name, summary=specProps.SUMMARY, group=specProps.GROUP,
        license=specProps.LICENSE, release=int(specProps.RELEASE),
        change_log=specProps.CHANGE_LOG, version=specProps.VERSION,
        extra_requires=specProps.EXTRA_REQUIRES,
        extra_build_requires=specProps.EXTRA_BUILD_REQUIRES)

    rpm_db[rpm_name] = RpmInfo(rpm, rpm_spec)

    return rpm


class SpackRpmProperties(Properties):
    """This is intended to store details useful to Spack but not tracked by an
    RPM .spec file."""
    PROPERTIES = set([
        'pkg_name', 'pkg_spec', 'path', 'rpm_deps', 'non_rpm_deps',
        'non_rpm_dep_specs', 'ignore_deps', 'root', 'name_spec',
        'provides_spec'])

    CONVERSION = {
        'pkgName': 'pkg_name', 'pkgSpec': 'pkg_spec', 'rpmDeps': 'rpm_deps',
        'nonRpmDeps': 'non_rpm_deps', 'ignoreDeps': 'ignore_deps',
        'nameSpec': 'name_spec', 'providesSpec': 'provides_spec'}

    DEFAULT_PROPERTIES = {'non_rpm_dep_specs': list}

    @staticmethod
    def convert_old_names(properties):
        new = dict()
        for k, v in properties.items():
            new_k = SpackRpmProperties.CONVERSION.get(k, k)
            new[new_k] = v
        return new

    def __init__(self, **kwargs):
        super(SpackRpmProperties, self).__init__(
            SpackRpmProperties.PROPERTIES, **kwargs)

    def namespace(self):
        return CustomizedNamespace(
            self.name_spec, self.provides_spec, self.root)

    def to_json(self):
        json_data = self.to_dict(
            rpm_deps=list(self.rpm_deps),
            non_rpm_deps=list(self.non_rpm_deps),
            ignore_deps=list(self.ignore_deps))
        return json.dumps(json_data, sort_keys=True, indent=4)

    @staticmethod
    def from_json(string):
        json_data = SpackRpmProperties.convert_old_names(json.loads(string))
        for prop, initializer in (
                SpackRpmProperties.DEFAULT_PROPERTIES.items()):
            if prop not in json_data:
                json_data[prop] = initializer()
        return SpackRpmProperties(**json_data)


class Rpm(object):
    def __init__(
            self, name, pkg_name, pkg_spec, path, rpm_deps,
            nonrpm_dep_specs=None, non_rpm_deps=None, ignore_deps=None,
            provides_name=None, root=None, name_spec=None,
            provides_spec=None, ignore_to_external=None,
            externals=None, full_deps=None, build_deps=None):
        self.name = name
        self.pkg_name = pkg_name
        self.pkg_spec = pkg_spec
        self.path = path  # Full path - everything up to {lib/, bin/, etc.}
        self.rpm_deps = rpm_deps
        # These are dependencies which should not be created as RPMs. These are
        # implied build dependencies (but not all build dependencies are
        # managed this way).
        self.non_rpm_deps = non_rpm_deps or set()
        # These are dependencies that are typically managed by Spack but in
        # this case should be delegated to an existing system install.
        self.ignore_deps = ignore_deps or set()
        self.nonrpm_dep_specs = nonrpm_dep_specs or list()
        self.provides_name = provides_name if provides_name != name else None

        self.externals = externals or {}
        self.full_deps = full_deps
        self.build_deps = build_deps

        self.root = root
        self.name_spec = name_spec
        self.provides_spec = provides_spec

    def diff(self, other):
        """Compare with another instance of the same RPM package. Note this
        does not consider RPMs different if details of their dependencies are
        different, only if the names of the dependencies are different."""
        rpm_dep_names = frozenset(x.name for x in self.rpm_deps)
        other_rpm_dep_names = frozenset(x.name for x in other.rpm_deps)
        if self.name != other.name:
            raise ValueError("Diff is not useful for different RPM packages.")
        to_compare = list([
            (self.pkg_spec, other.pkg_spec),
            (self.path, other.path), (rpm_dep_names, other_rpm_dep_names),
            (frozenset(self.non_rpm_deps), frozenset(other.non_rpm_deps)),
            (frozenset(self.ignore_deps), frozenset(other.ignore_deps)),
            (self.provides_name, other.provides_name)])
        return set((x, y) for x, y in to_compare if x != y)

    def __eq__(self, other):
        if not isinstance(other, Rpm):
            return False
        if self.name != other.name:
            return False
        if self.diff(other):
            return False
        deps = sorted(self.rpm_deps, key=lambda x: x.name)
        other_deps = sorted(other.rpm_deps, key=lambda x: x.name)
        return deps == other_deps

    @property
    def dep_name(self):
        return self.provides_name if self.provides_name else self.name

    def path_config(self):
        pkg_to_path = self._transitive_paths()
        formatPaths = {}
        for (pkg_name, spec), path in pkg_to_path.items():
            formatPaths[pkg_name] = {'paths': {spec: path}, 'buildable': False}
        # Undo path config for root
        del formatPaths[self.pkg_name]
        return {'packages': formatPaths} if formatPaths else {}

    def new_rpm_spec_variables(self, rpm_spec, redirect=True):
        requires = list(self.full_deps)
        build_requires = list(self.full_deps) + list(self.build_deps)

        set_path = "--install-path={0}".format(self.path)
        install_args = ['./bin/spack install', '--verbose']
        if redirect:
            install_args.append('--destdir=%{buildroot}')
        skip_deps = self.ignore_deps | set(x.pkg_name for x in self.rpm_deps)
        if skip_deps:
            install_args.append('--skip-deps=' + ','.join(skip_deps))
        install_args.extend([set_path, self.pkg_spec])
        install = ' '.join(install_args)

        return rpm_spec.new_spec_variables(
            requires, build_requires, install, self.path,
            provides_name=self.provides_name)

    def _transitive_paths(self):
        paths = {(self.pkg_name, self.pkg_spec): self.path}
        for dep in self.rpm_deps:
            paths.update(dep._transitive_paths())
        return paths

    def direct_deps(self):
        return set(self.rpm_deps) - set(itertools.chain.from_iterable(
            x.transitive_deps() for x in self.rpm_deps))

    def transitive_deps(self):
        return set(itertools.chain(
            itertools.chain.from_iterable(
                x.transitive_deps() for x in self.rpm_deps),
            set(self.rpm_deps)))

    def write_files_for_install(
            self, rpm_spec, cfg_store, redirect=True):
        spec_vars = self.new_rpm_spec_variables(rpm_spec, redirect=redirect)
        cfg_store.save_spec_properties(self.name, spec_vars.to_json())

        spack_rpm_props = SpackRpmProperties(
            pkg_name=self.pkg_name, pkg_spec=self.pkg_spec, path=self.path,
            rpm_deps=set(dep_rpm.name for dep_rpm in self.rpm_deps),
            non_rpm_deps=self.non_rpm_deps, ignore_deps=self.ignore_deps,
            root=self.root, name_spec=self.name_spec,
            provides_spec=self.provides_spec,
            non_rpm_dep_specs=self.nonrpm_dep_specs)
        cfg_store.save_rpm_properties(self.name, spack_rpm_props.to_json())

        system_pkg_cfg = list()
        for dep in self.ignore_deps:
            if dep in self.externals:
                continue

            depCfg = cfg_store.determine_dep_pkg_cfg(self.name, dep)
            if not depCfg:
                tty.msg("No package.yaml associated with dependency " + dep)
            else:
                system_pkg_cfg.append(depCfg)
        path_cfg = self.path_config()
        for pkgCfg in system_pkg_cfg:
            spack.config._merge_yaml(path_cfg, pkgCfg)
        if self.externals:
            externals_cfg = {'packages': self.externals}
            spack.config._merge_yaml(path_cfg, externals_cfg)
        if path_cfg:
            cfg_store.savePkgCfg(
                self.name, yaml.dump(path_cfg, default_flow_style=False))


def generate_rpms_transitive(args):
    cfg_store = ConfigStore(
        args.output_dir, specs_dir=args.specs_dir, pkgs_dir=args.pkgs_dir)

    if args.complete_specs:
        cfg_store.complete_specs()
        return

    if args.bootstrap:
        rpm_name, pkg_name, root = args.bootstrap
        spec_contents = cfg_store.get_spec(rpm_name)
        spec_vars, rpm_props = RpmSpecParser().parse_to_properties(
            spec_contents, pkg_name, root)

        cfg_store.save_rpm_properties(rpm_name, rpm_props.to_json())
        cfg_store.save_spec_properties(rpm_name, spec_vars.to_json())
        return

    if cfg_store.specs_dir:
        rpm_db = {}

        if args.rpm_db_spec:
            seed = args.rpm_db_spec
            if seed.endswith('.spec'):
                seed = seed[:-5]
            rpm_seeds = [seed]
        else:
            rpm_seeds = list()
            for root, dirs, files in os.walk(cfg_store.specs_dir):
                rpm_seeds.extend(f[:-5] for f in files if f.endswith('.spec'))

        for seed in rpm_seeds:
            read_rpms_transitive(cfg_store, seed, rpm_db)
    else:
        rpm_db = {}

    subspace_cfg = SubspaceConfig()
    subspace_cfg.set_up_namespaces(
        args.universal_subspace, args.get_namespace_from_specs,
        args.default_namespace, cfg_store)

    build_norpm_deps = expandOption(args.build_norpm_deps)
    ignore_deps = expandOption(args.ignore_deps)

    specs = spack.cmd.parse_specs(args.package, concretize=True)
    if len(specs) > 1:
        tty.die("Only 1 top-level package can be specified")
    top_spec = iter(specs).next()
    new = set()
    dependency_cfg = DependencyConfig(
        build_norpm_deps, ignore_deps, rpm_db, subspace_cfg,
        args.infer_build_norpm_deps, args.infer_ignore_from_rpms)
    rpm = resolve_autoname(
        top_spec, subspace_cfg, rpm_db, new, dependency_cfg)

    # RPMs may have been created that are not going to be used
    new &= rpm.transitive_deps()

    # TODO: For now, the rpm associated with the top-level spec always
    # generates a new spec (regardless of whether it changed) since as of now
    # there is not sufficient functionality to check this properly (i.e. a
    # package hash)
    rpm.pkg_spec = top_spec.format()
    for rpm in set(itertools.chain([rpm], new)):
        tty.msg("New or updated rpm: " + rpm.name)
        rpm_spec = rpm_db[rpm.name].spec
        rpm.write_files_for_install(
            rpm_spec, cfg_store, redirect=(not args.no_redirect))

    if not args.properties_only:
        cfg_store.complete_specs()


class DependencyConfig(object):
    def __init__(self, build_norpm_deps, ignore_deps, rpm_db, subspace_cfg,
                 infer_build_norpm_deps=False, infer_ignore_from_rpms=False,
                 infer_ignore_from_nobuild=True):
        self.build_norpm_deps = build_norpm_deps
        self.overwrite_build_norpm_deps = self.build_norpm_deps is not None
        self.ignore_deps = ignore_deps or set()

        self.infer_build_norpm_deps = infer_build_norpm_deps
        self.infer_ignore_from_rpms = infer_ignore_from_rpms
        self.infer_ignore_from_nobuild = infer_ignore_from_nobuild

        self.rpm_db = rpm_db
        self.subspace_cfg = subspace_cfg

    def collect_transitive_ignore_deps(self, pkg_spec):
        collected = set()
        for spec in pkg_spec.traverse():
            rpm = self._prev_rpm(pkg_spec)
            if rpm:
                collected.update(rpm.ignore_deps)
        return collected

    def _prev_rpm(self, pkg_spec):
        namespace = self.subspace_cfg.get_namespace(pkg_spec.name)
        rpm_name = namespace.name(pkg_spec)
        if rpm_name in self.rpm_db:
            return self.rpm_db[rpm_name].rpm

    def ignore_deps_for_pkg(self, pkg_spec):
        collected = set(self.ignore_deps)
        collected.update(self.subspace_cfg.get_ignore_deps(pkg_spec.name))

        # Infer which packages to ignore based on prior RPMs
        if self.infer_ignore_from_rpms:
            collected.update(self.collect_transitive_ignore_deps(pkg_spec))
        if self.infer_ignore_from_nobuild:
            collected.update(self.nobuild_from_pkgs_cfg())
        return collected

    def nobuild_from_pkgs_cfg(self):
        packages = spack.config.get_config('packages')
        return set(pkg_name for pkg_name, info in packages.items()
                   if not info.get('buildable', True))

    def external_pkg_cfg(self, pkg_spec, ignore_deps):
        packages = spack.config.get_config('packages')
        externals = {}
        replace = {}
        for pkg_name, info in packages.items():
            if pkg_name in ignore_deps:
                dep = pkg_spec[pkg_name]
                path_entries = info.get('paths', {})
                replace_entries = info.get('rpms', {})
                for spec_str, path in path_entries.items():
                    if dep.satisfies(spack.spec.Spec(spec_str)):
                        externals[str(pkg_name)] = {
                            'paths': {str(spec_str): str(path)},
                            'buildable': False}
                        if spec_str in replace_entries:
                            replace[str(pkg_name)] = replace_entries[spec_str]
                        break
        return externals, replace

    def split_by_rpm_deptype(self, pkg_spec, replace, spack_rpms):
        build_deps = (set(pkg_spec.traverse()) -
                      set(pkg_spec.traverse(deptype=('link', 'run'))))
        build_deps = set(x.name for x in build_deps)
        build_rpms = set()
        full_rpms = set()
        for pkg_name, rpms in replace.items():
            if pkg_name in build_deps:
                build_rpms.update(rpms)
            else:
                full_rpms.update(rpms)
        for pkg_name, rpm in spack_rpms.items():
            if pkg_name in build_deps:
                build_rpms.add(rpm)
            else:
                full_rpms.add(rpm)
        return build_rpms, full_rpms

    def direct_deps(self, pkg_spec):
        deps = set(pkg_spec.dependencies())
        indirect_deps = set(itertools.chain.from_iterable(
            x.traverse(root=False) for x in deps))
        direct = deps - indirect_deps
        return set(x.name for x in direct)

    def build_norpm_deps_for_pkg(self, pkg_spec):
        collected = set()
        if self.overwrite_build_norpm_deps:
            collected.update(self.build_norpm_deps)
        else:
            rpm = self._prev_rpm(pkg_spec)
            if rpm and rpm.non_rpm_deps:
                collected.update(rpm.non_rpm_deps)

        # Infer which packages not to create as RPMs based on dependency info
        # stored in the package.py file
        if self.infer_build_norpm_deps:
            dependencies = pkg_spec.dependencies_dict()
            collected.update(
                dep_name for dep_name, dep in dependencies.items()
                if set(dep.deptypes) == set(['build']))
        return collected


def resolve_autoname(
        pkg_spec, subspace_cfg, rpm_db, new, dependency_cfg, visited=None):
    """Because this automatically generates rpm names it can create rpms
    transitively.

    Notes:

     * If a package is marked as a build dependency it is a build dependency
       everywhere (even if other packages require it as a runtime dependency an
       rpm will not be generated)
     * Transitive dependencies of packages marked as build dependencies will
       also not generate RPMs unless there is a path from the root which does
       not traverse any build dependencies
    """
    if not visited:
        visited = set()

    namespace = subspace_cfg.get_namespace(pkg_spec.name)
    rpm_name = namespace.name(pkg_spec)
    if pkg_spec in visited:
        return rpm_db[rpm_name].rpm
    visited.add(pkg_spec)

    ignore_deps = dependency_cfg.ignore_deps_for_pkg(pkg_spec)
    build_norpm_deps = dependency_cfg.build_norpm_deps_for_pkg(pkg_spec)
    omit_deps = ignore_deps | build_norpm_deps

    rpm_deps = set()
    for dep_name, dep in pkg_spec.dependencies_dict().items():
        if dep_name in omit_deps:
            pass
        else:
            dep_rpm = resolve_autoname(
                dep.spec, subspace_cfg, rpm_db, new, dependency_cfg, visited)
            rpm_deps.add(dep_rpm)

    dep_pkg_names = set(x.pkg_name for x in rpm_deps)
    transitive_norpm = get_build_norpm_transitive(
        pkg_spec, build_norpm_deps, ignore_deps, dep_pkg_names)

    ignore_deps = (set(x.name for x in pkg_spec.traverse()) &
                   ignore_deps)
    externals, replace = dependency_cfg.external_pkg_cfg(pkg_spec, ignore_deps)
    build_norpm_deps = set(pkg_spec.dependencies_dict()) & build_norpm_deps
    build_norpm_deps -= ignore_deps

    direct_deps = dependency_cfg.direct_deps(pkg_spec)
    direct_rpm_deps = set(
        x for x in rpm_deps
        if x.pkg_name in direct_deps)
    spec_to_rpm_name = dict((x.pkg_name, x.name) for x in direct_rpm_deps)
    replace = dict((x, y) for x, y in replace.items()
                   if x in direct_deps)
    build_rpms, full_rpms = dependency_cfg.split_by_rpm_deptype(
        pkg_spec, replace, spec_to_rpm_name)

    extra_build_rpms, extra_full_rpms = (
        subspace_cfg.get_extra_system_deps(pkg_spec.name))
    rpm = Rpm(
        rpm_name, pkg_spec.name, pkg_spec.format(),
        namespace.path(pkg_spec), rpm_deps,
        nonrpm_dep_specs=list(x.format() for x in transitive_norpm),
        non_rpm_deps=build_norpm_deps,
        ignore_deps=ignore_deps,
        provides_name=namespace.provides_name(pkg_spec),
        root=namespace.root, name_spec=namespace.name_spec,
        provides_spec=namespace.provides_spec, externals=externals,
        full_deps=full_rpms | extra_full_rpms,
        build_deps=build_rpms | extra_build_rpms)

    if rpm_name not in rpm_db:
        rpm_spec = RpmSpec.new(rpm_name, pkg_spec)
        new.add(rpm)
        rpm_info = RpmInfo(rpm, rpm_spec)
        rpm_db[rpm_name] = rpm_info
    else:
        old_rpm = rpm_db[rpm_name].rpm
        # It is never correct for two different spack packages to have matching
        # RPM names: this is easy to avoid (e.g. if the name projection
        # includes the spack package name)
        if rpm.pkg_name != old_rpm.pkg_name:
            raise ValueError(
                "Name collision: new RPM for" +
                "{0} collides with existing RPM for {1}".format(
                    rpm.pkg_name, old_rpm.pkg_name))
        # Check if the rpm has changed in some way
        diff = rpm.diff(old_rpm)
        if diff:
            tty.msg("RPM update: " + rpm.pkg_name)
            tty.msg(
                "{0}:\n{1}".format(
                    rpm.name,
                    '\n'.join('/'.join((str(x), str(y))) for x, y in diff)))
            rpm_db[rpm_name].rpm = rpm
            new.add(rpm)
        else:
            rpm = old_rpm

    # TODO: if package.py contents change then a new rpm release should be made

    return rpm


def disconnected(pkg_spec, remove):
    return (set(pkg_spec.traverse()) -
            connected_after_removal(pkg_spec, remove))


def connected_after_removal(pkg_spec, remove):
    return set(x for x in pkg_spec.traverse(
               visited=set(remove), cover='edges', key=lambda x: x.name)
               if x.name not in remove)


def get_build_norpm_transitive(pkg_spec, norpm_deps, ignore_deps, rpm_deps):
    return (connected_after_removal(
                pkg_spec, set(ignore_deps) | set(rpm_deps)) -  # NOQA: ignore=E126
            set([pkg_spec]))


def get_pkgspec_for_rpm(concrete_spec, transitive_norpm):
    base = concrete_spec.format()
    base += ' '.join([concrete_spec[x].format() for x in transitive_norpm
                      if x in concrete_spec])
    return base


class MissingNamespaceError(Exception):
    pass


class CustomizedNamespace(object):
    def __init__(self, name_spec, provides_spec, root):
        self.name_spec = str(name_spec)
        self.provides_spec = provides_spec or self.name_spec
        self.root = root

    def name(self, spec):
        return spec.format(self.name_spec)

    def provides_name(self, spec):
        return spec.format(self.provides_spec)

    def path(self, spec):
        return os.path.join(self.root, spec.name, self.provides_name(spec))


class RpmInfo(object):
    def __init__(self, rpm, rpm_spec):
        self.rpm = rpm
        self.spec = rpm_spec


class ConfigStore(object):
    """Stores and retrieves information related to rpms and their specs. The
    user can start with Spack-package-level configuration which is stored at
    the rpm-package-level as associated RPMs are created. It expects the
    following directory structure:

    <pkgs_dir>/
        <pkg name>/
            spec.skel
            filter* (any exe with the prefix "filter")
            systempkg.yaml

        ... (one folder per package)

    and

    <specs_dir>/
        <rpm name>/
            spec.skel
            filter*
            <deppkg>_systempkg.yaml (one file for each dep maintained by system)  # NOQA: ignore=E501
            rpmprops.json
            specvars.json
            <rpm name>.spec

        ... (one folder per rpm)
    """
    def __init__(self, output_dir, pkgs_dir=None, specs_dir=None):
        self.pkgs_dir = pkgs_dir
        self.specs_dir = specs_dir
        self.output_dir = output_dir

    def determine_spec_template(self, rpm_name, pkg_name):
        search_paths = []
        search_paths.append(self.output_location(rpm_name, 'spec.skel'))
        if self.specs_dir:
            search_paths.append(self.specs_location(rpm_name, 'spec.skel'))
        if self.pkgs_dir:
            search_paths.append(self.pkgs_location(pkg_name, 'spec.skel'))
        template_path = self.get_first_existing(search_paths, self.find)
        if template_path:
            template = retrieve_file_contents(template_path)
        else:
            tty.msg("Using default spec template for " + pkg_name)
            template = default_spec()

        self.saveRpmCfg(rpm_name, 'spec.skel', template)
        return template

    def determine_dep_pkg_cfg(self, rpm_name, dep_pkg_name):
        """For packages that should not be managed by Spack"""
        dst_file = dep_pkg_name + '_systempkg.yaml'
        search_paths = []
        if self.specs_dir:
            search_paths.append(self.specs_location(rpm_name, dst_file))
        if self.pkgs_dir:
            search_paths.append(
                self.pkgs_location(dep_pkg_name, 'systempkg.yaml'))
        pkg_cfg_path = self.get_first_existing(search_paths, self.find)

        if not pkg_cfg_path:
            return
        shutil.copy(
            pkg_cfg_path, self.set_up_output_location(rpm_name, dst_file))
        with open(pkg_cfg_path, 'rb') as F:
            return yaml.safe_load(F)

    def apply_transform(self, rpm_name, pkg_name):
        vars_file = self.output_location(rpm_name, 'specvars.json')
        search_paths = []
        if self.specs_dir:
            search_paths.append(self.specs_location(rpm_name))
        if self.pkgs_dir:
            search_paths.append(self.pkgs_location(pkg_name))
        script_path = self.get_first_existing(search_paths, self.find_script)
        if not script_path:
            return
        Executable(script_path)(vars_file)
        shutil.copy(script_path, self.set_up_output_location(
            rpm_name, os.path.basename(script_path)))
        with open(vars_file, 'rb') as F:
            return RpmTemplateVars.from_json(F.read())

    def specs_location(self, rpm_name, fName=None):
        base = os.path.join(self.specs_dir, rpm_name)
        return os.path.join(base, fName) if fName else base

    def pkgs_location(self, pkg_name, fName=None):
        base = os.path.join(self.pkgs_dir, pkg_name)
        return os.path.join(base, fName) if fName else base

    def get_rpms(self):
        return set(os.listdir(self.specs_dir))

    def get_spec(self, rpm_name):
        """Should only be called if specs_dir is set"""
        specName = (
            rpm_name + '.spec' if not rpm_name.endswith('.spec') else rpm_name)
        return retrieve_file_contents(self.specs_location(rpm_name, specName))

    def get_rpm_properties(self, rpm_name, use_output=False):
        """Should only be called if specs_dir is set"""
        location_fn = (
            self.output_location if use_output else self.specs_location)
        return SpackRpmProperties.from_json(
            retrieve_file_contents(location_fn(rpm_name, 'rpmprops.json')))

    def get_spec_properties(self, rpm_name, use_output=False):
        """Should only be called if specs_dir is set"""
        location_fn = (
            self.output_location if use_output else self.specs_location)
        return RpmTemplateVars.from_json(
            retrieve_file_contents(location_fn(rpm_name, 'specvars.json')))

    def save_spec_properties(self, rpm_name, content):
        self.saveRpmCfg(rpm_name, 'specvars.json', content)

    def save_rpm_properties(self, rpm_name, content):
        self.saveRpmCfg(rpm_name, 'rpmprops.json', content)

    def save_spec(self, rpm_name, content):
        self.saveRpmCfg(rpm_name, '%s.spec' % rpm_name, content)

    def savePkgCfg(self, rpm_name, content):
        self.saveRpmCfg(rpm_name, 'packages.yaml', content)

    def saveRpmCfg(self, rpm_name, fName, content):
        with open(self.set_up_output_location(rpm_name, fName), 'wb') as F:
            F.write(content)

    def set_up_output_location(self, rpm_name, fName):
        path = self.output_location(rpm_name, fName)
        directory = os.path.dirname(path)
        try:
            os.makedirs(directory)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(directory):
                pass
            else:
                raise

        return path

    def output_location(self, rpm_name, fName):
        return os.path.join(self.output_dir, rpm_name, fName)

    def find_script(self, directory):
        if not os.path.exists(directory):
            return
        files = set(os.listdir(directory))
        scripts = list(x for x in files if x.startswith('filter'))
        scripts = list(os.path.join(directory, x) for x in scripts)
        scripts = list(x for x in scripts if os.access(x, os.X_OK))
        if scripts:
            return iter(scripts).next()

    def find(self, path):
        return path if os.path.exists(path) else None

    def get_first_existing(self, paths, find):
        for path in paths:
            result = find(path)
            if result:
                return result

    def complete_specs(self):
        rpm_names = os.listdir(self.output_dir)
        for rpm_name in rpm_names:
            try:
                self.complete_spec(rpm_name)
            except KeyError as e:
                template_location = self.output_location(rpm_name, 'spec.skel')
                key = e.args[0]
                raise ValueError(
                    "{0} has unaddressed key {1},".format(
                        template_location, key) +
                    " edit and rerun with --complete-specs")

    def complete_spec(self, rpm_name):
        rpm_props = self.get_rpm_properties(rpm_name, use_output=True)
        self.apply_transform(rpm_name, rpm_props.pkg_name)
        spec_vars = self.get_spec_properties(rpm_name, use_output=True)
        spec_template = self.determine_spec_template(
            rpm_name, rpm_props.pkg_name)
        spec_contents = fill_spec_template(spec_vars, spec_template)
        self.save_spec(rpm_name, spec_contents)


class SubspaceConfig(object):
    """Manages configuration for:

    - Determining descriptors for Spack packages (to generate names from specs)
    - Specifying spack packages that are system-managed (as an alternative to
      the options and in addition to what is collected from existing Spack RPM
      deps)

    Name projections are created from: rpm properties files of existing
    Spack-built packages; rpms.yaml configuration file. Using the rpm
    properties files is optional; if they are used then they have priority
    over the yaml config.
    """
    def set_up_namespaces(
            self, universal_subspace, get_namespace_from_specs,
            default_namespace, cfg_store):

        self.pkg_to_subspace = resolve_pkg_to_subspace(universal_subspace)
        pkg_to_namespace = resolve_pkg_to_namespace(self.pkg_to_subspace)
        if get_namespace_from_specs:
            pkg_to_namespace.update(self.get_namespaces_from_specs(cfg_store))
        self.pkg_to_namespace = pkg_to_namespace

        if default_namespace:
            name_spec, prefix = default_namespace
            self.default_namespace = CustomizedNamespace(
                name_spec, name_spec, prefix)
        else:
            self.default_namespace = None

    def get_ignore_deps(self, pkg_name):
        return self._get_subspace_property(pkg_name, 'ignore-deps', [])

    def get_extra_system_deps(self, pkg_name):
        extra_full_deps = set(
            self._get_subspace_property(pkg_name, 'add-system-deps', []))
        extra_build_deps = set(
            self._get_subspace_property(pkg_name, 'add-system-build-deps', []))
        return extra_build_deps, extra_full_deps

    def get_namespace(self, pkg_name, required=True):
        namespace = self.pkg_to_namespace.get(
            pkg_name,
            self.pkg_to_namespace.get('all', self.default_namespace))
        if not namespace and required:
            raise MissingNamespaceError("No namespace for " + pkg_name)
        return namespace

    def _get_subspace_property(self, pkg_name, prop, default=None):
        subspace = self.pkg_to_subspace.get(pkg_name, {})
        default_subspace = self.pkg_to_subspace.get('all', {})
        return subspace.get(prop, default_subspace.get(prop, default))

    def get_namespaces_from_specs(self, cfg_store):
        pkg_to_namespace = {}
        for rpm_name in cfg_store.get_rpms():
            rpm_props = cfg_store.get_rpm_properties(rpm_name)
            pkg_to_namespace[rpm_props.pkg_name] = rpm_props.namespace()
        return pkg_to_namespace


# TODO: move this to config?
def resolve_pkg_to_namespace(pkg_to_subspace):
    packages = spack.config.get_config('rpms')
    pkg_to_namespace = {}
    for pkg_name, info in packages.items():
        subspace = pkg_to_subspace.get(pkg_name, {})
        if not all(p in subspace for p in ['name', 'prefix']):
            continue
        name_spec = subspace['name']
        provides_spec = subspace.get('provides', name_spec)
        root = subspace['prefix']
        pkg_to_namespace[pkg_name] = CustomizedNamespace(
            name_spec, provides_spec, root)
    return pkg_to_namespace


def resolve_pkg_to_subspace(universal_subspace=None):
    pkg_to_subspace = {}
    packages = spack.config.get_config('rpms')
    for pkg_name, info in packages.items():
        subspaces = info.get('subspaces', {})
        pkg_to_subspace[pkg_name] = subspaces.get(universal_subspace, info)
    return pkg_to_subspace


def retrieve_file_contents(path):
    with open(path, 'rb') as F:
        return F.read()


def expandOption(opt):
    """Distinguish between an empty option vs. not specifying the option
    at all"""
    if opt or opt == '':
        return set(opt.split(','))


def rpm_spec(args):
    """Given a Spack spec, create RPM spec. This also creates Spack-specific
    property files to manage future updates to the RPM."""
    generate_rpms_transitive(args)


def rpm_source(args):
    """Package this Spack repository into a source archive that the RPM spec
    can use to build the RPM."""
    create_rpm_source(
        args.destination_path, args.spec_path, args.no_network_build)


def rpm(parser, args):
    action = {'spec': rpm_spec,
              'source': rpm_source}
    action[args.rpm_command](args)


def create_rpm_source(dst_path, spec_file_path, cache_resources=False):
    cfg_dir = os.path.join(os.path.dirname(spec_file_path), os.pardir)
    cfg_store = ConfigStore(None, specs_dir=cfg_dir)
    _, spec_fname = os.path.split(spec_file_path)
    rpm_name = spec_fname[:-5]
    spec_props = cfg_store.get_spec_properties(rpm_name)

    source_name = "{0}-{1}".format(rpm_name, spec_props.VERSION)
    spack_prefix = spack.spack_root  # Prefix for this spack install
    spack_dst = os.path.join(dst_path, source_name)
    mkdirp(spack_dst)

    def spack_move(rel_path):
        head, tail = os.path.split(subdir)
        if head:
            mkdirp(os.path.join(spack_dst, head))
        dst = os.path.join(spack_dst, rel_path)

        shutil.copytree(os.path.join(spack_prefix, subdir), dst)

    for subdir in ['bin', 'lib', 'etc', 'var/spack/repos']:
        tty.msg("Copying: " + subdir)
        spack_move(subdir)

    if cache_resources:
        mkdirp(os.path.join(spack_dst, 'var/spack/cache'))

        rpm_props = cfg_store.get_rpm_properties(rpm_name)
        specs = [rpm_props.pkg_spec] + list(rpm_props.non_rpm_dep_specs)
        for spec in specs:
            tty.msg("Staging: " + str(spec))
            spec = spack.spec.Spec(spec)
            spec._mark_concrete()
            package = spack.repo.get(spec)
            package.do_stage()
            source_path = os.path.abspath(package.stage.archive_file)

            for component in package.stage:
                relative_path = component.mirror_path
                dst_path = os.path.join(
                    spack_dst, 'var/spack/cache', relative_path)
                mkdirp(os.path.dirname(dst_path))
                shutil.copy(source_path, dst_path)

            package.do_clean()


def default_spec():
    return """#don't construct debug package
%define          debug_package %{{nil}}
#avoid stripping binary (and just do compression)
%define        __os_install_post /usr/lib/rpm/brp-compress

Summary: {SUMMARY}
Name: {RPM_NAME}
{PROVIDES}
Version: 1.0
Release: {RELEASE}%{{?dist}}
License: {LICENSE}
Group: {GROUP}
{BUILD_REQUIRES}
{REQUIRES}
SOURCE0 : %{{name}}-%{{version}}.tar.gz

%description
%{{summary}}

%prep
%setup -q

%build
# Empty section.

%install
rm -rf %{{buildroot}}
{INSTALL}
find %{{buildroot}}/{PACKAGE_PATH} -name "build.out" | xargs rm
find %{{buildroot}}/{PACKAGE_PATH} -name "build.env" | xargs rm

%clean
rm -rf %{{buildroot}}

%files
%defattr(-,root,root,-)
{PACKAGE_PATH}

%changelog
{CHANGE_LOG}
"""
