import exceptions
import re
import os

import spack.spec as spec
from spack.util import *
from spack.error import SpackError


class DirectoryLayout(object):
    """A directory layout is used to associate unique paths with specs.
       Different installations are going to want differnet layouts for their
       install, and they can use this to customize the nesting structure of
       spack installs.
    """
    def __init__(self, root):
        self.root = root


    def all_specs(self):
        """To be implemented by subclasses to traverse all specs for which there is
           a directory within the root.
        """
        raise NotImplementedError()


    def relative_path_for_spec(self, spec):
        """Implemented by subclasses to return a relative path from the install
           root to a unique location for the provided spec."""
        raise NotImplementedError()


    def path_for_spec(self, spec):
        """Return an absolute path from the root to a directory for the spec."""
        if not spec.concrete:
            raise ValueError("path_for_spec requires a concrete spec.")

        path = self.relative_path_for_spec(spec)
        assert(not path.startswith(self.root))
        return os.path.join(self.root, path)


    def remove_path_for_spec(self, spec):
        """Removes a prefix and any empty parent directories from the root."""
        path = self.path_for_spec(spec)
        assert(path.startswith(self.root))

        if os.path.exists(path):
            shutil.rmtree(path, True)

        path = os.path.dirname(path)
        while not os.listdir(path) and path != self.root:
            os.rmdir(path)
            path = os.path.dirname(path)


def traverse_dirs_at_depth(root, depth, path_tuple=(), curdepth=0):
    """For each directory at <depth> within <root>, return a tuple representing
       the ancestors of that directory.
    """
    if curdepth == depth and curdepth != 0:
        yield path_tuple
    elif depth > curdepth:
        for filename in os.listdir(root):
            child = os.path.join(root, filename)
            if os.path.isdir(child):
                child_tuple = path_tuple + (filename,)
                for tup in traverse_dirs_at_depth(
                        child, depth, child_tuple, curdepth+1):
                    yield tup


class DefaultDirectoryLayout(DirectoryLayout):
    def __init__(self, root):
        super(DefaultDirectoryLayout, self).__init__(root)


    def relative_path_for_spec(self, spec):
        if not spec.concrete:
            raise ValueError("relative_path_for_spec requires a concrete spec.")

        return new_path(
            spec.architecture,
            spec.compiler,
            "%s@%s%s%s" % (spec.name,
                           spec.version,
                           spec.variants,
                           spec.dependencies))


    def all_specs(self):
        if not os.path.isdir(self.root):
            return

        for path in traverse_dirs_at_depth(self.root, 3):
            arch, compiler, last_dir = path
            spec_str = "%s%%%s=%s" % (last_dir, compiler, arch)
            yield spec.parse(spec_str)
