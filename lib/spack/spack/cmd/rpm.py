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
import cPickle as pickle
import datetime
import errno
import itertools
import json
import os
import re
import shutil
import yaml

import llnl.util.tty as tty

import spack
import spack.cmd
from spack.util.executable import Executable
import spack.config

description = "Create RPM specs and sources for RPM installs"

def setup_parser(subparser):
    subparser.add_argument(
        '--output-dir', dest='outputDir', help="rpmbuild SOURCES directory")
    subparser.add_argument(
        '--universal-subspace', dest='universalSubspace',
        help="choose the subspace to use for all packages (where available)")
    subparser.add_argument(
        '--build-deps', dest='buildDeps',
        help="comma-separated packages which should not become rpms")
    subparser.add_argument(
        '--ignore-deps', dest='ignoreDeps',
        help="comma-separated packages which should not be managed by Spack")
    subparser.add_argument(
        '--specs-dir', dest='specsDir',
        help="parse rpm config from spec files in this directory")
    subparser.add_argument(
        '--pkgs-dir', dest='pkgsDir', help="spec templates/filters are stored here")
    subparser.add_argument(
        '--rpm-db-from-spec', dest='rpmDbSpec',
        help="create rpm db from a given spec (default is to use all specs in --specs-dir)")
    subparser.add_argument(
        '--complete-specs', dest='completeSpecs', action="store_true", 
        help="create specs from existing properties files")
    subparser.add_argument(
        '--properties-only', dest='propertiesOnly', action="store_true", 
        help="only create properties files, do not create specs")
    subparser.add_argument(
        '--get-namespace-from-specs', dest='getNamespaceFromSpecs',
        action="store_true", 
        help="get package namespaces from property files in spec directories")
    subparser.add_argument(
        '--bootstrap', dest='bootstrap', nargs=3,
        help="create properties files from spec for rpm which has (up to now) not been managed with Spack")
    subparser.add_argument(
        '--infer-build-deps', dest='inferBuildDeps', action="store_true", 
        help="<RPM name> <package name> <root dir>: use package dependency types to infer whether a package should not be an rpm")
    subparser.add_argument(
        '--infer-ignore-deps', dest='inferIgnoreDeps', action="store_true", 
        help="track packages maintained by spack but ignored by dependencies")
    subparser.add_argument(
        '--no-redirect', dest='noRedirect', action="store_true", 
        help="Spack installation in spec file will not redirect")
    subparser.add_argument(
        '--default-namespace', dest='defaultNamespace', nargs=2,
        help="<name-scheme> <prefix-root>: use this name scheme for packages when there is no other option")
    subparser.add_argument(
        'package', nargs=argparse.REMAINDER, help="spec of package to install")

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
    PROPERTIES = set(['RPM_NAME', 'PROVIDES', 'VERSION', 'RELEASE', 'REQUIRES',
        'BUILD_REQUIRES', 'INSTALL', 'PACKAGE_PATH', 'CHANGE_LOG', 'SUMMARY', 
        'LICENSE', 'GROUP', 'SYSTEM_REQUIRES', 'SYSTEM_BUILD_REQUIRES'])

    # When reading from properties files, allow for these to be unset. However
    # when the properties object is initialized in code these should be set. 
    DEFAULT_PROPERTIES = {'SYSTEM_REQUIRES':list, 'SYSTEM_BUILD_REQUIRES':list}

    def __init__(self, **kwargs):
        super(RpmTemplateVars, self).__init__(
            RpmTemplateVars.PROPERTIES, **kwargs)

    def toJson(self):
        jsonData = self.to_dict(CHANGE_LOG=list(self.CHANGE_LOG))
        return json.dumps(jsonData, sort_keys=True, indent=4)
    
    @staticmethod
    def fromJson(string):
        jsonData = json.loads(string)
        for prop, initializer in RpmTemplateVars.DEFAULT_PROPERTIES.iteritems():
            if prop not in jsonData:
                jsonData[prop] = initializer()
        return RpmTemplateVars(**jsonData)

