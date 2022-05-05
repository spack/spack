# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import copy
import inspect
from typing import Any, List, Optional, Tuple

import six

import llnl.util.compat

import spack.build_environment

#: Builder classes, as registered by the "builder" decorator
BUILDER_CLS = {}


def builder(name):
    """Class decorator used to register a builder with a given name"""

    def _decorator(cls):
        cls.build_system = name
        BUILDER_CLS[name] = cls
        return cls

    return _decorator


_RUN_BEFORE_PACKAGE_ATTRIBUTE = "run_before_callbacks"
_RUN_AFTER_PACKAGE_ATTRIBUTE = "run_after_callbacks"
_PHASE_OVERRIDE_PACKAGE_ATTRIBUTE = "phase_overrides"


class BuilderMeta(type):
    #: Temporary stage for "run_before" decorators
    _run_before_stage = []  # type: List[Any]
    #: Temporary stage for "run_after" decorators
    _run_after_stage = []  # type: List[Any]
    #: Temporary stage for phase override decorators
    _phases_stage = []  # type: List[Any]

    def __new__(mcs, name, bases, attr_dict):

        stage2attribute = [
            ("_run_before_stage", _RUN_BEFORE_PACKAGE_ATTRIBUTE),
            ("_run_after_stage", _RUN_AFTER_PACKAGE_ATTRIBUTE),
            ("_phases_stage", _PHASE_OVERRIDE_PACKAGE_ATTRIBUTE),
        ]

        for stage_name, attribute_name in stage2attribute:
            stage = getattr(BuilderMeta, stage_name)

            # We don't have any callback registered, so move to the next attribute
            if not stage:
                continue

            # If we are here we have callbacks. To get a complete list, get first what
            # was attached to parent classes, then prepend what we have registered here.
            #
            # The order should be:
            # 1. Callbacks are registered in order within the same class
            # 2. Callbacks defined in derived classes precede those defined in base
            #    classes
            for base in bases:
                callbacks_from_base = getattr(base, attribute_name, None)
                if callbacks_from_base:
                    break
            callbacks_from_base = callbacks_from_base or []

            # Set the attribute for the class to be created
            callbacks = stage[:] + callbacks_from_base
            attr_dict[attribute_name] = callbacks

            # Reset the stage
            setattr(BuilderMeta, stage_name, [])

        return super(BuilderMeta, mcs).__new__(mcs, name, bases, attr_dict)

    @staticmethod
    def make_decorator(build_system):
        class Decorator(object):
            def __init__(self, build_system):
                self.build_system = build_system

            def __call__(self, fn):
                key = (self.build_system, fn.__name__)
                item = (key, fn)
                BuilderMeta._phases_stage.append(item)

            def run_after(self, phase, when=None):
                def _decorator(fn):
                    key = (self.build_system, phase, when)
                    item = (key, fn)
                    BuilderMeta._run_after_stage.append(item)
                    return fn

                return _decorator

            def run_before(self, phase, when=None):
                def _decorator(fn):
                    key = (self.build_system, phase, when)
                    item = (key, fn)
                    BuilderMeta._run_before_stage.append(item)
                    return fn

                return _decorator

        return Decorator(build_system)


