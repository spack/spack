# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
import re
import sys

try:
    import sysconfig  # novm
except ImportError:
    # Not supported on Python 2.6
    pass

import archspec.cpu

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.binary_distribution
import spack.config
import spack.detection
import spack.environment
import spack.main
import spack.modules
import spack.paths
import spack.platforms
import spack.repo
import spack.spec
import spack.store
import spack.user_environment
import spack.util.executable
import spack.util.path
from spack.util.environment import EnvironmentModifications

#: "spack buildcache" command, initialized lazily
_buildcache_cmd = None

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


def _try_import_from_store(module, abstract_spec_str):
    """Return True if the module can be imported from an already
    installed spec, False otherwise.

    Args:
        module: Python module to be imported
        abstract_spec_str: abstract spec that may provide the module
    """
    bincache_platform = spack.platforms.real_host()
    if str(bincache_platform) == 'cray':
        bincache_platform = spack.platforms.linux.Linux()
        with spack.platforms.use_platform(bincache_platform):
            abstract_spec_str = str(spack.spec.Spec(abstract_spec_str))

    # We have to run as part of this python interpreter
    abstract_spec_str += ' ^' + spec_for_current_python()

    installed_specs = spack.store.db.query(abstract_spec_str, installed=True)

    for candidate_spec in installed_specs:
        lib_spd = candidate_spec['python'].package.default_site_packages_dir
        lib64_spd = lib_spd.replace('lib/', 'lib64/')
        module_paths = [
            os.path.join(candidate_spec.prefix, lib_spd),
            os.path.join(candidate_spec.prefix, lib64_spd)
        ]
        sys.path.extend(module_paths)

        try:
            _fix_ext_suffix(candidate_spec)
            if _python_import(module):
                msg = ('[BOOTSTRAP MODULE {0}] The installed spec "{1}/{2}" '
                       'provides the "{0}" Python module').format(
                    module, abstract_spec_str, candidate_spec.dag_hash()
                )
                tty.debug(msg)
                return True
        except Exception as e:
            msg = ('unexpected error while trying to import module '
                   '"{0}" from spec "{1}" [error="{2}"]')
            tty.warn(msg.format(module, candidate_spec, str(e)))
        else:
            msg = "Spec {0} did not provide module {1}"
            tty.warn(msg.format(candidate_spec, module))

        sys.path = sys.path[:-2]

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


def _executables_in_store(executables, abstract_spec_str):
    """Return True if at least one of the executables can be retrieved from
    a spec in store, False otherwise.

    The different executables must provide the same functionality and are
    "alternate" to each other, i.e. the function will exit True on the first
    executable found.

    Args:
        executables: list of executables to be searched
        abstract_spec_str: abstract spec that may provide the executable
    """
    executables_str = ', '.join(executables)
    msg = "[BOOTSTRAP EXECUTABLES {0}] Try installed specs with query '{1}'"
    tty.debug(msg.format(executables_str, abstract_spec_str))
    installed_specs = spack.store.db.query(abstract_spec_str, installed=True)
    if installed_specs:
        for concrete_spec in installed_specs:
            bin_dir = concrete_spec.prefix.bin
            # IF we have a "bin" directory and it contains
            # the executables we are looking for
            if (os.path.exists(bin_dir) and os.path.isdir(bin_dir) and
                    spack.util.executable.which_string(*executables, path=bin_dir)):
                spack.util.environment.path_put_first('PATH', [bin_dir])
                return True
    return False


