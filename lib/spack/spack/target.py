# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import functools
import warnings

import six

import archspec.cpu

import llnl.util.tty as tty

import spack.compiler
import spack.compilers
import spack.spec
import spack.util.spack_yaml as syaml


def _ensure_other_is_target(method):
    """In a single argument method, ensure that the argument is an
    instance of ``Target``.
    """
    @functools.wraps(method)
    def _impl(self, other):
        if isinstance(other, six.string_types):
            other = Target(other)

        if not isinstance(other, Target):
            return NotImplemented

        return method(self, other)

    return _impl


class Target(object):
    def __init__(self, name, module_name=None):
        """Target models microarchitectures and their compatibility.

        Args:
            name (str or Microarchitecture): microarchitecture of the target
            module_name (str): optional module name to get access to the
                current target. This is typically used on machines
                like Cray (e.g. craype-compiler)
        """
        if not isinstance(name, archspec.cpu.Microarchitecture):
            name = archspec.cpu.TARGETS.get(
                name, archspec.cpu.generic_microarchitecture(name)
            )
        self.microarchitecture = name
        self.module_name = module_name

    @property
    def name(self):
        return self.microarchitecture.name

    @_ensure_other_is_target
    def __eq__(self, other):
        return (self.microarchitecture == other.microarchitecture and
                self.module_name == other.module_name)

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
        return hash((self.name, self.module_name))

    @staticmethod
    def from_dict_or_value(dict_or_value):
        # A string here represents a generic target (like x86_64 or ppc64) or
        # a custom micro-architecture
        if isinstance(dict_or_value, six.string_types):
            return Target(dict_or_value)

        # TODO: From a dict we actually retrieve much more information than
        # TODO: just the name. We can use that information to reconstruct an
        # TODO: "old" micro-architecture or check the current definition.
        target_info = dict_or_value
        return Target(target_info['name'])

    def to_dict_or_value(self):
        """Returns a dict or a value representing the current target.

        String values are used to keep backward compatibility with generic
        targets, like e.g. x86_64 or ppc64. More specific micro-architectures
        will return a dictionary which contains information on the name,
        features, vendor, generation and parents of the current target.
        """
        # Generic targets represent either an architecture
        # family (like x86_64) or a custom micro-architecture
        if self.microarchitecture.vendor == 'generic':
            return str(self)

        return syaml.syaml_dict(
            self.microarchitecture.to_dict(return_list_of_items=True)
        )

    def __repr__(self):
        cls_name = self.__class__.__name__
        fmt = cls_name + '({0}, {1})'
        return fmt.format(repr(self.microarchitecture),
                          repr(self.module_name))

    def __str__(self):
        return str(self.microarchitecture)

    def __contains__(self, cpu_flag):
        return cpu_flag in self.microarchitecture

    def optimization_flags(self, compiler):
        """Returns the flags needed to optimize for this target using
        the compiler passed as argument.

        Args:
            compiler (spack.spec.CompilerSpec or spack.compiler.Compiler): object that
                contains both the name and the version of the compiler we want to use
        """
        # Mixed toolchains are not supported yet
        if isinstance(compiler, spack.compiler.Compiler):
            if spack.compilers.is_mixed_toolchain(compiler):
                msg = ('microarchitecture specific optimizations are not '
                       'supported yet on mixed compiler toolchains [check'
                       ' {0.name}@{0.version} for further details]')
                warnings.warn(msg.format(compiler))
                return ''

        # Try to check if the current compiler comes with a version number or
        # has an unexpected suffix. If so, treat it as a compiler with a
        # custom spec.
        compiler_version = compiler.version
        version_number, suffix = archspec.cpu.version_components(
            compiler.version
        )
        if not version_number or suffix not in ('', 'apple'):
            # Try to deduce the underlying version of the compiler, regardless
            # of its name in compilers.yaml. Depending on where this function
            # is called we might get either a CompilerSpec or a fully fledged
            # compiler object.
            if isinstance(compiler, spack.spec.CompilerSpec):
                compiler = spack.compilers.compilers_for_spec(compiler).pop()
            try:
                compiler_version = compiler.real_version
            except spack.util.executable.ProcessError as e:
                # log this and just return compiler.version instead
                tty.debug(str(e))

        return self.microarchitecture.optimization_flags(
            compiler.name, str(compiler_version)
        )
