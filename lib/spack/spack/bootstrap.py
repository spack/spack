# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import contextlib
import fnmatch
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

import spack.architecture
import spack.binary_distribution
import spack.config
import spack.environment
import spack.main
import spack.modules
import spack.paths
import spack.platforms
import spack.repo
import spack.spec
import spack.store
import spack.user_environment as uenv
import spack.util.executable
import spack.util.path
from spack.util.environment import EnvironmentModifications

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
    bincache_platform = spack.architecture.real_platform()
    if str(bincache_platform) == 'cray':
        bincache_platform = spack.platforms.linux.Linux()
        with spack.architecture.use_platform(bincache_platform):
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


@_bootstrapper(type='buildcache')
class _BuildcacheBootstrapper(object):
    """Install the software needed during bootstrapping from a buildcache."""
    def __init__(self, conf):
        self.name = conf['name']
        self.url = conf['info']['url']

    def try_import(self, module, abstract_spec_str):
        if _try_import_from_store(module, abstract_spec_str):
            return True

        # Try to install from an unsigned binary cache
        abstract_spec = spack.spec.Spec(
            abstract_spec_str + ' ^' + spec_for_current_python()
        )

        # On Cray we want to use Linux binaries if available from mirrors
        bincache_platform = spack.architecture.real_platform()
        if str(bincache_platform) == 'cray':
            bincache_platform = spack.platforms.Linux()
            with spack.architecture.use_platform(bincache_platform):
                abstract_spec = spack.spec.Spec(
                    abstract_spec_str + ' ^' + spec_for_current_python()
                )

        # Read information on verified clingo binaries
        json_filename = '{0}.json'.format(module)
        json_path = os.path.join(
            spack.paths.share_path, 'bootstrap', self.name, json_filename
        )
        with open(json_path) as f:
            data = json.load(f)

        buildcache = spack.main.SpackCommand('buildcache')
        # Ensure we see only the buildcache being used to bootstrap
        mirror_scope = spack.config.InternalConfigScope(
            'bootstrap', {'mirrors:': {self.name: self.url}}
        )
        with spack.config.override(mirror_scope):
            # This index is currently needed to get the compiler used to build some
            # specs that wwe know by dag hash.
            spack.binary_distribution.binary_index.regenerate_spec_cache()
            index = spack.binary_distribution.update_cache_and_get_specs()
            for item in data['verified']:
                candidate_spec = item['spec']
                python_spec = item['python']
                # Skip specs which are not compatible
                if not abstract_spec.satisfies(candidate_spec):
                    continue

                if python_spec not in abstract_spec:
                    continue

                for pkg_name, pkg_hash, pkg_sha256 in item['binaries']:
                    msg = ('[BOOTSTRAP MODULE {0}] Try installing "{1}" from binary '
                           'cache at "{2}"')
                    tty.debug(msg.format(module, pkg_name, self.url))
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
                    with spack.architecture.use_platform(bincache_platform):
                        with spack.config.override(
                                'compilers', [{'compiler': compiler_entry}]
                        ):
                            spec_str = '/' + pkg_hash
                            install_args = [
                                'install',
                                '--sha256', pkg_sha256,
                                '-a', '-u', '-o', '-f', spec_str
                            ]
                            buildcache(*install_args, fail_on_error=False)
                # TODO: undo installations that didn't complete?

                if _try_import_from_store(module, abstract_spec_str):
                    return True
        return False