def fill_spec_template(specVars, specTemplate):
    requires = list(itertools.chain(
        specVars.REQUIRES, specVars.SYSTEM_REQUIRES))
    if requires:
        REQUIRES = 'Requires: ' + ' '.join(requires)
    else:
        REQUIRES = ''
    
    build_requires = list(itertools.chain(
        specVars.BUILD_REQUIRES, specVars.SYSTEM_BUILD_REQUIRES))
    if build_requires:
        BUILD_REQUIRES = 'BuildRequires: ' + ' '.join(build_requires)
    else:
        BUILD_REQUIRES = ''
    
    if specVars.PROVIDES:
        PROVIDES = 'Provides: ' + specVars.PROVIDES
    else:
        PROVIDES = ''

    logEntries = list()
    for date, author, releaseTag, comment in specVars.CHANGE_LOG:
        logEntries.append("* {0} {1} {2}\n- {3}".format(
            date, author, releaseTag, comment))
    CHANGE_LOG = '\n\n'.join(logEntries)
    
    RELEASE = str(specVars.RELEASE)
    
    templateVars = specVars.to_dict(REQUIRES=REQUIRES, 
        BUILD_REQUIRES=BUILD_REQUIRES, PROVIDES=PROVIDES, 
        CHANGE_LOG=CHANGE_LOG, RELEASE=RELEASE)
    
    return specTemplate.format(**templateVars)

class RpmSpec(object):
    """
    This does not update .spec files by parsing them, but rather keeps
    track of information that is stored in a .spec file, updates the info, and 
    generates completely new files as .spec updates for an rpm package.
    """
    def __init__(self, rpmName, summary=None, license=None, release=None, 
            changeLog=None, version=None, group=None, systemRequires=None,
            systemBuildRequires=None):
        self.name = rpmName
        # The provided change log is expected to be ordered, with the oldest 
        # entry first 
        self.changeLog = changeLog or list()
        self.release = release
        self.version = version or '1.0'
        self.group = group or 'Spack'
        self.summary = summary
        self.license = license
        self.systemRequires = systemRequires or list()
        self.systemBuildRequires = systemBuildRequires or list()
    
    @staticmethod
    def new(rpmName, pkgSpec):
        summary = re.sub("\s+", " ", pkgSpec.package.__doc__)
        license = pkgSpec.package.license
        return RpmSpec(rpmName, summary=summary, license=license)
    
    def _add_log_entry(self, author, comment):
        # Time format: weekday, month, day, year
        time = datetime.datetime.now().strftime("%a %b %d %Y") 
        releaseTag = "{0}-{1}".format(str(self.version), str(self.release))
        self.changeLog.append((time, author, releaseTag, comment))
    
    def new_spec_variables(self, deps, install, installPath, author=None, 
            comment=None, providesName=None):
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
        # When reading a spec file top-to-bottom, the newest entry should appear
        # first in the changelog
        changeLog = list(reversed(self.changeLog))
        
        return RpmTemplateVars(RPM_NAME=self.name, PROVIDES=providesName, 
            RELEASE=self.release, REQUIRES=deps, BUILD_REQUIRES=deps,
            INSTALL=install, PACKAGE_PATH=installPath, CHANGE_LOG=changeLog, 
            SUMMARY=self.summary, LICENSE=license, VERSION=self.version,
            GROUP=self.group, SYSTEM_REQUIRES=self.systemRequires,
            SYSTEM_BUILD_REQUIRES=self.systemBuildRequires)

class RpmSpecParser(object):
    TAGS = set(['name', 'provides', 'version', 'release', 'group', 'license', 
        'summary'])
    
    @staticmethod
    def parse(specContents):
        tags = {}
        clog = None
        for i, line in enumerate(specContents):
            m = re.match(r'([a-zA-Z]+):\s*(.*)', line)
            if m:
                tag = m.group(1)
                val = m.group(2)
                if tag.lower() in RpmSpecParser.TAGS:
                    tags[tag.lower()] = val
            if line.startswith('%changelog'):
                clog = RpmSpecParser.clogSection(specContents[i:])
        tags['release'] = re.match('([^%]+)', tags['release']).group(1)
        return tags, clog
    
    @staticmethod
    def clogSection(specContents):
        ids = list()
        comments = list()
        for line in specContents:
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
        
    def parse_to_properties(self, cfgStore, specContents, pkgName, root):
        tags, clog = RpmSpecParser.parse(specContents.split('\n'))
        
        #BUILDREQUIRES, REQUIRES, INSTALL, PACKAGE_PATH
        #are inferred from rpm properties, command line
        #arguments, and spec concretization
        rpmName = tags['name']
        provides = tags.get('provides', None)
        specVars = RpmTemplateVars(RPM_NAME=rpmName, 
            PROVIDES=provides, RELEASE=tags['release'], 
            REQUIRES=None, BUILD_REQUIRES=None, INSTALL=None, PACKAGE_PATH=None, 
            CHANGE_LOG=clog, SUMMARY=tags['summary'], LICENSE=tags['license'], 
            VERSION=tags['version'], GROUP=tags['group'])
        
        #nonRpmDeps is not recorded in a spec so must be filled manually.
        #ignoreDeps has the same issue. rpmDeps could be inferred from the
        #'requires' tag but is only intended to track packages maintained by
        #Spack/rpm-install
        rpmProps = SpackRpmProperties(pkgName=pkgName, pkgSpec=None, path=None,
            rpmDeps=[], nonRpmDeps=[], ignoreDeps=[], root=root,
            nameSpec=rpmName, providesSpec=provides)

        cfgStore.saveRpmProperties(rpmName, rpmProps.toJson())
        cfgStore.saveSpecProperties(rpmName, specVars.toJson())