@_bootstrapper(type='buildcache')
class _BuildcacheBootstrapper(object):
    """Install the software needed during bootstrapping from a buildcache."""
    def __init__(self, conf):
        self.name = conf['name']
        self.url = conf['info']['url']

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
        if str(bincache_platform) == 'cray':
            bincache_platform = spack.platforms.Linux()
            with spack.platforms.use_platform(bincache_platform):
                abstract_spec = spack.spec.Spec(abstract_spec_str)
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
        global _buildcache_cmd

        if _buildcache_cmd is None:
            _buildcache_cmd = spack.main.SpackCommand('buildcache')

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
                install_args = [
                    'install',
                    '--sha256', pkg_sha256,
                    '--only-root',
                    '-a', '-u', '-o', '-f', spec_str
                ]
                _buildcache_cmd(*install_args, fail_on_error=False)

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

                if test_fn():
                    return True
        return False

    @property
    def mirror_scope(self):
        return spack.config.InternalConfigScope(
            'bootstrap_buildcache', {'mirrors:': {self.name: self.url}}
        )

    def try_import(self, module, abstract_spec_str):
        test_fn = functools.partial(_try_import_from_store, module, abstract_spec_str)
        if test_fn():
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
        test_fn = functools.partial(
            _executables_in_store, executables, abstract_spec_str
        )
        if test_fn():
            return True

        abstract_spec, bincache_platform = self._spec_and_platform(
            abstract_spec_str
        )
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

    @staticmethod
    def try_import(module, abstract_spec_str):
        if _try_import_from_store(module, abstract_spec_str):
            return True

        tty.info("Bootstrapping {0} from sources".format(module))

        # If we compile code from sources detecting a few build tools
        # might reduce compilation time by a fair amount
        _add_externals_if_missing()

        # Try to build and install from sources
        with spack_python_interpreter():
            # Add hint to use frontend operating system on Cray
            if str(spack.platforms.host()) == 'cray':
                abstract_spec_str += ' os=fe'

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

        return _try_import_from_store(module, abstract_spec_str=abstract_spec_str)

    def try_search_path(self, executables, abstract_spec_str):
        if _executables_in_store(executables, abstract_spec_str):
            return True

        # If we compile code from sources detecting a few build tools
        # might reduce compilation time by a fair amount
        _add_externals_if_missing()

        # Add hint to use frontend operating system on Cray
        if str(spack.platforms.host()) == 'cray':
            abstract_spec_str += ' os=fe'

        concrete_spec = spack.spec.Spec(abstract_spec_str)
        concrete_spec.concretize()

        msg = "[BOOTSTRAP GnuPG] Try installing '{0}' from sources"
        tty.debug(msg.format(abstract_spec_str))
        concrete_spec.package.do_install()
        return _executables_in_store(executables, abstract_spec_str)


def _make_bootstrapper(conf):
    """Return a bootstrap object built according to the
    configuration argument
    """
    btype = conf['type']
    return _bootstrap_methods[btype](conf)


def _source_is_trusted(conf):
    trusted, name = spack.config.get('bootstrap:trusted'), conf['name']
    if name not in trusted:
        return False
    return trusted[name]


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

    errors = {}

    for current_config in source_configs:
        if not _source_is_trusted(current_config):
            msg = ('[BOOTSTRAP MODULE {0}] Skipping source "{1}" since it is '
                   'not trusted').format(module, current_config['name'])
            tty.debug(msg)
            continue

        b = _make_bootstrapper(current_config)
        try:
            if b.try_import(module, abstract_spec):
                return
        except Exception as e:
            msg = '[BOOTSTRAP MODULE {0}] Unexpected error "{1}"'
            tty.debug(msg.format(module, str(e)))
            errors[current_config['name']] = e

    # We couldn't import in any way, so raise an import error
    msg = 'cannot bootstrap the "{0}" Python module'.format(module)
    if abstract_spec:
        msg += ' from spec "{0}"'.format(abstract_spec)
    msg += ' due to the following failures:\n'
    for method in errors:
        err = errors[method]
        msg += "    '{0}' raised {1}: {2}\n".format(
            method, err.__class__.__name__, str(err))
    msg += '    Please run `spack -d spec zlib` for more verbose error messages'
    raise ImportError(msg)


def ensure_executables_in_path_or_raise(executables, abstract_spec):
    """Ensure that some executables are in path or raise.

    Args:
        executables (list): list of executables to be searched in the PATH,
            in order. The function exits on the first one found.
        abstract_spec (str): abstract spec that provides the executables

    Raises:
        RuntimeError: if the executables cannot be ensured to be in PATH
    """
    if spack.util.executable.which_string(*executables):
        return

    executables_str = ', '.join(executables)
    source_configs = spack.config.get('bootstrap:sources', [])
    for current_config in source_configs:
        if not _source_is_trusted(current_config):
            msg = ('[BOOTSTRAP EXECUTABLES {0}] Skipping source "{1}" since it is '
                   'not trusted').format(executables_str, current_config['name'])
            tty.debug(msg)
            continue

        b = _make_bootstrapper(current_config)
        try:
            if b.try_search_path(executables, abstract_spec):
                return
        except Exception as e:
            msg = '[BOOTSTRAP EXECUTABLES {0}] Unexpected error "{1}"'
            tty.debug(msg.format(executables_str, str(e)))

    # We couldn't import in any way, so raise an import error
    msg = 'cannot bootstrap any of the {0} executables'.format(executables_str)
    if abstract_spec:
        msg += ' from spec "{0}"'.format(abstract_spec)
    raise RuntimeError(msg)


