##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
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
import collections
from llnl.util.filesystem import join_path
import spack
import spack.spec
import spack.compilers
import spack.architecture
import spack.error
from spack.util.naming import mod_to_class
from spack.version import *
from functools import partial
from spec import DependencyMap
from itertools import chain
from spack.config import *


class DefaultConcretizer(object):
    """This class doesn't have any state, it just provides some methods for
       concretization.  You can subclass it to override just some of the
       default concretization strategies, or you can override all of them.
    """

    def _find_other_spec(self, spec, condition):
        """Searches the dag from spec in an intelligent order and looks
           for a spec that matches a condition"""
        dagiter = chain(spec.traverse(direction='parents'), spec.traverse(direction='children'))
        found = next((x for x in dagiter if x is not spec and condition(x)), None)
        if found:
            return found
        dagiter = chain(spec.traverse(direction='parents'), spec.traverse(direction='children'))
        searched = list(dagiter)
        found = next((x for x in spec.root.traverse() if x not in searched and x is not spec and condition(x)), None)
        if found:
            return found
        if condition(spec):
            return spec
        return None
                                   

    def _valid_virtuals_and_externals(self, spec):
        """Returns a list of spec/external-path pairs for both virtuals and externals
           that can concretize this spec.""" 

        # Get a list of candidate packages that could satisfy this spec
        packages = []
        if spec.virtual:
            providers = spack.db.providers_for(spec)
            if not providers:
                raise UnsatisfiableProviderSpecError(providers[0], spec)
            spec_w_preferred_providers = self._find_other_spec(spec, \
                    lambda(x): spack.pkgsort.spec_has_preferred_provider(x.name, spec.name))
            if not spec_w_preferred_providers:
                spec_w_preferred_providers = spec
            provider_cmp = partial(spack.pkgsort.provider_compare, spec_w_preferred_providers.name, spec.name)
            packages = sorted(providers, cmp=provider_cmp)
        else:
            if spec.external:
                return False
            packages = [spec]

        # For each candidate package, if it has externals add those to the candidates
        # if it's a nobuild, then only add the externals.
        result = []
        all_compilers = spack.compilers.all_compilers()
        for pkg in packages:
            externals = spec_externals(pkg)
            buildable = not is_spec_nobuild(pkg)
            if buildable:
                result.append((pkg, None, None))
            if externals:
                sorted_externals = sorted(externals, cmp=lambda a,b: a[0].__cmp__(b[0]))
                for external in sorted_externals:
                    if external[0].satisfies(spec):
                        result.append(external)
        if not result:
            raise NoBuildError(spec)
        return result


    def concretize_virtual_and_external(self, spec):
        """From a list of candidate virtual and external packages, concretize to one that
           is ABI compatible with the rest of the DAG."""
        candidates = self._valid_virtuals_and_externals(spec)
        if not candidates:
            return False

        #Find the another spec in the dag that has a compiler.  We'll use that
        # spec to test compiler compatibility.
        other_spec = self._find_other_spec(spec, lambda(x): x.compiler)
        if not other_spec:
            other_spec = spec.root

        #Choose an ABI-compatible candidate, or the first match otherwise.
        candidate = None
        if other_spec:
            candidate = next((c for c in candidates if spack.abi.compatible(c[0], other_spec)), None)
            if not candidate:
                #Try a looser ABI matching
                candidate = next((c for c in candidates if spack.abi.compatible(c[0], other_spec, loose=True)), None)
        if not candidate:
            #No ABI matches. Pick the top choice based on the orignal preferences.
            candidate = candidates[0]
        external_module = candidate[2]
        external = candidate[1]
        candidate_spec = candidate[0]
        
        #Refine this spec to the candidate.
        changed = False
        if spec.virtual:
            spec._replace_with(candidate_spec)
            changed = True
        if spec._dup(candidate_spec, deps=False, cleardeps=False):
            changed = True
        if not spec.external and external:
            spec.external = external
            changed = True
        if not spec.external_module and external_module:
            spec.external_module = external_module
            changed = True

        #If we're external then trim the dependencies
        if external and spec.dependencies:
            changed = True
            spec.dependencies = DependencyMap()
        
        return changed
        
        
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
        pkg = spec.package # Gives error here with dynist
        cmp_versions = partial(spack.pkgsort.version_compare, spec.name)
        valid_versions = sorted(
            [v for v in pkg.versions
             if any(v.satisfies(sv) for sv in spec.versions)],
            cmp=cmp_versions)

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

    def _concretize_platform(self, arch, platform):
        if issubclass(arch.platform.__class__, spack.architecture.Platform):
            return False
        else:
            arch.platform = platform
            return True

    def _concretize_operating_system(self, arch, platform):
        """ Future method for concretizing operating system """
        if isinstance(arch.platform_os, spack.architecture.OperatingSystem):
            return False
        else:
            arch.arch_os = platform.operating_system('default_os')
            return True
            
        
    def _concretize_target(self, arch, platform):
        if isinstance(arch.target, spack.architecture.Target):
            return False
        else:
            arch.target = platform.target('default')
            return True

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

        platform = spack.architecture.sys_type()
        if spec.architecture is None:
            # Create an empty tuple
            Arch = spack.architecture.Arch
            # Set the architecture to all defaults
            spec.architecture = Arch(platform=platform, 
                    platform_os=platform.operating_system('default_os'),
                    target=platform.target('default'))
            return True
         #If there is a target and it is a tuple and has both filled return
         #False
        if not isinstance(spec.architecture, basestring):
            return any((
                self._concretize_platform(spec.architecture, platform),
                self._concretize_operating_system(spec.architecture, platform),
                self._concretize_target(spec.architecture, platform)))
        else:
            spec.add_architecture_from_string(spec.architecture)

        # Does not look pretty at all!!!
        if spec.root.architecture and \
            not isinstance(spec.root.architecture, basestring):
                bool_flag =  any((
                    self._concretize_platform(spec.root.architecture, platform),
                    self._concretize_operating_system(spec.root.architecture, 
                                                      platform),
                    self._concretize_target(spec.root.target, platform)))
                spec.architecture =spec.root.architecture
                return bool_flag
        else:
            spec.add_architecture_from_string(spec.root.architecture)

        return True
                
        # if there is no target specified used the defaults
    
        #if spec.target is not None:
        #    if isinstance(spec.target,spack.architecture.Target):
        #        return False
        #    else:
        #        spec.add_target_from_string(spec.target)
        #        return True #changed

        #if spec.root.target:
        #    if isinstance(spec.root.target,spack.architecture.Target):
        #        spec.target = spec.root.target
        #    else:
        #        spec.add_target_from_string(spec.root.target)
        #else:
        #    platform = spack.architecture.sys_type()
        #    spec.target = platform.target('default')

        #return True #changed


    def concretize_variants(self, spec):
        """If the spec already has variants filled in, return.  Otherwise, add
           the default variants from the package specification.
        """
        changed = False
        for name, variant in spec.package.variants.items():
            if name not in spec.variants:
                spec.variants[name] = spack.spec.VariantSpec(name, variant.default)
                changed = True
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
        if not spec.architecture.target:
            #Although this usually means changed, this means awaiting other changes
            return True

        # Only use a matching compiler if it is of the proper style
        # Takes advantage of the proper logic already existing in compiler_for_spec
        # Should think whether this can be more efficient
        def _proper_compiler_style(cspec, architecture):
            compilers = spack.compilers.compilers_for_spec(cspec)
            if architecture.target.compiler_strategy == 'PATH':
                filter(lambda c: not c.modules, compilers)
            if architecture.target.compiler_strategy == 'MODULES':
                filter(lambda c: c.modules, compilers)
            return compilers

        
        all_compilers = spack.compilers.all_compilers()

        if (spec.compiler and
            spec.compiler.concrete and
            spec.compiler in all_compilers):
            return False

        #Find the another spec that has a compiler, or the root if none do
        other_spec = self._find_other_spec(spec, lambda(x) : x.compiler)
        if not other_spec:
            other_spec = spec.root
        other_compiler = other_spec.compiler
        assert(other_spec)
        
        # Check if the compiler is already fully specified
        if other_compiler in all_compilers:
            spec.compiler = other_compiler.copy()
            return True
            
        # Filter the compilers into a sorted list based on the compiler_order from spackconfig
        compiler_list = all_compilers if not other_compiler else spack.compilers.find(other_compiler)
        cmp_compilers = partial(spack.pkgsort.compiler_compare, other_spec.name)
        matches = sorted(compiler_list, cmp=cmp_compilers)
        if not matches:
            raise UnavailableCompilerVersionError(other_compiler)
            
        # copy concrete version into other_compiler
        index = len(matches)-1
        while not _proper_compiler_style(matches[index], spec.architecture):
            index -= 1
            if index == 0:
                raise NoValidVersionError(spec)
        spec.compiler = matches[index].copy()
        assert(spec.compiler.concrete)
        return True  # things changed.


    def choose_provider(self, package_spec, spec, providers):
        """This is invoked for virtual specs.  Given a spec with a virtual name,
           say "mpi", and a list of specs of possible providers of that spec,
           select a provider and return it.
        """
        assert(spec.virtual)
        assert(providers)
        
        provider_cmp = partial(spack.pkgsort.provider_compare, package_spec.name, spec.name)
        sorted_providers = sorted(providers, cmp=provider_cmp)
        first_key = sorted_providers[0]

        return first_key


class UnavailableCompilerVersionError(spack.error.SpackError):
    """Raised when there is no available compiler that satisfies a
       compiler spec."""
    def __init__(self, compiler_spec):
        super(UnavailableCompilerVersionError, self).__init__(
            "No available compiler version matches '%s'" % compiler_spec,
            "Run 'spack compilers' to see available compiler Options.")


class NoValidVersionError(spack.error.SpackError):
    """Raised when there is no way to have a concrete version for a
       particular spec."""
    def __init__(self, spec):
        super(NoValidVersionError, self).__init__(
            "There are no valid versions for %s that match '%s'" % (spec.name, spec.versions))


class NoBuildError(spack.error.SpackError):
    """Raised when a package is configured with the nobuild option, but
       no satisfactory external versions can be found"""
    def __init__(self, spec):
        super(NoBuildError, self).__init__(
            "The spec '%s' is configured as nobuild, and no matching external installs were found" % spec.name)
       
