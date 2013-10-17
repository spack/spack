import re
import os
import sys
import string
import inspect
import glob

import spack
import spack.error
import spack.spec
from spack.util.filesystem import new_path
from spack.util.lang import list_modules
import spack.arch as arch

# Valid package names can contain '-' but can't start with it.
valid_package_re = r'^\w[\w-]*$'

# Don't allow consecutive [_-] in package names
invalid_package_re = r'[_-][_-]+'

instances = {}


def get(pkg_name):
    if not pkg_name in instances:
        package_class = get_class_for_package_name(pkg_name)
        instances[pkg_name] = package_class(pkg_name)

    return instances[pkg_name]


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

    # TODO: replace this with a proper package DB class, instead of this hackiness.
    packages_path = re.sub(spack.module_path + '\/+', 'spack.', spack.packages_path)
    packages_module = re.sub(r'\/', '.', packages_path)

    class_name = pkg_name.capitalize()
    try:
        module_name = "%s.%s" % (packages_module, pkg_name)
        module = __import__(module_name, fromlist=[class_name])
    except ImportError, e:
        tty.die("Error while importing %s.%s:\n%s" % (pkg_name, class_name, e.message))

    klass = getattr(module, class_name)
    if not inspect.isclass(klass):
        tty.die("%s.%s is not a class" % (pkg_name, class_name))

    return klass


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
