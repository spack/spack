"""
This file defines the dependence relation in spack.

"""

import packages


class Dependency(object):
    """Represents a dependency from one package to another.
    """
    def __init__(self, name):
        self.name = name

    @property
    def package(self):
        return packages.get(self.name)

    def __str__(self):
        return "<dep: %s>" % self.name
