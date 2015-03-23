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
Spack allows very fine-grained control over how packages are installed and
over how they are built and configured.  To make this easy, it has its own
syntax for declaring a dependence.  We call a descriptor of a particular
package configuration a "spec".

The syntax looks like this:

.. code-block:: sh

    $ spack install mpileaks ^openmpi @1.2:1.4 +debug %intel @12.1 =bgqos_0
                    0        1        2        3      4      5     6

The first part of this is the command, 'spack install'.  The rest of the
line is a spec for a particular installation of the mpileaks package.

0. The package to install

1. A dependency of the package, prefixed by ^

2. A version descriptor for the package.  This can either be a specific
   version, like "1.2", or it can be a range of versions, e.g. "1.2:1.4".
   If multiple specific versions or multiple ranges are acceptable, they
   can be separated by commas, e.g. if a package will only build with
   versions 1.0, 1.2-1.4, and 1.6-1.8 of mavpich, you could say:

       depends_on("mvapich@1.0,1.2:1.4,1.6:1.8")

3. A compile-time variant of the package.  If you need openmpi to be
   built in debug mode for your package to work, you can require it by
   adding +debug to the openmpi spec when you depend on it.  If you do
   NOT want the debug option to be enabled, then replace this with -debug.

4. The name of the compiler to build with.

5. The versions of the compiler to build with.  Note that the identifier
   for a compiler version is the same '@' that is used for a package version.
   A version list denoted by '@' is associated with the compiler only if
   if it comes immediately after the compiler name.  Otherwise it will be
   associated with the current package spec.

6. The architecture to build with.  This is needed on machines where
   cross-compilation is required

Here is the EBNF grammar for a spec::

  spec-list    = { spec [ dep-list ] }
  dep_list     = { ^ spec }
  spec         = id [ options ]
  options      = { @version-list | +variant | -variant | ~variant |
                   %compiler | =architecture }
  variant      = id
  architecture = id
  compiler     = id [ version-list ]
  version-list = version [ { , version } ]
  version      = id | id: | :id | id:id
  id           = [A-Za-z0-9_][A-Za-z0-9_.-]*

There is one context-sensitive part: ids in versions may contain '.', while
other ids may not.