def read_rpms_transitive(cfgStore, rpmName, rpmDb):
    if rpmName in rpmDb:
        return rpmDb[rpmName].rpm
    
    specProps = cfgStore.getSpecProperties(rpmName)
    rpmProps = cfgStore.getRpmProperties(rpmName)

    rpmDeps = set(read_rpms_transitive(cfgStore, dep, rpmDb)
        for dep in rpmProps.rpmDeps)

    rpm = Rpm(rpmName, rpmProps.pkgName, rpmProps.pkgSpec, rpmProps.path, 
        rpmDeps, nonRpmDeps=rpmProps.nonRpmDeps, ignoreDeps=rpmProps.ignoreDeps, 
        providesName=specProps.PROVIDES)
    
    rpmSpec = RpmSpec(rpmName, summary=specProps.SUMMARY, group=specProps.GROUP,
        license=specProps.LICENSE, release=int(specProps.RELEASE), 
        changeLog=specProps.CHANGE_LOG, version=specProps.VERSION,
        systemRequires=specProps.SYSTEM_REQUIRES, 
        systemBuildRequires=specProps.SYSTEM_BUILD_REQUIRES)
        
    rpmDb[rpmName] = RpmInfo(rpm, rpmSpec)
    
    return rpm

class SpackRpmProperties(Properties):
    """This is intended to store details useful to Spack but not tracked by an 
    RPM .spec file."""
    PROPERTIES = set(['pkgName', 'pkgSpec', 'path', 'rpmDeps', 'nonRpmDeps', 
        'ignoreDeps', 'root', 'nameSpec', 'providesSpec'])
    
    def __init__(self, **kwargs):
        super(SpackRpmProperties, self).__init__(
            SpackRpmProperties.PROPERTIES, **kwargs)
    
    def namespace(self):
        return CustomizedNamespace(self.nameSpec, self.providesSpec, self.root)
    
    def toJson(self):
        jsonData = self.to_dict(rpmDeps=list(self.rpmDeps), 
            nonRpmDeps=list(self.nonRpmDeps),
            ignoreDeps=list(self.ignoreDeps))
        return json.dumps(jsonData, sort_keys=True, indent=4)
    
    @staticmethod
    def fromJson(string):
        return SpackRpmProperties(**json.loads(string))

