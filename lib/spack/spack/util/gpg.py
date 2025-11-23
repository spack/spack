# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib
import datetime
import enum
import errno
import functools
import os
import re
from typing import Any, Callable, Dict, List, Optional

import spack.error
import spack.llnl.util.filesystem
import spack.paths
import spack.util.executable
import spack.version

#: Executable instance for "gpg", initialized lazily
GPG = None
#: Executable instance for "gpgconf", initialized lazily
GPGCONF = None
#: Socket directory required if a non default home directory is used
SOCKET_DIR = None
#: GNUPGHOME environment variable in the context of this Python module
GNUPGHOME = None


class GpgKeyCapability(enum.Enum):
    """Gpg Capabilities"""

    ENCRYPT = "e"
    SIGN = "s"
    CERTIFY = "c"
    AUTHENTICATE = "a"
    DISABLED = "D"
    UNKNOWN = "?"

    @classmethod
    def _missing_(cls, value):
        for cap in cls:
            if value.lower() == cap.value:
                return cap
        return GpgKeyCapability.UNKNOWN


class GpgKeyTrust(enum.Enum):
    """Gpg Trust normalized for Field 1 and Field 9"""

    INVALID = "i"
    REVOKED = "r"
    EXPIRED = "e"
    UNKNOWN = "q"  # - o
    NEVER = "n"
    MARGINAL = "m"
    FULL = "f"
    ULTIMATE = "u"
    KNOWN = "w"
    SPECIAL = "s"

    @classmethod
    def _missing_(cls, value):
        # If it is not found, then it is unknown
        return GpgKeyTrust.UNKNOWN


class GpgKeyAlgorithm(enum.Enum):
    """Gpg Algormithms"""

    RSA = 1
    RSA_SO = 2
    RSA_EO = 3
    ELGAMAL_EO = 16
    DSA = 17
    EC = 18
    ECDSA = 19
    ELGAMAL = 20
    DH = 21
    LIBGCRYPT = 256

    @classmethod
    def _missing_(cls, value):
        if value > 255:
            return GpgKeyAlgorithm.LIBGCRYPT
        return None

    def __str__(cls):
        name = cls.name.lower()
        name = name.replace("_so", " (Signing only)")
        name = name.replace("_eo", " (Encryption only)")
        return name

    def __format__(cls, fspec):
        """Format type with length
        ex. f"{gpg_algo:{gpg_len}}"
        """
        int(fspec)
        name = cls.name.lower()
        name = name.replace("_so", f"{fspec} (Signing only)")
        name = name.replace("_eo", f"{fspec} (Encryption only)")
        return name


class GpgKeyCompliance(enum.Enum):
    """Gpg compliance codes"""

    RFC4880BIS = 8
    DE_VS = 23
    DE_VS_EXP = 2023
    VULN = 6001
    UNKNOWN = 0


class GpgKeyType(enum.Enum):
    """Gpg Key types"""

    PUBLIC = "pub"
    SUBKEY = "sub"
    SECRET = "sec"
    SECRET_SUBKEY = "ssb"
    REVOCATION = "rvk"


class GpgSigType(enum.Enum):
    """Gpg Key signature types"""

    SIGNATURE = "sig"
    REVOCATION = "rev"
    REVOCATION_SO = "rvs"


class GpgUserId:
    def __init__(self, data: Dict[str, str]):
        assert data["type"] in ("uid", "uat")

        self.type = data["type"]
        self.trust = GpgKeyTrust(data["trust"])
        self.hash = data["misc"]
        self.uid = data["uid"]


class GpgSignature:
    def __init__(self, data: Dict[str, str]):
        assert data["type"] in ("sig", "rev", "rvs")

        self.algo = GpgKeyAlgorithm(int(data["key_algo"]))
        self.id = data["key_id"]
        self.created_at = datetime.datetime.fromtimestamp(int(data["created_at"]))
        self.uid = data["uid"]
        self.sig_class = data["sig_class"]