There is one ambiguity: since '-' is allowed in an id, you need to put
whitespace space before -variant for it to be tokenized properly.  You can
either use whitespace, or you can just use ~variant since it means the same
thing.  Spack uses ~variant in directory names and in the canonical form of
specs to avoid ambiguity.  Both are provided because ~ can cause shell
expansion when it is the first character in an id typed on the command line.
"""
import sys
import itertools
import hashlib
from StringIO import StringIO
from operator import attrgetter

import llnl.util.tty as tty
from llnl.util.lang import *
from llnl.util.tty.color import *

import spack
import spack.parse
import spack.error
import spack.compilers as compilers

from spack.version import *
from spack.util.string import *
from spack.util.prefix import Prefix
from spack.virtual import ProviderIndex

# Convenient names for color formats so that other things can use them
compiler_color         = '@g'
version_color          = '@c'
architecture_color     = '@m'
enabled_variant_color  = '@B'
disabled_variant_color = '@r'
dependency_color       = '@.'

"""This map determines the coloring of specs when using color output.
   We make the fields different colors to enhance readability.
   See spack.color for descriptions of the color codes. """
color_formats = {'%' : compiler_color,
                 '@' : version_color,
                 '=' : architecture_color,
                 '+' : enabled_variant_color,
                 '~' : disabled_variant_color,
                 '^' : dependency_color }

"""Regex used for splitting by spec field separators."""
_separators = '[%s]' % ''.join(color_formats.keys())

"""Versionlist constant so we don't have to build a list
   every time we call str()"""
_any_version = VersionList([':'])


def index_specs(specs):
    """Take a list of specs and return a dict of lists.  Dict is
       keyed by spec name and lists include all specs with the
       same name.
    """
    spec_dict = {}
    for spec in specs:
        if not spec.name in spec_dict:
            spec_dict[spec.name] = []
        spec_dict[spec.name].append(spec)
    return spec_dict


def colorize_spec(spec):
    """Returns a spec colorized according to the colors specified in
       color_formats."""
    class insert_color:
        def __init__(self):
            self.last = None

        def __call__(self, match):
            # ignore compiler versions (color same as compiler)
            sep = match.group(0)
            if self.last == '%' and sep == '@':
                return cescape(sep)
            self.last = sep

            return '%s%s' % (color_formats[sep], cescape(sep))

    return colorize(re.sub(_separators, insert_color(), str(spec)) + '@.')


@key_ordering
class CompilerSpec(object):
    """The CompilerSpec field represents the compiler or range of compiler
       versions that a package should be built with.  CompilerSpecs have a
       name and a version list. """
    def __init__(self, *args):
        nargs = len(args)
        if nargs == 1:
            arg = args[0]
            # If there is one argument, it's either another CompilerSpec
            # to copy or a string to parse
            if isinstance(arg, basestring):
                c = SpecParser().parse_compiler(arg)
                self.name = c.name
                self.versions = c.versions

            elif isinstance(arg, CompilerSpec):
                self.name = arg.name
                self.versions = arg.versions.copy()

            else:
                raise TypeError(
                    "Can only build CompilerSpec from string or CompilerSpec." +
                    "  Found %s" % type(arg))

        elif nargs == 2:
            name, version = args
            self.name = name
            self.versions = VersionList()
            self.versions.add(ver(version))

        else:
            raise TypeError(
                "__init__ takes 1 or 2 arguments. (%d given)" % nargs)


    def _add_version(self, version):
        self.versions.add(version)


    def _autospec(self, compiler_spec_like):
        if isinstance(compiler_spec_like, CompilerSpec):
            return compiler_spec_like
        return CompilerSpec(compiler_spec_like)


    def satisfies(self, other):
        other = self._autospec(other)
        return (self.name == other.name and
                self.versions.satisfies(other.versions))


    def constrain(self, other):
        other = self._autospec(other)

        # ensure that other will actually constrain this spec.
        if not other.satisfies(self):
            raise UnsatisfiableCompilerSpecError(other, self)

        self.versions.intersect(other.versions)


    @property
    def concrete(self):
        """A CompilerSpec is concrete if its versions are concrete and there
           is an available compiler with the right version."""
        return self.versions.concrete


    @property
    def version(self):
        if not self.concrete:
            raise SpecError("Spec is not concrete: " + str(self))
        return self.versions[0]


    def copy(self):
        clone = CompilerSpec.__new__(CompilerSpec)
        clone.name = self.name
        clone.versions = self.versions.copy()
        return clone


    def _cmp_key(self):
        return (self.name, self.versions)


    def __str__(self):
        out = self.name
        if self.versions and self.versions != _any_version:
            vlist = ",".join(str(v) for v in self.versions)
            out += "@%s" % vlist
        return out

    def __repr__(self):
        return str(self)


@key_ordering
class Variant(object):
    """Variants are named, build-time options for a package.  Names depend
       on the particular package being built, and each named variant can
       be enabled or disabled.
    """
    def __init__(self, name, enabled):
        self.name = name
        self.enabled = enabled


    def _cmp_key(self):
        return (self.name, self.enabled)


    def copy(self):
        return Variant(self.name, self.enabled)


    def __str__(self):
        out = '+' if self.enabled else '~'
        return out + self.name


class VariantMap(HashableMap):
    def satisfies(self, other):
        return all(self[key].enabled == other[key].enabled
                   for key in other if key in self)


    def __str__(self):
        sorted_keys = sorted(self.keys())
        return ''.join(str(self[key]) for key in sorted_keys)


class DependencyMap(HashableMap):
    """Each spec has a DependencyMap containing specs for its dependencies.
       The DependencyMap is keyed by name. """
    @property
    def concrete(self):
        return all(d.concrete for d in self.values())


    def __str__(self):
        return ''.join(
            ["^" + str(self[name]) for name in sorted(self.keys())])


@key_ordering
class Spec(object):
    def __init__(self, spec_like, *dep_like, **kwargs):
        # Copy if spec_like is a Spec.
        if isinstance(spec_like, Spec):
            self._dup(spec_like)
            return

        # Parse if the spec_like is a string.
        if not isinstance(spec_like, basestring):
            raise TypeError("Can't make spec out of %s" % type(spec_like))

        spec_list = SpecParser().parse(spec_like)
        if len(spec_list) > 1:
            raise ValueError("More than one spec in string: " + spec_like)
        if len(spec_list) < 1:
            raise ValueError("String contains no specs: " + spec_like)

        # Take all the attributes from the first parsed spec without copying.
        # This is safe b/c we throw out the parsed spec.  It's a bit nasty,
        # but it's nastier to implement the constructor so that the parser
        # writes directly into this Spec object.
        other = spec_list[0]
        self.name = other.name
        self.dependents = other.dependents
        self.versions = other.versions
        self.variants = other.variants
        self.architecture = other.architecture
        self.compiler = other.compiler
        self.dependencies = other.dependencies

        # Specs are by default not assumed to be normal, but in some
        # cases we've read them from a file want to assume normal.
        # This allows us to manipulate specs that Spack doesn't have
        # package.py files for.
        self._normal = kwargs.get('normal', False)
        self._concrete = kwargs.get('concrete', False)

        # This allows users to construct a spec DAG with literals.
        # Note that given two specs a and b, Spec(a) copies a, but
        # Spec(a, b) will copy a but just add b as a dep.
        for dep in dep_like:
            spec = dep if isinstance(dep, Spec) else Spec(dep)
            self._add_dependency(spec)


    #
    # Private routines here are called by the parser when building a spec.
    #
    def _add_version(self, version):
        """Called by the parser to add an allowable version."""
        self.versions.add(version)


    def _add_variant(self, name, enabled):
        """Called by the parser to add a variant."""
        if name in self.variants: raise DuplicateVariantError(
                "Cannot specify variant '%s' twice" % name)
        self.variants[name] = Variant(name, enabled)


    def _set_compiler(self, compiler):
        """Called by the parser to set the compiler."""
        if self.compiler: raise DuplicateCompilerSpecError(
                "Spec for '%s' cannot have two compilers." % self.name)
        self.compiler = compiler


    def _set_architecture(self, architecture):
        """Called by the parser to set the architecture."""
        if self.architecture: raise DuplicateArchitectureError(
                "Spec for '%s' cannot have two architectures." % self.name)
        self.architecture = architecture


    def _add_dependency(self, spec):
        """Called by the parser to add another spec as a dependency."""
        if spec.name in self.dependencies:
            raise DuplicateDependencyError("Cannot depend on '%s' twice" % spec)
        self.dependencies[spec.name] = spec
        spec.dependents[self.name] = self


    @property
    def root(self):
        """Follow dependent links and find the root of this spec's DAG.
           In spack specs, there should be a single root (the package being
           installed).  This will throw an assertion error if that is not
           the case.
        """
        if not self.dependents:
            return self

        # If the spec has multiple dependents, ensure that they all
        # lead to the same place.  Spack shouldn't deal with any DAGs
        # with multiple roots, so something's wrong if we find one.
        depiter = iter(self.dependents.values())
        first_root = next(depiter).root
        assert(all(first_root is d.root for d in depiter))
        return first_root


    @property
    def package(self):
        return spack.db.get(self)


    @property
    def virtual(self):
        """Right now, a spec is virtual if no package exists with its name.

           TODO: revisit this -- might need to use a separate namespace and
           be more explicit about this.
           Possible idea: just use conventin and make virtual deps all
           caps, e.g., MPI vs mpi.
        """
        return not spack.db.exists(self.name)


    @property
    def concrete(self):
        """A spec is concrete if it can describe only ONE build of a package.
           If any of the name, version, architecture, compiler, or depdenencies
           are ambiguous,then it is not concrete.
        """
        if self._concrete:
            return True

        self._concrete = bool(not self.virtual
                              and self.versions.concrete
                              and self.architecture
                              and self.compiler and self.compiler.concrete
                              and self.dependencies.concrete)
        return self._concrete


    def traverse(self, visited=None, d=0, **kwargs):
        """Generic traversal of the DAG represented by this spec.
           This will yield each node in the spec.  Options:

           order    [=pre|post]
               Order to traverse spec nodes. Defaults to preorder traversal.
               Options are:

               'pre':  Pre-order traversal; each node is yielded before its
                       children in the dependency DAG.
               'post': Post-order  traversal; each node is yielded after its
                       children in the dependency DAG.

           cover    [=nodes|edges|paths]
               Determines how extensively to cover the dag.  Possible vlaues:

               'nodes': Visit each node in the dag only once.  Every node
                        yielded by this function will be unique.
               'edges': If a node has been visited once but is reached along a
                        new path from the root, yield it but do not descend
                        into it.  This traverses each 'edge' in the DAG once.
               'paths': Explore every unique path reachable from the root.
                        This descends into visited subtrees and will yield
                        nodes twice if they're reachable by multiple paths.

           depth    [=False]
               Defaults to False.  When True, yields not just nodes in the
               spec, but also their depth from the root in a (depth, node)
               tuple.

           key   [=id]
               Allow a custom key function to track the identity of nodes
               in the traversal.

           root     [=True]
               If false, this won't yield the root node, just its descendents.

           direction [=children|parents]
               If 'children', does a traversal of this spec's children.  If
               'parents', traverses upwards in the DAG towards the root.

        """
        # get initial values for kwargs
        depth      = kwargs.get('depth', False)
        key_fun    = kwargs.get('key', id)
        if isinstance(key_fun, basestring):
            key_fun = attrgetter(key_fun)
        yield_root = kwargs.get('root', True)
        cover      = kwargs.get('cover', 'nodes')
        direction  = kwargs.get('direction', 'children')
        order      = kwargs.get('order', 'pre')

        # Make sure kwargs have legal values; raise ValueError if not.
        def validate(name, val, allowed_values):
            if val not in allowed_values:
                raise ValueError("Invalid value for %s: %s.  Choices are %s"
                                 % (name, val, ",".join(allowed_values)))
        validate('cover',     cover,     ('nodes', 'edges', 'paths'))
        validate('direction', direction, ('children', 'parents'))
        validate('order',     order,     ('pre', 'post'))

        if visited is None:
            visited = set()
        key = key_fun(self)

        # Node traversal does not yield visited nodes.
        if key in visited and cover == 'nodes':
            return

        # Determine whether and what to yield for this node.
        yield_me = yield_root or d > 0
        result = (d, self) if depth else self

        # Preorder traversal yields before successors
        if yield_me and order == 'pre':
            yield result

        # Edge traversal yields but skips children of visited nodes
        if not (key in visited and cover == 'edges'):
            # This code determines direction and yields the children/parents
            successors = self.dependencies
            if direction == 'parents':
                successors = self.dependents

            visited.add(key)
            for name in sorted(successors):
                child = successors[name]
                for elt in child.traverse(visited, d+1, **kwargs):
                    yield elt

        # Postorder traversal yields after successors
        if yield_me and order == 'post':
            yield result


    @property
    def short_spec(self):
        """Returns a version of the spec with the dependencies hashed
           instead of completely enumerated."""
        return self.format('$_$@$%@$+$=$#')


    @property
    def cshort_spec(self):
        """Returns a version of the spec with the dependencies hashed
           instead of completely enumerated."""
        return self.format('$_$@$%@$+$=$#', color=True)


    @property
    def prefix(self):
        return Prefix(spack.install_layout.path_for_spec(self))


    def dep_hash(self, length=None):
        """Return a hash representing all dependencies of this spec
           (direct and indirect).

           If you want this hash to be consistent, you should
           concretize the spec first so that it is not ambiguous.
        """
        sha = hashlib.sha1()
        sha.update(self.dep_string())
        full_hash = sha.hexdigest()

        return full_hash[:length]


    def _concretize_helper(self, presets=None, visited=None):
        """Recursive helper function for concretize().
           This concretizes everything bottom-up.  As things are
           concretized, they're added to the presets, and ancestors
           will prefer the settings of their children.
        """
        if presets is None: presets = {}
        if visited is None: visited = set()

        if self.name in visited:
            return

        # Concretize deps first -- this is a bottom-up process.
        for name in sorted(self.dependencies.keys()):
            self.dependencies[name]._concretize_helper(presets, visited)

        if self.name in presets:
            self.constrain(presets[self.name])
        else:
            # Concretize virtual dependencies last.  Because they're added
            # to presets below, their constraints will all be merged, but we'll
            # still need to select a concrete package later.
            if not self.virtual:
                spack.concretizer.concretize_architecture(self)
                spack.concretizer.concretize_compiler(self)
                spack.concretizer.concretize_version(self)
            presets[self.name] = self

        visited.add(self.name)


    def _replace_with(self, concrete):
        """Replace this virtual spec with a concrete spec."""
        assert(self.virtual)
        for name, dependent in self.dependents.items():
            del dependent.dependencies[self.name]
            dependent._add_dependency(concrete)


    def _expand_virtual_packages(self):
        """Find virtual packages in this spec, replace them with providers,
           and normalize again to include the provider's (potentially virtual)
           dependencies.  Repeat until there are no virtual deps.

           Precondition: spec is normalized.

           .. todo::

              If a provider depends on something that conflicts with
              other dependencies in the spec being expanded, this can
              produce a conflicting spec.  For example, if mpich depends
              on hwloc@:1.3 but something in the spec needs hwloc1.4:,
              then we should choose an MPI other than mpich.  Cases like
              this are infrequent, but should implement this before it is
              a problem.
        """
        while True:
            virtuals =[v for v in self.traverse() if v.virtual]
            if not virtuals:
                return

            for spec in virtuals:
                providers = spack.db.providers_for(spec)
                concrete = spack.concretizer.choose_provider(spec, providers)
                concrete = concrete.copy()
                spec._replace_with(concrete)

            # If there are duplicate providers or duplicate provider deps, this
            # consolidates them and merge constraints.
            self.normalize(force=True)


    def concretize(self):
        """A spec is concrete if it describes one build of a package uniquely.
           This will ensure that this spec is concrete.

           If this spec could describe more than one version, variant, or build
           of a package, this will add constraints to make it concrete.

           Some rigorous validation and checks are also performed on the spec.
           Concretizing ensures that it is self-consistent and that it's consistent
           with requirements of its pacakges.  See flatten() and normalize() for
           more details on this.
        """
        if self._concrete:
            return

        self.normalize()
        self._expand_virtual_packages()
        self._concretize_helper()
        self._concrete = True


    def concretized(self):
        """This is a non-destructive version of concretize().  First clones,
           then returns a concrete version of this package without modifying
           this package. """
        clone = self.copy()
        clone.concretize()
        return clone


    def flat_dependencies(self, **kwargs):
        """Return a DependencyMap containing all of this spec's
           dependencies with their constraints merged.

           If copy is True, returns merged copies of its dependencies
           without modifying the spec it's called on.

           If copy is False, clears this spec's dependencies and
           returns them.
        """
        copy = kwargs.get('copy', True)

        flat_deps = DependencyMap()
        try:
            for spec in self.traverse(root=False):
                if spec.name not in flat_deps:
                    if copy:
                        flat_deps[spec.name] = spec.copy(deps=False)
                    else:
                        flat_deps[spec.name] = spec
                else:
                    flat_deps[spec.name].constrain(spec)

            if not copy:
                for dep in flat_deps.values():
                    dep.dependencies.clear()
                    dep.dependents.clear()
                self.dependencies.clear()

            return flat_deps

        except UnsatisfiableSpecError, e:
            # Here, the DAG contains two instances of the same package
            # with inconsistent constraints.  Users cannot produce
            # inconsistent specs like this on the command line: the
            # parser doesn't allow it. Spack must be broken!
            raise InconsistentSpecError("Invalid Spec DAG: %s" % e.message)


    def index(self):
        """Return DependencyMap that points to all the dependencies in this
           spec."""
        dm = DependencyMap()
        for spec in self.traverse():
            dm[spec.name] = spec
        return dm


    def flatten(self):
        """Pull all dependencies up to the root (this spec).
           Merge constraints for dependencies with the same name, and if they
           conflict, throw an exception. """
        for dep in self.flat_dependencies(copy=False):
            self._add_dependency(dep)


    def _normalize_helper(self, visited, spec_deps, provider_index):
        """Recursive helper function for _normalize."""
        if self.name in visited:
            return
        visited.add(self.name)

        # if we descend into a virtual spec, there's nothing more
        # to normalize.  Concretize will finish resolving it later.
        if self.virtual:
            return

        # Combine constraints from package dependencies with
        # constraints on the spec's dependencies.
        pkg = spack.db.get(self.name)
        for name, pkg_dep in self.package.dependencies.items():
            # If it's a virtual dependency, try to find a provider
            if pkg_dep.virtual:
                providers = provider_index.providers_for(pkg_dep)

                # If there is a provider for the vpkg, then use that instead of
                # the virtual package.
                if providers:
                    # Can't have multiple providers for the same thing in one spec.
                    if len(providers) > 1:
                        raise MultipleProviderError(pkg_dep, providers)

                    pkg_dep = providers[0]
                    name    = pkg_dep.name

                else:
                    # The user might have required something insufficient for
                    # pkg_dep -- so we'll get a conflict.  e.g., user asked for
                    # mpi@:1.1 but some package required mpi@2.1:.
                    required = provider_index.providers_for(name)
                    if len(required) > 1:
                        raise MultipleProviderError(pkg_dep, required)
                    elif required:
                        raise UnsatisfiableProviderSpecError(
                            required[0], pkg_dep)
            else:
                # if it's a real dependency, check whether it provides something
                # already required in the spec.
                index = ProviderIndex([pkg_dep], restrict=True)
                for vspec in (v for v in spec_deps.values() if v.virtual):
                    if index.providers_for(vspec):
                        vspec._replace_with(pkg_dep)
                        del spec_deps[vspec.name]
                    else:
                        required = index.providers_for(vspec.name)
                        if required:
                            raise UnsatisfiableProviderSpecError(
                                required[0], pkg_dep)
                provider_index.update(pkg_dep)

            if name not in spec_deps:
                # If the spec doesn't reference a dependency that this package
                # needs, then clone it from the package description.
                spec_deps[name] = pkg_dep.copy()

            try:
                # Constrain package information with spec info
                spec_deps[name].constrain(pkg_dep)

            except UnsatisfiableSpecError, e:
                e.message =  "Invalid spec: '%s'. "
                e.message += "Package %s requires %s %s, but spec asked for %s"
                e.message %= (spec_deps[name], name, e.constraint_type,
                              e.required, e.provided)
                raise e

            # Add merged spec to my deps and recurse
            dependency = spec_deps[name]
            self._add_dependency(dependency)
            dependency._normalize_helper(visited, spec_deps, provider_index)


    def normalize(self, **kwargs):
        """When specs are parsed, any dependencies specified are hanging off
           the root, and ONLY the ones that were explicitly provided are there.
           Normalization turns a partial flat spec into a DAG, where:

           1. ALL dependencies of the root package are in the DAG.
           2. Each node's dependencies dict only contains its direct deps.
           3. There is only ONE unique spec for each package in the DAG.

              * This includes virtual packages.  If there a non-virtual
                package that provides a virtual package that is in the spec,
                then we replace the virtual package with the non-virtual one.

           4. The spec DAG matches package DAG.

           TODO: normalize should probably implement some form of cycle detection,
           to ensure that the spec is actually a DAG.
        """
        if self._normal and not kwargs.get('force', False):
            return

        # Ensure first that all packages & compilers in the DAG exist.
        self.validate_names()

        # Ensure that the package & dep descriptions are consistent & sane
        if not self.virtual:
            self.package.validate_dependencies()

        # Get all the dependencies into one DependencyMap
        spec_deps = self.flat_dependencies(copy=False)

        # Figure out which of the user-provided deps provide virtual deps.
        # Remove virtual deps that are already provided by something in the spec
        spec_packages = [d.package for d in spec_deps.values() if not d.virtual]

        index = ProviderIndex(spec_deps.values(), restrict=True)

        visited = set()
        self._normalize_helper(visited, spec_deps, index)

        # If there are deps specified but not visited, they're not
        # actually deps of this package.  Raise an error.
        extra = set(spec_deps.keys()).difference(visited)

        # Also subtract out all the packags that provide a needed vpkg
        vdeps = [v for v in self.package.virtual_dependencies()]

        vpkg_providers = index.providers_for(*vdeps)
        extra.difference_update(p.name for p in vpkg_providers)

        # Anything left over is not a valid part of the spec.
        if extra:
            raise InvalidDependencyException(
                self.name + " does not depend on " + comma_or(extra))

        # Mark the spec as normal once done.
        self._normal = True


    def normalized(self):
        """Return a normalized copy of this spec without modifying this spec."""
        clone = self.copy()
        clone.normalize()
        return clone


    def validate_names(self):
        """This checks that names of packages and compilers in this spec are real.
           If they're not, it will raise either UnknownPackageError or
           UnsupportedCompilerError.
        """
        for spec in self.traverse():
            # Don't get a package for a virtual name.
            if not spec.virtual:
                spack.db.get(spec.name)

            # validate compiler in addition to the package name.
            if spec.compiler:
                if not compilers.supported(spec.compiler):
                    raise UnsupportedCompilerError(spec.compiler.name)


    def constrain(self, other, **kwargs):
        other = self._autospec(other)
        constrain_deps = kwargs.get('deps', True)

        if not self.name == other.name:
            raise UnsatisfiableSpecNameError(self.name, other.name)

        if not self.versions.overlaps(other.versions):
            raise UnsatisfiableVersionSpecError(self.versions, other.versions)

        for v in other.variants:
            if (v in self.variants and
                self.variants[v].enabled != other.variants[v].enabled):
                raise UnsatisfiableVariantSpecError(self.variants[v],
                                                    other.variants[v])

        if self.architecture is not None and other.architecture is not None:
            if self.architecture != other.architecture:
                raise UnsatisfiableArchitectureSpecError(self.architecture,
                                                         other.architecture)

        if self.compiler is not None and other.compiler is not None:
            self.compiler.constrain(other.compiler)
        elif self.compiler is None:
            self.compiler = other.compiler

        self.versions.intersect(other.versions)
        self.variants.update(other.variants)
        self.architecture = self.architecture or other.architecture

        if constrain_deps:
            self._constrain_dependencies(other)


    def _constrain_dependencies(self, other):
        """Apply constraints of other spec's dependencies to this spec."""
        if not self.dependencies or not other.dependencies:
            return

        # TODO: might want more detail than this, e.g. specific deps
        # in violation. if this becomes a priority get rid of this
        # check and be more specici about what's wrong.
        if not other.satisfies_dependencies(self):
            raise UnsatisfiableDependencySpecError(other, self)

        # Handle common first-order constraints directly
        for name in self.common_dependencies(other):
            self[name].constrain(other[name], deps=False)

        # Update with additional constraints from other spec
        for name in other.dep_difference(self):
            self._add_dependency(other[name].copy())


    def common_dependencies(self, other):
        """Return names of dependencies that self an other have in common."""
        common = set(
            s.name for s in self.traverse(root=False))
        common.intersection_update(
            s.name for s in other.traverse(root=False))
        return common


    def dep_difference(self, other):
        """Returns dependencies in self that are not in other."""
        mine = set(s.name for s in self.traverse(root=False))
        mine.difference_update(
            s.name for s in other.traverse(root=False))
        return mine


    def _autospec(self, spec_like):
        """Used to convert arguments to specs.  If spec_like is a spec, returns it.
           If it's a string, tries to parse a string.  If that fails, tries to parse
           a local spec from it (i.e. name is assumed to be self's name).
        """
        if isinstance(spec_like, spack.spec.Spec):
            return spec_like

        try:
            return spack.spec.Spec(spec_like)
        except SpecError:
            return parse_anonymous_spec(spec_like, self.name)


    def satisfies(self, other, **kwargs):
        other = self._autospec(other)
        satisfy_deps = kwargs.get('deps', True)

        # First thing we care about is whether the name matches
        if self.name != other.name:
            return False

        # All these attrs have satisfies criteria of their own,
        # but can be None to indicate no constraints.
        for s, o in ((self.versions, other.versions),
                     (self.variants, other.variants),
                     (self.compiler, other.compiler)):
            if s and o and not s.satisfies(o):
                return False

        # Architecture satisfaction is currently just string equality.
        # Can be None for unconstrained, though.
        if (self.architecture and other.architecture and
            self.architecture != other.architecture):
            return False

        # If we need to descend into dependencies, do it, otherwise we're done.
        if satisfy_deps:
            return self.satisfies_dependencies(other)
        else:
            return True


    def satisfies_dependencies(self, other):
        """This checks constraints on common dependencies against each other."""
        # if either spec doesn't restrict dependencies then both are compatible.
        if not self.dependencies or not other.dependencies:
            return True

        # Handle first-order constraints directly
        for name in self.common_dependencies(other):
            if not self[name].satisfies(other[name]):
                return False

        # For virtual dependencies, we need to dig a little deeper.
        self_index = ProviderIndex(self.traverse(), restrict=True)
        other_index = ProviderIndex(other.traverse(), restrict=True)

        # This handles cases where there are already providers for both vpkgs
        if not self_index.satisfies(other_index):
            return False

        # These two loops handle cases where there is an overly restrictive vpkg
        # in one spec for a provider in the other (e.g., mpi@3: is not compatible
        # with mpich2)
        for spec in self.virtual_dependencies():
            if spec.name in other_index and not other_index.providers_for(spec):
                return False

        for spec in other.virtual_dependencies():
            if spec.name in self_index and not self_index.providers_for(spec):
                return False

        return True


    def virtual_dependencies(self):
        """Return list of any virtual deps in this spec."""
        return [spec for spec in self.traverse() if spec.virtual]


    def _dup(self, other, **kwargs):
        """Copy the spec other into self.  This is an overwriting
           copy.  It does not copy any dependents (parents), but by default
           copies dependencies.

           To duplicate an entire DAG, call _dup() on the root of the DAG.

           Options:
           dependencies[=True]
               Whether deps should be copied too.  Set to false to copy a
               spec but not its dependencies.
        """
        # Local node attributes get copied first.
        self.name = other.name
        self.versions = other.versions.copy()
        self.variants = other.variants.copy()
        self.architecture = other.architecture
        self.compiler = other.compiler.copy() if other.compiler else None
        self.dependents = DependencyMap()
        self.dependencies = DependencyMap()

        # If we copy dependencies, preserve DAG structure in the new spec
        if kwargs.get('deps', True):
            # This copies the deps from other using _dup(deps=False)
            new_nodes = other.flat_dependencies()
            new_nodes[self.name] = self

            # Hook everything up properly here by traversing.
            for spec in other.traverse(cover='nodes'):
                parent = new_nodes[spec.name]
                for child in spec.dependencies:
                    if child not in parent.dependencies:
                        parent._add_dependency(new_nodes[child])

        # Since we preserved structure, we can copy _normal safely.
        self._normal = other._normal
        self._concrete = other._concrete


    def copy(self, **kwargs):
        """Return a copy of this spec.
           By default, returns a deep copy.  Supply dependencies=False
           to get a shallow copy.
        """
        clone = Spec.__new__(Spec)
        clone._dup(self, **kwargs)
        return clone


    @property
    def version(self):
        if not self.versions.concrete:
            raise SpecError("Spec version is not concrete: " + str(self))
        return self.versions[0]


    def __getitem__(self, name):
        """TODO: reconcile __getitem__, _add_dependency, __contains__"""
        for spec in self.traverse():
            if spec.name == name:
                return spec

        raise KeyError("No spec with name %s in %s" % (name, self))


    def __contains__(self, spec):
        """True if this spec satisfis the provided spec, or if any dependency
           does.  If the spec has no name, then we parse this one first.
        """
        spec = self._autospec(spec)
        for s in self.traverse():
            if s.satisfies(spec):
                return True
        return False


    def sorted_deps(self):
        """Return a list of all dependencies sorted by name."""
        deps = self.flat_dependencies()
        return tuple(deps[name] for name in sorted(deps))


    def _eq_dag(self, other, vs, vo):
        """Recursive helper for eq_dag and ne_dag.  Does the actual DAG
           traversal."""
        vs.add(id(self))
        vo.add(id(other))

        if self.ne_node(other):
            return False

        if len(self.dependencies) != len(other.dependencies):
            return False

        ssorted = [self.dependencies[name]  for name in sorted(self.dependencies)]
        osorted = [other.dependencies[name] for name in sorted(other.dependencies)]

        for s, o in zip(ssorted, osorted):
            visited_s = id(s) in vs
            visited_o = id(o) in vo

            # Check for duplicate or non-equal dependencies
            if visited_s != visited_o: return False

            # Skip visited nodes
            if visited_s or visited_o: continue

            # Recursive check for equality
            if not s._eq_dag(o, vs, vo):
                return False

        return True


    def eq_dag(self, other):
        """True if the full dependency DAGs of specs are equal"""
        return self._eq_dag(other, set(), set())


    def ne_dag(self, other):
        """True if the full dependency DAGs of specs are not equal"""
        return not self.eq_dag(other)


    def _cmp_node(self):
        """Comparison key for just *this node* and not its deps."""
        return (self.name, self.versions, self.variants,
                self.architecture, self.compiler)


    def eq_node(self, other):
        """Equality with another spec, not including dependencies."""
        return self._cmp_node() == other._cmp_node()


    def ne_node(self, other):
        """Inequality with another spec, not including dependencies."""
        return self._cmp_node() != other._cmp_node()


    def _cmp_key(self):
        """Comparison key for this node and all dependencies *without*
           considering structure.  This is the default, as
           normalization will restore structure.
        """
        return self._cmp_node() + (self.sorted_deps(),)


    def colorized(self):
        return colorize_spec(self)


    def format(self, format_string='$_$@$%@$+$=', **kwargs):
        """Prints out particular pieces of a spec, depending on what is
           in the format string.  The format strings you can provide are::

               $_   Package name
               $@   Version with '@' prefix
               $%   Compiler with '%' prefix
               $%@  Compiler with '%' prefix & compiler version with '@' prefix
               $+   Options 
               $=   Architecture with '=' prefix
               $#   Dependencies' 8-char sha1 prefix with '-' prefix
               $$   $

               You can also use full-string versions, which leave off the prefixes:

               ${PACKAGE}       Package name
               ${VERSION}       Version
               ${COMPILER}      Full compiler string
               ${COMPILERNAME}  Compiler name
               ${COMPILERVER}   Compiler version
               ${OPTIONS}       Options
               ${ARCHITECTURE}  Architecture
               ${SHA1}          Dependencies 8-char sha1 prefix

               ${SPACK_ROOT}    The spack root directory
               ${SPACK_INSTALL} The default spack install directory, ${SPACK_PREFIX}/opt


           Optionally you can provide a width, e.g. $20_ for a 20-wide name.
           Like printf, you can provide '-' for left justification, e.g.
           $-20_ for a left-justified name.

           Anything else is copied verbatim into the output stream.

           *Example:*  ``$_$@$+`` translates to the name, version, and options
           of the package, but no dependencies, arch, or compiler.

           TODO: allow, e.g., $6# to customize short hash length
           TODO: allow, e.g., $## for full hash.
           """
        color    = kwargs.get('color', False)
        length = len(format_string)
        out = StringIO()
        named = escape = compiler = False
        named_str = fmt = ''

        def write(s, c):
            if color:
                f = color_formats[c] + cescape(s) + '@.'
                cwrite(f, stream=out, color=color)
            else:
                out.write(s)

        iterator = enumerate(format_string)
        for i, c in iterator:
            if escape:
                fmt = '%'
                if c == '-':
                    fmt += c
                    i, c = next(iterator)

                while c in '0123456789':
                    fmt += c
                    i, c = next(iterator)
                fmt += 's'

                if c == '_':
                    out.write(fmt % self.name)
                elif c == '@':
                    if self.versions and self.versions != _any_version:
                        write(fmt % (c + str(self.versions)), c)
                elif c == '%':
                    if self.compiler:
                        write(fmt % (c + str(self.compiler.name)), c)
                    compiler = True
                elif c == '+':
                    if self.variants:
                        write(fmt % str(self.variants), c)
                elif c == '=':
                    if self.architecture:
                        write(fmt % (c + str(self.architecture)), c)
                elif c == '#':
                    if self.dependencies:
                        out.write(fmt % ('-' + self.dep_hash(8)))
                elif c == '$':
                    if fmt != '%s':
                        raise ValueError("Can't use format width with $$.")
                    out.write('$')
                elif c == '{':
                    named = True
                    named_str = ''
                escape = False

            elif compiler:
                if c == '@':
                    if self.compiler and self.compiler.versions:
                        write(c + str(self.compiler.versions), '%')
                elif c == '$':
                    escape = True
                else:
                    out.write(c)
                compiler = False

            elif named:
                if not c == '}':
                    if i == length - 1:
                        raise ValueError("Error: unterminated ${ in format: '%s'"
                                         % format_string)
                    named_str += c
                    continue;
                if named_str == 'PACKAGE':
                    write(fmt % self.name, '@')
                if named_str == 'VERSION':
                    if self.versions and self.versions != _any_version:
                        write(fmt % str(self.versions), '@')
                elif named_str == 'COMPILER':
                    if self.compiler:
                        write(fmt % self.compiler, '%')
                elif named_str == 'COMPILERNAME':
                    if self.compiler:
                        write(fmt % self.compiler.name, '%')
                elif named_str == 'COMPILERVER':
                    if self.compiler:
                        write(fmt % self.compiler.versions, '%')
                elif named_str == 'OPTIONS':
                    if self.variants:
                        write(fmt % str(self.variants), '+')
                elif named_str == 'ARCHITECTURE':
                    if self.architecture:
                        write(fmt % str(self.architecture), '=')
                elif named_str == 'SHA1':
                    if self.dependencies:
                        out.write(fmt % str(self.dep_hash(8)))
                elif named_str == 'SPACK_ROOT':
                    out.write(fmt % spack.prefix)
                elif named_str == 'SPACK_INSTALL':
                    out.write(fmt % spack.install_path)

                named = False

            elif c == '$':
                escape = True
                if i == length - 1:
                    raise ValueError("Error: unterminated $ in format: '%s'"
                                     % format_string)
            else:
                out.write(c)

        result = out.getvalue()
        return result


    def dep_string(self):
        return ''.join("^" + dep.format() for dep in self.sorted_deps())


    def __str__(self):
        return self.format() + self.dep_string()


    def tree(self, **kwargs):
        """Prints out this spec and its dependencies, tree-formatted
           with indentation."""
        color  = kwargs.pop('color', False)
        depth  = kwargs.pop('depth', False)
        showid = kwargs.pop('ids',   False)
        cover  = kwargs.pop('cover', 'nodes')
        indent = kwargs.pop('indent', 0)
        fmt    = kwargs.pop('format', '$_$@$%@$+$=')
        check_kwargs(kwargs, self.tree)

        out = ""
        cur_id = 0
        ids = {}
        for d, node in self.traverse(order='pre', cover=cover, depth=True):
            out += " " * indent
            if depth:
                out += "%-4d" % d
            if not id(node) in ids:
                cur_id += 1
                ids[id(node)] = cur_id
            if showid:
                out += "%-4d" % ids[id(node)]
            out += ("    " * d)
            if d > 0:
                out += "^"
            out += node.format(fmt, color=color) + "\n"
        return out


    def __repr__(self):
        return str(self)


