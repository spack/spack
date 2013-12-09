import re
import os
import sys
import string
import inspect
import glob

import spack
import spack.error
import spack.spec
import spack.tty as tty
from spack.util.filesystem import new_path
from spack.util.lang import list_modules
import spack.arch as arch

# Valid package names can contain '-' but can't start with it.
valid_package_re = r'^\w[\w-]*$'

# Don't allow consecutive [_-] in package names
invalid_package_re = r'[_-][_-]+'

instances = {}


class ProviderIndex(object):
    """This is a dict of dicts used for finding providers of particular
       virtual dependencies. The dict of dicts looks like:

       { vpkg name :
           { full vpkg spec : package providing spec } }

       Callers can use this to first find which packages provide a vpkg,
       then find a matching full spec.  e.g., in this scenario:

       { 'mpi' :
           { mpi@:1.1 : mpich,
             mpi@:2.3 : mpich2@1.9: } }

       Calling find_provider(spec) will find a package that provides a
       matching implementation of MPI.
    """
    def __init__(self, specs, **kwargs):
        restrict = kwargs.setdefault('restrict', False)
        self.providers = {}

        for spec in specs:
            if type(spec) != spack.spec.Spec:
                spec = spack.spec.Spec(spec)

            if spec.virtual:
                continue

            pkg = spec.package
            for provided_spec, provider_spec in pkg.provided.iteritems():
                if provider_spec.satisfies(spec):
                    provided_name = provided_spec.name
                    if provided_name not in self.providers:
                        self.providers[provided_name] = {}

                    if restrict:
                        self.providers[provided_name][provided_spec] = spec

                    else:
                        # Before putting the spec in the map, constrain it so that
                        # it provides what was asked for.
                        constrained = spec.copy()
                        constrained.constrain(provider_spec)
                        self.providers[provided_name][provided_spec] = constrained



    def providers_for(self, *vpkg_specs):
        """Gives names of all packages that provide virtual packages
           with the supplied names."""
        providers = set()
        for vspec in vpkg_specs:
            # Allow string names to be passed as input, as well as specs
            if type(vspec) == str:
                vspec = spack.spec.Spec(vspec)

            # Add all the providers that satisfy the vpkg spec.
            if vspec.name in self.providers:
                for provider_spec, spec in self.providers[vspec.name].items():
                    if provider_spec.satisfies(vspec):
                        providers.add(spec)

        # Return providers in order
        return sorted(providers)


def get(pkg_name):
    if not pkg_name in instances:
        package_class = get_class_for_package_name(pkg_name)
        instances[pkg_name] = package_class(pkg_name)

    return instances[pkg_name]


def providers_for(vpkg_spec):
    if providers_for.index is None:
        providers_for.index = ProviderIndex(all_package_names())

    providers = providers_for.index.providers_for(vpkg_spec)
    if not providers:
        raise UnknownPackageError("No such virtual package: %s" % vpkg_spec)
    return providers
providers_for.index = None


def valid_package_name(pkg_name):
    return (re.match(valid_package_re, pkg_name) and
            not re.search(invalid_package_re, pkg_name))


def validate_package_name(pkg_name):
    if not valid_package_name(pkg_name):
        raise InvalidPackageNameError(pkg_name)


def filename_for_package_name(pkg_name):
    """Get the filename where a package name should be stored."""
    validate_package_name(pkg_name)
    return new_path(spack.packages_path, "%s.py" % pkg_name)


def installed_packages():
    return spack.install_layout.all_specs()


def all_package_names():
    """Generator function for all packages."""
    for module in list_modules(spack.packages_path):
        yield module


def all_packages():
    for name in all_package_names():
        yield get(name)


def class_name_for_package_name(pkg_name):
    """Get a name for the class the package file should contain.  Note that
       conflicts don't matter because the classes are in different modules.
    """
    validate_package_name(pkg_name)
    class_name = string.capwords(pkg_name.replace('_', '-'), '-')

    # If a class starts with a number, prefix it with Number_ to make it a valid
    # Python class name.
    if re.match(r'^[0-9]', class_name):
        class_name = "Num_%s" % class_name

    return class_name


def exists(pkg_name):
    """Whether a package is concrete."""
    return os.path.exists(filename_for_package_name(pkg_name))


def packages_module():
    # TODO: replace this with a proper package DB class, instead of this hackiness.
    packages_path = re.sub(spack.module_path + '\/+', 'spack.', spack.packages_path)
    packages_module = re.sub(r'\/', '.', packages_path)
    return packages_module


def get_class_for_package_name(pkg_name):
    file_name = filename_for_package_name(pkg_name)

    if os.path.exists(file_name):
        if not os.path.isfile(file_name):
            tty.die("Something's wrong. '%s' is not a file!" % file_name)
        if not os.access(file_name, os.R_OK):
            tty.die("Cannot read '%s'!" % file_name)
    else:
        raise UnknownPackageError(pkg_name)

    # Figure out pacakges module from spack.packages_path
    # This allows us to change the module path.
    if not re.match(r'%s' % spack.module_path, spack.packages_path):
        raise RuntimeError("Packages path is not a submodule of spack.")

    class_name = pkg_name.capitalize()
    try:
        module_name = "%s.%s" % (packages_module(), pkg_name)
        module = __import__(module_name, fromlist=[class_name])
    except ImportError, e:
        tty.die("Error while importing %s.%s:\n%s" % (pkg_name, class_name, e.message))

    cls = getattr(module, class_name)
    if not inspect.isclass(cls):
        tty.die("%s.%s is not a class" % (pkg_name, class_name))

    return cls


def compute_dependents():
    """Reads in all package files and sets dependence information on
       Package objects in memory.
    """
    for pkg in all_packages():
        if pkg._dependents is None:
            pkg._dependents = []

        for name, dep in pkg.dependencies.iteritems():
            dpkg = get(name)
            if dpkg._dependents is None:
                dpkg._dependents = []
            dpkg._dependents.append(pkg.name)


def graph_dependencies(out=sys.stdout):
    """Print out a graph of all the dependencies between package.
       Graph is in dot format."""
    out.write('digraph G {\n')
    out.write('  label = "Spack Dependencies"\n')
    out.write('  labelloc = "b"\n')
    out.write('  rankdir = "LR"\n')
    out.write('  ranksep = "5"\n')
    out.write('\n')

    def quote(string):
        return '"%s"' % string

    deps = []
    for pkg in all_packages():
        out.write('  %-30s [label="%s"]\n' % (quote(pkg.name), pkg.name))
        for dep_name, dep in pkg.dependencies.iteritems():
            deps.append((pkg.name, dep_name))
    out.write('\n')

    for pair in deps:
        out.write('  "%s" -> "%s"\n' % pair)
    out.write('}\n')


class InvalidPackageNameError(spack.error.SpackError):
    """Raised when we encounter a bad package name."""
    def __init__(self, name):
        super(InvalidPackageNameError, self).__init__(
            "Invalid package name: " + name)
        self.name = name


class UnknownPackageError(spack.error.SpackError):
    """Raised when we encounter a package spack doesn't have."""
    def __init__(self, name):
        super(UnknownPackageError, self).__init__("Package %s not found." % name)
        self.name = name
