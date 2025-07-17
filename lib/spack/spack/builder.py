# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import collections.abc
import copy
import functools
import os
from typing import Callable, Dict, List, Optional, Tuple, Type

import spack.directives
import spack.error
import spack.multimethod
import spack.package_base
import spack.phase_callbacks
import spack.relocate
import spack.repo
import spack.spec
import spack.util.environment
from spack.error import SpackError
from spack.util.prefix import Prefix

#: Builder classes, as registered by the "builder" decorator
BUILDER_CLS: Dict[str, Type["Builder"]] = {}

#: Map id(pkg) to a builder, to avoid creating multiple
#: builders for the same package object.
_BUILDERS: Dict[int, "Builder"] = {}


def register_builder(build_system_name: str):
    """Class decorator used to register the default builder for a given build system. The name
    corresponds to the ``build_system`` variant value of the package.

    Example::

       @register_builder("cmake")
       class CMakeBuilder(BuilderWithDefaults):
           pass


    Args:
        build_system_name: name of the build system
    """

    def _decorator(cls):
        cls.build_system = build_system_name
        BUILDER_CLS[build_system_name] = cls
        return cls

    return _decorator


def create(pkg: spack.package_base.PackageBase) -> "Builder":
    """Given a package object with an associated concrete spec, return the builder object that can
    install it."""
    if id(pkg) not in _BUILDERS:
        _BUILDERS[id(pkg)] = _create(pkg)
    return _BUILDERS[id(pkg)]


class _PhaseAdapter:
    def __init__(self, builder, phase_fn):
        self.builder = builder
        self.phase_fn = phase_fn

    def __call__(self, spec, prefix):
        return self.phase_fn(self.builder.pkg, spec, prefix)


def get_builder_class(pkg, name: str) -> Optional[Type["Builder"]]:
    """Return the builder class if a package module defines it."""
    cls = getattr(pkg.module, name, None)
    if cls and spack.repo.is_package_module(cls.__module__):
        return cls
    return None


