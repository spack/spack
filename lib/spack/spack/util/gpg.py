# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib
import datetime
import enum
import errno
import functools
import os
import pathlib
import re
import sys
import warnings
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import spack.error
import spack.llnl.util.filesystem
import spack.llnl.util.tty as tty
import spack.paths
import spack.util.executable
import spack.util.spack_json as sjson
import spack.version
from spack.util.executable import Executable

GPG_NAMES = ("gpg", "gpg2")
GPGCONF_NAMES = ("gpgconf", "gpg2conf", "gpgconf2")

#: Executable instance for "gpg", initialized lazily
GPG: Optional["Gpg"] = None
#: Executable instance for "gpgconf", initialized lazily
GPGCONF: Optional[Executable] = None
#: Socket directory required if a non default home directory is used
SOCKET_DIR = None
#: GNUPGHOME environment variable in the context of this Python module
GNUPGHOME = None

#: Regular expression to pull spec contents out of clearsigned signature
#: file.
CLEARSIGN_FILE_REGEX = re.compile(
    (
        r"^-----BEGIN PGP SIGNED MESSAGE-----"
        r"\s+Hash:\s+[^\s]+\s+(.+)-----BEGIN PGP SIGNATURE-----"
    ),
    re.MULTILINE | re.DOTALL,
)

#: PGP cleartext signature header
PGP_CLEARSIG_HEADER = "-----BEGIN PGP SIGNED MESSAGE-----"


def is_clearsig(data: str) -> bool:
    """Check if data is wrapped in a cleartext signature"""
    return data.startswith(PGP_CLEARSIG_HEADER)


def extract_data_from_clearsig(data: str) -> str:
    """Extract data from a gpg cleartext signed file"""
    m = CLEARSIGN_FILE_REGEX.search(data)
    if m:
        return m.group(1)
    return data


def extract_json_from_clearsig(data) -> Dict[Any, Any]:
    """Extract data from a gpg cleartext signed file as json"""
    return sjson.load(extract_data_from_clearsig(data))


