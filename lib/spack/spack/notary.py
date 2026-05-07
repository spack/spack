import abc
import os
import pathlib
import warnings
from typing import List, Optional, Tuple, Union

import spack.config
import spack.error
import spack.util.executable
import spack.util.gpg
from spack.mirrors.mirror import Mirror


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
        self, blob: Union[str, pathlib.Path], signature: Optional[Union[str, pathlib.Path]]
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
    def is_signing(cls):
        return True

    @property
    def is_validating(cls):
        return True


class NonSigningNotary(Notary):
    def sign(self, blob: Union[str, pathlib.Path]) -> Tuple[pathlib.Path, pathlib.Path]:
        """Sign a blob

        Args:
            blob: Path to blob to sign

        Returns:
            Path to original blob and the to the signature
        """
        return blob, blob

    def verify(
        self, blob: Union[str, pathlib.Path], signature: Optional[Union[str, pathlib.Path]]
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
    def is_signing(cls):
        return False

    @property
    def is_validating(cls):
        return False


class GpgNotary(Notary):
    """Verify and sign GPG signatures using a specific key"""

    def __init__(self, gpg, key: str, signature_type: spack.util.gpg.Signature):
        self.gpg = gpg
        self.key = key
        self.cleartext = signature_type == spack.util.gpg.Signature.Cleartext

    def sign(self, blob: Union[str, pathlib.Path]) -> Tuple[pathlib.Path, pathlib.Path]:
        """Sign a blob

        Args:
            blob: Path to blob to sign

        Returns:
            Path to original blob and the to the signature. If they are the same path,
            then then signature wraps the original blob content (cleartext).
        """
        signed_file_path = f"{blob}.asc"
        signopt = "--clearsign" if self.cleartext else "--detach-sign"
        self.gpg(signopt, "--armor", "--local-user", self.key, "--output", signed_file_path, blob)
        if not self.cleartext:
            return blob, signed_file_path
        return signed_file_path, signed_file_path

    def verify(
        self,
        blob: Union[str, pathlib.Path],
        signature: Optional[Union[str, pathlib.Path]] = None,
        output: Optional[pathlib.Path] = None,
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

        keys = spack.util.gpg.public_keys(*(keys or ()))
        files = [os.path.join(tmpdir, f"{key}.pub") for key in keys]

        for key, file in zip(keys, files):
            spack.util.gpg.export_keys(file, [key])

        return zip(keys, files)


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

    # This calls spack.util.gpg.init
    keys = spack.util.gpg.signing_keys()
    num = len(keys)
    if not key:
        if num > 1:
            raise PickKeyException(str(keys))
        elif num == 0:
            raise NoKeyException(
                "No keys available for signing.\n"
                "Use spack gpg init and spack gpg create"
                " to create a default key."
            )
    elif key not in keys:
        raise NoKeyException(f"Could not find specified key {key} in keyring.")

    # Assumes the gpg state is initialized.
    # TODO: Don't rely on global state
    return GpgNotary(spack.util.gpg.GPG, key or keys[0], mirror.signing_type)


class PickKeyException(spack.error.SpackError):
    """Raised when multiple keys can be used to sign."""

    def __init__(self, keys):
        err_msg = "Multiple keys available for signing\n%s\n" % keys
        err_msg += "Use spack buildcache create -k <key hash> to pick a key."
        super().__init__(err_msg)


class NoKeyException(spack.error.SpackError):
    """Raised when gpg has no to key added."""