def _create(pkg: spack.package_base.PackageBase) -> "Builder":
    """Return a new builder object for the package object being passed as argument.

    The function inspects the build-system used by the package object and try to:

    1. Return a custom builder, if any is defined in the same ``package.py`` file.
    2. Return a customization of more generic builders, if any is defined in the
       class hierarchy (look at AspellDictPackage for an example of that)
    3. Return a run-time generated adapter builder otherwise

    The run-time generated adapter builder is capable of adapting an old-style package
    to the new architecture, where the installation procedure has been extracted from
    the ``*Package`` hierarchy into a ``*Builder`` hierarchy. This means that the
    adapter looks for attribute or method overrides preferably in the ``*Package``
    before using the default builder implementation.

    Note that in case a builder is explicitly coded in ``package.py``, no attempt is made
    to look for build-related methods in the ``*Package``.

    Args:
        pkg: package object for which we need a builder
    """
    package_buildsystem = buildsystem_name(pkg)
    default_builder_cls = BUILDER_CLS[package_buildsystem]
    builder_cls_name = default_builder_cls.__name__
    builder_class = get_builder_class(pkg, builder_cls_name)

    if builder_class:
        return builder_class(pkg)

    # Specialized version of a given buildsystem can subclass some
    # base classes and specialize certain phases or methods or attributes.
    # In that case they can store their builder class as a class level attribute.
    # See e.g. AspellDictPackage as an example.
    base_cls = getattr(pkg, builder_cls_name, default_builder_cls)

    # From here on we define classes to construct a special builder that adapts to the
    # old, single class, package format. The adapter forwards any call or access to an
    # attribute related to the installation procedure to a package object wrapped in
    # a class that falls-back on calling the base builder if no override is found on the
    # package. The semantic should be the same as the method in the base builder were still
    # present in the base class of the package.

    class _ForwardToBaseBuilder:
        def __init__(self, wrapped_pkg_object, root_builder):
            self.wrapped_package_object = wrapped_pkg_object
            self.root_builder = root_builder

            package_cls = type(wrapped_pkg_object)
            wrapper_cls = type(self)
            bases = (package_cls, wrapper_cls)
            new_cls_name = package_cls.__name__ + "Wrapper"
            # Forward attributes that might be monkey patched later
            new_cls = type(
                new_cls_name,
                bases,
                {
                    "__module__": package_cls.__module__,
                    "run_tests": property(lambda x: x.wrapped_package_object.run_tests),
                    "test_requires_compiler": property(
                        lambda x: x.wrapped_package_object.test_requires_compiler
                    ),
                    "test_suite": property(lambda x: x.wrapped_package_object.test_suite),
                    "tester": property(lambda x: x.wrapped_package_object.tester),
                },
            )
            self.__class__ = new_cls
            self.__dict__.update(wrapped_pkg_object.__dict__)

        def __getattr__(self, item):
            result = getattr(super(type(self.root_builder), self.root_builder), item)
            if item in super(type(self.root_builder), self.root_builder).phases:
                result = _PhaseAdapter(self.root_builder, result)
            return result

    def forward_method_to_getattr(fn_name):
        def __forward(self, *args, **kwargs):
            return self.__getattr__(fn_name)(*args, **kwargs)

        return __forward

    # Add fallback methods for the Package object to refer to the builder. If a method
    # with the same name is defined in the Package, it will override this definition
    # (when _ForwardToBaseBuilder is initialized)
    for method_name in (
        base_cls.phases  # type: ignore
        + package_methods(base_cls)  # type: ignore
        + package_long_methods(base_cls)  # type: ignore
        + ("setup_build_environment", "setup_dependent_build_environment")
    ):
        setattr(_ForwardToBaseBuilder, method_name, forward_method_to_getattr(method_name))

    def forward_property_to_getattr(property_name):
        def __forward(self):
            return self.__getattr__(property_name)

        return __forward

    for attribute_name in package_attributes(base_cls):  # type: ignore
        setattr(
            _ForwardToBaseBuilder,
            attribute_name,
            property(forward_property_to_getattr(attribute_name)),
        )

    class Adapter(base_cls, metaclass=_PackageAdapterMeta):  # type: ignore
        def __init__(self, pkg):
            # Deal with custom phases in packages here
            if hasattr(pkg, "phases"):
                self.phases = pkg.phases
                for phase in self.phases:
                    setattr(Adapter, phase, _PackageAdapterMeta.phase_method_adapter(phase))

            # Attribute containing the package wrapped in dispatcher with a `__getattr__`
            # method that will forward certain calls to the default builder.
            self.pkg_with_dispatcher = _ForwardToBaseBuilder(pkg, root_builder=self)
            super().__init__(pkg)

        # These two methods don't follow the (self, spec, prefix) signature of phases nor
        # the (self) signature of methods, so they are added explicitly to avoid using a
        # catch-all (*args, **kwargs)
        def setup_build_environment(
            self, env: spack.util.environment.EnvironmentModifications
        ) -> None:
            return self.pkg_with_dispatcher.setup_build_environment(env)

        def setup_dependent_build_environment(
            self,
            env: spack.util.environment.EnvironmentModifications,
            dependent_spec: spack.spec.Spec,
        ) -> None:
            return self.pkg_with_dispatcher.setup_dependent_build_environment(env, dependent_spec)

    return Adapter(pkg)


def buildsystem_name(pkg: spack.package_base.PackageBase) -> str:
    """Given a package object with an associated concrete spec,
    return the name of its build system."""
    try:
        return pkg.spec.variants["build_system"].value
    except KeyError as e:
        # We are reading an old spec without the build_system variant
        if hasattr(pkg, "default_buildsystem"):
            # Package API v2.2
            return pkg.default_buildsystem
        elif hasattr(pkg, "legacy_buildsystem"):
            return pkg.legacy_buildsystem

        raise SpackError(f"Package {pkg.name} does not define a build system.") from e


class BuilderMeta(
    spack.phase_callbacks.PhaseCallbacksMeta,
    spack.multimethod.MultiMethodMeta,
    type(collections.abc.Sequence),  # type: ignore
):
    pass


