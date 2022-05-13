# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import contextlib
import fnmatch
import functools
import json
import os
import os.path
import platform
import re
import sys
import sysconfig

import six

import archspec.cpu

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.lang import GroupedExceptionHandler

import spack.binary_distribution
import spack.config
import spack.detection
import spack.environment
import spack.modules
import spack.paths
import spack.platforms
import spack.repo
import spack.spec
import spack.store
import spack.user_environment
import spack.util.environment
import spack.util.executable
import spack.util.path

#: Map a bootstrapper type to the corresponding class
_bootstrap_methods = {}


def _bootstrapper(type):
    """Decorator to register classes implementing bootstrapping
    methods.

    Args:
        type (str): string identifying the class
    """
    def _register(cls):
        _bootstrap_methods[type] = cls
        return cls
    return _register


def _try_import_from_store(module, query_spec, query_info=None):
    """Return True if the module can be imported from an already
    installed spec, False otherwise.

    Args:
        module: Python module to be imported
        query_spec: spec that may provide the module
        query_info (dict or None): if a dict is passed it is populated with the
            command found and the concrete spec providing it
    """
    # If it is a string assume it's one of the root specs by this module
    if isinstance(query_spec, six.string_types):
        # We have to run as part of this python interpreter
        query_spec += ' ^' + spec_for_current_python()

    installed_specs = spack.store.db.query(query_spec, installed=True)

    for candidate_spec in installed_specs:
        pkg = candidate_spec['python'].package
        module_paths = {
            os.path.join(candidate_spec.prefix, pkg.purelib),
            os.path.join(candidate_spec.prefix, pkg.platlib),
        }
        sys.path.extend(module_paths)

        try:
            _fix_ext_suffix(candidate_spec)
            if _python_import(module):
                msg = ('[BOOTSTRAP MODULE {0}] The installed spec "{1}/{2}" '
                       'provides the "{0}" Python module').format(
                    module, query_spec, candidate_spec.dag_hash()
                )
                tty.debug(msg)
                if query_info is not None:
                    query_info['spec'] = candidate_spec
                return True
        except Exception as e:
            msg = ('unexpected error while trying to import module '
                   '"{0}" from spec "{1}" [error="{2}"]')
            tty.warn(msg.format(module, candidate_spec, str(e)))
        else:
            msg = "Spec {0} did not provide module {1}"
            tty.warn(msg.format(candidate_spec, module))

        sys.path = sys.path[:-3]

    return False


def _fix_ext_suffix(candidate_spec):
    """Fix the external suffixes of Python extensions on the fly for
    platforms that may need it

    Args:
        candidate_spec (Spec): installed spec with a Python module
            to be checked.
    """
    # Here we map target families to the patterns expected
    # by pristine CPython. Only architectures with known issues
    # are included. Known issues:
    #
    # [RHEL + ppc64le]: https://github.com/spack/spack/issues/25734
    #
    _suffix_to_be_checked = {
        'ppc64le': {
            'glob': '*.cpython-*-powerpc64le-linux-gnu.so',
            're': r'.cpython-[\w]*-powerpc64le-linux-gnu.so',
            'fmt': r'{module}.cpython-{major}{minor}m-powerpc64le-linux-gnu.so'
        }
    }

    # If the current architecture is not problematic return
    generic_target = archspec.cpu.host().family
    if str(generic_target) not in _suffix_to_be_checked:
        return

    # If there's no EXT_SUFFIX (Python < 3.5) or the suffix matches
    # the expectations, return since the package is surely good
    ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
    if ext_suffix is None:
        return

    expected = _suffix_to_be_checked[str(generic_target)]
    if fnmatch.fnmatch(ext_suffix, expected['glob']):
        return

    # If we are here it means the current interpreter expects different names
    # than pristine CPython. So:
    # 1. Find what we have installed
    # 2. Create symbolic links for the other names, it they're not there already

    # Check if standard names are installed and if we have to create
    # link for this interpreter
    standard_extensions = fs.find(candidate_spec.prefix, expected['glob'])
    link_names = [re.sub(expected['re'], ext_suffix,  s) for s in standard_extensions]
    for file_name, link_name in zip(standard_extensions, link_names):
        if os.path.exists(link_name):
            continue
        os.symlink(file_name, link_name)

    # Check if this interpreter installed something and we have to create
    # links for a standard CPython interpreter
    non_standard_extensions = fs.find(candidate_spec.prefix, '*' + ext_suffix)
    for abs_path in non_standard_extensions:
        directory, filename = os.path.split(abs_path)
        module = filename.split('.')[0]
        link_name = os.path.join(directory, expected['fmt'].format(
            module=module, major=sys.version_info[0], minor=sys.version_info[1])
        )
        if os.path.exists(link_name):
            continue
        os.symlink(abs_path, link_name)


