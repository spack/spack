"""
Spack allows very fine-grained control over how packages are installed and
over how they are built and configured.  To make this easy, it has its own
syntax for declaring a dependence.  We call a descriptor of a particular
package configuration a "spec".

The syntax looks like this:

    spack install mpileaks ^openmpi @1.2:1.4 +debug %intel @12.1
                  0        1        2        3      4      5

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

Here is the EBNF grammar for a spec:

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
from StringIO import StringIO

import tty
import spack.parse
import spack.error
import spack.compilers
import spack.compilers.gcc
import spack.packages as packages
import spack.arch as arch

from spack.version import *
from spack.color import *
from spack.util.lang import *
from spack.util.string import *

"""This map determines the coloring of specs when using color output.
   We make the fields different colors to enhance readability.
   See spack.color for descriptions of the color codes.
"""
color_formats = {'%' : '@g',   # compiler
                 '@' : '@c',   # version
                 '=' : '@m',   # architecture
                 '+' : '@B',   # enable variant
                 '~' : '@r',   # disable variant
                 '^' : '@.'}   # dependency

"""Regex used for splitting by spec field separators."""
separators = '[%s]' % ''.join(color_formats.keys())


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

    return colorize(re.sub(separators, insert_color(), str(spec)) + '@.')


@key_ordering
class Compiler(object):
    """The Compiler field represents the compiler or range of compiler
       versions that a package should be built with.  Compilers have a
       name and a version list.
    """
    def __init__(self, name, version=None):
        if name not in spack.compilers.supported_compilers():
            raise UnknownCompilerError(name)

        self.name = name
        self.versions = VersionList()
        if version:
            self.versions.add(version)


    def _add_version(self, version):
        self.versions.add(version)


    def satisfies(self, other):
        return (self.name == other.name and
                self.versions.overlaps(other.versions))


    def constrain(self, other):
        if not self.satisfies(other.compiler):
            raise UnsatisfiableCompilerSpecError(
                "%s does not satisfy %s" % (self.compiler, other.compiler))

        self.versions.intersect(other.versions)


    @property
    def concrete(self):
        return self.versions.concrete


    def _concretize(self):
        """If this spec could describe more than one version, variant, or build
           of a package, this will resolve it to be concrete.
        """
        # TODO: support compilers other than GCC.
        if self.concrete:
            return
        gcc_version = spack.compilers.gcc.get_version()
        self.versions = VersionList([gcc_version])


    def concretized(self):
        clone = self.copy()
        clone._concretize()
        return clone


    @property
    def version(self):
        if not self.concrete:
            raise SpecError("Spec is not concrete: " + str(self))
        return self.versions[0]


    def copy(self):
        clone = Compiler(self.name)
        clone.versions = self.versions.copy()
        return clone


    def _cmp_key(self):
        return (self.name, self.versions)


    def __str__(self):
        out = self.name
        if self.versions:
            vlist = ",".join(str(v) for v in sorted(self.versions))
            out += "@%s" % vlist
        return out


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


    def satisfies(self, other):
        return all(self[name].satisfies(other[name]) for name in self
                   if name in other)


    def __str__(self):
        sorted_dep_names = sorted(self.keys())
        return ''.join(
            ["^" + str(self[name]) for name in sorted_dep_names])


@key_ordering
class Spec(object):
    def __init__(self, name):
        self.name = name
        self.versions = VersionList()
        self.variants = VariantMap()
        self.architecture = None
        self.compiler = None
        self.dependencies = DependencyMap()

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
        if self.compiler: raise DuplicateCompilerError(
                "Spec for '%s' cannot have two compilers." % self.name)
        self.compiler = compiler


    def _set_architecture(self, architecture):
        """Called by the parser to set the architecture."""
        if self.architecture: raise DuplicateArchitectureError(
                "Spec for '%s' cannot have two architectures." % self.name)
        self.architecture = architecture


    def _add_dependency(self, dep):
        """Called by the parser to add another spec as a dependency."""
        if dep.name in self.dependencies:
            raise DuplicateDependencyError("Cannot depend on '%s' twice" % dep)
        self.dependencies[dep.name] = dep


    @property
    def concrete(self):
        return bool(self.versions.concrete
                    # TODO: support variants
                    and self.architecture
                    and self.compiler and self.compiler.concrete
                    and self.dependencies.concrete)


    def _concretize(self):
        """A spec is concrete if it describes one build of a package uniquely.
           This will ensure that this spec is concrete.

           If this spec could describe more than one version, variant, or build
           of a package, this will resolve it to be concrete.

           Ensures that the spec is in canonical form.

           This means:
           1. All dependencies of this package and of its dependencies are
              in the dependencies list (transitive closure of deps).
           2. All dependencies in the dependencies list are canonicalized.

           This function also serves to validate the spec, in that it makes sure
           that each package exists an that spec criteria don't violate package
           criteria.
        """
        # TODO: modularize the process of selecting concrete versions.
        # There should be a set of user-configurable policies for these decisions.
        self.validate()

        # take the system's architecture for starters
        if not self.architecture:
             self.architecture = arch.sys_type()

        if self.compiler:
            self.compiler._concretize()

        # TODO: handle variants.

        pkg = packages.get(self.name)

        # Take the highest version in a range
        if not self.versions.concrete:
            preferred = self.versions.highest() or pkg.version
            self.versions = VersionList([preferred])

        # Ensure dependencies have right versions


    @property
    def traverse_deps(self, visited=None):
        """Yields dependencies in depth-first order"""
        if not visited:
            visited = set()

        for name in sorted(self.dependencies.keys()):
            dep = dependencies[name]
            if dep in visited:
                continue

            for d in dep.traverse_deps(seen):
                yield d
            yield dep


    def _normalize_helper(self, visited, spec_deps):
        """Recursive helper function for _normalize."""
        if self.name in visited:
            return
        visited.add(self.name)

        # Combine constraints from package dependencies with
        # information in this spec's dependencies.
        pkg = packages.get(self.name)
        for pkg_dep in pkg.dependencies:
            name = pkg_dep.name

            if name not in spec_deps:
                # Clone the spec from the package
                spec_deps[name] = pkg_dep.copy()

            try:
                # intersect package information with spec info
                spec_deps[name].constrain(pkg_dep)
            except UnsatisfiableSpecError, e:
                error_type = type(e)
                raise error_type(
                    "Violated depends_on constraint from package %s: %s"
                    % (self.name, e.message))

            # Add merged spec to my deps and recurse
            self.dependencies[name] = spec_deps[name]
            self.dependencies[name]._normalize_helper(visited, spec_deps)


    def normalize(self):
        if any(dep.dependencies for dep in self.dependencies.values()):
            raise SpecError("Spec has already been normalized.")

        self.validate_package_names()

        spec_deps = self.dependencies
        self.dependencies = DependencyMap()

        visited = set()
        self._normalize_helper(visited, spec_deps)

        # If there are deps specified but not visited, they're not
        # actually deps of this package.  Raise an error.
        extra = set(spec_deps.viewkeys()).difference(visited)
        if extra:
            raise InvalidDependencyException(
                self.name + " does not depend on " + comma_or(extra))


    def validate_package_names(self):
        for name in self.dependencies:
            packages.get(name)


    def constrain(self, other):
        if not self.versions.overlaps(other.versions):
            raise UnsatisfiableVersionSpecError(
                "%s does not satisfy %s" % (self.versions, other.versions))

        conflicting_variants = [
            v for v in other.variants if v in self.variants and
            self.variants[v].enabled != other.variants[v].enabled]

        if conflicting_variants:
            raise UnsatisfiableVariantSpecError(comma_and(
                "%s does not satisfy %s" % (self.variants[v], other.variants[v])
                for v in conflicting_variants))

        if self.architecture is not None and other.architecture is not None:
            if self.architecture != other.architecture:
                raise UnsatisfiableArchitectureSpecError(
                    "Asked for architecture %s, but required %s"
                    % (self.architecture, other.architecture))

        if self.compiler is not None and other.compiler is not None:
            self.compiler.constrain(other.compiler)
        elif self.compiler is None:
            self.compiler = other.compiler

        self.versions.intersect(other.versions)
        self.variants.update(other.variants)
        self.architecture = self.architecture or other.architecture


    def satisfies(self, other):
        def sat(attribute):
            s = getattr(self, attribute)
            o = getattr(other, attribute)
            return not s or not o or s.satisfies(o)

        return (self.name == other.name and
                all(sat(attr) for attr in
                    ('versions', 'variants', 'compiler', 'architecture')) and
                # TODO: what does it mean to satisfy deps?
                self.dependencies.satisfies(other.dependencies))


    def concretized(self):
        clone = self.copy()
        clone._concretize()
        return clone


    def copy(self):
        clone = Spec(self.name)
        clone.versions = self.versions.copy()
        clone.variants = self.variants.copy()
        clone.architecture = self.architecture
        clone.compiler = None
        if self.compiler:
            clone.compiler = self.compiler.copy()
        clone.dependencies = self.dependencies.copy()
        return clone


    @property
    def version(self):
        if not self.concrete:
            raise SpecError("Spec is not concrete: " + str(self))
        return self.versions[0]


    def _cmp_key(self):
        return (self.name, self.versions, self.variants,
                self.architecture, self.compiler)


    def colorized(self):
        return colorize_spec(self)


    def str_without_deps(self):
        out = self.name

        # If the version range is entirely open, omit it
        if self.versions and self.versions != VersionList([':']):
            out += "@%s" % self.versions

        if self.compiler:
            out += "%%%s" % self.compiler

        out += str(self.variants)

        if self.architecture:
            out += "=%s" % self.architecture

        return out


    def tree(self, indent=""):
        """Prints out this spec and its dependencies, tree-formatted
           with indentation."""
        out = indent + self.str_without_deps()
        for dep in sorted(self.dependencies.keys()):
            out += "\n" + self.dependencies[dep].tree(indent + "    ")
        return out


    def __repr__(self):
        return str(self)


    def __str__(self):
        return self.str_without_deps() + str(self.dependencies)


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

        return specs


    def spec(self):
        self.check_identifier()
        spec = Spec(self.token.value)
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
        self.check_identifier()
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
        compiler = Compiler(self.token.value)
        if self.accept(AT):
            vlist = self.version_list()
            for version in vlist:
                compiler._add_version(version)
        return compiler


    def check_identifier(self):
        """The only identifiers that can contain '.' are versions, but version
           ids are context-sensitive so we have to check on a case-by-case
           basis. Call this if we detect a version id where it shouldn't be.
        """
        if '.' in self.token.value:
            self.last_token_error("Identifier cannot contain '.'")


def parse(string):
    """Returns a list of specs from an input string."""
    return SpecParser().parse(string)


def parse_one(string):
    """Parses a string containing only one spec, then returns that
       spec.  If more than one spec is found, raises a ValueError.
    """
    spec_list = parse(string)
    if len(spec_list) > 1:
        raise ValueError("string contains more than one spec!")
    elif len(spec_list) < 1:
        raise ValueError("string contains no specs!")
    return spec_list[0]


def make_spec(spec_like):
    if type(spec_like) == str:
        specs = parse(spec_like)
        if len(specs) != 1:
            raise ValueError("String contains multiple specs: '%s'" % spec_like)
        return specs[0]

    elif type(spec_like) == Spec:
        return spec_like

    else:
        raise TypeError("Can't make spec out of %s" % type(spec_like))


class SpecError(spack.error.SpackError):
    """Superclass for all errors that occur while constructing specs."""
    def __init__(self, message):
        super(SpecError, self).__init__(message)


class DuplicateDependencyError(SpecError):
    """Raised when the same dependency occurs in a spec twice."""
    def __init__(self, message):
        super(DuplicateDependencyError, self).__init__(message)


class DuplicateVariantError(SpecError):
    """Raised when the same variant occurs in a spec twice."""
    def __init__(self, message):
        super(DuplicateVariantError, self).__init__(message)


class DuplicateCompilerError(SpecError):
    """Raised when the same compiler occurs in a spec twice."""
    def __init__(self, message):
        super(DuplicateCompilerError, self).__init__(message)


class UnknownCompilerError(SpecError):
    """Raised when the user asks for a compiler spack doesn't know about."""
    def __init__(self, compiler_name):
        super(UnknownCompilerError, self).__init__(
            "Unknown compiler: %s" % compiler_name)