class _PackageAdapterMeta(BuilderMeta):
    """Metaclass to adapt old-style packages to the new architecture based on builders
    for the installation phase.

    This class does the necessary mangling to function argument so that a call to a
    builder object can delegate to a package object.
    """

    @staticmethod
    def phase_method_adapter(phase_name):
        def _adapter(self, pkg, spec, prefix):
            phase_fn = getattr(self.pkg_with_dispatcher, phase_name)
            return phase_fn(spec, prefix)

        return _adapter

    @staticmethod
    def legacy_long_method_adapter(method_name):
        def _adapter(self, spec, prefix):
            bind_method = getattr(self.pkg_with_dispatcher, method_name)
            return bind_method(spec, prefix)

        return _adapter

    @staticmethod
    def legacy_method_adapter(method_name):
        def _adapter(self):
            bind_method = getattr(self.pkg_with_dispatcher, method_name)
            return bind_method()

        return _adapter

    @staticmethod
    def legacy_attribute_adapter(attribute_name):
        def _adapter(self):
            return getattr(self.pkg_with_dispatcher, attribute_name)

        return property(_adapter)

    @staticmethod
    def combine_callbacks(pipeline_attribute_name):
        """This function combines callbacks from old-style packages with callbacks that might
        be registered for the default builder.

        It works by:
        1. Extracting the callbacks from the old-style package
        2. Transforming those callbacks by adding an adapter that receives a builder as argument
           and calls the wrapped function with ``builder.pkg``
        3. Combining the list of transformed callbacks with those that might be present in the
           default builder
        """

        def _adapter(self):
            def unwrap_pkg(fn):
                @functools.wraps(fn)
                def _wrapped(builder):
                    return fn(builder.pkg_with_dispatcher)

                return _wrapped

            # Concatenate the current list with the one from package
            callbacks_from_package = getattr(self.pkg, pipeline_attribute_name, [])
            callbacks_from_package = [(key, unwrap_pkg(x)) for key, x in callbacks_from_package]
            callbacks_from_builder = getattr(super(type(self), self), pipeline_attribute_name, [])
            return callbacks_from_package + callbacks_from_builder

        return property(_adapter)

    def __new__(mcs, name, bases, attr_dict):
        # Add ways to intercept methods and attribute calls and dispatch
        # them first to a package object
        default_builder_cls = bases[0]
        for phase_name in default_builder_cls.phases:
            attr_dict[phase_name] = _PackageAdapterMeta.phase_method_adapter(phase_name)

        for method_name in package_methods(default_builder_cls):
            attr_dict[method_name] = _PackageAdapterMeta.legacy_method_adapter(method_name)

        # These exist e.g. for Python, see discussion in https://github.com/spack/spack/pull/32068
        for method_name in package_long_methods(default_builder_cls):
            attr_dict[method_name] = _PackageAdapterMeta.legacy_long_method_adapter(method_name)

        for attribute_name in package_attributes(default_builder_cls):
            attr_dict[attribute_name] = _PackageAdapterMeta.legacy_attribute_adapter(
                attribute_name
            )

        combine_callbacks = _PackageAdapterMeta.combine_callbacks
        attr_dict[spack.phase_callbacks._RUN_BEFORE.attribute_name] = combine_callbacks(
            spack.phase_callbacks._RUN_BEFORE.attribute_name
        )
        attr_dict[spack.phase_callbacks._RUN_AFTER.attribute_name] = combine_callbacks(
            spack.phase_callbacks._RUN_AFTER.attribute_name
        )

        return super(_PackageAdapterMeta, mcs).__new__(mcs, name, bases, attr_dict)