def _executables_in_store(executables, query_spec, query_info=None):
    """Return True if at least one of the executables can be retrieved from
    a spec in store, False otherwise.

    The different executables must provide the same functionality and are
    "alternate" to each other, i.e. the function will exit True on the first
    executable found.

    Args:
        executables: list of executables to be searched
        query_spec: spec that may provide the executable
        query_info (dict or None): if a dict is passed it is populated with the
            command found and the concrete spec providing it
    """
    executables_str = ', '.join(executables)
    msg = "[BOOTSTRAP EXECUTABLES {0}] Try installed specs with query '{1}'"
    tty.debug(msg.format(executables_str, query_spec))
    installed_specs = spack.store.db.query(query_spec, installed=True)
    if installed_specs:
        for concrete_spec in installed_specs:
            bin_dir = concrete_spec.prefix.bin
            # IF we have a "bin" directory and it contains
            # the executables we are looking for
            if (os.path.exists(bin_dir) and os.path.isdir(bin_dir) and
                    spack.util.executable.which_string(*executables, path=bin_dir)):
                spack.util.environment.path_put_first('PATH', [bin_dir])
                if query_info is not None:
                    query_info['command'] = spack.util.executable.which(
                        *executables, path=bin_dir
                    )
                    query_info['spec'] = concrete_spec
                return True
    return False


@_bootstrapper(type='buildcache')
class _BuildcacheBootstrapper(object):
    """Install the software needed during bootstrapping from a buildcache."""
    def __init__(self, conf):
        self.name = conf['name']
        self.url = conf['info']['url']
        self.last_search = None

    @staticmethod
    def _spec_and_platform(abstract_spec_str):
        """Return the spec object and platform we need to use when
        querying the buildcache.

        Args:
            abstract_spec_str: abstract spec string we are looking for
        """
        # This import is local since it is needed only on Cray
        import spack.platforms.linux

        # Try to install from an unsigned binary cache
        abstract_spec = spack.spec.Spec(abstract_spec_str)
        # On Cray we want to use Linux binaries if available from mirrors
        bincache_platform = spack.platforms.real_host()
        return abstract_spec, bincache_platform

    def _read_metadata(self, package_name):
        """Return metadata about the given package."""
        json_filename = '{0}.json'.format(package_name)
        json_path = os.path.join(
            spack.paths.share_path, 'bootstrap', self.name, json_filename
        )
        with open(json_path) as f:
            data = json.load(f)
        return data

    def _install_by_hash(self, pkg_hash, pkg_sha256, index, bincache_platform):
        index_spec = next(x for x in index if x.dag_hash() == pkg_hash)
        # Reconstruct the compiler that we need to use for bootstrapping
        compiler_entry = {
            "modules": [],
            "operating_system": str(index_spec.os),
            "paths": {
                "cc": "/dev/null",
                "cxx": "/dev/null",
                "f77": "/dev/null",
                "fc": "/dev/null"
            },
            "spec": str(index_spec.compiler),
            "target": str(index_spec.target.family)
        }
        with spack.platforms.use_platform(bincache_platform):
            with spack.config.override(
                    'compilers', [{'compiler': compiler_entry}]
            ):
                spec_str = '/' + pkg_hash
                query = spack.binary_distribution.BinaryCacheQuery(
                    all_architectures=True
                )
                matches = spack.store.find([spec_str], multiple=False, query_fn=query)
                for match in matches:
                    spack.binary_distribution.install_root_node(
                        match,
                        allow_root=True,
                        unsigned=True,
                        force=True,
                        sha256=pkg_sha256
                    )

    def _install_and_test(
            self, abstract_spec, bincache_platform, bincache_data, test_fn
    ):
        # Ensure we see only the buildcache being used to bootstrap
        with spack.config.override(self.mirror_scope):
            # This index is currently needed to get the compiler used to build some
            # specs that we know by dag hash.
            spack.binary_distribution.binary_index.regenerate_spec_cache()
            index = spack.binary_distribution.update_cache_and_get_specs()

            if not index:
                raise RuntimeError("The binary index is empty")

            for item in bincache_data['verified']:
                candidate_spec = item['spec']
                # This will be None for things that don't depend on python
                python_spec = item.get('python', None)
                # Skip specs which are not compatible
                if not abstract_spec.satisfies(candidate_spec):
                    continue

                if python_spec is not None and python_spec not in abstract_spec:
                    continue

                for pkg_name, pkg_hash, pkg_sha256 in item['binaries']:
                    # TODO: undo installations that didn't complete?
                    self._install_by_hash(
                        pkg_hash, pkg_sha256, index, bincache_platform
                    )

                info = {}
                if test_fn(query_spec=abstract_spec, query_info=info):
                    self.last_search = info
                    return True
        return False

    @property
    def mirror_scope(self):
        return spack.config.InternalConfigScope(
            'bootstrap_buildcache', {'mirrors:': {self.name: self.url}}
        )

    def try_import(self, module, abstract_spec_str):
        test_fn, info = functools.partial(_try_import_from_store, module), {}
        if test_fn(query_spec=abstract_spec_str, query_info=info):
            return True

        tty.info("Bootstrapping {0} from pre-built binaries".format(module))
        abstract_spec, bincache_platform = self._spec_and_platform(
            abstract_spec_str + ' ^' + spec_for_current_python()
        )
        data = self._read_metadata(module)
        return self._install_and_test(
            abstract_spec, bincache_platform, data, test_fn
        )

    def try_search_path(self, executables, abstract_spec_str):
        test_fn, info = functools.partial(_executables_in_store, executables), {}
        if test_fn(query_spec=abstract_spec_str, query_info=info):
            self.last_search = info
            return True

        abstract_spec, bincache_platform = self._spec_and_platform(abstract_spec_str)
        tty.info("Bootstrapping {0} from pre-built binaries".format(abstract_spec.name))
        data = self._read_metadata(abstract_spec.name)
        return self._install_and_test(
            abstract_spec, bincache_platform, data, test_fn
        )