class GpgKey:
    def __init__(self, data: Dict[str, str]):
        assert data["type"] in ("pub", "sec", "sub", "ssb")

        self.type = GpgKeyType(data["type"])

        self.trust = GpgKeyTrust(data["trust"])
        self.key_len = data["len"]
        self.key_algorithm = GpgKeyAlgorithm(int(data["key_algo"]))
        self.key_id = data["key_id"]
        self.created_at = datetime.datetime.fromtimestamp(int(data["created_at"]))
        self.expires_at: Optional[datetime.datetime] = None
        if data.get("expired_at"):
            self.expires_at = datetime.datetime.fromtimestamp(int(data["expired_at"]))

        self.owner_trust = GpgKeyTrust(data["owner_trust"])

        self.capabilities = set()
        for cap in data.get("capabilities", []):
            self.capabilities.add(GpgKeyCapability(cap))

        self.compliance = GpgKeyCompliance(int(data.get("compliance") or 0))

        self.updated_at: Optional[datetime.datetime] = None
        if data.get("updated_at"):
            self.updated_at = datetime.datetime.fromtimestamp(int(data["updated_at"]))
        self.origin = data.get("origin")
        self.comment = data.get("comment", "")

        self.fpr: str = ""
        self.rev: List[GpgSignature] = []
        self.sig: List[GpgSignature] = []
        self.uid: List[GpgUserId] = []
        self.subkey: List[GpgKey] = []

    def add(self, data: Dict[str, str]):
        """Add metadata to a key"""

        if data["type"] in ("fpr", "fp2"):
            self.fpr = data["uid"]

        elif data["type"] in ("uid", "uat"):
            self.uid.append(GpgUserId(data))

        elif data["type"] == "sig":
            self.sig.append(GpgSignature(data))

        elif data["type"] == "rev":
            assert self.trust == GpgKeyTrust.REVOKED
            self.rev.append(GpgSignature(data))

    def __eq__(self, otherkey):
        if isinstance(otherkey, str):
            return self.fpr == otherkey
        elif isinstance(otherkey, GpgKey):
            return self.fpr == otherkey.fpr
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.fpr)

    def __str__(self):
        return self.fpr

    def __format__(self, fspec):
        """Formatted output for GPG key

        Default:
            <fingerprint>

        g[pg] - GPG style output (without colons)
        c[olons] - GPG style output (with colons)
        s[hort] - Shortened output ie. <fingerprint> (<uid>)
        """

        if fspec.startswith("g"):
            return GPG("--list-keys", "--fingerprint", self.fpr, output=str)
        elif fspec.startswith("c"):
            return GPG("--list-keys", "--fingerprint", "--with-colons", self.fpr, output=str)
        elif fspec.startswith("s"):
            return f"{self.fpr} ({self.uid[0].uid})"
        else:
            return self.fpr


def clear():
    """Reset the global state to uninitialized."""
    global GPG, GPGCONF, SOCKET_DIR, GNUPGHOME
    GPG, GPGCONF, SOCKET_DIR, GNUPGHOME = None, None, None, None


def init(gnupghome: Optional[str] = None, force: bool = False):
    """Initialize the global objects in the module, if not set.

    When calling any gpg executable, the GNUPGHOME environment
    variable is set to:

    1. The value of the ``gnupghome`` argument, if not None
    2. The value of the "SPACK_GNUPGHOME" environment variable, if set
    3. The default gpg path for Spack otherwise

    Args:
        gnupghome: value to be used for GNUPGHOME when calling
            GnuPG executables
        force: if True forces the re-initialization even if the
            global objects are set already
    """
    global GPG, GPGCONF, SOCKET_DIR, GNUPGHOME
    import spack.bootstrap

    if force:
        clear()

    # If the executables are already set, there's nothing to do
    if GPG and GNUPGHOME:
        return

    # Set the value of GNUPGHOME to be used in this module
    GNUPGHOME = gnupghome or os.getenv("SPACK_GNUPGHOME") or spack.paths.gpg_path

    # Set the executable objects for "gpg" and "gpgconf"
    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_gpg_in_path_or_raise()
        GPG, GPGCONF = _gpg(), _gpgconf()

    GPG.add_default_env("GNUPGHOME", GNUPGHOME)
    if GPGCONF:
        GPGCONF.add_default_env("GNUPGHOME", GNUPGHOME)
        # Set the socket dir if not using GnuPG defaults
        SOCKET_DIR = _socket_dir(GPGCONF)

    # Make sure that the GNUPGHOME exists
    if not os.path.exists(GNUPGHOME):
        os.makedirs(GNUPGHOME)
        os.chmod(GNUPGHOME, 0o700)

    if not os.path.isdir(GNUPGHOME):
        msg = 'GNUPGHOME "{0}" exists and is not a directory'.format(GNUPGHOME)
        raise SpackGPGError(msg)

    if SOCKET_DIR is not None:
        GPGCONF("--create-socketdir")


def _autoinit(func: Callable[..., Any]):
    """Decorator to ensure that global variables have been initialized before
    running the decorated function.

    Args:
        func: decorated function
    """

    @functools.wraps(func)
    def _wrapped(*args, **kwargs):
        init()
        return func(*args, **kwargs)

    return _wrapped