class InstallationPhase:
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
        self.run_before = self._make_callbacks(spack.phase_callbacks._RUN_BEFORE.attribute_name)
        self.run_after = self._make_callbacks(spack.phase_callbacks._RUN_AFTER.attribute_name)

    def _make_callbacks(self, callbacks_attribute):
        result = []
        callbacks = getattr(self.builder, callbacks_attribute, [])
        for (phase, condition), fn in callbacks:
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
            callback(self.builder)

        self.phase_fn(pkg, pkg.spec, pkg.prefix)

        for callback in self.run_after:
            callback(self.builder)

        self._on_phase_exit(pkg)

    def _select_phase_fn(self):
        phase_fn = getattr(self.builder, self.name, None)

        if not phase_fn:
            msg = (
                'unexpected error: package "{0.fullname}" must implement an '
                '"{1}" phase for the "{2}" build system'
            )
            raise RuntimeError(msg.format(self.builder.pkg, self.name, self.builder.build_system))

        return phase_fn

    def _on_phase_start(self, instance):
        # If a phase has a matching stop_before_phase attribute,
        # stop the installation process raising a StopPhase
        if getattr(instance, "stop_before_phase", None) == self.name:
            raise spack.error.StopPhase("Stopping before '{0}' phase".format(self.name))

    def _on_phase_exit(self, instance):
        # If a phase has a matching last_phase attribute,
        # stop the installation process raising a StopPhase
        if getattr(instance, "last_phase", None) == self.name:
            raise spack.error.StopPhase("Stopping at '{0}' phase".format(self.name))

    def copy(self):
        return copy.deepcopy(self)


class BaseBuilder(metaclass=BuilderMeta):
    """An interface for builders, without any phases defined. This class is exposed in the package
    API, so that packagers can create a single class to define :meth:`setup_build_environment` and
    :func:`spack.phase_callbacks.run_before` and :func:`spack.phase_callbacks.run_after`
    callbacks that can be shared among different builders.

    Example:

    .. code-block:: python

       class AnyBuilder(BaseBuilder):
           @run_after("install")
           def fixup_install(self):
                # do something after the package is installed
                pass

           def setup_build_environment(self, env: EnvironmentModifications) -> None:
                env.set("MY_ENV_VAR", "my_value")

        class CMakeBuilder(cmake.CMakeBuilder, AnyBuilder):
            pass

        class AutotoolsBuilder(autotools.AutotoolsBuilder, AnyBuilder):
            pass
    """

    def __init__(self, pkg: spack.package_base.PackageBase) -> None:
        self.pkg = pkg

    @property
    def spec(self) -> spack.spec.Spec:
        return self.pkg.spec

    @property
    def stage(self):
        return self.pkg.stage

    @property
    def prefix(self):
        return self.pkg.prefix

    def setup_build_environment(
        self, env: spack.util.environment.EnvironmentModifications
    ) -> None:
        """Sets up the build environment for a package.

        This method will be called before the current package prefix exists in
        Spack's store.

        Args:
            env: environment modifications to be applied when the package is built. Package authors
                can call methods on it to alter the build environment.
        """
        if not hasattr(super(), "setup_build_environment"):
            return
        super().setup_build_environment(env)  # type: ignore

    def setup_dependent_build_environment(
        self, env: spack.util.environment.EnvironmentModifications, dependent_spec: spack.spec.Spec
    ) -> None:
        """Sets up the build environment of a package that depends on this one.

        This is similar to ``setup_build_environment``, but it is used to modify the build
        environment of a package that *depends* on this one.

        This gives packages the ability to set environment variables for the build of the
        dependent, which can be useful to provide search hints for headers or libraries if they are
        not in standard locations.

        This method will be called before the dependent package prefix exists in Spack's store.

        Args:
            env: environment modifications to be applied when the dependent package is built.
                Package authors can call methods on it to alter the build environment.

            dependent_spec: the spec of the dependent package about to be built. This allows the
                extendee (self) to query the dependent's state. Note that *this* package's spec is
                available as ``self.spec``
        """
        if not hasattr(super(), "setup_dependent_build_environment"):
            return
        super().setup_dependent_build_environment(env, dependent_spec)  # type: ignore

    def __repr__(self):
        fmt = "{name}{/hash:7}"
        return f"{self.__class__.__name__}({self.spec.format(fmt)})"

    def __str__(self):
        fmt = "{name}{/hash:7}"
        return f'"{self.__class__.__name__}" builder for "{self.spec.format(fmt)}"'


