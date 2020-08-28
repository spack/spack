# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import errno
import functools
import os
import re

import llnl.util.lang

import spack.error
import spack.paths
import spack.util.executable
import spack.version


_gnupg_version_re = r"^gpg(conf)? \(GnuPG\) (.*)$"
_gnupg_home_override = None
_global_gpg_instance = None


def get_gnupg_home(gnupg_home=None):
    """Returns the directory that should be used as the GNUPGHOME environment
    variable when calling gpg.

    If a [gnupg_home] is passed directly (and not None), that value will be
    used.

    Otherwise, if there is an override set (and it is not None), then that
    value will be used.

    Otherwise, if the environment variable "SPACK_GNUPGHOME" is set, then that
    value will be used.

    Otherwise, the default gpg path for Spack will be used.

    See also: gnupg_home_override()
    """
    return (gnupg_home or
            _gnupg_home_override or
            os.getenv('SPACK_GNUPGHOME') or
            spack.paths.gpg_path)


@contextlib.contextmanager
def gnupg_home_override(new_gnupg_home):
    global _gnupg_home_override
    global _global_gpg_instance

    old_gnupg_home_override = _gnupg_home_override
    old_global_gpg_instance = _global_gpg_instance

    _gnupg_home_override = new_gnupg_home
    _global_gpg_instance = None

    yield

    _gnupg_home_override = old_gnupg_home_override
    _global_gpg_instance = old_global_gpg_instance


def get_global_gpg_instance():
    global _global_gpg_instance
    if _global_gpg_instance is None:
        _global_gpg_instance = Gpg()
    return _global_gpg_instance


def parse_secret_keys_output(output):
    keys = []
    found_sec = False
    for line in output.split('\n'):
        if found_sec:
            if line.startswith('fpr'):
                keys.append(line.split(':')[9])
                found_sec = False
            elif line.startswith('ssb'):
                found_sec = False
        elif line.startswith('sec'):
            found_sec = True
    return keys


def parse_public_keys_output(output):
    keys = []
    found_pub = False
    for line in output.split('\n'):
        if found_pub:
            if line.startswith('fpr'):
                keys.append(line.split(':')[9])
                found_pub = False
            elif line.startswith('ssb'):
                found_pub = False
        elif line.startswith('pub'):
            found_pub = True
    return keys


cached_property = getattr(functools, 'cached_property', None)

# If older python version has no cached_property, emulate it here.
# TODO(opadron): maybe this shim should be moved to llnl.util.lang?
if not cached_property:
    def cached_property(*args, **kwargs):
        result = property(llnl.util.lang.memoized(*args, **kwargs))
        attr = result.fget.__name__

        @result.deleter
        def result(self):
            getattr(type(self), attr).fget.cache.pop((self,), None)

        return result