#
# These are possible token types in the spec grammar.
#
DEP, AT, COLON, COMMA, ON, OFF, PCT, EQ, ID = range(9)

class SpecLexer(spack.parse.Lexer):
    """Parses tokens that make up spack specs."""
    def __init__(self):
        super(SpecLexer, self).__init__([
            (r'\^',        lambda scanner, val: self.token(DEP,   val)),
            (r'\@',        lambda scanner, val: self.token(AT,    val)),
            (r'\:',        lambda scanner, val: self.token(COLON, val)),
            (r'\,',        lambda scanner, val: self.token(COMMA, val)),
            (r'\+',        lambda scanner, val: self.token(ON,    val)),
            (r'\-',        lambda scanner, val: self.token(OFF,   val)),
            (r'\~',        lambda scanner, val: self.token(OFF,   val)),
            (r'\%',        lambda scanner, val: self.token(PCT,   val)),
            (r'\=',        lambda scanner, val: self.token(EQ,    val)),
            (r'\w[\w.-]*', lambda scanner, val: self.token(ID,    val)),
            (r'\s+',       lambda scanner, val: None)])


class SpecParser(spack.parse.Parser):
    def __init__(self):
        super(SpecParser, self).__init__(SpecLexer())


    def do_parse(self):
        specs = []

        try:
            while self.next:
                if self.accept(ID):
                    specs.append(self.spec())

                elif self.accept(DEP):
                    if not specs:
                        self.last_token_error("Dependency has no package")
                    self.expect(ID)
                    specs[-1]._add_dependency(self.spec())

                else:
                    self.unexpected_token()
        except spack.parse.ParseError, e:
            raise SpecParseError(e)

        return specs


    def parse_compiler(self, text):
        self.setup(text)
        return self.compiler()


    def spec(self):
        """Parse a spec out of the input.  If a spec is supplied, then initialize
           and return it instead of creating a new one."""
        self.check_identifier()

        # This will init the spec without calling __init__.
        spec = Spec.__new__(Spec)
        spec.name = self.token.value
        spec.versions = VersionList()
        spec.variants = VariantMap()
        spec.architecture = None
        spec.compiler = None
        spec.dependents   = DependencyMap()
        spec.dependencies = DependencyMap()

        spec._normal = False
        spec._concrete = False

        # record this so that we know whether version is
        # unspecified or not.
        added_version = False

        while self.next:
            if self.accept(AT):
                vlist = self.version_list()
                for version in vlist:
                    spec._add_version(version)
                added_version = True

            elif self.accept(ON):
                spec._add_variant(self.variant(), True)

            elif self.accept(OFF):
                spec._add_variant(self.variant(), False)

            elif self.accept(PCT):
                spec._set_compiler(self.compiler())

            elif self.accept(EQ):
                spec._set_architecture(self.architecture())

            else:
                break

        # If there was no version in the spec, consier it an open range
        if not added_version:
            spec.versions = VersionList(':')

        return spec


    def variant(self):
        self.expect(ID)
        self.check_identifier()
        return self.token.value


    def architecture(self):
        self.expect(ID)
        return self.token.value


    def version(self):
        start = None
        end = None
        if self.accept(ID):
            start = self.token.value

        if self.accept(COLON):
            if self.accept(ID):
                end = self.token.value
        elif start:
            # No colon, but there was a version.
            return Version(start)
        else:
            # No colon and no id: invalid version.
            self.next_token_error("Invalid version specifier")

        if start: start = Version(start)
        if end: end = Version(end)
        return VersionRange(start, end)


    def version_list(self):
        vlist = []
        vlist.append(self.version())
        while self.accept(COMMA):
            vlist.append(self.version())
        return vlist


    def compiler(self):
        self.expect(ID)
        self.check_identifier()

        compiler = CompilerSpec.__new__(CompilerSpec)
        compiler.name = self.token.value
        compiler.versions = VersionList()
        if self.accept(AT):
            vlist = self.version_list()
            for version in vlist:
                compiler._add_version(version)
        else:
            compiler.versions = VersionList(':')
        return compiler


    def check_identifier(self):
        """The only identifiers that can contain '.' are versions, but version
           ids are context-sensitive so we have to check on a case-by-case
           basis. Call this if we detect a version id where it shouldn't be.
        """
        if '.' in self.token.value:
            self.last_token_error("Identifier cannot contain '.'")