class Rpm(object):
    def __init__(self, name, pkgName, pkgSpec, path, rpmDeps, 
            nonRpmDepSpecs=None, nonRpmDeps=None, ignoreDeps=None,
            providesName=None):
        self.name = name
        self.pkgName = pkgName
        self.pkgSpec = pkgSpec
        self.path = path # Full path - everything up to {lib/, bin/, etc.}
        self.rpmDeps = rpmDeps
        # These are dependencies which should not be created as RPMs. These are
        # implied build dependencies (but not all build dependencies are managed
        # this way).
        self.nonRpmDeps = nonRpmDeps or set()
        # These are dependencies that are typically managed by Spack but in this 
        # case should be delegated to an existing system install.
        self.ignoreDeps = ignoreDeps or set()
        self.nonRpmDepSpecs = nonRpmDepSpecs or list()
        self.providesName = providesName if providesName != name else None
    
    def diff(self, other):
        """Compare with another instance of the same RPM package. Note this
        does not consider RPMs different if details of their dependencies are
        different, only if the names of the dependencies are different."""
        rpmDepNames = frozenset(x.name for x in self.rpmDeps)
        otherRpmDepNames = frozenset(x.name for x in other.rpmDeps)
        if self.name != other.name:
            raise ValueError("Diff is not useful for different RPM packages.")
        #TODO: This compares everything except nonRpmDepSpecs (as of now those
        #are not stored/parsed)
        toCompare = list([(self.pkgSpec, other.pkgSpec), 
            (self.path, other.path), (rpmDepNames, otherRpmDepNames), 
            (frozenset(self.nonRpmDeps), frozenset(other.nonRpmDeps)),
            (frozenset(self.ignoreDeps), frozenset(other.ignoreDeps)),
            (self.providesName, other.providesName)])
        return set((x, y) for x, y in toCompare if x != y)
        
    def __eq__(self, other):
        if not isinstance(other, Rpm):
            return False
        if self.name != other.name:
            return False
        if self.diff(other):
            return False
        deps = sorted(self.rpmDeps, key=lambda x: x.name)
        otherDeps = sorted(other.rpmDeps, key=lambda x: x.name)
        return deps == otherDeps
    
    @property
    def depName(self):
        return self.providesName if self.providesName else self.name
    
    def path_config(self):
        pkgToPath = self._transitive_paths()
        formatPaths = {}
        for (pkgName, spec), path in pkgToPath.iteritems():
            formatPaths[pkgName] = {'paths':{spec: path}, 'buildable':False}
        # Undo path config for root
        del formatPaths[self.pkgName]
        return {'packages':formatPaths} if formatPaths else {}

    def new_rpm_spec_variables(self, rpmSpec, redirect=True):
        requiredDepNames = list(x.depName for x in self.direct_deps())
        
        setPath = "--install-path={0}".format(self.path)
        installArgs = ['./bin/spack install', '--verbose']
        if redirect:
            installArgs.append('--destdir=%{buildroot}')
        skipDeps = self.ignoreDeps | set(x.pkgName for x in self.rpmDeps)
        if skipDeps:
            installArgs.append('--skip-deps=' + ','.join(skipDeps))
        installArgs.extend([setPath, self.pkgSpec])
        install = ' '.join(installArgs)
        
        return rpmSpec.new_spec_variables(requiredDepNames, install,
            self.path, providesName=self.providesName)
    
    def _transitive_paths(self):
        paths = {(self.pkgName, self.pkgSpec):self.path}
        for dep in self.rpmDeps:
            paths.update(dep._transitive_paths())
        return paths
    
    def direct_deps(self):
        return set(self.rpmDeps) - set(itertools.chain.from_iterable(
            x.transitive_deps() for x in self.rpmDeps))
    
    def transitive_deps(self):
        return set(itertools.chain(
            itertools.chain.from_iterable(
                x.transitive_deps() for x in self.rpmDeps),
            set(self.rpmDeps)))

    def write_files_for_install(self, rpmSpec, cfgStore, redirect=True,
            spackRpmProps=None):
        specVars = self.new_rpm_spec_variables(rpmSpec, redirect=redirect)
        cfgStore.saveSpecProperties(self.name, specVars.toJson())

        if spackRpmProps:
            cfgStore.saveRpmProperties(self.name, spackRpmProps.toJson())

        systemPkgCfg = list()
        for dep in self.ignoreDeps:
            depCfg = cfgStore.determineDepPkgCfg(self.name, dep)
            if not depCfg:
                tty.msg("No package.yaml associated with dependency " + dep)
            else:
                systemPkgCfg.append(depCfg)
        pathCfg = self.path_config()
        for pkgCfg in systemPkgCfg:
            spack.config._merge_yaml(pathCfg, pkgCfg)
        if pathCfg:
            cfgStore.savePkgCfg(self.name, 
                yaml.dump(pathCfg, default_flow_style=False))

