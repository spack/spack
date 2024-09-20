# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import functools

import archspec.cpu

import spack.util.spack_yaml as syaml


def _ensure_other_is_target(method):
    """In a single argument method, ensure that the argument is an
    instance of ``Target``.
    """

    @functools.wraps(method)
    def _impl(self, other):
        if isinstance(other, str):
            other = Target(other)

        if not isinstance(other, Target):
            return NotImplemented

        return method(self, other)

    return _impl


class Target:
    def __init__(self, name):
        """Target models microarchitectures and their compatibility.

        Args:
            name (str or Microarchitecture): microarchitecture of the target
        """
        if not isinstance(name, archspec.cpu.Microarchitecture):
            name = archspec.cpu.TARGETS.get(name, archspec.cpu.generic_microarchitecture(name))
        self.microarchitecture = name

    @property
    def name(self):
        return self.microarchitecture.name

    @_ensure_other_is_target
    def __eq__(self, other):
        return self.microarchitecture == other.microarchitecture

    def __ne__(self, other):
        # This method is necessary as long as we support Python 2. In Python 3
        # __ne__ defaults to the implementation below
        return not self == other

    @_ensure_other_is_target
    def __lt__(self, other):
        # TODO: In the future it would be convenient to say
        # TODO: `spec.architecture.target < other.architecture.target`
        # TODO: and change the semantic of the comparison operators

        # This is needed to sort deterministically specs in a list.
        # It doesn't implement a total ordering semantic.
        return self.microarchitecture.name < other.microarchitecture.name

    def __hash__(self):
        return hash(self.name)

    @staticmethod
    def from_dict_or_value(dict_or_value):
        # A string here represents a generic target (like x86_64 or ppc64) or
        # a custom micro-architecture
        if isinstance(dict_or_value, str):
            return Target(dict_or_value)

        # TODO: From a dict we actually retrieve much more information than
        # TODO: just the name. We can use that information to reconstruct an
        # TODO: "old" micro-architecture or check the current definition.
        target_info = dict_or_value
        return Target(target_info["name"])

    def to_dict_or_value(self):
        """Returns a dict or a value representing the current target.

        String values are used to keep backward compatibility with generic
        targets, like e.g. x86_64 or ppc64. More specific micro-architectures
        will return a dictionary which contains information on the name,
        features, vendor, generation and parents of the current target.
        """
        # Generic targets represent either an architecture
        # family (like x86_64) or a custom micro-architecture
        if self.microarchitecture.vendor == "generic":
            return str(self)

        # Get rid of compiler flag information before turning the uarch into a dict
        uarch_dict = self.microarchitecture.to_dict()
        uarch_dict.pop("compilers", None)
        return syaml.syaml_dict(uarch_dict.items())

    def __repr__(self):
        cls_name = self.__class__.__name__
        fmt = cls_name + "({0})"
        return fmt.format(repr(self.microarchitecture))

    def __str__(self):
        return str(self.microarchitecture)

    def __contains__(self, cpu_flag):
        return cpu_flag in self.microarchitecture