def parse(string):
    """Returns a list of specs from an input string.
       For creating one spec, see Spec() constructor.
    """
    return SpecParser().parse(string)


def parse_anonymous_spec(spec_like, pkg_name):
    """Allow the user to omit the package name part of a spec if they
       know what it has to be already.

       e.g., provides('mpi@2', when='@1.9:') says that this package
       provides MPI-3 when its version is higher than 1.9.
    """
    if not isinstance(spec_like, (str, Spec)):
        raise TypeError('spec must be Spec or spec string.  Found %s'
                        % type(spec_like))

    if isinstance(spec_like, str):
        try:
            anon_spec = Spec(spec_like)
        except SpecParseError:
            anon_spec = Spec(pkg_name + spec_like)
            if anon_spec.name != pkg_name: raise ValueError(
                    "Invalid spec for package %s: %s" % (pkg_name, spec_like))
    else:
        anon_spec = spec_like.copy()

    if anon_spec.name != pkg_name:
        raise ValueError("Spec name '%s' must match package name '%s'"
                         % (anon_spec.name, pkg_name))

    return anon_spec


class SpecError(spack.error.SpackError):
    """Superclass for all errors that occur while constructing specs."""
    def __init__(self, message):
        super(SpecError, self).__init__(message)


class SpecParseError(SpecError):
    """Wrapper for ParseError for when we're parsing specs."""
    def __init__(self, parse_error):
        super(SpecParseError, self).__init__(parse_error.message)
        self.string = parse_error.string
        self.pos = parse_error.pos