def generate_rpms_transitive(args):
    cfgStore = ConfigStore(args.outputDir, specsDir=args.specsDir,
        pkgsDir=args.pkgsDir)
    
    if args.completeSpecs:
        cfgStore.completeSpecs()
        return
    
    if args.bootstrap:
        rpmName, pkgName, root = args.bootstrap
        specContents = cfgStore.getSpec(rpmName)
        RpmSpecParser().parse_to_properties(
            cfgStore, specContents, pkgName, root)
        return

    if cfgStore.specsDir:
        rpmDb = {}
        
        if args.rpmDbSpec:
            seed = args.rpmDbSpec
            if seed.endswith('.spec'):
                seed = seed[:-5]
            rpmSeeds = [seed]
        else:
            rpmSeeds = list()
            for root, dirs, files in os.walk(cfgStore.specsDir):
                rpmSeeds.extend(f[:-5] for f in files if f.endswith('.spec'))
        
        for seed in rpmSeeds:
            read_rpms_transitive(cfgStore, seed, rpmDb)
    else:
        rpmDb = {}
    
    namespaceStore = NamespaceStore()
    namespaceStore.set_up_namespaces(args.universalSubspace, 
        args.getNamespaceFromSpecs, args.defaultNamespace, cfgStore)
    
    buildDeps = expandOption(args.buildDeps)
    ignoreDeps = expandOption(args.ignoreDeps)

    specs = spack.cmd.parse_specs(args.package, concretize=True)
    if len(specs) > 1:
        tty.die("Only 1 top-level package can be specified")
    topSpec = iter(specs).next()
    new = set()
    pkgToRpmProps = dict()
    rpm = resolve_autoname(topSpec, namespaceStore, rpmDb, new, buildDeps,
        ignoreDeps, pkgToRpmProps, inferBuildDeps=args.inferBuildDeps,
        inferIgnoreDeps=args.inferIgnoreDeps)
    
    new &= rpm.transitive_deps() #RPMs may have been created that are not going to be used
    
    #TODO: For now, the rpm associated with the top-level spec always generates
    #a new spec (regardless of whether it changed) since as of now there is not
    #sufficient functionality to check this properly (i.e. a package hash)
    rpm.pkgSpec = topSpec.format() 
    for rpm in set(itertools.chain([rpm], new)):
        tty.msg("New or updated rpm: " + rpm.name)
        rpmSpec = rpmDb[rpm.name].spec
        rpm.write_files_for_install(rpmSpec, cfgStore, 
            redirect=(not args.noRedirect),
            spackRpmProps=pkgToRpmProps[rpm.pkgName])

    if not args.propertiesOnly:
        cfgStore.completeSpecs()

def resolve_autoname(pkgSpec, namespaceStore, rpmDb, new, buildDeps, 
        ignoreDeps, pkgToRpmProps, visited=None, inferBuildDeps=False,
        inferIgnoreDeps=False):
    """Because this automatically generates rpm names it can create rpms
    transitively.
    
    Notes:
    -If a package is marked as a build dependency it is a build dependency
     everywhere (even if other packages require it as a runtime dependency an
     rpm will not be generated)
    -Transitive dependencies of packages marked as build dependencies will also
     not generate RPMs unless there is a path from the root which does not
     traverse any build dependencies
    """
    if not visited:
        visited = set()

    namespace = namespaceStore.get_namespace(pkgSpec.name)
    rpmName = namespace.name(pkgSpec)

    rpm = rpmDb[rpmName].rpm if rpmName in rpmDb else None

    if pkgSpec in visited:
        return rpm        
    visited.add(pkgSpec)

    # Unlike specified build dependencies, inferred build dependencies are not
    # propagated transitively.
    inferredBuildDeps = set()
    if buildDeps is not None:
        # Prefer using build deps specified by the user. If not specified, use
        # whatever build dependencies were associated with the previous release
        # of the RPM.
        inferredBuildDeps.update(buildDeps)
    elif rpm and rpm.nonRpmDeps:
        inferredBuildDeps.update(rpm.nonRpmDeps)
    
    inferredIgnoreDeps = set()
    if ignoreDeps is not None:
        inferredIgnoreDeps.update(ignoreDeps)
    elif rpm and rpm.ignoreDeps:
        inferredIgnoreDeps.update(rpm.ignoreDeps)       

    dependencies = pkgSpec.dependencies_dict()
    if inferBuildDeps:
        inferredBuildDeps.update(depName for depName, dep 
            in dependencies.iteritems() 
            if set(dep.deptypes) == set(['build']))

    rpmDeps = set()
    nonRpmDepSpecs = list()
    skipped = set()
    for depName, dep in dependencies.iteritems():
        if depName in inferredIgnoreDeps:
            pass
        elif depName in inferredBuildDeps:
            nonRpmDepSpecs.append(str(dep.spec))
        else:
            if namespaceStore.get_namespace(dep.spec.name, required=False): 
                depRpm = resolve_autoname(dep.spec, namespaceStore, rpmDb, new, 
                    buildDeps, ignoreDeps, pkgToRpmProps, visited, 
                    inferBuildDeps=inferBuildDeps,
                    inferIgnoreDeps=inferIgnoreDeps)
                rpmDeps.add(depRpm)
            else:
                skipped.add(dep.spec.name)
    
    if inferIgnoreDeps:
        transitiveDeps = set(itertools.chain.from_iterable(x.transitive_deps()
            for x in rpmDeps)) | rpmDeps
        inferredIgnoreDeps.update(itertools.chain.from_iterable(
            x.ignoreDeps for x in transitiveDeps))
    if skipped:
        tty.debug("Skipped: " + ', '.join(skipped))
    skipped -= inferredIgnoreDeps
    if skipped:
        raise MissingNamespaceError("The following packages are not ignored" +
            " and are missing namespace information: [{0}]".format(
            ', '.join(skipped)))
    
    omitDeps = inferredBuildDeps | inferredIgnoreDeps
    rpmDeps = set(x for x in rpmDeps if x.pkgName not in omitDeps)

    rpm = Rpm(rpmName, pkgSpec.name, pkgSpec.format(), 
        namespace.path(pkgSpec), rpmDeps, nonRpmDepSpecs=nonRpmDepSpecs, 
        nonRpmDeps=set(dependencies) & inferredBuildDeps,
        ignoreDeps=set(x.name for x in pkgSpec.traverse()) & inferredIgnoreDeps,
        providesName=namespace.provides_name(pkgSpec))

    if rpmName not in rpmDb:
        rpmSpec = RpmSpec.new(rpmName, pkgSpec)
        new.add(rpm)
        rpmInfo = RpmInfo(rpm, rpmSpec)
        rpmDb[rpmName] = rpmInfo
    else:
        oldRpm = rpmDb[rpmName].rpm
        # It is never correct for two different spack packages to have matching 
        # RPM names: this is easy to avoid (e.g. if the name projection includes
        # the spack package name)
        if rpm.pkgName != oldRpm.pkgName:
            raise ValueError("Name collision: new RPM for" + 
                "{0} collides with existing RPM for {1}".format(
                    rpm.pkgName, oldRpm.pkgName))
        # Check if the rpm has changed in some way
        diff = rpm.diff(oldRpm)
        if diff:
            tty.msg("RPM update: " + rpm.pkgName)
            tty.msg("{0}:\n{1}".format(rpm.name, 
                '\n'.join('/'.join((str(x), str(y))) for x, y in diff)))
            rpmDb[rpmName].rpm = rpm
            new.add(rpm)
        else:
            rpm = oldRpm

    #TODO: if package.py contents change then a new rpm release should be made

    pkgToRpmProps[pkgSpec.name] = SpackRpmProperties(pkgName=rpm.pkgName, 
        pkgSpec=rpm.pkgSpec, path=rpm.path, 
        rpmDeps=set(depRpm.name for depRpm in rpm.rpmDeps), 
        nonRpmDeps=rpm.nonRpmDeps, ignoreDeps=rpm.ignoreDeps, 
        root=namespace.root, nameSpec=namespace.nameSpec, 
        providesSpec=namespace.providesSpec)

    return rpm

