import re
import sys
import types
import traceback

from llnl.util.lang import *
import spack

# Name of module under which packages are imported
imported_packages_module = 'spack.repos'

# Name of the package file inside a package directory
package_file_name = 'package.py'

import sys
class LazyLoader:
    """The LazyLoader handles cases when repo modules or classes
       are imported.  It watches for 'spack.repos.*' loads, then
       redirects the load to the appropriate module."""
    def find_module(self, fullname, pathname):
        if not fullname.startswith(imported_packages_module):
            return None

        print "HERE ==="
        print
        for line in traceback.format_stack():
            print "    ", line.strip()
        print
        print "full: ", fullname
        print "path: ", pathname
        print

        partial_name = fullname[len(imported_packages_module)+1:]

        print "partial: ", partial_name
        print

        last_dot = partial_name.rfind('.')
        repo = partial_name[:last_dot]
        module = partial_name[last_dot+1:]

        repo_loader = spack.db.repo_loaders.get(repo)
        if repo_loader:
            try:
                self.mod = repo_loader.get_module(module)
                return self
            except (ImportError, spack.packages.UnknownPackageError):
                return None

    def load_module(self, fullname):
        return self.mod

sys.meta_path.append(LazyLoader())

_reponames = {}
class RepoNamespace(types.ModuleType):
    """The RepoNamespace holds the repository namespaces under
       spack.repos.  For example, when accessing spack.repos.original
       this class will use __getattr__ to translate the 'original'
       into one of spack's known repositories"""
    def __init__(self):
        import sys
        sys.modules[imported_packages_module] = self

    def __getattr__(self, name):
        if name in _reponames:
            return _reponames[name]
        raise AttributeError

    @property
    def __file__(self):
        return None

    @property
    def __path__(self):
        return []


class RepoLoader(types.ModuleType):
    """Each RepoLoader is associated with a repository, and the RepoLoader is
       responsible for loading packages out of that repository.  For example,
       a RepoLoader may be responsible for spack.repos.original, and when someone
       references spack.repos.original.libelf that RepoLoader will load the
       libelf package."""
    def __init__(self, reponame, repopath):
        self.path = repopath
        self.reponame = reponame
        self.module_name = imported_packages_module + '.' + reponame
        if not reponame in _reponames:
            _reponames[reponame] = self

        import sys
        sys.modules[self.module_name] = self


    @property
    def __path__(self):
        return [ self.path ]


    def __getattr__(self, name):
        if name[0] == '_':
            raise AttributeError
        return self.get_module(name)


    @memoized
    def get_module(self, pkg_name):
        import os
        import imp
        import llnl.util.tty as tty

        file_path = os.path.join(self.path, pkg_name, package_file_name)
        if os.path.exists(file_path):
            if not os.path.isfile(file_path):
                tty.die("Something's wrong. '%s' is not a file!" % file_path)
            if not os.access(file_path, os.R_OK):
                tty.die("Cannot read '%s'!" % file_path)
        else:
            raise spack.packages.UnknownPackageError(pkg_name, self.reponame if self.reponame != 'original' else None)

        try:
            module_name = imported_packages_module + '.' + self.reponame + '.' + pkg_name
            module = imp.load_source(module_name, file_path)

        except ImportError, e:
            tty.die("Error while importing %s from %s:\n%s" % (
                pkg_name, file_path, e.message))

        return module