class GpgConstants(object):
    @cached_property
    def target_version(self):
        return spack.version.Version('2')

    @cached_property
    def gpgconf_string(self):
        exe_str = spack.util.executable.which_string(
            'gpgconf', 'gpg2conf', 'gpgconf2')

        no_gpgconf_msg = (
            'Spack requires gpgconf version >= 2\n'
            '  To install a suitable version using Spack, run\n'
            '    spack install gnupg@2:\n'
            '  and load it by running\n'
            '    spack load gnupg@2:')

        if not exe_str:
            raise SpackGPGError(no_gpgconf_msg)

        exe = spack.util.executable.Executable(exe_str)
        output = exe('--version', output=str)
        match = re.search(_gnupg_version_re, output, re.M)

        if not match:
            raise SpackGPGError('Could not determine gpgconf version')

        if spack.version.Version(match.group(2)) < self.target_version:
            raise SpackGPGError(no_gpgconf_msg)

        # ensure that the gpgconf we found can run "gpgconf --create-socketdir"
        try:
            exe('--dry-run', '--create-socketdir')
        except spack.util.executable.ProcessError:
            # no dice
            exe_str = None

        return exe_str

    @cached_property
    def gpg_string(self):
        exe_str = spack.util.executable.which_string('gpg2', 'gpg')

        no_gpg_msg = (
            'Spack requires gpg version >= 2\n'
            '  To install a suitable version using Spack, run\n'
            '    spack install gnupg@2:\n'
            '  and load it by running\n'
            '    spack load gnupg@2:')

        if not exe_str:
            raise SpackGPGError(no_gpg_msg)

        exe = spack.util.executable.Executable(exe_str)
        output = exe('--version', output=str)
        match = re.search(_gnupg_version_re, output, re.M)

        if not match:
            raise SpackGPGError('Could not determine gpg version')

        if spack.version.Version(match.group(2)) < self.target_version:
            raise SpackGPGError(no_gpg_msg)

        return exe_str

    @cached_property
    def user_run_dir(self):
        # Try to ensure that (/var)/run/user/$(id -u) exists so that
        #  `gpgconf --create-socketdir` can be run later.
        #
        # NOTE(opadron): This action helps prevent a large class of
        #                "file-name-too-long" errors in gpg.

        try:
            has_suitable_gpgconf = bool(GpgConstants.gpgconf_string)
        except SpackGPGError:
            has_suitable_gpgconf = False

        # If there is no suitable gpgconf, don't even bother trying to
        # precreate a user run dir.
        if not has_suitable_gpgconf:
            return None

        result = None
        for var_run_user in ('/run/user', '/var/run/user'):
            user_dir = os.path.join(var_run_user, str(os.getuid()))
            try:
                mkdir = (os.path.isdir(var_run_user) and
                         not os.path.exists(user_dir))
                if mkdir:
                    os.mkdir(user_dir)
                    os.chmod(user_dir, 0o700)

            # If the above operation fails due to lack of permissions, then
            # just carry on without running gpgconf and hope for the best.
            #
            # NOTE(opadron): Without a dir in which to create a socket for IPC,
            #                gnupg may fail if GNUPGHOME is set to a path that
            #                is too long, where "too long" in this context is
            #                actually quite short; somewhere in the
            #                neighborhood of more than 100 characters.
            #
            # TODO(opadron): Maybe a warning should be printed in this case?
            except OSError as exc:
                if exc.errno not in (errno.EPERM, errno.EACCES):
                    raise
                user_dir = None

            # return the last iteration that provides a usable user run dir
            if user_dir is not None:
                result = user_dir

        return result

    def clear(self):
        for attr in ('gpgconf_string', 'gpg_string', 'user_run_dir'):
            try:
                delattr(self, attr)
            except AttributeError:
                pass


GpgConstants = GpgConstants()


def ensure_gpg(reevaluate=False):
    if reevaluate:
        GpgConstants.clear()

    if GpgConstants.user_run_dir is not None:
        GpgConstants.gpgconf_string

    GpgConstants.gpg_string
    return True


def has_gpg(*args, **kwargs):
    try:
        return ensure_gpg(*args, **kwargs)
    except SpackGPGError:
        return False


class wrap(list):
    def __call__(self, *args):
        if len(args) > 2:
            raise ValueError('too many args')

        if len(args) == 0:
            return self

        if len(args) == 1:
            name = args[0]
            if callable(name):
                func = name
                name = func.__name__
            else:
                return (lambda func: self(func, name))

        if len(args) == 2:
            func, name = args

        self.append((func, name))
        return func


wrap = wrap()


