import re
import os
import sys
import string
import inspect
import glob

import spack
from spack.utils import *
import spack.arch as arch
import spack.version as version
import spack.attr as attr

# Valid package names
valid_package = r'^[a-zA-Z0-9_-]*$'

# Don't allow consecutive [_-] in package names
invalid_package = r'[_-][_-]+'

instances = {}


def valid_name(pkg):
    return re.match(valid_package, pkg) and not re.search(invalid_package, pkg)


def validate_name(pkg):
    if not valid_name(pkg):
        raise spack.InvalidPackageNameException(pkg)


def filename_for(pkg):
    """Get the filename where a package name should be stored."""
    validate_name(pkg)
    return new_path(spack.packages_path, "%s.py" % pkg)


def installed_packages(**kwargs):
    """Returns a dict from SysType to lists of Package objects."""
    list_installed = kwargs.get('installed', False)

    pkgs = {}
    if not os.path.isdir(spack.install_path):
        return pkgs

    for sys_type in os.listdir(spack.install_path):
        sys_type = arch.SysType(sys_type)
        sys_path = new_path(spack.install_path, sys_type)
        pkgs[sys_type] = [get(pkg) for pkg in os.listdir(sys_path)
                          if os.path.isdir(new_path(sys_path, pkg))]
    return pkgs


def all_package_names():
    """Generator function for all packages."""
    os.chdir(spack.packages_path)
    for name in glob.glob("*.py"):
        if name != '__init__.py':
            yield re.sub('.py$', '', name)


def all_packages():
    for name in all_package_names():
        yield get(name)


def class_for(pkg):
    """Get a name for the class the package file should contain.  Note that
       conflicts don't matter because the classes are in different modules.
    """
    validate_name(pkg)
    class_name = string.capwords(pkg.replace('_', '-'), '-')

    # If a class starts with a number, prefix it with Number_ to make it a valid
    # Python class name.
    if re.match(r'^[0-9]', class_name):
        class_name = "Number_%s" % class_name

    return class_name


def get_class(pkg):
    file = filename_for(pkg)

    if os.path.exists(file):
        if not os.path.isfile(file):
            tty.die("Something's wrong. '%s' is not a file!" % file)
        if not os.access(file, os.R_OK):
            tty.die("Cannot read '%s'!" % file)

    class_name = pkg.capitalize()
    try:
        module_name = "%s.%s" % (__name__, pkg)
        module = __import__(module_name, fromlist=[class_name])
    except ImportError, e:
        tty.die("Error while importing %s.%s:\n%s" % (pkg, class_name, e.message))

    klass = getattr(module, class_name)
    if not inspect.isclass(klass):
        tty.die("%s.%s is not a class" % (pkg, class_name))

    return klass


def get(pkg, arch=arch.sys_type()):
    key = (pkg, arch)
    if not key in instances:
        package_class = get_class(pkg)
        instances[key] = package_class(arch)
    return instances[key]


def compute_dependents():
    """Reads in all package files and sets dependence information on
       Package objects in memory.
    """
    for pkg in all_packages():
        if pkg._dependents is None:
            pkg._dependents = []

        for dep in pkg.dependencies:
            dpkg = get(dep.name)
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
        for dep in pkg.dependencies:
            deps.append((pkg.name, dep.name))
    out.write('\n')

    for pair in deps:
        out.write('  "%s" -> "%s"\n' % pair)
    out.write('}\n')