@contextlib.contextmanager
def gnupghome_override(dir: str):
    """Set the GNUPGHOME to a new location for this context.

    Args:
        dir: new value for GNUPGHOME
    """
    global GPG, GPGCONF, SOCKET_DIR, GNUPGHOME

    # Store backup values
    _GPG, _GPGCONF = GPG, GPGCONF
    _SOCKET_DIR, _GNUPGHOME = SOCKET_DIR, GNUPGHOME
    clear()

    # Clear global state
    init(gnupghome=dir, force=True)

    yield

    clear()
    GPG, GPGCONF = _GPG, _GPGCONF
    SOCKET_DIR, GNUPGHOME = _SOCKET_DIR, _GNUPGHOME


def _parse_gpg_fields(karray: List[str]):
    """Parse gpg line into a dict"""
    fields = [
        "type",
        "trust",
        "len",
        "key_algo",
        "key_id",
        "created_at",
        "expire_at",
        "misc",
        "owner_trust",
        "uid",
        "sig_class",
        "capabilities",
        "issuer_cert",
        "flag",
        "token",
        "hash_algo",
        "curve_name",
        "compliance",
        "updated_at",
        "origin",
        "comment",
    ]
    data = {}
    for key, value in zip(fields, karray):
        data[key] = value

    return data


def _parse_gpg_output(output: str):
    current_key: Optional[GpgKey] = None
    current_subkey: Optional[GpgKey] = None
    keys = []
    for line in output.split("\n"):
        # Only parse lines with colons
        if ":" not in line:
            continue

        data = _parse_gpg_fields(line.split(":"))
        # Skip special fields, Spack doesn't use them
        if data["type"] in ("cfg", "pfc", "pkd", "tfs", "tru", "spk"):
            continue

        # Start of a new key
        if data["type"] in ("pub", "sec"):
            if current_subkey:
                assert current_key
                current_key.subkey.append(current_subkey)
                current_subkey = None
            if current_key:
                keys.append(current_key)
            current_key = GpgKey(data)

        # This should never happen, but in case it does continue
        # as spack doesn't care about lines before the first key
        # is found.
        if not current_key:
            continue

        # Start of a new subkey
        if data["type"] in ("sub", "ssb"):
            if current_subkey:
                current_key.subkey.append(current_subkey)
            current_subkey = GpgKey(data)

        # For the fields that can be in both key and subkey
        if data["type"] in ("sig", "fpr", "fp2"):
            if current_subkey:
                current_subkey.add(data)
            else:
                current_key.add(data)
        else:
            current_key.add(data)

    # Append the last keys
    if current_key:
        if current_subkey:
            current_key.subkey.append(current_subkey)
        keys.append(current_key)

    return keys


class SpackGPGError(spack.error.SpackError):
    """Class raised when GPG errors are detected."""


@_autoinit
def create(**kwargs):
    """Create a new key pair."""
    r, w = os.pipe()
    with contextlib.closing(os.fdopen(r, "r")) as r:
        with contextlib.closing(os.fdopen(w, "w")) as w:
            w.write(
                """
Key-Type: rsa
Key-Length: 4096
Key-Usage: sign
Name-Real: %(name)s
Name-Email: %(email)s
Name-Comment: %(comment)s
Expire-Date: %(expires)s
%%no-protection
%%commit
"""
                % kwargs
            )
        GPG("--gen-key", "--batch", input=r)


@_autoinit
def signing_keys(*args) -> List[str]:
    """Return the keys that can be used to sign binaries."""
    assert GPG
    output: str = GPG("--list-secret-keys", "--with-colons", "--fingerprint", *args, output=str)
    return _parse_gpg_output(output)


@_autoinit
def public_keys(*args):
    """Return a list of fingerprints"""
    assert GPG
    output = GPG("--list-public-keys", "--with-colons", "--fingerprint", *args, output=str)
    return _parse_gpg_output(output)


@_autoinit
def export_keys(location: str, keys: List[GpgKey], secret: bool = False):
    """Export public keys to a location passed as argument.

    Args:
        location: where to export the keys
        keys: keys to be exported
        secret: whether to export secret keys or not
    """
    assert GPG
    fprs = [str(k) for k in keys]
    if secret:
        GPG("--export-secret-keys", "--armor", "--output", location, *fprs)
    else:
        GPG("--batch", "--yes", "--armor", "--export", "--output", location, *fprs)


@_autoinit
def extract_public_keys(keyfile: str):
    """Extract the public key ids from a file

    Args:
        keyfile: file with the public key
    """
    assert GPG
    # Get the public keys we are about to import
    output = GPG("--with-colons", "--with-fingerprint", keyfile, output=str, error=str)
    return [k for k in _parse_gpg_output(output) if k.type == GpgKeyType.PUBLIC]