class Builder(BaseBuilder, collections.abc.Sequence):
    """A builder is a class that, given a package object (i.e. associated with concrete spec),
    knows how to install it.

    The builder behaves like a sequence, and when iterated over return the "phases" of the
    installation in the correct order.
    """

    #: Sequence of phases. Must be defined in derived classes
    phases: Tuple[str, ...] = ()
    #: Build system name. Must also be defined in derived classes.
    build_system: Optional[str] = None

    #: Methods, with no arguments, that the adapter can find in Package classes,
    #: if a builder is not defined.
    package_methods: Tuple[str, ...]
    # Use :attr:`package_methods` instead of this attribute, which is deprecated
    legacy_methods: Tuple[str, ...] = ()

    #: Methods with the same signature as phases, that the adapter can find in Package classes,
    #: if a builder is not defined.
    package_long_methods: Tuple[str, ...]
    # Use :attr:`package_long_methods` instead of this attribute, which is deprecated
    legacy_long_methods: Tuple[str, ...]

    #: Attributes that the adapter can find in Package classes, if a builder is not defined
    package_attributes: Tuple[str, ...]
    # Use :attr:`package_attributes` instead of this attribute, which is deprecated
    legacy_attributes: Tuple[str, ...] = ()

    # type hints for some of the legacy methods
    build_time_test_callbacks: List[str]
    install_time_test_callbacks: List[str]

    #: List of glob expressions. Each expression must either be absolute or relative to the package
    #: source path. Matching artifacts found at the end of the build process will be copied in the
    #: same directory tree as _spack_build_logfile and _spack_build_envfile.
    @property
    def archive_files(self) -> List[str]:
        return []

    def __init__(self, pkg: spack.package_base.PackageBase) -> None:
        super().__init__(pkg)
        self.callbacks = {}
        for phase in self.phases:
            self.callbacks[phase] = InstallationPhase(phase, self)

    def __getitem__(self, idx):
        key = self.phases[idx]
        return self.callbacks[key]

    def __len__(self):
        return len(self.phases)


def package_methods(builder: Type[Builder]) -> Tuple[str, ...]:
    """Returns the list of methods, taking no arguments, that are defined in the package
    class and are associated with the builder.
    """
    if hasattr(builder, "package_methods"):
        # Package API v2.2
        return builder.package_methods

    return builder.legacy_methods


def package_attributes(builder: Type[Builder]) -> Tuple[str, ...]:
    """Returns the list of attributes that are defined in the package class and are associated
    with the builder.
    """
    if hasattr(builder, "package_attributes"):
        # Package API v2.2
        return builder.package_attributes

    return builder.legacy_attributes


def package_long_methods(builder: Type[Builder]) -> Tuple[str, ...]:
    """Returns the list of methods, with the same signature as phases, that are defined in
    the package class and are associated with the builder.
    """
    if hasattr(builder, "package_long_methods"):
        # Package API v2.2
        return builder.package_long_methods

    return getattr(builder, "legacy_long_methods", tuple())


def sanity_check_prefix(builder: Builder):
    """Check that specific directories and files are created after installation.

    The files to be checked are in the ``sanity_check_is_file`` attribute of the
    package object, while the directories are in the ``sanity_check_is_dir``.

    Args:
        builder: builder that installed the package
    """
    pkg = builder.pkg

    def check_paths(path_list: List[str], filetype: str, predicate: Callable[[str], bool]) -> None:
        if isinstance(path_list, str):
            path_list = [path_list]

        for path in path_list:
            if not predicate(os.path.join(pkg.prefix, path)):
                raise spack.error.InstallError(
                    f"Install failed for {pkg.name}. No such {filetype} in prefix: {path}"
                )

    check_paths(pkg.sanity_check_is_file, "file", os.path.isfile)
    check_paths(pkg.sanity_check_is_dir, "directory", os.path.isdir)

    # Check that the prefix is not empty apart from the .spack/ directory
    with os.scandir(pkg.prefix) as entries:
        f = next(
            (f for f in entries if not (f.name == ".spack" and f.is_dir(follow_symlinks=False))),
            None,
        )

    if f is None:
        raise spack.error.InstallError(f"Install failed for {pkg.name}.  Nothing was installed!")


class BuilderWithDefaults(Builder):
    """Base class for all specific builders with common callbacks registered."""

    # Check that self.prefix is there after installation
    spack.phase_callbacks.run_after("install")(sanity_check_prefix)


