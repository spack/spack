import abc
import os
import pathlib
import warnings
from typing import List, Optional, Tuple, Union

import spack.config
import spack.error
import spack.oci.image
import spack.util.executable
import spack.util.gpg
from spack.mirrors.mirror import Mirror


def _raise_no_signing_keys():
    """Helper function to raise a consistent error when
    there are no default signing keys available"""
    raise NoKeyException(
        "No keys available for signing.\n"
        "Use spack gpg init and spack gpg create to create a default key."
    )


class Notary(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def sign(self, blob: Union[str, pathlib.Path]) -> Tuple[pathlib.Path, pathlib.Path]:
        """Sign a blob

        Args:
            blob: Path to blob to sign

        Returns:
            Path to original blob and the to the signature
        """
        pass

    @abc.abstractmethod
    def verify(
        self, blob: Union[str, pathlib.Path], signature: Optional[Union[str, pathlib.Path]] = None
    ) -> bool:
        """Verify the signature is valid for the blob

        Args:
            blob: Path to blob to validate
            signature: (optional) signature of the blob. If not provided, the blob is assumed to
                       also be the signature

        Returns:
            Boolean denoting if blob is valid and path to file with any signature data attached
        """
        pass

    @abc.abstractmethod
    def get_keys(self, *keys, tmpdir=None) -> List[Tuple[str, pathlib.Path]]:
        """Return list of public key names to key files.

        Args:
            keys: list of specific keys to list if they exist
            tmpdir: (optional) Root directory to place key files
        """
        pass

    @property
    def is_signing(self):
        return True

    @property
    def is_validating(self):
        return True


class NonSigningNotary(Notary):
    def sign(self, blob: Union[str, pathlib.Path]) -> Tuple[pathlib.Path, pathlib.Path]:
        """Sign a blob

        Args:
            blob: Path to blob to sign

        Returns:
            Path to original blob and the to the signature
        """
        return pathlib.Path(blob), pathlib.Path(blob)

    def verify(
        self, blob: Union[str, pathlib.Path], signature: Optional[Union[str, pathlib.Path]] = None
    ) -> bool:
        """Verify the signature is valid for the blob

        Args:
            blob: Path to blob to validate
            signature: (optional) signature of the blob. If not provided, the blob is assumed to
                       also be the signature

        Returns:
            Boolean denoting if blob is valid and path to file with any signature data attached
        """
        return True

    def get_keys(self, *keys, tmpdir=None) -> List[Tuple[str, pathlib.Path]]:
        """Return list of public key names to key files.

        Args:
            keys: list of specific keys to list if they exist
            tmpdir: (optional) Root directory to place key files
        """
        return []

    @property
    def is_signing(self):
        return False

    @property
    def is_validating(self):
        return False


class GpgNotary(Notary):
    """Verify and sign GPG signatures using a specific key"""

    def __init__(self, gpg, key: Optional[str] = None, signature_type: Optional[str] = None):
        self.gpg = gpg
        self.key = key
        self.cleartext = signature_type == "pgp-cleartext"

    @property
    def _signing_key(self):
        if self.key:
            return self.key

        # Fallback here to get the first private key in the keyring
        # TODO: Don't use the global state, use the passed gpg
        keys: List[str] = spack.util.gpg.signing_keys()
        if not keys:
            _raise_no_signing_keys()
        self.key = keys[0]

        return self.key

    def sign(self, blob: Union[str, pathlib.Path]) -> Tuple[pathlib.Path, pathlib.Path]:
        """Sign a blob

        Args:
            blob: Path to blob to sign

        Returns:
            Path to original blob and the to the signature. If they are the same path,
            then then signature wraps the original blob content (cleartext).
        """
        signed_file_path = pathlib.Path(f"{blob}.asc")
        signopt = "--clearsign" if self.cleartext else "--detach-sign"
        self.gpg(
            signopt,
            "--armor",
            "--local-user",
            self._signing_key,
            "--output",
            str(signed_file_path),
            str(blob),
        )
        if not self.cleartext:
            return pathlib.Path(blob), signed_file_path
        return signed_file_path, signed_file_path

    def verify(
        self, blob: Union[str, pathlib.Path], signature: Optional[Union[str, pathlib.Path]] = None
    ) -> bool:
        """Verify the signature is valid for the blob

        Args:
            blob: Path to blob to validate
            signature: (optional) signature of the blob. If not provided, the blob is assumed to
                                  also contain the signature (cleartext)

        Returns:
            Boolean denoting if blob is valid
        """
        args = [signature or blob]
        if signature:
            args.append(blob)
        suppress_warnings = spack.config.get("config:suppress_gpg_warnings", False)
        kwargs = {"error": str} if suppress_warnings else {}
        try:
            self.gpg("--verify", *args, **kwargs)
        except spack.util.executable.ProcessError:
            return False
        return True

    def get_keys(self, *keys, tmpdir=None) -> List[Tuple[str, pathlib.Path]]:
        """Return list of public key names to key files.

        Args:
            keys: list of specific keys to list if they exist
            tmpdir: Root directory to place key files
        """

        if tmpdir is None:
            tmpdir = os.getcwd()

        keys: List[str] = spack.util.gpg.public_keys(*(keys or ()))
        files = [pathlib.Path(os.path.join(tmpdir, f"{key}.pub")) for key in keys]

        for key, file in zip(keys, files):
            spack.util.gpg.export_keys(str(file), [key])

        return list(zip(keys, files))

    @property
    def is_signing(self):
        # Attempt to load the Gpg signing key to ensure that this notary
        # can actual sign things
        _ = self._signing_key
        return True


def select_notary(
    mirror: Mirror, key: Optional[str] = None, signed: Optional[bool] = None
) -> Notary:
    """Select the correct notary for a mirror

    Args:
        mirror: Mirror to configure notary for
        key: Specific key name/id to use for the notary
    """
    if signed is None and key is None:
        signed = mirror.signed
    else:
        signed = bool(key or signed)

    if not signed:
        return NonSigningNotary()

    if spack.oci.image.is_oci_url(mirror.push_url):
        warnings.warn(
            "Code signing is currently not supported for OCI images. "
            "Specify unsigned to silence this warning."
        )

    # Attempt to get a list of signing keys.
    # If there are none, then fall back to a list of None and defer the error
    # to the call point of Notary::sign to allow for verify
    keys: List[str] = spack.util.gpg.signing_keys() or [None]
    num = len(keys)
    if not key:
        if num > 1:
            raise PickKeyException(str(keys))
    elif key not in keys:
        raise NoKeyException(f"Could not find specified key {key} in keyring.")

    # Assumes the gpg state is initialized.
    # TODO: Don't rely on global state
    return GpgNotary(spack.util.gpg.GPG, key or keys[0], mirror.signing_type or "pgp-clearsign")


class PickKeyException(spack.error.SpackError):
    """Raised when multiple keys can be used to sign."""

    def __init__(self, keys):
        err_msg = "Multiple keys available for signing\n%s\n" % keys
        err_msg += "Use spack buildcache create -k <key hash> to pick a key."
        super().__init__(err_msg)


class NoKeyException(spack.error.SpackError):
    """Raised when gpg has no to key added."""