@_autoinit
def trust(keyfile: str):
    """Import a public key from a file and trust it.

    Args:
        keyfile: file with the public key
    """
    assert GPG
    keys = extract_public_keys(keyfile)

    # Import them
    GPG("--batch", "--import", keyfile)

    # Set trust to ultimate
    known_keys = public_keys()
    for key in keys:
        # Skip over keys we cannot find a fingerprint for.
        if key not in known_keys:
            continue

        r, w = os.pipe()
        with contextlib.closing(os.fdopen(r, "r")) as rc:
            with contextlib.closing(os.fdopen(w, "w")) as wc:
                wc.write("{0}:6:\n".format(str(key)))
            GPG("--import-ownertrust", input=rc)


@_autoinit
def untrust(signing: bool, *keys):
    """Delete known keys.

    Args:
        signing: if True deletes the secret keys
        *keys: keys to be deleted
    """
    assert GPG
    if signing:
        skeys = [str(k) for k in signing_keys(*keys)]
        GPG("--batch", "--yes", "--delete-secret-keys", *skeys)

    pkeys = [str(k) for k in public_keys(*keys)]
    GPG("--batch", "--yes", "--delete-keys", *pkeys)


@_autoinit
def sign(key: str, file: str, output: str, clearsign: bool = False):
    """Sign a file with a key.

    Args:
        key: key to be used to sign
        file: file to be signed
        output: output file (either the clearsigned file or
            the detached signature)
        clearsign: if True wraps the document in an ASCII-armored
            signature, if False creates a detached signature
    """
    assert GPG
    signopt = "--clearsign" if clearsign else "--detach-sign"
    GPG(signopt, "--armor", "--local-user", key, "--output", output, file)


@_autoinit
def verify(signature: str, file: Optional[str] = None, suppress_warnings: bool = False):
    """Verify the signature on a file.

    Args:
        signature: signature of the file (or clearsigned file)
        file: file to be verified.  If None, then signature is
            assumed to be a clearsigned file.
        suppress_warnings: whether or not to suppress warnings
            from GnuPG
    """
    assert GPG
    args = [signature]
    if file:
        args.append(file)
    kwargs = {"error": str} if suppress_warnings else {}
    GPG("--verify", *args, **kwargs)


@_autoinit
def list(trusted: bool, signing: bool):
    """List known keys.

    Args:
        trusted: if True list public keys
        signing: if True list private keys
    """
    assert GPG
    if trusted:
        GPG("--list-public-keys")

    if signing:
        GPG("--list-secret-keys")


def _verify_exe_or_raise(exe):
    msg = (
        "Spack requires gpgconf version >= 2\n"
        "  To install a suitable version using Spack, run\n"
        "    spack install gnupg@2:\n"
        "  and load it by running\n"
        "    spack load gnupg@2:"
    )
    if not exe:
        raise SpackGPGError(msg)

    output = exe("--version", output=str)
    match = re.search(r"^gpg(conf)? \(GnuPG(?:/MacGPG2)?\) (.*)$", output, re.M)
    if not match:
        raise SpackGPGError('Could not determine "{0}" version'.format(exe.name))

    if spack.version.Version(match.group(2)) < spack.version.Version("2"):
        raise SpackGPGError(msg)


def _gpgconf():
    exe = spack.util.executable.which("gpgconf", "gpg2conf", "gpgconf2")
    _verify_exe_or_raise(exe)

    # ensure that the gpgconf we found can run "gpgconf --create-socketdir"
    try:
        exe("--dry-run", "--create-socketdir", output=os.devnull, error=os.devnull)
    except spack.util.executable.ProcessError:
        # no dice
        exe = None

    return exe


def _gpg():
    exe = spack.util.executable.which("gpg2", "gpg")
    _verify_exe_or_raise(exe)
    return exe


def _socket_dir(gpgconf):
    # Try to ensure that (/var)/run/user/$(id -u) exists so that
    # `gpgconf --create-socketdir` can be run later.
    #
    # NOTE(opadron): This action helps prevent a large class of
    #                "file-name-too-long" errors in gpg.

    # If there is no suitable gpgconf, don't even bother trying to
    # pre-create a user run dir.
    if not gpgconf:
        return None

    result = None
    for var_run in ("/run", "/var/run"):
        if not os.path.exists(var_run):
            continue

        var_run_user = os.path.join(var_run, "user")
        try:
            if not os.path.exists(var_run_user):
                os.mkdir(var_run_user)
                os.chmod(var_run_user, 0o777)

            user_dir = os.path.join(var_run_user, str(spack.llnl.util.filesystem.getuid()))

            if not os.path.exists(user_dir):
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