class MissingNamespaceError(Exception):
    pass

class CustomizedNamespace(object):
    def __init__(self, nameSpec, providesSpec, root):
        self.nameSpec = str(nameSpec)
        self.providesSpec = providesSpec or self.nameSpec
        self.root = root
    
    def name(self, spec):
        return spec.format(self.nameSpec)
    
    def provides_name(self, spec):
        return spec.format(self.providesSpec)
    
    def path(self, spec):
        return os.path.join(self.root, spec.name, self.provides_name(spec))

#TODO: move this to config?
def resolve_pkg_to_namespace(universalSubspace=None):
    """If you only have 1 subspace or want to specify a default
    subspace, you can place the descriptors at the package level. If
    you want to create a subspace which is not default then an explicit
    subspace must be created under the package level. 
    'universalSubspace' will choose the same subspace for each package
    where available; if the subspace is not available for the package
    but it has a default then that will be used (if the subspace is not
    available and there is no default, that is an error).
    """
    packages = spack.config.get_config('packages')
    pkgToSubspace = resolve_pkg_to_subspace(universalSubspace)
    pkgToNamespace = {}
    for pkgName, info in packages.iteritems():
        if pkgName in pkgToSubspace:
            subspace = info['subspaces'][pkgToSubspace[pkgName]] 
        elif all(p in info for p in ['name', 'prefix']):
            subspace = info
        else:
            continue
        nameSpec = subspace['name']
        providesSpec = subspace.get('provides', nameSpec)
        root = subspace['prefix']
        pkgToNamespace[pkgName] = CustomizedNamespace(nameSpec, providesSpec, root)
    return pkgToNamespace