class InstallationPhase(object):
    """Manages a single phase of the installation.

    This descriptor stores at creation time the name of the method it should
    search for execution. The method is retrieved at __get__ time, so that
    it can be overridden by subclasses of whatever class declared the phases.

    It also provides hooks to execute arbitrary callbacks before and after
    the phase.
    """

    def __init__(self, name, builder):
        self.name = name
        self.builder = builder
        self.phase_fn = self._select_phase_fn()
        self.run_before = self._make_callbacks(_RUN_BEFORE_PACKAGE_ATTRIBUTE)
        self.run_after = self._make_callbacks(_RUN_AFTER_PACKAGE_ATTRIBUTE)

    def _make_callbacks(self, callbacks_attribute):
        result = []
        callbacks = getattr(self.builder.pkg, callbacks_attribute, [])
        for (build_system, phase, condition), fn in callbacks:
            # If the callback was specifically for another build system, move on
            if build_system != self.builder.build_system and build_system is not None:
                continue

            # Same if it is for another phase
            if phase != self.name:
                continue

            # If we have no condition or the callback satisfies a condition, register it
            if condition is None or self.builder.pkg.spec.satisfies(condition):
                result.append(fn)
        return result

    def __str__(self):
        msg = '{0}: executing "{1}" phase'
        return msg.format(self.builder, self.name)

    def execute(self):
        pkg = self.builder.pkg
        self._on_phase_start(pkg)

        for callback in self.run_before:
            callback(pkg)

        self.phase_fn(pkg, pkg.spec, pkg.prefix)

        for callback in self.run_after:
            callback(pkg)

        self._on_phase_exit(pkg)

    def _select_phase_fn(self):
        package_cls = type(self.builder.pkg)
        for current_cls in inspect.getmro(package_cls):
            # Try to get first a specific override decorated for this build system
            candidates = current_cls.__dict__.get(_PHASE_OVERRIDE_PACKAGE_ATTRIBUTE, [])
            for (build_system, name), candidate_fn in candidates:
                if build_system == self.builder.build_system and name == self.name:
                    phase_fn = candidate_fn
                    break
            else:
                phase_fn = current_cls.__dict__.get(self.name, None)

            if phase_fn:
                break

        else:
            msg = (
                'unexpected error: package "{0.fullname}" must implement an '
                '"{1}" phase for the "{2}" build system'
            )
            raise RuntimeError(
                msg.format(self.builder.pkg, self.name, self.builder.build_system)
            )

        return phase_fn

    def _on_phase_start(self, instance):
        # If a phase has a matching stop_before_phase attribute,
        # stop the installation process raising a StopPhase
        if getattr(instance, "stop_before_phase", None) == self.name:
            raise spack.build_environment.StopPhase(
                "Stopping before '{0}' phase".format(self.name)
            )

    def _on_phase_exit(self, instance):
        # If a phase has a matching last_phase attribute,
        # stop the installation process raising a StopPhase
        if getattr(instance, "last_phase", None) == self.name:
            raise spack.build_environment.StopPhase(
                "Stopping at '{0}' phase".format(self.name)
            )

    def copy(self):
        return copy.deepcopy(self)


class Builder(llnl.util.compat.Sequence):
    """A builder is a class that, given a package object (i.e. associated with
    concrete spec), knows how to install it.

    Args:
        pkg (spack.package.PackageBase): package object to be built
    """

    #: Sequence of phases. Must be defined in derived classes
    phases = None  # type: Optional[Tuple[str, ...]]
    #: Build system name. Must also be defined in derived classes.
    build_system = None  # type: Optional[str]

    def __init__(self, pkg):
        self.pkg = self.inject_build_methods(pkg)
        self.callbacks = {}
        for phase in self.phases:
            self.callbacks[phase] = InstallationPhase(phase, self)

    def inject_build_methods(self, pkg):
        builder_cls = type(self)
        return builder_cls.PackageWrapper(pkg)

    def __getitem__(self, idx):
        key = self.phases[idx]
        return self.callbacks[key]

    def __len__(self):
        return len(self.phases)

    def __repr__(self):
        msg = "{0}({1})"
        return msg.format(
            type(self).__name__, self.package.spec.format("{name}/{hash:7}")
        )

    def __str__(self):
        msg = '"{0}" builder for "{1}"'
        return msg.format(
            type(self).build_system, self.pkg.spec.format("{name}/{hash:7}")
        )


class BuildWrapper(six.with_metaclass(BuilderMeta, object)):
    #: List of glob expressions. Each expression must either be
    #: absolute or relative to the package source path.
    #: Matching artifacts found at the end of the build process will be
    #: copied in the same directory tree as _spack_build_logfile and
    #: _spack_build_envfile.
    archive_files = []  # type: List[str]

    def __init__(self, package_object):
        package_cls = type(package_object)
        wrapper_cls = type(self)
        bases = (package_cls, wrapper_cls)
        new_cls_name = package_cls.__name__ + "BuildWrapper"
        new_cls = type(new_cls_name, bases, {})
        new_cls.__module__ = package_cls.__module__
        for attribute_name in (
            _RUN_BEFORE_PACKAGE_ATTRIBUTE,
            _RUN_AFTER_PACKAGE_ATTRIBUTE,
            _PHASE_OVERRIDE_PACKAGE_ATTRIBUTE,
        ):
            package_callbacks = getattr(package_cls, attribute_name, [])
            wrapper_callbacks = getattr(wrapper_cls, attribute_name, [])
            # FIXME: check that wrapper_cls has no phase overrides,
            # FIXME: they should be simple callbacks
            setattr(new_cls, attribute_name, package_callbacks + wrapper_callbacks)

        self.__class__ = new_cls
        self.__dict__ = package_object.__dict__


# Create generic run_after and run_before decorators not tied to build-systems
# for backward compatibility
_ = BuilderMeta.make_decorator(build_system=None)
run_after = _.run_after
run_before = _.run_before