#:
_GPG_FIELD_MAP = [
    "type",
    "trust",
    "len",
    "key_algo",
    "key_id",
    "created_at",
    "expires_at",
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
            if value.lower() == cap.value.lower():
                return cap
        return GpgKeyCapability.UNKNOWN


class GpgKeyTrust(enum.Enum):
    """Gpg Trust normalized for Field 1 and Field 9"""

    UNKNOWN = "-"  # also o or i
    EXPIRED = "e"
    UNDEFINED = "q"
    NEVER = "n"
    MARGINAL = "m"
    FULL = "f"
    ULTIMATE = "u"
    REVOKED = "r"
    ERROR = "?"
    KNOWN = "w"
    SPECIAL = "s"

    @classmethod
    def _missing_(cls, value):

        if isinstance(value, str):
            value = value.lower()

            # If it is not found, then it is unknown
            if value in ("o", "i"):
                return GpgKeyTrust.UNKNOWN

            value_to_trust = dict([(t.value, t) for t in GpgKeyTrust])
            return value_to_trust.get(value, GpgKeyTrust.ERROR)

        if isinstance(value, int):
            try:
                return list(GpgKeyTrust)[:8][value]
            except IndexError:
                return GpgKeyTrust.ERROR

    @property
    def ownertrust(self) -> int:
        """Return the ownertrust file integer corresponding to the GpgKeyTrust"""
        try:
            return list(GpgKeyTrust)[:8].index(self)
        except ValueError:
            return 8  # GpgKeyTrust.ERROR


class GpgKeyAlgorithm(enum.Enum):
    """Gpg Algormithms

    ref. https://www.iana.org/assignments/openpgp/openpgp.xhtml#openpgp-public-key-algorithms
    """

    RSA = 1
    RSA_SO = 2
    RSA_EO = 3
    ELGAMAL_EO = 16
    DSA = 17
    EC = 18
    ECDSA = 19
    ELGAMAL = 20
    DH = 21
    EDDSA = 22
    X25519 = 25
    X448 = 26
    ED25519 = 27
    ED448 = 28
    ML_DSA_65 = 30
    ML_DSA_87 = 31
    SLH_DSA_SHAKE_128S = 32
    SLH_DSA_SHAKE_128F = 33
    SLH_DSA_SHAKE_256S = 34
    ML_KEM_786 = 35
    ML_KEM_1024 = 36
    # Note: 255 is currently unassigned
    # use it as a catch all for anything not listed
    UNKNOWN = 255
    LIBGCRYPT = 256

    @classmethod
    def _missing_(cls, value):
        if not isinstance(value, int):
            raise ValueError(
                "GpgKeyAlgorithm can only be constructed from another Enum or an `int`"
            )

        if value > 255:
            return GpgKeyAlgorithm.LIBGCRYPT
        else:  # value < 255
            return GpgKeyAlgorithm.UNKNOWN

    def __str__(cls):
        name = cls.name.lower()
        name = name.replace("_so", " (Signing only)")
        name = name.replace("_eo", " (Encryption only)")
        return name

    def __format__(cls, fspec):
        """Format type with length
        ex.
            gpg_algo = GpgKeyAlgorithm.RSA
            gpg_len = 2046
            f"{gpg_algo:{gpg_len}}" -> "rsa 2046"

            f"{gpg_algo}" -> "rsa"
        """
        # Only allow integer sizes
        name = cls.name.lower()
        if fspec:
            fspec = int(fspec)
            name += f" {fspec}"

        name = name.replace("_so", " (Signing only)")
        name = name.replace("_eo", " (Encryption only)")
        return name


class GpgKeyCompliance(enum.Enum):
    """Gpg compliance codes"""

    RFC4880BIS = 8
    DE_VS = 23
    DE_VS_EXP = 2023
    VULN = 6001
    UNKNOWN = 0


class GpgKeyType(enum.Flag):
    """Gpg Key types"""

    PUBLIC = enum.auto()
    SUBKEY = enum.auto()
    SECRET = enum.auto()
    REVOCATION = enum.auto()

    SECRET_SUBKEY_ONLY = enum.auto()

    PUBLIC_SUBKEY = PUBLIC | SUBKEY
    SECRET_SUBKEY = SECRET | SUBKEY

    @classmethod
    def _missing_(cls, value):
        kname = value.strip().lower()
        if kname == "pub":
            return GpgKeyType.PUBLIC
        if kname == "sub":
            return GpgKeyType.PUBLIC_SUBKEY
        if kname == "sec":
            return GpgKeyType.SECRET
        if kname == "sec#":
            return GpgKeyType.SECRET_SUBKEY_ONLY
        if kname == "ssb":
            return GpgKeyType.SECRET_SUBKEY
        if kname == "rvk":
            return GpgKeyType.REVOCATION
        return None

    def __str__(self):
        if self == GpgKeyType.PUBLIC:
            return "pub"
        if self == GpgKeyType.PUBLIC_SUBKEY:
            return "sub"
        if self == GpgKeyType.SECRET:
            return "sec"
        if self == GpgKeyType.SECRET_SUBKEY_ONLY:
            return "sec#"
        if self == GpgKeyType.SECRET_SUBKEY:
            return "ssb"
        if self == GpgKeyType.REVOCATION:
            return "rvk"

        return self.name


class GpgSigType(enum.Enum):
    """Gpg Key signature types"""

    SIGNATURE = "sig"
    REVOCATION = "rev"
    REVOCATION_SO = "rvs"


class GpgUserId:
    def __init__(self, data: Dict[str, str]):
        assert data["type"] in ("uid", "uat")

        self.type = data["type"]
        self.trust = GpgKeyTrust(data.get("trust", ""))
        if "created_at" not in data:
            warnings.warn("GPG Key User ID has no creation date")
            self.created_at = None
        else:
            self.created_at = datetime.datetime.fromtimestamp(int(data["created_at"]))
        self.hash = data.get("misc", "")
        self.uid = data["uid"]
        self.origin = data.get("origin")

    def _format_colons(self) -> str:
        data: Dict[str, Any] = {}
        data["type"] = self.type
        data["trust"] = self.trust.value
        if self.created_at:
            data["created_at"] = int(self.created_at.timestamp())
        data["misc"] = self.hash
        data["uid"] = self.uid
        data["origin"] = self.origin or ""

        return ":".join([str(data.get(f, "")) for f in _GPG_FIELD_MAP])


class GpgSignature:
    def __init__(self, data: Dict[str, str]):
        self.type = GpgSigType(data["type"])
        self.algo = GpgKeyAlgorithm(int(data["key_algo"]))
        self.id = data["key_id"]
        self.created_at = datetime.datetime.fromtimestamp(int(data["created_at"]))
        self.uid = data["uid"]
        self.sig_class = data["sig_class"]

    def _format_colons(self) -> str:
        data: Dict[str, Any] = {}
        data["type"] = self.type.value
        data["key_algo"] = self.algo.value
        data["key_id"] = self.id
        data["created_at"] = int(self.created_at.timestamp())
        data["uid"] = self.uid
        data["sig_class"] = self.sig_class
        return ":".join([str(data.get(f, "")) for f in _GPG_FIELD_MAP])


class GpgKey:
    def __init__(self, data: Dict[str, str]):
        assert data["type"] in ("pub", "sec", "sec#", "sub", "ssb")

        self.type = GpgKeyType(data["type"])

        self.trust = GpgKeyTrust(data.get("trust", ""))
        self.key_len = data["len"]
        self.key_algorithm = GpgKeyAlgorithm(int(data["key_algo"]))
        self.key_id = data["key_id"]
        self.created_at = datetime.datetime.fromtimestamp(int(data["created_at"]))
        self.expires_at: Optional[datetime.datetime] = None
        if data.get("expires_at"):
            self.expires_at = datetime.datetime.fromtimestamp(int(data["expires_at"]))

        self.owner_trust = GpgKeyTrust(data.get("owner_trust", ""))

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

    def _format_colons(self) -> List[str]:
        data: Dict[str, Any] = {}
        data["type"] = self.type
        data["trust"] = self.trust.value

        data["len"] = self.key_len
        data["key_algo"] = self.key_algorithm.value
        data["key_id"] = self.key_id
        data["created_at"] = int(self.created_at.timestamp())
        if self.expires_at:
            data["expires_at"] = int(self.expires_at.timestamp())
        if self.updated_at:
            data["updated_at"] = int(self.updated_at.timestamp())

        data["owner_trust"] = self.owner_trust.value
        cap_list = set()
        if self.subkey:
            cap_list.update([c.value.upper() for c in self.capabilities])
            for k in self.subkey:
                cap_list.update([c.value.lower() for c in k.capabilities])
        else:
            cap_list.update([c.value.lower() for c in self.capabilities])
        data["capabilities"] = "".join(sorted(cap_list))

        data["compliance"] = self.compliance.value

        data["origin"] = self.origin or ""
        data["comment"] = self.comment

        colons = []
        nkey_fields = len(_GPG_FIELD_MAP)
        if self.type.value & GpgKeyType.SUBKEY.value:
            nkey_fields -= 3
        colons.append(":".join([str(data.get(f, "")) for f in _GPG_FIELD_MAP[: nkey_fields + 1]]))

        if self.fpr:
            fpr_data = {}
            fpr_data["type"] = "fpr"
            fpr_data["uid"] = self.fpr
            colons.append(":".join([str(fpr_data.get(f, "")) for f in _GPG_FIELD_MAP[:11]]))

        for u in self.uid:
            colons.append(u._format_colons())

        for s in self.sig:
            colons.append(s._format_colons())

        for r in self.rev:
            colons.append(r._format_colons())

        for k in self.subkey:
            colons.extend(k._format_colons())

        return colons

    def __format__(self, fspec):
        """Formatted output for GPG key

        Default:
            <fingerprint>

        c[olons] - Output everything using a gpg style colon format ie.
        s[hort] - Shortened output ie. <fingerprint> (<uid>)
        f[pr] - Fingerprint only output ie. <fingerprint>
        """

        if fspec.startswith("s"):
            return f"{self.fpr} ({self.uid[0].uid})"
        elif fspec.startswith("f"):
            return self.fpr
        elif fspec.startswith("c"):
            return "\n".join(self._format_colons())
        else:
            return str(self)


class Gpg:
    """Wrapper for GPG"""

    def __init__(self, gnupghome: Optional[str] = None):
        if sys.platform == "win32":
            self.home = Gpg._init_gnupghome_dir(gnupghome)
        else:
            self.home = Gpg._init_gnupghome_posix(gnupghome)

        self._gpg: Optional[Executable] = None
        self._gpgconf: Optional[Executable] = None
        self._version: Optional[spack.version.VersionType] = None
        self._socket_dir: Optional[pathlib.Path] = None

    @staticmethod
    def _init_gnupghome_dir(gnupghome: Optional[str] = None) -> pathlib.Path:
        """Init gnupg home but don't check permissions"""
        # Make sure that the gnupghome exists
        gnupghome = gnupghome or os.getenv("SPACK_GNUPGHOME") or spack.paths.gpg_path
        if not os.path.exists(gnupghome):
            os.makedirs(gnupghome)
            os.chmod(gnupghome, 0o700)

        if not os.path.isdir(gnupghome):
            msg = 'gnupghome "{0}" exists and is not a directory'.format(gnupghome)
            raise SpackGPGError(msg)

        if not os.access(gnupghome, os.R_OK | os.W_OK | os.X_OK):
            msg = 'gnupghome "{0}" exists but is not accessible'.format(gnupghome)
            raise SpackGPGError(msg)

        return pathlib.Path(gnupghome)

    @staticmethod
    def _init_gnupghome_posix(gnupghome: Optional[str] = None) -> pathlib.Path:
        """Init gnupg home and check permissions."""
        gnupghome = Gpg._init_gnupghome_dir(gnupghome)

        # Ensure safe permissions on posix systems
        st = gnupghome.stat()
        if st.st_mode != (st.st_mode & 0o040700):
            os.chmod(gnupghome, 0o700)

        return gnupghome

    def _create_gpgfn(
        self, finder: Callable[..., Optional[Tuple[Executable, spack.version.VersionType]]]
    ) -> Optional[Executable]:
        """Create a GPG function wrapper"""
        import spack.bootstrap

        with spack.bootstrap.ensure_bootstrap_configuration():
            spack.bootstrap.ensure_gpg_in_path_or_raise()
            result = finder()

        if result is None:
            return None

        gpgfn, version = result

        if self._version and version != self._version:
            warnings.warn(
                "Version mismatch between gpg and gpgconf. This may lead to unexpected behavior"
            )
        else:
            self._version = version

        gpgfn.add_default_env("GNUPGHOME", str(self.home))

        return gpgfn

    @property
    def gpg(self):
        if not self._gpg:
            self._gpg = self._create_gpgfn(_gpg)
            # Ensure the GPG Socket exists
            _ = self.socket_dir

        return self._gpg

    def __call__(self, *args, **kwargs):
        return self.gpg(*args, **kwargs)

    @property
    def conf(self) -> Optional[Executable]:
        if not self._gpgconf:
            self._gpgconf = self._create_gpgfn(_gpgconf)

        return self._gpgconf

    @property
    def socket_dir(self) -> Optional[pathlib.Path]:
        if self._socket_dir:
            return self._socket_dir

        if self.conf:
            # Set the socket dir if not using GnuPG defaults
            self._socket_dir = _socket_dir(self.conf)

            if self._socket_dir is not None:
                self.conf("--create-socketdir")

        return self._socket_dir

    def list_keyfile(
        self, keyfile: str, ktype: Union[GpgKeyType, List[GpgKeyType]] = GpgKeyType.PUBLIC
    ) -> List[GpgKey]:
        """List keys in a keyfile"""
        assert self._version is not None, "GPG version is not set; ensure GPG is initialized"
        ktypes = {ktype} if isinstance(ktype, GpgKeyType) else set(ktype)

        gpg_args = ["--with-colons", "--with-fingerprint"]
        if self._version >= spack.version.Version("2.2.8"):
            gpg_args.append("--show-keys")
        elif self._version >= spack.version.Version("2.1.23"):
            gpg_args.extend(["--import-options", "show-only", "--import"])
        elif self._version >= spack.version.Version("2.1.14"):
            gpg_args.extend(["--import-options", "import-show", "--dry-run", "--import"])
        # For older versions of gpg we fall back to using keyfile as a bare positional argument.

        output = self.gpg(*gpg_args, keyfile, output=str, error=str)
        return [k for k in _parse_gpg_output(output) if k.type in ktypes]

    def _list_keys(self, *fprs, colons: bool = True, ktype: GpgKeyType = GpgKeyType.PUBLIC) -> str:
        gpg_args = []

        # Determine the list option
        if GpgKeyType.PUBLIC in ktype:
            gpg_args.append("--list-public-keys")
        elif GpgKeyType.SECRET in ktype:
            gpg_args.append("--list-secret-keys")
        else:
            gpg_args.append("--list-keys")

        # Determine output format
        # colons or a spack abbreviated format
        if colons:
            gpg_args.append("--with-colons")

        # Get list of keys from keyring
        return self.gpg(*gpg_args, *fprs, output=str)

    def keys(self, *fprs, ktype: GpgKeyType = GpgKeyType.PUBLIC) -> List[GpgKey]:
        return _parse_gpg_output(self._list_keys(*fprs, colons=True, ktype=ktype))

    def list_keys(
        self, *fprs, ktype: GpgKeyType = GpgKeyType.PUBLIC, fmt: str = ""
    ) -> Union[str, List[GpgKey]]:
        """List known keys.

        Args:
            fprs: list of key fingerprints
            ktype: Type of dey to list (default: PUBLIC)
            fmt: format to print/return keys (default: None)
                default (aka "") -> return default output from gpg
                GpgKey format string->  See GpgKey __format__
        """

        # Get list of keys from keyring
        out = self._list_keys(*fprs, colons=bool(fmt), ktype=ktype)
        if fmt:
            buffer = ""
            keys = _parse_gpg_output(out)
            for key in keys:
                buffer += f"{{key:{fmt}}}".format(key=key)
            return buffer
        else:
            return out

    def trust(
        self,
        keyfile: str,
        *,
        fprs: Optional[List[str]] = None,
        ownertrust: GpgKeyTrust = GpgKeyTrust.ULTIMATE,
        yes_to_all: bool = False,
    ):
        """Import a key from a file and trust it.

        The keyfile may contain public keys, secret keys (which embed public
        key material), or both.

        Args:
            keyfile: file with the public or secret key(s)
            fprs: list of fingerprints to trust, if provided, then yes_to_all is ignored
            ownertrust: level of trust to assign to the key(s)
            yes_to_all: trust all keys in the file if True, otherwise ask for each key
        """

        # This global method is safe to use to list keys in a file without importing them
        imported_keys = self.list_keyfile(keyfile, ktype=[GpgKeyType.PUBLIC, GpgKeyType.SECRET])
        if not imported_keys:
            tty.info(f"No keys to trust in {keyfile}")
            return

        # Import the keys from they keyfile and verify trust for all new keys after.
        # This avoids TOCTOU errors where the keyfile may change between extracting
        # the expected keys and trusting the keys.
        self.gpg("--yes", "--batch", "--import", keyfile)

        # Iterate all of the keys in the keychain and confirm trust
        for key in self.keys():
            # Skip keys we had before trusting the keys in the file
            if key not in imported_keys:
                continue
            # if fprs is provided, then only trust keys in the file with matching fingerprints
            # yes_to_all is ignored in this case
            if fprs:
                trusted = key.fpr in fprs
            else:
                trusted = yes_to_all or bool(tty.get_yes_or_no(f"Trust key: {key}", default=False))

            if not trusted:
                tty.info(f"Spack will not trust key {key}")
                self.untrust([key])
                continue

            # Update the owner trust to ultimate
            r, w = os.pipe()
            with contextlib.closing(os.fdopen(r, "r")) as rc:
                with contextlib.closing(os.fdopen(w, "w")) as wc:
                    wc.write(f"{key.fpr}:{ownertrust.ownertrust}:\n")
                self.gpg("--import-ownertrust", input=rc)

    def untrust(self, keys: List[GpgKey]):
        """Delete known keys.

        Args:
            keys: keys to be deleted
        """
        skeys = [str(k) for k in keys if GpgKeyType.SECRET in k.type]
        if skeys:
            self.gpg("--batch", "--yes", "--delete-secret-keys", *skeys)

        pkeys = [str(k) for k in keys if GpgKeyType.PUBLIC in k.type]
        if pkeys:
            self.gpg("--batch", "--yes", "--delete-keys", *pkeys)

    def verify(
        self,
        signature: Union[str, pathlib.Path],
        blob: Union[str, pathlib.Path],
        suppress_warnings: bool = False,
    ):
        """Verify the signature on a blob.

        Args:
            signature: signature file (or clearsigned file)
            blob: blob to be verified.  If None, then signature is
                assumed to be a clearsigned file.
            suppress_warnings: whether or not to suppress warnings
                from GnuPG
        """
        args = [str(signature)]
        if blob and str(blob) != str(signature):
            args.append(str(blob))
        kwargs = {"error": os.devnull} if suppress_warnings else {}
        self.gpg("--verify", *args, **kwargs)

    def sign(
        self,
        blob: Union[str, pathlib.Path],
        output: Optional[Union[str, pathlib.Path]] = None,
        key: Optional[Union[str, GpgKey]] = None,
        armor: bool = True,
        clearsign: bool = False,
    ):
        """Sign a file with a key.

        Args:
            blob: file to be signed
            output: output file (default: f"{blob}.sig")
            key: key to be used to sign (default: first secret key in keyring)
            armor: ascii armored output
            clearsign: if True wraps the document in an ASCII-armored
                signature, if False creates a detached signature
        """
        args = []
        if armor:
            args.append("--armor")

        if key:
            args.extend(["--local-user", str(key)])

        if output:
            args.extend(["--output", str(output)])

        args.append("--clearsign" if clearsign else "--detach-sign")
        self.gpg(*args, blob)

    def export_keys(self, keyfile: str, keys: List[GpgKey], ktype: GpgKeyType = GpgKeyType.PUBLIC):
        """Export public keys to a location passed as argument.

        Args:
            keyfile: where to export the keys
            keys: keys to be exported
            secret: whether to export secret keys or not
        """
        args = ["--yes", "--batch", "--armor", "--output", keyfile]

        if GpgKeyType.SECRET in ktype:
            args.append("--export-secret-keys")
        else:
            args.extend(["--export"])

        fprs = [str(k) for k in keys]
        self.gpg(*args, *fprs)


def clear():
    """Reset the global state to uninitialized."""
    global GPG, GPGCONF, SOCKET_DIR, GNUPGHOME
    GPG, GPGCONF, SOCKET_DIR, GNUPGHOME = None, None, None, None


def init(gnupghome: Optional[str] = None, force: bool = False):
    """Initialize the global state for Gpg."""
    global GPG, GPGCONF, SOCKET_DIR, GNUPGHOME

    if force:
        clear()

    if GPG and GNUPGHOME:
        return

    GPG = Gpg(gnupghome)
    GNUPGHOME, GPGCONF, SOCKET_DIR = GPG.home, GPG.conf, GPG.socket_dir


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
    _GPG = GPG

    # Reset global state
    clear()
    GPG = Gpg(gnupghome=dir)
    GNUPGHOME, GPGCONF, SOCKET_DIR = GPG.home, GPG.conf, GPG.socket_dir

    yield

    # Restore previous state
    clear()
    GPG = _GPG
    if GPG:
        GNUPGHOME, GPGCONF, SOCKET_DIR = GPG.home, GPG.conf, GPG.socket_dir


def _parse_gpg_fields(karray: List[str]):
    """Parse gpg line into a dict"""
    data = {}
    for key, value in zip(_GPG_FIELD_MAP, karray):
        if value:
            data[key] = value

    return data


def _parse_gpg_output(output: str) -> List[GpgKey]:
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
        if data["type"] in ("pub", "sec", "sec#"):
            if current_subkey:
                assert current_key
                current_key.subkey.append(current_subkey)
                current_key.subkey.sort(key=lambda k: k.created_at)
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
            # Sort subkeys by creation time, then by capability
            current_key.subkey.sort(key=lambda k: k.created_at)
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
def signing_keys(*args) -> List[GpgKey]:
    """Return the keys that can be used to sign binaries."""
    assert GPG
    return GPG.keys(*args, ktype=GpgKeyType.SECRET)


@_autoinit
def public_keys(*args) -> List[GpgKey]:
    """Return a list of fingerprints"""
    assert GPG
    return GPG.keys(*args, ktype=GpgKeyType.PUBLIC)


@_autoinit
def export_keys(location: str, keys: List[GpgKey], secret: bool = False):
    """Export public keys to a location passed as argument.

    Args:
        location: where to export the keys
        keys: keys to be exported
        secret: whether to export secret keys or not
    """
    assert GPG
    ktype = GpgKeyType.SECRET if secret else GpgKeyType.PUBLIC
    GPG.export_keys(location, keys, ktype=ktype)


@_autoinit
def extract_public_keys(keyfile: str):
    """Extract the key ids from a file

    Args:
        keyfile: file with the public key
    """
    assert GPG
    return GPG.list_keyfile(keyfile, ktype=GpgKeyType.PUBLIC)


@_autoinit
def trust(keyfile: str, *, fprs: Optional[List[str]] = None, yes_to_all: bool = False):
    """Import a public key from a file and trust it.

    Args:
        keyfile: file with the public key
        fprs: fingerprints of keys to trust.
        yes_to_all: trust all keys in the file if True, otherwise ask for each key.
                    Ignored if fprs is provided.
    """
    assert GPG
    GPG.trust(keyfile, fprs=fprs, ownertrust=GpgKeyTrust.ULTIMATE, yes_to_all=yes_to_all)


@_autoinit
def untrust(signing: bool, *keys):
    """Delete known keys.

    Args:
        signing: if True deletes the secret keys
        *keys: keys to be deleted
    """
    assert GPG
    if signing:
        GPG.untrust(GPG.keys(*keys, ktype=GpgKeyType.SECRET))

    untrust_keys = GPG.keys(*keys, ktype=GpgKeyType.PUBLIC)
    GPG.untrust(untrust_keys)


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
    GPG.sign(file, output, key, clearsign=clearsign)


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
    if not file:
        file = signature
    GPG.verify(signature, file, suppress_warnings=suppress_warnings)


@_autoinit
def glist(trusted: bool, signing: bool, fmt: str = "default"):
    """List known keys.

    Args:
        trusted: if True list public keys
        signing: if True list private keys
        fmt: Key formatting string (default, colons, short, fpr)
    """
    assert GPG

    if trusted:
        tty.msg("Trusted keys")
        print(GPG.list_keys(ktype=GpgKeyType.PUBLIC, fmt=fmt))

    if signing:
        tty.msg("Signing keys")
        print(GPG.list_keys(ktype=GpgKeyType.SECRET, fmt=fmt))


def _verify_exe_or_raise(exe) -> spack.version.VersionType:
    """Verify that the gpg executable is a new enough version."""

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

    gpg_version = spack.version.Version(match.group(2))
    if gpg_version < spack.version.Version("2"):
        raise SpackGPGError(msg)

    return gpg_version


def _gpgconf() -> Optional[Tuple[Executable, spack.version.VersionType]]:
    """Get executable for gpgconf if it exists"""
    # ensure that the gpgconf we found can run "gpgconf --create-socketdir"
    exe = spack.util.executable.which(*GPGCONF_NAMES)
    if not exe:
        return None

    try:
        version = _verify_exe_or_raise(exe)
        exe("--dry-run", "--create-socketdir", output=os.devnull, error=os.devnull)
        return exe, version
    except spack.util.executable.ProcessError:
        # no dice
        return None


def _gpg() -> Tuple[Executable, spack.version.VersionType]:
    """Get executable for gpg"""
    exe = spack.util.executable.which(*GPG_NAMES, required=True)
    version = _verify_exe_or_raise(exe)
    return exe, version


def _socket_dir(gpgconf: Optional[Executable]) -> Optional[pathlib.Path]:
    """Try to ensure that (/var)/run/user/$(id -u) exists so that
       `gpgconf --create-socketdir` can be run later.

    NOTE: This action helps prevent a large class of
                   "file-name-too-long" errors in gpg.

    If there is no suitable gpgconf, don't even bother trying to
    pre-create a user run dir.

    Returns:
        path to gpg socket directory
    """
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
        # NOTE: Without a dir in which to create a socket for IPC,
        #                gnupg may fail if GNUPGHOME is set to a path that
        #                is too long, where "too long" in this context is
        #                actually quite short; somewhere in the
        #                neighborhood of more than 100 characters.
        #
        except OSError as exc:
            if exc.errno not in (errno.EPERM, errno.EACCES):
                raise
            user_dir = None

        # return the last iteration that provides a usable user run dir
        if user_dir is not None:
            result = pathlib.Path(user_dir)

    return result