@_bootstrapper(type='install')
class _SourceBootstrapper(object):
    """Install the software needed during bootstrapping from sources."""
    def __init__(self, conf):
        self.conf = conf
        self.last_search = None

    def try_import(self, module, abstract_spec_str):
        info = {}
        if _try_import_from_store(module, abstract_spec_str, query_info=info):
            self.last_search = info
            return True

        tty.info("Bootstrapping {0} from sources".format(module))

        # If we compile code from sources detecting a few build tools
        # might reduce compilation time by a fair amount
        _add_externals_if_missing()

        # Try to build and install from sources
        with spack_python_interpreter():
            # Add hint to use frontend operating system on Cray
            concrete_spec = spack.spec.Spec(
                abstract_spec_str + ' ^' + spec_for_current_python()
            )

            if module == 'clingo':
                # TODO: remove when the old concretizer is deprecated
                concrete_spec._old_concretize(deprecation_warning=False)
            else:
                concrete_spec.concretize()

        msg = "[BOOTSTRAP MODULE {0}] Try installing '{1}' from sources"
        tty.debug(msg.format(module, abstract_spec_str))

        # Install the spec that should make the module importable
        concrete_spec.package.do_install(fail_fast=True)

        if _try_import_from_store(module, query_spec=concrete_spec, query_info=info):
            self.last_search = info
            return True
        return False

    def try_search_path(self, executables, abstract_spec_str):
        info = {}
        if _executables_in_store(executables, abstract_spec_str, query_info=info):
            self.last_search = info
            return True

        # If we compile code from sources detecting a few build tools
        # might reduce compilation time by a fair amount
        _add_externals_if_missing()

        concrete_spec = spack.spec.Spec(abstract_spec_str)
        if concrete_spec.name == 'patchelf':
            concrete_spec._old_concretize(deprecation_warning=False)
        else:
            concrete_spec.concretize()

        msg = "[BOOTSTRAP] Try installing '{0}' from sources"
        tty.debug(msg.format(abstract_spec_str))
        concrete_spec.package.do_install()
        if _executables_in_store(executables, concrete_spec, query_info=info):
            self.last_search = info
            return True
        return False


