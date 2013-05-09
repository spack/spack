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
"""
from functools import total_ordering

import spack.parse
from spack.version import Version, VersionRange
import spack.error


class DuplicateDependenceError(spack.error.SpackError):
    """Raised when the same dependence occurs in a spec twice."""
    def __init__(self, message):
        super(DuplicateDependenceError, self).__init__(message)

class DuplicateVariantError(spack.error.SpackError):
    """Raised when the same variant occurs in a spec twice."""
    def __init__(self, message):
        super(VariantVariantError, self).__init__(message)

class DuplicateCompilerError(spack.error.SpackError):
    """Raised when the same compiler occurs in a spec twice."""
    def __init__(self, message):
        super(DuplicateCompilerError, self).__init__(message)


class Compiler(object):
    def __init__(self, name):
        self.name = name
        self.versions = []

    def add_version(self, version):
        self.versions.append(version)

    def __str__(self):
        out = "%%%s" % self.name
        if self.versions:
            vlist = ",".join(str(v) for v in sorted(self.versions))
            out += "@%s" % vlist
        return out


class Spec(object):
    def __init__(self, name):
        self.name = name
        self.versions = []
        self.variants = {}
        self.compiler = None
        self.dependencies = {}

    def add_version(self, version):
        self.versions.append(version)

    def add_variant(self, name, enabled):
        self.variants[name] = enabled

    def add_compiler(self, compiler):
        self.compiler = compiler

    def add_dependency(self, dep):
        if dep.name in self.dependencies:
            raise ValueError("Cannot depend on %s twice" % dep)
        self.dependencies[dep.name] = dep

    def __str__(self):
        out = self.name

        if self.versions:
            vlist = ",".join(str(v) for v in sorted(self.versions))
            out += "@%s" % vlist

        if self.compiler:
            out += str(self.compiler)

        for name in sorted(self.variants.keys()):
            enabled = self.variants[name]
            if enabled:
                out += '+%s' % name
            else:
                out += '~%s' % name

        for name in sorted(self.dependencies.keys()):
            out += " ^%s" % str(self.dependencies[name])

        return out

#
# These are possible token types in the spec grammar.
#
DEP, AT, COLON, COMMA, ON, OFF, PCT, ID = range(8)

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
            (r'\w[\w.-]*', lambda scanner, val: self.token(ID,    val)),
            (r'\s+',       lambda scanner, val: None)])

class SpecParser(spack.parse.Parser):
    def __init__(self):
        super(SpecParser, self).__init__(SpecLexer())

    def spec(self):
        self.expect(ID)
        self.check_identifier()

        spec = Spec(self.token.value)
        while self.next:
            if self.accept(DEP):
                dep = self.spec()
                spec.add_dependency(dep)

            elif self.accept(AT):
                vlist = self.version_list()
                for version in vlist:
                    spec.add_version(version)

            elif self.accept(ON):
                self.expect(ID)
                self.check_identifier()
                spec.add_variant(self.token.value, True)

            elif self.accept(OFF):
                self.expect(ID)
                self.check_identifier()
                spec.add_variant(self.token.value, False)

            elif self.accept(PCT):
                spec.add_compiler(self.compiler())

            else:
                self.unexpected_token()

        return spec


    def version(self):
        start = None
        end = None
        if self.accept(ID):
            start = self.token.value

        if self.accept(COLON):
            if self.accept(ID):
                end = self.token.value
        else:
            return Version(start)

        if not start and not end:
            raise ParseError("Lone colon: version range needs at least one version.")
        else:
            if start: start = Version(start)
            if end: end = Version(end)
            return VersionRange(start, end)


    def version_list(self):
        vlist = []
        while True:
            vlist.append(self.version())
            if not self.accept(COMMA):
                break
        return vlist


    def compiler(self):
        self.expect(ID)
        self.check_identifier()
        compiler = Compiler(self.token.value)
        if self.accept(AT):
            vlist = self.version_list()
            for version in vlist:
                compiler.add_version(version)
        return compiler


    def check_identifier(self):
        """The only identifiers that can contain '.' are versions, but version
           ids are context-sensitive so we have to check on a case-by-case
           basis. Call this if we detect a version id where it shouldn't be.
        """
        if '.' in self.token.value:
            raise spack.parse.ParseError(
                "Non-version identifier cannot contain '.'")


    def do_parse(self):
        specs = []
        while self.next:
            specs.append(self.spec())
        return specs