def resolve_pkg_to_subspace(universalSubspace=None):
    pkgToSubspace = {}
    packages = spack.config.get_config('packages')
    for pkgName, info in packages.iteritems():
        #TODO: since these can be specified at the package level, use a more
        #descriptive name? like 'name' -> 'rpmnameprojection'
        if all(p in info for p in ['name', 'prefix']):
            defaultSubspace = info
        else:
            defaultSubspace = None
    
        subspaces = info['subspaces'] if 'subspaces' in info else {}
        if universalSubspace in subspaces:
            pkgToSubspace[pkgName] = universalSubspace
        elif defaultSubspace:
            pass
        else:
            tty.msg("{0}: universal subspace not specified, and/or no suitable default".format(pkgName))
    return pkgToSubspace

class RpmInfo(object):
    def __init__(self, rpm, rpmSpec):
        self.rpm = rpm
        self.spec = rpmSpec

class ConfigStore(object):
    """Stores and retrieves information related to rpms and their specs. The
    user can start with Spack-package-level configuration which is stored at the
    rpm-package-level as associated RPMs are created. It expects the following 
    directory structure:
    
    <pkgsDir>/
        <pkg name>/
            spec.skel
            filter* (any exe with the prefix "filter")
            systempkg.yaml
        ... (one folder per package)
    
    and
    
    <specsDir>/
        <rpm name>/
            spec.skel
            filter*
            <deppkg>_systempkg.yaml (one file for each dep maintained by system)
            rpmprops.json
            specvars.json
            <rpm name>.spec
        ... (one folder per rpm)
    """
    def __init__(self, outputDir, pkgsDir=None, specsDir=None):
        self.pkgsDir = pkgsDir
        self.specsDir = specsDir
        self.outputDir = outputDir

    def determineSpecTemplate(self, rpmName, pkgName):
        searchPaths = []
        searchPaths.append(self.outputLocation(rpmName, 'spec.skel'))
        if self.specsDir:
            searchPaths.append(self.specsLocation(rpmName, 'spec.skel'))
        if self.pkgsDir:
            searchPaths.append(self.pkgsLocation(pkgName, 'spec.skel'))
        templatePath = self.getFirstExisting(searchPaths, self.find)
        if templatePath:
            template = retrieveFileContents(templatePath)
        else:
            tty.msg("Using default spec template for " + pkgName)
            template = default_spec()
            
        self.saveRpmCfg(rpmName, 'spec.skel', template)
        return template

    def determineDepPkgCfg(self, rpmName, depPkgName):
        """For packages that should not be managed by Spack"""
        dstFile = depPkgName + '_systempkg.yaml'
        searchPaths = []
        if self.specsDir:
            searchPaths.append(self.specsLocation(rpmName, dstFile))
        if self.pkgsDir:
            searchPaths.append(self.pkgsLocation(depPkgName, 'systempkg.yaml'))
        pkgCfgPath = self.getFirstExisting(searchPaths, self.find)
        
        if not pkgCfgPath:
            return
        shutil.copy(pkgCfgPath, self.setUpOutputLocation(rpmName, dstFile))
        with open(pkgCfgPath, 'rb') as F:
            return yaml.safe_load(F)
        
    def applyTransform(self, rpmName, pkgName):
        varsFile = self.outputLocation(rpmName, 'specvars.json')
        searchPaths = []
        if self.specsDir:
            searchPaths.append(self.specsLocation(rpmName))
        if self.pkgsDir:
            searchPaths.append(self.pkgsLocation(pkgName))
        scriptPath = self.getFirstExisting(searchPaths, self.findScript)
        if not scriptPath:
            return
        Executable(scriptPath)(varsFile)
        shutil.copy(scriptPath, self.setUpOutputLocation(
            rpmName, os.path.basename(scriptPath)))
        with open(varsFile, 'rb') as F:
            return RpmTemplateVars.fromJson(F.read())

    def specsLocation(self, rpmName, fName=None):
        base = os.path.join(self.specsDir, rpmName)
        return os.path.join(base, fName) if fName else base
    
    def pkgsLocation(self, pkgName, fName=None):
        base = os.path.join(self.pkgsDir, pkgName)
        return os.path.join(base, fName) if fName else base

    def getRpms(self):
        return set(os.listdir(self.specsDir))

    def getSpec(self, rpmName):
        """Should only be called if specsDir is set"""
        specName = rpmName + '.spec' if not rpmName.endswith('.spec') else rpmName
        return retrieveFileContents(self.specsLocation(rpmName, specName))

    def getRpmProperties(self, rpmName, useOutput=False):
        """Should only be called if specsDir is set"""
        locationFn = self.outputLocation if useOutput else self.specsLocation
        return SpackRpmProperties.fromJson(
            retrieveFileContents(locationFn(rpmName, 'rpmprops.json')))

    def getSpecProperties(self, rpmName, useOutput=False):
        """Should only be called if specsDir is set"""
        locationFn = self.outputLocation if useOutput else self.specsLocation
        return RpmTemplateVars.fromJson(
            retrieveFileContents(locationFn(rpmName, 'specvars.json')))

    def saveSpecProperties(self, rpmName, content):
        self.saveRpmCfg(rpmName, 'specvars.json', content)
    
    def saveRpmProperties(self, rpmName, content):
        self.saveRpmCfg(rpmName, 'rpmprops.json', content)

    def saveSpec(self, rpmName, content):
        self.saveRpmCfg(rpmName, '%s.spec' % rpmName, content)

    def savePkgCfg(self, rpmName, content):
        self.saveRpmCfg(rpmName, 'packages.yaml', content)

    def saveRpmCfg(self, rpmName, fName, content):
        with open(self.setUpOutputLocation(rpmName, fName), 'wb') as F:
            F.write(content)

    def setUpOutputLocation(self, rpmName, fName):
        path = self.outputLocation(rpmName, fName)
        directory = os.path.dirname(path)
        try:
            os.makedirs(directory)
        except OSError as exc: 
            if exc.errno == errno.EEXIST and os.path.isdir(directory):
                pass
            else:
                raise
        
        return path

    def outputLocation(self, rpmName, fName):
        return os.path.join(self.outputDir, rpmName, fName)

    def findScript(self, directory):
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

    def getFirstExisting(self, paths, find):
        for path in paths:
            result = find(path)
            if result:
                return result 

    def completeSpecs(self):
        rpmNames = os.listdir(self.outputDir)
        for rpmName in rpmNames:
            try:
                self.completeSpec(rpmName)
            except KeyError as e:
                templateLocation = self.outputLocation(rpmName, 'spec.skel')
                key = e.args[0]
                raise ValueError("{0} has unaddressed key {1},".format(
                        templateLocation, key) + 
                    " edit and rerun with --complete-specs")

    def completeSpec(self, rpmName):
        rpmProps = self.getRpmProperties(rpmName, useOutput=True)
        self.applyTransform(rpmName, rpmProps.pkgName)
        specVars = self.getSpecProperties(rpmName, useOutput=True)
        specTemplate = self.determineSpecTemplate(rpmName, rpmProps.pkgName)
        specContents = fill_spec_template(specVars, specTemplate)
        self.saveSpec(rpmName, specContents)