def _make_bootstrapper(conf):
    """Return a bootstrap object built according to the
    configuration argument
    """
    btype = conf['type']
    return _bootstrap_methods[btype](conf)


def _validate_source_is_trusted(conf):
    trusted, name = spack.config.get('bootstrap:trusted'), conf['name']
    if name not in trusted:
        raise ValueError('source is not trusted')


def spec_for_current_python():
    """For bootstrapping purposes we are just interested in the Python
    minor version (all patches are ABI compatible with the same minor)
    and on whether ucs4 support has been enabled for Python 2.7

    See:
      https://www.python.org/dev/peps/pep-0513/
      https://stackoverflow.com/a/35801395/771663
    """
    version_str = '.'.join(str(x) for x in sys.version_info[:2])
    variant_str = ''
    if sys.version_info[0] == 2 and sys.version_info[1] == 7:
        unicode_size = sysconfig.get_config_var('Py_UNICODE_SIZE')
        variant_str = '+ucs4' if unicode_size == 4 else '~ucs4'

    spec_fmt = 'python@{0} {1}'
    return spec_fmt.format(version_str, variant_str)


@contextlib.contextmanager
def spack_python_interpreter():
    """Override the current configuration to set the interpreter under
    which Spack is currently running as the only Python external spec
    available.
    """
    python_prefix = sys.exec_prefix
    external_python = spec_for_current_python()

    entry = {
        'buildable': False,
        'externals': [
            {'prefix': python_prefix, 'spec': str(external_python)}
        ]
    }

    with spack.config.override('packages:python::', entry):
        yield


def ensure_module_importable_or_raise(module, abstract_spec=None):
    """Make the requested module available for import, or raise.

    This function tries to import a Python module in the current interpreter
    using, in order, the methods configured in bootstrap.yaml.

    If none of the methods succeed, an exception is raised. The function exits
    on first success.

    Args:
        module (str): module to be imported in the current interpreter
        abstract_spec (str): abstract spec that might provide the module. If not
            given it defaults to "module"

    Raises:
        ImportError: if the module couldn't be imported
    """
    # If we can import it already, that's great
    tty.debug("[BOOTSTRAP MODULE {0}] Try importing from Python".format(module))
    if _python_import(module):
        return

    abstract_spec = abstract_spec or module
    source_configs = spack.config.get('bootstrap:sources', [])

    h = GroupedExceptionHandler()

    for current_config in source_configs:
        with h.forward(current_config['name']):
            _validate_source_is_trusted(current_config)

            b = _make_bootstrapper(current_config)
            if b.try_import(module, abstract_spec):
                return

    assert h, 'expected at least one exception to have been raised at this point: while bootstrapping {0}'.format(module)  # noqa: E501
    msg = 'cannot bootstrap the "{0}" Python module '.format(module)
    if abstract_spec:
        msg += 'from spec "{0}" '.format(abstract_spec)
    msg += h.grouped_message()
    raise ImportError(msg)


def ensure_executables_in_path_or_raise(executables, abstract_spec):
    """Ensure that some executables are in path or raise.

    Args:
        executables (list): list of executables to be searched in the PATH,
            in order. The function exits on the first one found.
        abstract_spec (str): abstract spec that provides the executables

    Raises:
        RuntimeError: if the executables cannot be ensured to be in PATH

    Return:
        Executable object
    """
    cmd = spack.util.executable.which(*executables)
    if cmd:
        return cmd

    executables_str = ', '.join(executables)
    source_configs = spack.config.get('bootstrap:sources', [])

    h = GroupedExceptionHandler()

    for current_config in source_configs:
        with h.forward(current_config['name']):
            _validate_source_is_trusted(current_config)

            b = _make_bootstrapper(current_config)
            if b.try_search_path(executables, abstract_spec):
                # Additional environment variables needed
                concrete_spec, cmd = b.last_search['spec'], b.last_search['command']
                env_mods = spack.util.environment.EnvironmentModifications()
                for dep in concrete_spec.traverse(
                        root=True, order='post', deptype=('link', 'run')
                ):
                    env_mods.extend(
                        spack.user_environment.environment_modifications_for_spec(
                            dep, set_package_py_globals=False
                        )
                    )
                cmd.add_default_envmod(env_mods)
                return cmd

    assert h, 'expected at least one exception to have been raised at this point: while bootstrapping {0}'.format(executables_str)  # noqa: E501
    msg = 'cannot bootstrap any of the {0} executables '.format(executables_str)
    if abstract_spec:
        msg += 'from spec "{0}" '.format(abstract_spec)
    msg += h.grouped_message()
    raise RuntimeError(msg)