@_bootstrapper(type='install')
class _SourceBootstrapper(object):
    """Install the software needed during bootstrapping from sources."""
    def __init__(self, conf):
        self.conf = conf

    @staticmethod
    def try_import(module, abstract_spec_str):
        if _try_import_from_store(module, abstract_spec_str):
            return True

        # Try to build and install from sources
        with spack_python_interpreter():
            # Add hint to use frontend operating system on Cray
            if str(spack.architecture.platform()) == 'cray':
                abstract_spec_str += ' os=fe'

            concrete_spec = spack.spec.Spec(
                abstract_spec_str + ' ^' + spec_for_current_python()
            )

            if module == 'clingo':
                # TODO: remove when the old concretizer is deprecated
                concrete_spec._old_concretize()
            else:
                concrete_spec.concretize()

        msg = "[BOOTSTRAP MODULE {0}] Try installing '{1}' from sources"
        tty.debug(msg.format(module, abstract_spec_str))

        # Install the spec that should make the module importable
        concrete_spec.package.do_install()

        return _try_import_from_store(module, abstract_spec_str=abstract_spec_str)


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

    # We couldn't import in any way, so raise an import error
    msg = 'cannot bootstrap the "{0}" Python module'.format(module)
    if abstract_spec:
        msg += ' from spec "{0}"'.format(abstract_spec)
    raise ImportError(msg)


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
                envmod.extend(uenv.environment_modifications_for_spec(dep))
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
            envmod.extend(uenv.environment_modifications_for_spec(dep))
        ret.add_default_envmod(envmod)
        return ret

    _raise_error(exe, spec)


def _bootstrap_config_scopes():
    tty.debug('[BOOTSTRAP CONFIG SCOPE] name=_builtin')
    config_scopes = [
        spack.config.InternalConfigScope('_builtin', spack.config.config_defaults)
    ]
    for name, path in spack.config.configuration_paths:
        platform = spack.architecture.platform().name
        platform_scope = spack.config.ConfigScope(
            '/'.join([name, platform]), os.path.join(path, platform)
        )
        generic_scope = spack.config.ConfigScope(name, path)
        config_scopes.extend([generic_scope, platform_scope])
        msg = '[BOOTSTRAP CONFIG SCOPE] name={0}, path={1}'
        tty.debug(msg.format(generic_scope.name, generic_scope.path))
        tty.debug(msg.format(platform_scope.name, platform_scope.path))
    return config_scopes


@contextlib.contextmanager
def ensure_bootstrap_configuration():
    # We may need to compile code from sources, so ensure we have compilers
    # for the current platform before switching parts.
    arch = spack.architecture.default_arch()
    arch = spack.spec.ArchSpec(str(arch))  # The call below expects an ArchSpec object
    if not spack.compilers.compilers_for_arch(arch):
        compiler_cmd = spack.main.SpackCommand('compiler')
        compiler_cmd(
            'find', output=os.devnull, error=os.devnull, fail_on_error=False
        )

    bootstrap_store_path = store_path()
    with spack.environment.deactivate_environment():
        with spack.architecture.use_platform(spack.architecture.real_platform()):
            with spack.repo.use_repositories(spack.paths.packages_path):
                with spack.store.use_store(bootstrap_store_path):
                    # Default configuration scopes excluding command line
                    # and builtin but accounting for platform specific scopes
                    config_scopes = _bootstrap_config_scopes()
                    with spack.config.use_configuration(*config_scopes):
                        with spack.modules.disable_modules():
                            with spack_python_interpreter():
                                yield


def store_path():
    """Path to the store used for bootstrapped software"""
    enabled = spack.config.get('bootstrap:enable', True)
    if not enabled:
        msg = ('bootstrapping is currently disabled. '
               'Use "spack bootstrap enable" to enable it')
        raise RuntimeError(msg)

    bootstrap_root_path = spack.config.get(
        'bootstrap:root', spack.paths.user_bootstrap_path
    )
    bootstrap_store_path = spack.util.path.canonicalize_path(
        os.path.join(bootstrap_root_path, 'store')
    )
    return bootstrap_store_path


def clingo_root_spec():
    # Construct the root spec that will be used to bootstrap clingo
    spec_str = 'clingo-bootstrap@spack+python'

    # Add a proper compiler hint to the root spec. We use GCC for
    # everything but MacOS.
    if str(spack.architecture.platform()) == 'darwin':
        spec_str += ' %apple-clang'
    else:
        spec_str += ' %gcc'

    # Add the generic target
    generic_target = archspec.cpu.host().family
    spec_str += ' target={0}'.format(str(generic_target))

    tty.debug('[BOOTSTRAP ROOT SPEC] clingo: {0}'.format(spec_str))

    return spec_str


def ensure_clingo_importable_or_raise():
    """Ensure that the clingo module is available for import."""
    ensure_module_importable_or_raise(
        module='clingo', abstract_spec=clingo_root_spec()
    )