def _python_import(module):
    try:
        __import__(module)
    except ImportError:
        return False
    return True


def get_executable(exe, spec=None, install=False):
    """Find an executable named exe, either in PATH or in Spack

    Args:
        exe (str): needed executable name
        spec (spack.spec.Spec or str): spec to search for exe in (default exe)
        install (bool): install spec if not available

    When ``install`` is True, Spack will use the python used to run Spack as an
    external. The ``install`` option should only be used with packages that
    install quickly (when using external python) or are guaranteed by Spack
    organization to be in a binary mirror (clingo).
    """
    # Search the system first
    runner = spack.util.executable.which(exe)
    if runner:
        return runner

    # Check whether it's already installed
    spec = spack.spec.Spec(spec or exe)
    installed_specs = spack.store.db.query(spec, installed=True)
    for ispec in installed_specs:
        # filter out directories of the same name as the executable
        exe_path = [exe_p for exe_p in fs.find(ispec.prefix, exe)
                    if fs.is_exe(exe_p)]
        if exe_path:
            ret = spack.util.executable.Executable(exe_path[0])
            envmod = EnvironmentModifications()
            for dep in ispec.traverse(root=True, order='post'):
                envmod.extend(
                    spack.user_environment.environment_modifications_for_spec(dep)
                )
            ret.add_default_envmod(envmod)
            return ret
        else:
            tty.warn('Exe %s not found in prefix %s' % (exe, ispec.prefix))

    def _raise_error(executable, exe_spec):
        error_msg = 'cannot find the executable "{0}"'.format(executable)
        if exe_spec:
            error_msg += ' from spec "{0}'.format(exe_spec)
        raise RuntimeError(error_msg)

    # If we're not allowed to install this for ourselves, we can't find it
    if not install:
        _raise_error(exe, spec)

    with spack_python_interpreter():
        # We will install for ourselves, using this python if needed
        # Concretize the spec
        spec.concretize()

    spec.package.do_install()
    # filter out directories of the same name as the executable
    exe_path = [exe_p for exe_p in fs.find(spec.prefix, exe)
                if fs.is_exe(exe_p)]
    if exe_path:
        ret = spack.util.executable.Executable(exe_path[0])
        envmod = EnvironmentModifications()
        for dep in spec.traverse(root=True, order='post'):
            envmod.extend(
                spack.user_environment.environment_modifications_for_spec(dep)
            )
        ret.add_default_envmod(envmod)
        return ret

    _raise_error(exe, spec)


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


@contextlib.contextmanager
def ensure_bootstrap_configuration():
    bootstrap_store_path = store_path()
    user_configuration = _read_and_sanitize_configuration()
    with spack.environment.no_active_environment():
        with spack.platforms.use_platform(spack.platforms.real_host()):
            with spack.repo.use_repositories(spack.paths.packages_path):
                with spack.store.use_store(bootstrap_store_path):
                    # Default configuration scopes excluding command line
                    # and builtin but accounting for platform specific scopes
                    config_scopes = _bootstrap_config_scopes()
                    with spack.config.use_configuration(*config_scopes):
                        # We may need to compile code from sources, so ensure we have
                        # compilers for the current platform before switching parts.
                        _add_compilers_if_missing()
                        spack.config.set('bootstrap', user_configuration['bootstrap'])
                        spack.config.set('config', user_configuration['config'])
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
    # everything but MacOS.
    if str(spack.platforms.host()) == 'darwin':
        spec_str += ' %apple-clang'
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
    ensure_executables_in_path_or_raise(
        executables=['gpg2', 'gpg'], abstract_spec=gnupg_root_spec(),
    )