class DuplicateDependencyError(SpecError):
    """Raised when the same dependency occurs in a spec twice."""
    def __init__(self, message):
        super(DuplicateDependencyError, self).__init__(message)


class DuplicateVariantError(SpecError):
    """Raised when the same variant occurs in a spec twice."""
    def __init__(self, message):
        super(DuplicateVariantError, self).__init__(message)


class DuplicateCompilerSpecError(SpecError):
    """Raised when the same compiler occurs in a spec twice."""
    def __init__(self, message):
        super(DuplicateCompilerSpecError, self).__init__(message)


class UnsupportedCompilerError(SpecError):
    """Raised when the user asks for a compiler spack doesn't know about."""
    def __init__(self, compiler_name):
        super(UnsupportedCompilerError, self).__init__(
            "The '%s' compiler is not yet supported." % compiler_name)


class DuplicateArchitectureError(SpecError):
    """Raised when the same architecture occurs in a spec twice."""
    def __init__(self, message):
        super(DuplicateArchitectureError, self).__init__(message)


class InconsistentSpecError(SpecError):
    """Raised when two nodes in the same spec DAG have inconsistent
       constraints."""
    def __init__(self, message):
        super(InconsistentSpecError, self).__init__(message)


class InvalidDependencyException(SpecError):
    """Raised when a dependency in a spec is not actually a dependency
       of the package."""
    def __init__(self, message):
        super(InvalidDependencyException, self).__init__(message)