def _python_import(module):
    try:
        __import__(module)
    except ImportError:
        return False
    return True


def _bootstrap_config_scopes():
    tty.debug('[BOOTSTRAP CONFIG SCOPE] name=_builtin')
    config_scopes = [
        spack.config.InternalConfigScope('_builtin', spack.config.config_defaults)
    ]
    configuration_paths = (
        spack.config.configuration_defaults_path,
        ('bootstrap', _config_path())
    )
    for name, path in configuration_paths:
        platform = spack.platforms.host().name
        platform_scope = spack.config.ConfigScope(
            '/'.join([name, platform]), os.path.join(path, platform)
        )
        generic_scope = spack.config.ConfigScope(name, path)
        config_scopes.extend([generic_scope, platform_scope])
        msg = '[BOOTSTRAP CONFIG SCOPE] name={0}, path={1}'
        tty.debug(msg.format(generic_scope.name, generic_scope.path))
        tty.debug(msg.format(platform_scope.name, platform_scope.path))
    return config_scopes


def _add_compilers_if_missing():
    arch = spack.spec.ArchSpec.frontend_arch()
    if not spack.compilers.compilers_for_arch(arch):
        new_compilers = spack.compilers.find_new_compilers()
        if new_compilers:
            spack.compilers.add_compilers_to_config(new_compilers, init_config=False)


def _add_externals_if_missing():
    search_list = [
        # clingo
        spack.repo.path.get('cmake'),
        spack.repo.path.get('bison'),
        # GnuPG
        spack.repo.path.get('gawk')
    ]
    detected_packages = spack.detection.by_executable(search_list)
    spack.detection.update_configuration(detected_packages, scope='bootstrap')


#: Reference counter for the bootstrapping configuration context manager
_REF_COUNT = 0


@contextlib.contextmanager
def ensure_bootstrap_configuration():
    # The context manager is reference counted to ensure we don't swap multiple
    # times if there's nested use of it in the stack. One compelling use case
    # is bootstrapping patchelf during the bootstrap of clingo.
    global _REF_COUNT
    already_swapped = bool(_REF_COUNT)
    _REF_COUNT += 1
    try:
        if already_swapped:
            yield
        else:
            with _ensure_bootstrap_configuration():
                yield
    finally:
        _REF_COUNT -= 1


@contextlib.contextmanager
def _ensure_bootstrap_configuration():
    bootstrap_store_path = store_path()
    user_configuration = _read_and_sanitize_configuration()
    with spack.environment.no_active_environment():
        with spack.platforms.prevent_cray_detection():
            with spack.platforms.use_platform(spack.platforms.real_host()):
                with spack.repo.use_repositories(spack.paths.packages_path):
                    with spack.store.use_store(bootstrap_store_path):
                        # Default configuration scopes excluding command line
                        # and builtin but accounting for platform specific scopes
                        config_scopes = _bootstrap_config_scopes()
                        with spack.config.use_configuration(*config_scopes):
                            # We may need to compile code from sources, so ensure we
                            # have compilers for the current platform
                            _add_compilers_if_missing()
                            spack.config.set(
                                'bootstrap', user_configuration['bootstrap']
                            )
                            spack.config.set(
                                'config', user_configuration['config']
                            )
                            with spack.modules.disable_modules():
                                with spack_python_interpreter():
                                    yield


def _read_and_sanitize_configuration():
    """Read the user configuration that needs to be reused for bootstrapping
    and remove the entries that should not be copied over.
    """
    # Read the "config" section but pop the install tree (the entry will not be
    # considered due to the use_store context manager, so it will be confusing
    # to have it in the configuration).
    config_yaml = spack.config.get('config')
    config_yaml.pop('install_tree', None)
    user_configuration = {
        'bootstrap': spack.config.get('bootstrap'),
        'config': config_yaml
    }
    return user_configuration


def store_path():
    """Path to the store used for bootstrapped software"""
    enabled = spack.config.get('bootstrap:enable', True)
    if not enabled:
        msg = ('bootstrapping is currently disabled. '
               'Use "spack bootstrap enable" to enable it')
        raise RuntimeError(msg)

    return _store_path()


