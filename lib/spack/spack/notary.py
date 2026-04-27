import pathlib
from abc import abstractmethod
from typing import List, Optional, Tuple, Union

import spack.error
import spack.util.executable
import spack.util.gpg
from spack.mirrors.mirror import Mirror


class Notary:
    @abstractmethod
    def sign(self, blob: Union[str, pathlib.Path]) -> Tuple[pathlib.Path, pathlib.Path]:
        """Sign a blob

        Args:
            blob: Path to blob to sign

        Returns:
            Path to the signature and path to original blob
        """
        pass

    @abstractmethod
    def verify(
        self, blob: Union[str, pathlib.Path], signature: Optional[Union[str, pathlib.Path]]
    ) -> bool:
        """Verify the signature is valid for the blob

        Args:
            blob: Path to blob to validate
            signature: (optional) signature of the blob. If not provided, the blob is assumed to also contain the signature (cleartext)

        Returns:
            Boolean denoting if blob is valid and path to file with any signature data attached
        """
        pass

    def get_keys(self) -> List[Tuple[str, pathlib.Path]]:
        """Return list of public key names to key files"""
        pass


class GpgNotary(Notary):
    """Verify and sign GPG signatures using a specific key"""

    def __init__(self, gpg, key: str, signature_type: spack.util.gpg.Signature):
        self.gpg = gpg
        self.key = key
        self.cleartext = signature_type == spack.util.gpg.Signature.Cleartext

    @abstractmethod
    def sign(self, blob: Union[str, pathlib.Path]) -> Tuple[pathlib.Path, pathlib.Path]:
        """Sign a blob

        Args:
            blob: Path to blob to sign

        Returns:
            Path to the signature and path to original blob
        """
        signed_file_path = f"{blob}.sig"
        signopt = "--clearsign" if self.cleartext else "--detach-sign"
        self.gpg(signopt, "--armor", "--local-user", self.key, "--output", signed_file_path, blob)
        if detached:
            return blob, signed_file_path
        return signed_file_path, signed_file_path

    @abstractmethod
    def verify(
        blob: Union[str, pathlib.Path],
        signature: Optional[Union[str, pathlib.Path]] = None,
        output: Optional[pathlib.Path] = None,
    ) -> bool:
        """Verify the signature is valid for the blob

        Args:
            blob: Path to blob to validate
            signature: (optional) signature of the blob. If not provided, the blob is assumed to also contain the signature (cleartext)

        Returns:
            Boolean denoting if blob is valid
        """
        args = [signature or blob]
        if signature:
            args.append(blob)
        suppress_warnings = config.get("config:suppress_gpg_warnings", False)
        kwargs = {"error": str} if suppress_warnings else {}
        try:
            self.gpg("--verify", *args, **kwargs)
        except spack.util.executable.ProcessError:
            return False
        return True

    def get_keys(self) -> List[Tuple[str, pathlib.Path]]:
        """Return list of public key files"""

        keys = spack.util.gpg.public_keys(*(keys or ()))
        files = [os.path.join(tmpdir, f"{key}.pub") for key in keys]

        for key, file in zip(keys, files):
            spack.util.gpg.export_keys(file, [key])

        return zip(keys, files)


def select_notary(mirror: Mirror, key: Optional[str]) -> Notary:
    """Select the correct notary for a mirror

    Args:
        mirror: Mirror to configure notary for
        key: Specific key name/id to use for the notary
    """
    # This calls spack.util.gpg.init
    keys = spack.util.gpg.signing_keys()
    num = len(keys)
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