class DuplicateArchitectureError(SpecError):
    """Raised when the same architecture occurs in a spec twice."""
    def __init__(self, message):
        super(DuplicateArchitectureError, self).__init__(message)


class InvalidDependencyException(SpecError):
    """Raised when a dependency in a spec is not actually a dependency
       of the package."""
    def __init__(self, message):
        super(InvalidDependencyException, self).__init__(message)


class UnsatisfiableSpecError(SpecError):
    """Raised when a spec conflicts with package constraints."""
    def __init__(self, message):
        super(UnsatisfiableSpecError, self).__init__(message)


class UnsatisfiableVersionSpecError(UnsatisfiableSpecError):
    """Raised when a spec version conflicts with package constraints."""
    def __init__(self, message):
        super(UnsatisfiableVersionSpecError, self).__init__(message)


class UnsatisfiableCompilerSpecError(UnsatisfiableSpecError):
    """Raised when a spec comiler conflicts with package constraints."""
    def __init__(self, message):
        super(UnsatisfiableCompilerSpecError, self).__init__(message)


class UnsatisfiableVariantSpecError(UnsatisfiableSpecError):
    """Raised when a spec variant conflicts with package constraints."""
    def __init__(self, message):
        super(UnsatisfiableVariantSpecError, self).__init__(message)


class UnsatisfiableArchitectureSpecError(UnsatisfiableSpecError):
    """Raised when a spec architecture conflicts with package constraints."""
    def __init__(self, message):
        super(UnsatisfiableArchitectureSpecError, self).__init__(message)