def _root_path():
    """Root of all the bootstrap related folders"""
    return spack.config.get(
        'bootstrap:root', spack.paths.default_user_bootstrap_path
    )


def _store_path():
    bootstrap_root_path = _root_path()
    return spack.util.path.canonicalize_path(
        os.path.join(bootstrap_root_path, 'store')
    )


def _config_path():
    bootstrap_root_path = _root_path()
    return spack.util.path.canonicalize_path(
        os.path.join(bootstrap_root_path, 'config')
    )


def _root_spec(spec_str):
    """Add a proper compiler and target to a spec used during bootstrapping.

    Args:
        spec_str (str): spec to be bootstrapped. Must be without compiler and target.
    """
    # Add a proper compiler hint to the root spec. We use GCC for
    # everything but MacOS and Windows.
    if str(spack.platforms.host()) == 'darwin':
        spec_str += ' %apple-clang'
    elif str(spack.platforms.host()) == 'windows':
        spec_str += ' %msvc'
    else:
        spec_str += ' %gcc'

    target = archspec.cpu.host().family
    spec_str += ' target={0}'.format(target)

    tty.debug('[BOOTSTRAP ROOT SPEC] {0}'.format(spec_str))
    return spec_str


def clingo_root_spec():
    """Return the root spec used to bootstrap clingo"""
    return _root_spec('clingo-bootstrap@spack+python')


def ensure_clingo_importable_or_raise():
    """Ensure that the clingo module is available for import."""
    ensure_module_importable_or_raise(
        module='clingo', abstract_spec=clingo_root_spec()
    )


def gnupg_root_spec():
    """Return the root spec used to bootstrap GnuPG"""
    return _root_spec('gnupg@2.3:')


def ensure_gpg_in_path_or_raise():
    """Ensure gpg or gpg2 are in the PATH or raise."""
    return ensure_executables_in_path_or_raise(
        executables=['gpg2', 'gpg'], abstract_spec=gnupg_root_spec()
    )


def patchelf_root_spec():
    """Return the root spec used to bootstrap patchelf"""
    # TODO: patchelf is restricted to v0.13 since earlier versions have
    # TODO: bugs that we don't to deal with, while v0.14 requires a C++17
    # TODO: which may not be available on all platforms.
    return _root_spec('patchelf@0.13.1:0.13.99')


def ensure_patchelf_in_path_or_raise():
    """Ensure patchelf is in the PATH or raise."""
    return ensure_executables_in_path_or_raise(
        executables=['patchelf'], abstract_spec=patchelf_root_spec()
    )


###
# Development dependencies
###


def isort_root_spec():
    return _root_spec('py-isort@4.3.5:')


def ensure_isort_in_path_or_raise():
    """Ensure that isort is in the PATH or raise."""
    executable, root_spec = 'isort', isort_root_spec()
    return ensure_executables_in_path_or_raise([executable], abstract_spec=root_spec)


def mypy_root_spec():
    return _root_spec('py-mypy@0.900:')


def ensure_mypy_in_path_or_raise():
    """Ensure that mypy is in the PATH or raise."""
    executable, root_spec = 'mypy', mypy_root_spec()
    return ensure_executables_in_path_or_raise([executable], abstract_spec=root_spec)


def black_root_spec():
    return _root_spec('py-black')


def ensure_black_in_path_or_raise():
    """Ensure that isort is in the PATH or raise."""
    executable, root_spec = 'black', black_root_spec()
    return ensure_executables_in_path_or_raise([executable], abstract_spec=root_spec)


def flake8_root_spec():
    return _root_spec('py-flake8')


def ensure_flake8_in_path_or_raise():
    """Ensure that flake8 is in the PATH or raise."""
    executable, root_spec = 'flake8', flake8_root_spec()
    return ensure_executables_in_path_or_raise([executable], abstract_spec=root_spec)


def _missing(name, purpose, system_only=True):
    """Message to be printed if an executable is not found"""
    msg = '[{2}] MISSING "{0}": {1}'
    if not system_only:
        return msg.format(name, purpose, '@*y{{B}}')
    return msg.format(name, purpose, '@*y{{-}}')


def _required_system_executable(exes, msg):
    """Search for an executable is the system path only."""
    if isinstance(exes, six.string_types):
        exes = (exes,)
    if spack.util.executable.which_string(*exes):
        return True, None
    return False, msg


