# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import archspec.cpu


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

    def __eq__(self, other):
        if isinstance(other, str):
            other = Target(other)

        if not isinstance(other, Target):
            return NotImplemented

        return self.microarchitecture == other.microarchitecture

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        cls_name = self.__class__.__name__
        fmt = cls_name + "({0})"
        return fmt.format(repr(self.microarchitecture))

    def __str__(self):
        return str(self.microarchitecture)

    def __contains__(self, cpu_flag):
        return cpu_flag in self.microarchitecture