class NoProviderError(SpecError):
    """Raised when there is no package that provides a particular
       virtual dependency.
    """
    def __init__(self, vpkg):
        super(NoProviderError, self).__init__(
            "No providers found for virtual package: '%s'" % vpkg)
        self.vpkg = vpkg


class MultipleProviderError(SpecError):
    """Raised when there is no package that provides a particular
       virtual dependency.
    """
    def __init__(self, vpkg, providers):
        """Takes the name of the vpkg"""
        super(MultipleProviderError, self).__init__(
            "Multiple providers found for '%s': %s"
            % (vpkg, [str(s) for s in providers]))
        self.vpkg = vpkg
        self.providers = providers


class UnsatisfiableSpecError(SpecError):
    """Raised when a spec conflicts with package constraints.
       Provide the requirement that was violated when raising."""
    def __init__(self, provided, required, constraint_type):
        super(UnsatisfiableSpecError, self).__init__(
            "%s does not satisfy %s" % (provided, required))
        self.provided = provided
        self.required = required
        self.constraint_type = constraint_type


class UnsatisfiableSpecNameError(UnsatisfiableSpecError):
    """Raised when two specs aren't even for the same package."""
    def __init__(self, provided, required):
        super(UnsatisfiableSpecNameError, self).__init__(
            provided, required, "name")