class NamespaceStore(object):
    def set_up_namespaces(self, universalSubspace, getNamespaceFromSpecs,
            defaultNamespace, cfgStore):
            
        # Preferred compilers and versions can be associated with
        # subspaces. The global preferences object is updated based on
        # the specified subspace to prefer the desired compiler/version
        # for the associated package.
        spack.pkgsort.pkgToSubspace = resolve_pkg_to_subspace(universalSubspace)
        pkgToNamespace = resolve_pkg_to_namespace(universalSubspace)
        if getNamespaceFromSpecs:
            pkgToNamespace.update(self.get_namespaces_from_specs(cfgStore))
        self.pkgToNamespace = pkgToNamespace
        
        if defaultNamespace:
            nameSpec, prefix = defaultNamespace
            self.defaultNamespace = CustomizedNamespace(nameSpec, nameSpec, prefix)
        else:
            self.defaultNamespace = None
        
    def get_namespace(self, pkgName, required=True):
        namespace = self.pkgToNamespace.get(pkgName, self.defaultNamespace)
        if not namespace and required:
            raise MissingNamespaceError("No namespace for " + pkgName)
        return namespace

    def get_namespaces_from_specs(self, cfgStore):
        pkgToNamespace = {}
        for rpmName in cfgStore.getRpms():
            rpmProps = cfgStore.getRpmProperties(rpmName)
            pkgToNamespace[rpmProps.pkgName] = rpmProps.namespace()
        return pkgToNamespace

def retrieveFileContents(path):
    with open(path, 'rb') as F:
        return F.read()

def expandOption(opt):
    """Distinguish between an empty option vs. not specifying the option at 
    all"""
    if opt or opt == '':
        return set(opt.split(','))

def rpm(parser, args):
    generate_rpms_transitive(args)
        
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
