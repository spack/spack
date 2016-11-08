##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""
Functions here are used to take abstract specs and make them concrete.
For example, if a spec asks for a version between 1.8 and 1.9, these
functions might take will take the most recent 1.9 version of the
package available.  Or, if the user didn't specify a compiler for a
spec, then this will assign a compiler to the spec based on defaults
or user preferences.

TODO: make this customizable and allow users to configure
      concretization  policies.
"""
from __future__ import print_function
import spack
import spack.spec
import spack.compilers
import spack.architecture
import spack.error
from spack.version import *
from functools import partial
from itertools import chain
from spack.config import *
import spack.preferred_packages


class DefaultConcretizer(object):

    """This class doesn't have any state, it just provides some methods for
       concretization.  You can subclass it to override just some of the
       default concretization strategies, or you can override all of them.
    """

    def _valid_virtuals_and_externals(self, spec):
        """Returns a list of candidate virtual dep providers and external
           packages that coiuld be used to concretize a spec."""
        # First construct a list of concrete candidates to replace spec with.
        candidates = [spec]
        if spec.virtual:
            providers = spack.repo.providers_for(spec)
            if not providers:
                raise UnsatisfiableProviderSpecError(providers[0], spec)
            spec_w_preferred_providers = find_spec(
                spec,
                lambda x: spack.pkgsort.spec_has_preferred_provider(
                    x.name, spec.name))
            if not spec_w_preferred_providers:
                spec_w_preferred_providers = spec
            provider_cmp = partial(spack.pkgsort.provider_compare,
                                   spec_w_preferred_providers.name,
                                   spec.name)
            candidates = sorted(providers, cmp=provider_cmp)

        # For each candidate package, if it has externals, add those
        # to the usable list.  if it's not buildable, then *only* add
        # the externals.
        usable = []
        for cspec in candidates:
            if is_spec_buildable(cspec):
                usable.append(cspec)
            externals = spec_externals(cspec)
            for ext in externals:
                if ext.satisfies(spec):
                    usable.append(ext)

        # If nothing is in the usable list now, it's because we aren't
        # allowed to build anything.
        if not usable:
            raise NoBuildError(spec)

        def cmp_externals(a, b):
            if a.name != b.name and (not a.external or a.external_module and
                                     not b.external and b.external_module):
                # We're choosing between different providers, so
                # maintain order from provider sort
                index_of_a = next(i for i in range(0, len(candidates))
                                  if a.satisfies(candidates[i]))
                index_of_b = next(i for i in range(0, len(candidates))
                                  if b.satisfies(candidates[i]))
                return index_of_a - index_of_b

            result = cmp_specs(a, b)
            if result != 0:
                return result

            # prefer external packages to internal packages.
            if a.external is None or b.external is None:
                return -cmp(a.external, b.external)
            else:
                return cmp(a.external, b.external)

        usable.sort(cmp=cmp_externals)
        return usable

    # XXX(deptypes): Look here.
    def choose_virtual_or_external(self, spec):
        """Given a list of candidate virtual and external packages, try to
           find one that is most ABI compatible.
        """
        candidates = self._valid_virtuals_and_externals(spec)
        if not candidates:
            return candidates

        # Find the nearest spec in the dag that has a compiler.  We'll
        # use that spec to calibrate compiler compatibility.
        abi_exemplar = find_spec(spec, lambda x: x.compiler)
        if not abi_exemplar:
            abi_exemplar = spec.root

        # Make a list including ABI compatibility of specs with the exemplar.
        strict = [spack.abi.compatible(c, abi_exemplar) for c in candidates]
        loose = [spack.abi.compatible(c, abi_exemplar, loose=True)
                 for c in candidates]
        keys = zip(strict, loose, candidates)

        # Sort candidates from most to least compatibility.
        # Note:
        #   1. We reverse because True > False.
        #   2. Sort is stable, so c's keep their order.
        keys.sort(key=lambda k: k[:2], reverse=True)

        # Pull the candidates back out and return them in order
        candidates = [c for s, l, c in keys]
        return candidates

    def concretize_version(self, spec):
        """If the spec is already concrete, return.  Otherwise take
           the preferred version from spackconfig, and default to the package's
           version if there are no available versions.

           TODO: In many cases we probably want to look for installed
                 versions of each package and use an installed version
                 if we can link to it.  The policy implemented here will
                 tend to rebuild a lot of stuff becasue it will prefer
                 a compiler in the spec to any compiler already-
                 installed things were built with.  There is likely
                 some better policy that finds some middle ground
                 between these two extremes.
        """
        # return if already concrete.
        if spec.versions.concrete:
            return False

        # If there are known available versions, return the most recent
        # version that satisfies the spec
        pkg = spec.package

        # ---------- Produce prioritized list of versions
        # Get list of preferences from packages.yaml
        preferred = spack.pkgsort
        # NOTE: spack.pkgsort == spack.preferred_packages.PreferredPackages()

        yaml_specs = [
            x[0] for x in
            preferred._spec_for_pkgname(spec.name, 'version', None)]
        n = len(yaml_specs)
        yaml_index = dict(
            [(spc, n - index) for index, spc in enumerate(yaml_specs)])

        # List of versions we could consider, in sorted order
        unsorted_versions = [
            v for v in pkg.versions
            if any(v.satisfies(sv) for sv in spec.versions)]

        # The keys below show the order of precedence of factors used
        # to select a version when concretizing.  The item with
        # the "largest" key will be selected.
        #
        # NOTE: When COMPARING VERSIONS, the '@develop' version is always
        #       larger than other versions.  BUT when CONCRETIZING,
        #       the largest NON-develop version is selected by
        #       default.
        keys = [(
            # ------- Special direction from the user
            # Respect order listed in packages.yaml
            yaml_index.get(v, -1),

            # The preferred=True flag (packages or packages.yaml or both?)
            pkg.versions.get(Version(v)).get('preferred', False),

            # ------- Regular case: use latest non-develop version by default.
            # Avoid @develop version, which would otherwise be the "largest"
            # in straight version comparisons
            not v.isdevelop(),

            # Compare the version itself
            # This includes the logic:
            #    a) develop > everything (disabled by "not v.isdevelop() above)
            #    b) numeric > non-numeric
            #    c) Numeric or string comparison
            v) for v in unsorted_versions]
        keys.sort(reverse=True)

        # List of versions in complete sorted order
        valid_versions = [x[-1] for x in keys]
        # --------------------------

        if valid_versions:
            spec.versions = ver([valid_versions[0]])
        else:
            # We don't know of any SAFE versions that match the given
            # spec.  Grab the spec's versions and grab the highest
            # *non-open* part of the range of versions it specifies.
            # Someone else can raise an error if this happens,
            # e.g. when we go to fetch it and don't know how.  But it
            # *might* work.
            if not spec.versions or spec.versions == VersionList([':']):
                raise NoValidVersionError(spec)
            else:
                last = spec.versions[-1]
                if isinstance(last, VersionRange):
                    if last.end:
                        spec.versions = ver([last.end])
                    else:
                        spec.versions = ver([last.start])
                else:
                    spec.versions = ver([last])

        return True   # Things changed

    def _concretize_operating_system(self, spec):
        if spec.architecture.platform_os is not None and isinstance(
                spec.architecture.platform_os,
                spack.architecture.OperatingSystem):
            return False

        if spec.root.architecture and spec.root.architecture.platform_os:
            if isinstance(spec.root.architecture.platform_os,
                          spack.architecture.OperatingSystem):
                spec.architecture.platform_os = \
                    spec.root.architecture.platform_os
        else:
            spec.architecture.platform_os = \
                spec.architecture.platform.operating_system('default_os')
        return True  # changed

    def _concretize_target(self, spec):
        if spec.architecture.target is not None and isinstance(
                spec.architecture.target, spack.architecture.Target):
            return False
        if spec.root.architecture and spec.root.architecture.target:
            if isinstance(spec.root.architecture.target,
                          spack.architecture.Target):
                spec.architecture.target = spec.root.architecture.target
        else:
            spec.architecture.target = spec.architecture.platform.target(
                'default_target')
        return True  # changed

    def _concretize_platform(self, spec):
        if spec.architecture.platform is not None and isinstance(
                spec.architecture.platform, spack.architecture.Platform):
            return False
        if spec.root.architecture and spec.root.architecture.platform:
            if isinstance(spec.root.architecture.platform,
                          spack.architecture.Platform):
                spec.architecture.platform = spec.root.architecture.platform
        else:
            spec.architecture.platform = spack.architecture.platform()
        return True  # changed?

    def concretize_architecture(self, spec):
        """If the spec is empty provide the defaults of the platform. If the
        architecture is not a basestring, then check if either the platform,
        target or operating system are concretized. If any of the fields are
        changed then return True. If everything is concretized (i.e the
        architecture attribute is a namedtuple of classes) then return False.
        If the target is a string type, then convert the string into a
        concretized architecture. If it has no architecture and the root of the
        DAG has an architecture, then use the root otherwise use the defaults
        on the platform.
        """
        root_arch = spec.root.architecture
        sys_arch = spack.spec.ArchSpec(spack.architecture.sys_type())
        spec_changed = False

        if spec.architecture is None:
            spec.architecture = spack.spec.ArchSpec(sys_arch)
            spec_changed = True

        default_archs = [root_arch, sys_arch]
        while not spec.architecture.concrete and default_archs:
            default_arch = default_archs.pop(0)

            replacement_fields = [k for k, v in default_arch.to_cmp_dict()
                                  if v and not getattr(spec.architecture, k)]
            for field in replacement_fields:
                setattr(spec.architecture, field, getattr(default_arch, field))
                spec_changed = True

        return spec_changed

    def concretize_variants(self, spec):
        """If the spec already has variants filled in, return.  Otherwise, add
           the user preferences from packages.yaml or the default variants from
           the package specification.
        """
        changed = False
        preferred_variants = spack.pkgsort.spec_preferred_variants(
            spec.package_class.name)
        for name, variant in spec.package_class.variants.items():
            if name not in spec.variants:
                changed = True
                if name in preferred_variants:
                    spec.variants[name] = preferred_variants.get(name)
                else:
                    spec.variants[name] = \
                        spack.spec.VariantSpec(name, variant.default)
        return changed

    def concretize_compiler(self, spec):
        """If the spec already has a compiler, we're done.  If not, then take
           the compiler used for the nearest ancestor with a compiler
           spec and use that.  If the ancestor's compiler is not
           concrete, then used the preferred compiler as specified in
           spackconfig.

           Intuition: Use the spackconfig default if no package that depends on
           this one has a strict compiler requirement.  Otherwise, try to
           build with the compiler that will be used by libraries that
           link to this one, to maximize compatibility.
        """
        # Pass on concretizing the compiler if the target is not yet determined
        if not spec.architecture.platform_os:
            # Although this usually means changed, this means awaiting other
            # changes
            return True

        # Only use a matching compiler if it is of the proper style
        # Takes advantage of the proper logic already existing in
        # compiler_for_spec Should think whether this can be more
        # efficient
        def _proper_compiler_style(cspec, arch):
            platform = arch.platform
            compilers = spack.compilers.compilers_for_spec(cspec,
                                                           platform=platform)
            return filter(lambda c: c.operating_system ==
                          arch.platform_os, compilers)
            # return compilers

        all_compilers = spack.compilers.all_compilers()

        if (spec.compiler and
            spec.compiler.concrete and
                spec.compiler in all_compilers):
            return False

        # Find the another spec that has a compiler, or the root if none do
        other_spec = spec if spec.compiler else find_spec(
            spec, lambda x: x.compiler)

        if not other_spec:
            other_spec = spec.root
        other_compiler = other_spec.compiler
        assert(other_spec)

        # Check if the compiler is already fully specified
        if other_compiler in all_compilers:
            spec.compiler = other_compiler.copy()
            return True

        # Filter the compilers into a sorted list based on the compiler_order
        # from spackconfig
        compiler_list = all_compilers if not other_compiler else \
            spack.compilers.find(other_compiler)
        cmp_compilers = partial(
            spack.pkgsort.compiler_compare, other_spec.name)
        matches = sorted(compiler_list, cmp=cmp_compilers)
        if not matches:
            arch = spec.architecture
            raise UnavailableCompilerVersionError(other_compiler,
                                                  arch.platform_os)

        # copy concrete version into other_compiler
        try:
            spec.compiler = next(
                c for c in matches
                if _proper_compiler_style(c, spec.architecture)).copy()
        except StopIteration:
            raise UnavailableCompilerVersionError(
                spec.compiler, spec.architecture.platform_os
            )

        assert(spec.compiler.concrete)
        return True  # things changed.

    def concretize_compiler_flags(self, spec):
        """
        The compiler flags are updated to match those of the spec whose
        compiler is used, defaulting to no compiler flags in the spec.
        Default specs set at the compiler level will still be added later.
        """

        if not spec.architecture.platform_os:
            # Although this usually means changed, this means awaiting other
            # changes
            return True

        ret = False
        for flag in spack.spec.FlagMap.valid_compiler_flags():
            try:
                nearest = next(p for p in spec.traverse(direction='parents')
                               if ((p.compiler == spec.compiler and
                                    p is not spec) and
                                   flag in p.compiler_flags))
                if flag not in spec.compiler_flags or \
                        not (sorted(spec.compiler_flags[flag]) >=
                             sorted(nearest.compiler_flags[flag])):
                    if flag in spec.compiler_flags:
                        spec.compiler_flags[flag] = list(
                            set(spec.compiler_flags[flag]) |
                            set(nearest.compiler_flags[flag]))
                    else:
                        spec.compiler_flags[
                            flag] = nearest.compiler_flags[flag]
                    ret = True

            except StopIteration:
                if (flag in spec.root.compiler_flags and
                    ((flag not in spec.compiler_flags) or
                     sorted(spec.compiler_flags[flag]) !=
                     sorted(spec.root.compiler_flags[flag]))):
                    if flag in spec.compiler_flags:
                        spec.compiler_flags[flag] = list(
                            set(spec.compiler_flags[flag]) |
                            set(spec.root.compiler_flags[flag]))
                    else:
                        spec.compiler_flags[
                            flag] = spec.root.compiler_flags[flag]
                    ret = True
                else:
                    if flag not in spec.compiler_flags:
                        spec.compiler_flags[flag] = []

        # Include the compiler flag defaults from the config files
        # This ensures that spack will detect conflicts that stem from a change
        # in default compiler flags.
        compiler = spack.compilers.compiler_for_spec(
            spec.compiler, spec.architecture)
        for flag in compiler.flags:
            if flag not in spec.compiler_flags:
                spec.compiler_flags[flag] = compiler.flags[flag]
                if compiler.flags[flag] != []:
                    ret = True
            else:
                if ((sorted(spec.compiler_flags[flag]) !=
                     sorted(compiler.flags[flag])) and
                    (not set(spec.compiler_flags[flag]) >=
                     set(compiler.flags[flag]))):
                    ret = True
                    spec.compiler_flags[flag] = list(
                        set(spec.compiler_flags[flag]) |
                        set(compiler.flags[flag]))

        return ret


def find_spec(spec, condition):
    """Searches the dag from spec in an intelligent order and looks
       for a spec that matches a condition"""
    # First search parents, then search children
    deptype = ('build', 'link')
    dagiter = chain(
        spec.traverse(direction='parents',  deptype=deptype, root=False),
        spec.traverse(direction='children', deptype=deptype, root=False))
    visited = set()
    for relative in dagiter:
        if condition(relative):
            return relative
        visited.add(id(relative))

    # Then search all other relatives in the DAG *except* spec
    for relative in spec.root.traverse(deptypes=spack.alldeps):
        if relative is spec:
            continue
        if id(relative) in visited:
            continue
        if condition(relative):
            return relative

    # Finally search spec itself.
    if condition(spec):
        return spec

    return None   # Nothing matched the condition.


def cmp_specs(lhs, rhs):
    # Package name sort order is not configurable, always goes alphabetical
    if lhs.name != rhs.name:
        return cmp(lhs.name, rhs.name)

    # Package version is second in compare order
    pkgname = lhs.name
    if lhs.versions != rhs.versions:
        return spack.pkgsort.version_compare(
            pkgname, lhs.versions, rhs.versions)

    # Compiler is third
    if lhs.compiler != rhs.compiler:
        return spack.pkgsort.compiler_compare(
            pkgname, lhs.compiler, rhs.compiler)

    # Variants
    if lhs.variants != rhs.variants:
        return spack.pkgsort.variant_compare(
            pkgname, lhs.variants, rhs.variants)

    # Architecture
    if lhs.architecture != rhs.architecture:
        return spack.pkgsort.architecture_compare(
            pkgname, lhs.architecture, rhs.architecture)

    # Dependency is not configurable
    lhash, rhash = hash(lhs), hash(rhs)
    if lhash != rhash:
        return -1 if lhash < rhash else 1

    # Equal specs
    return 0


class UnavailableCompilerVersionError(spack.error.SpackError):

    """Raised when there is no available compiler that satisfies a
       compiler spec."""

    def __init__(self, compiler_spec, operating_system):
        super(UnavailableCompilerVersionError, self).__init__(
            "No available compiler version matches '%s' on operating_system %s"
            % (compiler_spec, operating_system),
            "Run 'spack compilers' to see available compiler Options.")


class NoValidVersionError(spack.error.SpackError):

    """Raised when there is no way to have a concrete version for a
       particular spec."""

    def __init__(self, spec):
        super(NoValidVersionError, self).__init__(
            "There are no valid versions for %s that match '%s'"
            % (spec.name, spec.versions))


class NoBuildError(spack.error.SpackError):
    """Raised when a package is configured with the buildable option False, but
       no satisfactory external versions can be found"""

    def __init__(self, spec):
        msg = ("The spec '%s' is configured as not buildable, "
               "and no matching external installs were found")
        super(NoBuildError, self).__init__(msg % spec.name)