class Gpg(object):
    def __init__(self, gnupg_home=None):
        self.gnupg_home = get_gnupg_home(gnupg_home)

    @cached_property
    def prep(self):
        # Make sure that suitable versions of gpgconf and gpg are available
        ensure_gpg()

        # Make sure that the GNUPGHOME exists
        if not os.path.exists(self.gnupg_home):
            os.makedirs(self.gnupg_home)

        if not os.path.isdir(self.gnupg_home):
            raise SpackGPGError(
                'GNUPGHOME "{0}" exists and is not a directory'.format(
                    self.gnupg_home))

        if GpgConstants.user_run_dir is not None:
            self.gpgconf_exe('--create-socketdir')

        return True

    @cached_property
    def gpgconf_exe(self):
        exe = spack.util.executable.Executable(GpgConstants.gpgconf_string)
        exe.add_default_env('GNUPGHOME', self.gnupg_home)
        return exe

    @cached_property
    def gpg_exe(self):
        exe = spack.util.executable.Executable(GpgConstants.gpg_string)
        exe.add_default_env('GNUPGHOME', self.gnupg_home)
        return exe

    @wrap('gpg')
    def __call__(self, *args, **kwargs):
        if self.prep:
            return self.gpg_exe(*args, **kwargs)

    @wrap
    def create(self, **kwargs):
        r, w = os.pipe()
        r = os.fdopen(r, 'r')
        w = os.fdopen(w, 'w')
        w.write('''
        Key-Type: rsa
        Key-Length: 4096
        Key-Usage: sign
        Name-Real: %(name)s
        Name-Email: %(email)s
        Name-Comment: %(comment)s
        Expire-Date: %(expires)s
        %%no-protection
        %%commit
        ''' % kwargs)
        w.close()
        self('--gen-key', '--batch', input=r)
        r.close()

    @wrap
    def signing_keys(self, *args):
        output = self('--list-secret-keys', '--with-colons', '--fingerprint',
                      *args, output=str)
        return parse_secret_keys_output(output)

    @wrap
    def public_keys(self, *args):
        output = self('--list-public-keys', '--with-colons', '--fingerprint',
                      *args, output=str)
        return parse_public_keys_output(output)

    @wrap
    def export_keys(self, location, *keys):
        self('--batch', '--yes',
             '--armor', '--export',
             '--output', location, *keys)

    @wrap
    def trust(self, keyfile):
        self('--import', keyfile)

    @wrap
    def untrust(self, signing, *keys):
        if signing:
            skeys = self.signing_keys(*keys)
            self('--batch', '--yes', '--delete-secret-keys', *skeys)

        pkeys = self.public_keys(*keys)
        self('--batch', '--yes', '--delete-keys', *pkeys)

    @wrap
    def sign(self, key, file, output, clearsign=False):
        self(('--clearsign' if clearsign else '--detach-sign'),
             '--armor', '--default-key', key,
             '--output', output, file)

    @wrap
    def verify(self, signature, file, suppress_warnings=False):
        self('--verify', signature, file,
             **({'error': str} if suppress_warnings else {}))

    @wrap
    def list(self, trusted, signing):
        if trusted:
            self('--list-public-keys')

        if signing:
            self('--list-secret-keys')


class SpackGPGError(spack.error.SpackError):
    """Class raised when GPG errors are detected."""


# Make wrapped versions of the Gpg instance methods for convenience
#
# Done so that most calling code can skip the creation of a Gpg instance.
#
#     Instead of this:
#         import spack.util.gpg
#         gpg = spack.util.gpg.Gpg(gnupg_home='...')
#         gpg('--version')
#         gpg.public_keys()
#
#     Use this:
#         import spack.util.gpg as gpg
#         gpg.gpg('--version')
#         gpg.public_keys()
#
#     If using a non-default GNUPGHOME:
#         with gpg.gnupg_home_override('...'):
#             ...
def _make_wrapped_callables(namespace):
    global wrap

    def _make_wrapped_callable(func, name):
        if func.__name__ == '__call__':
            @functools.wraps(func)
            def result(*args, **kwargs):
                _callable = get_global_gpg_instance()
                return _callable(*args, **kwargs)
        else:
            @functools.wraps(func)
            def result(*args, **kwargs):
                _callable = getattr(get_global_gpg_instance(), name)
                return _callable(*args, **kwargs)

        result.name = name
        return result

    for func, name in wrap:
        namespace[name] = _make_wrapped_callable(func, name)


_make_wrapped_callables(globals())

del _make_wrapped_callables
del wrap