def _required_python_module(module, query_spec, msg):
    """Check if a Python module is available in the current interpreter or
    if it can be loaded from the bootstrap store
    """
    if _python_import(module) or _try_import_from_store(module, query_spec):
        return True, None
    return False, msg


def _required_executable(exes, query_spec, msg):
    """Search for an executable in the system path or in the bootstrap store."""
    if isinstance(exes, six.string_types):
        exes = (exes,)
    if (spack.util.executable.which_string(*exes) or
            _executables_in_store(exes, query_spec)):
        return True, None
    return False, msg


def _core_requirements():
    _core_system_exes = {
        'make': _missing('make', 'required to build software from sources'),
        'patch': _missing('patch', 'required to patch source code before building'),
        'bash': _missing('bash', 'required for Spack compiler wrapper'),
        'tar': _missing('tar', 'required to manage code archives'),
        'gzip': _missing('gzip', 'required to compress/decompress code archives'),
        'unzip': _missing('unzip', 'required to compress/decompress code archives'),
        'bzip2': _missing('bzip2', 'required to compress/decompress code archives'),
        'git': _missing('git', 'required to fetch/manage git repositories')
    }
    if platform.system().lower() == 'linux':
        _core_system_exes['xz'] = _missing(
            'xz', 'required to compress/decompress code archives'
        )

    # Executables that are not bootstrapped yet
    result = [_required_system_executable(exe, msg)
              for exe, msg in _core_system_exes.items()]
    # Python modules
    result.append(_required_python_module(
        'clingo', clingo_root_spec(),
        _missing('clingo', 'required to concretize specs', False)
    ))
    return result


def _buildcache_requirements():
    _buildcache_exes = {
        'file': _missing('file', 'required to analyze files for buildcaches'),
        ('gpg2', 'gpg'): _missing('gpg2', 'required to sign/verify buildcaches', False)
    }
    if platform.system().lower() == 'darwin':
        _buildcache_exes['otool'] = _missing('otool', 'required to relocate binaries')

    # Executables that are not bootstrapped yet
    result = [_required_system_executable(exe, msg)
              for exe, msg in _buildcache_exes.items()]

    if platform.system().lower() == 'linux':
        result.append(_required_executable(
            'patchelf', patchelf_root_spec(),
            _missing('patchelf', 'required to relocate binaries', False)
        ))

    return result


def _optional_requirements():
    _optional_exes = {
        'zstd': _missing('zstd', 'required to compress/decompress code archives'),
        'svn': _missing('svn', 'required to manage subversion repositories'),
        'hg': _missing('hg', 'required to manage mercurial repositories')
    }
    # Executables that are not bootstrapped yet
    result = [_required_system_executable(exe, msg)
              for exe, msg in _optional_exes.items()]
    return result


def _development_requirements():
    return [
        _required_executable('isort', isort_root_spec(),
                             _missing('isort', 'required for style checks', False)),
        _required_executable('mypy', mypy_root_spec(),
                             _missing('mypy', 'required for style checks', False)),
        _required_executable('flake8', flake8_root_spec(),
                             _missing('flake8', 'required for style checks', False)),
        _required_executable('black', black_root_spec(),
                             _missing('black', 'required for code formatting', False))
    ]


def status_message(section):
    """Return a status message to be printed to screen that refers to the
    section passed as argument and a bool which is True if there are missing
    dependencies.

    Args:
        section (str): either 'core' or 'buildcache' or 'optional' or 'develop'
    """
    pass_token, fail_token = '@*g{[PASS]}', '@*r{[FAIL]}'

    # Contain the header of the section and a list of requirements
    spack_sections = {
        'core': ("{0} @*{{Core Functionalities}}", _core_requirements),
        'buildcache': ("{0} @*{{Binary packages}}", _buildcache_requirements),
        'optional': ("{0} @*{{Optional Features}}", _optional_requirements),
        'develop': ("{0} @*{{Development Dependencies}}", _development_requirements)
    }
    msg, required_software = spack_sections[section]

    with ensure_bootstrap_configuration():
        missing_software = False
        for found, err_msg in required_software():
            if not found:
                missing_software = True
                msg += "\n  " + err_msg
        msg += '\n'
        msg = msg.format(pass_token if not missing_software else fail_token)
    return msg, missing_software