class UnsatisfiableVersionSpecError(UnsatisfiableSpecError):
    """Raised when a spec version conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableVersionSpecError, self).__init__(
            provided, required, "version")


class UnsatisfiableCompilerSpecError(UnsatisfiableSpecError):
    """Raised when a spec comiler conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableCompilerSpecError, self).__init__(
            provided, required, "compiler")


class UnsatisfiableVariantSpecError(UnsatisfiableSpecError):
    """Raised when a spec variant conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableVariantSpecError, self).__init__(
            provided, required, "variant")


class UnsatisfiableArchitectureSpecError(UnsatisfiableSpecError):
    """Raised when a spec architecture conflicts with package constraints."""
    def __init__(self, provided, required):
        super(UnsatisfiableArchitectureSpecError, self).__init__(
            provided, required, "architecture")


class UnsatisfiableProviderSpecError(UnsatisfiableSpecError):
    """Raised when a provider is supplied but constraints don't match
       a vpkg requirement"""
    def __init__(self, provided, required):
        super(UnsatisfiableProviderSpecError, self).__init__(
            provided, required, "provider")

# TODO: get rid of this and be more specific about particular incompatible
# dep constraints
class UnsatisfiableDependencySpecError(UnsatisfiableSpecError):
    """Raised when some dependency of constrained specs are incompatible"""
    def __init__(self, provided, required):
        super(UnsatisfiableDependencySpecError, self).__init__(
            provided, required, "dependency")