def apply_macos_rpath_fixups(builder: Builder):
    """On Darwin, make installed libraries more easily relocatable.

    Some build systems (handrolled, autotools, makefiles) can set their own
    rpaths that are duplicated by spack's compiler wrapper. This fixup
    interrogates, and postprocesses if necessary, all libraries installed
    by the code.

    It should be added as a @run_after to packaging systems (or individual
    packages) that do not install relocatable libraries by default.

    Args:
        builder: builder that installed the package
    """
    spack.relocate.fixup_macos_rpaths(builder.spec)


def execute_install_time_tests(builder: Builder):
    """Execute the install-time tests prescribed by builder.

    Args:
        builder: builder prescribing the test callbacks. The name of the callbacks is
            stored as a list of strings in the ``install_time_test_callbacks`` attribute.
    """
    if not builder.pkg.run_tests or not builder.install_time_test_callbacks:
        return

    builder.pkg.tester.phase_tests(builder, "install", builder.install_time_test_callbacks)


class Package(spack.package_base.PackageBase):
    """Build system base class for packages that do not use a specific build system. It adds the
    ``build_system=generic`` variant to the package.

    This is the only build system base class defined in Spack core. All other build systems
    are defined in the builtin package repository :mod:`spack_repo.builtin.build_systems`.

    The associated builder is :class:`GenericBuilder`, which is only necessary when the package
    has multiple build systems.

    Example::

       from spack.package import *

       class MyPackage(Package):
           \"\"\"A package that does not use a specific build system.\"\"\"

           homepage = "https://example.com/mypackage"
           url = "https://example.com/mypackage-1.0.tar.gz"

           version("1.0", sha256="...")

           def install(self, spec: Spec, prefix: Prefix) -> None:
               # Custom installation logic here
               pass

    .. note::

       The difference between :class:`Package` and :class:`~spack.package_base.PackageBase` is that
       :class:`~spack.package_base.PackageBase` is the universal base class for all package
       classes, no matter their build system.

       The :class:`Package` class is a *build system base class*, similar to
       ``CMakePackage``, and ``AutotoolsPackage``. It is called ``Package`` and not
       ``GenericPackage`` for legacy reasons.

    """

    #: This attribute is used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = "Package"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    default_buildsystem = "generic"

    spack.directives.build_system("generic")


@register_builder("generic")
class GenericBuilder(BuilderWithDefaults):
    """The associated builder for the :class:`Package` base class. This class is typically only
    used in ``package.py`` files when a package has multiple build systems. Packagers need to
    implement the :meth:`install` phase to define how the package is installed.

    This is the only builder that is defined in the Spack core, all other builders are defined
    in the builtin package repository :mod:`spack_repo.builtin.build_systems`.

    Example::

       from spack.package import *

       class MyPackage(Package):
           \"\"\"A package that does not use a specific build system.\"\"\"
           homepage = "https://example.com/mypackage"
           url = "https://example.com/mypackage-1.0.tar.gz"

           version("1.0", sha256="...")

       class GenericBuilder(GenericBuilder):
           def install(self, pkg: Package, spec: Spec, prefix: Prefix) -> None:
               pass
    """

    #: A generic package has only the "install" phase
    phases = ("install",)

    #: Names associated with package methods in the old build-system format
    package_methods: Tuple[str, ...] = ()

    #: Names associated with package attributes in the old build-system format
    package_attributes: Tuple[str, ...] = ("archive_files", "install_time_test_callbacks")

    #: Callback names for post-install phase tests
    install_time_test_callbacks = []

    # On macOS, force rpaths for shared library IDs and remove duplicate rpaths
    spack.phase_callbacks.run_after("install", when="platform=darwin")(apply_macos_rpath_fixups)

    # unconditionally perform any post-install phase tests
    spack.phase_callbacks.run_after("install")(execute_install_time_tests)

    def install(self, pkg: Package, spec: spack.spec.Spec, prefix: Prefix) -> None:
        """Install phase for the generic builder, to be implemented by packagers."""
        raise NotImplementedError
