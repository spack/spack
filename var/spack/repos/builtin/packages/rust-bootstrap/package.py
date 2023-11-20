# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform
import re

from spack.package import *


class RustBootstrap(Package):
    """Binary bootstrap Rust compiler."""

    homepage = "https://www.rust-lang.org"
    url = "https://static.rust-lang.org/dist/rust-1.65.0-aarch64-apple-darwin.tar.gz"

    maintainers("alecbcs")

    # List binary rust releases for multiple operating systems and architectures.
    # These binary versions are not intended to stay up-to-date. Instead we
    # should update these binary releases as bootstrapping requirements are
    # modified by new releases of Rust.
    rust_releases = {
        "1.73.0": {
            "darwin": {
                "x86_64": "ece9646bb153d4bc0f7f1443989de0cbcd8989a7d0bf3b7fb9956e1223954f0c",
                "aarch64": "9c96e4c57328fb438ee2d87aa75970ce89b4426b49780ccb3c16af0d7c617cc6",
            },
            "linux": {
                "x86_64": "aa4cf0b7e66a9f5b7c623d4b340bb1ac2864a5f2c2b981f39f796245dc84f2cb",
                "aarch64": "e54d7d886ba413ae573151f668e76ea537f9a44406d3d29598269a4a536d12f6",
                "powerpc64le": "8fa215ee3e274fb64364e7084613bc570369488fa22cf5bc8e0fe6dc810fe2b9",
            },
        },
        "1.70.0": {
            "darwin": {
                "x86_64": "e5819fdbfc7f1a4d5d82cb4c3b7662250748450b45a585433bfb75648bc45547",
                "aarch64": "75cbc356a06c9b2daf6b9249febda0f0c46df2a427f7cc8467c7edbd44636e53",
            },
            "linux": {
                "x86_64": "8499c0b034dd881cd9a880c44021632422a28dc23d7a81ca0a97b04652245982",
                "aarch64": "3aa012fc4d9d5f17ca30af41f87e1c2aacdac46b51adc5213e7614797c6fd24c",
                "powerpc64le": "ba8cb5e3078b1bc7c6b27ab53cfa3af14001728db9a047d0bdf29b8f05a4db34",
            },
        },
        "1.65.0": {
            "darwin": {
                "x86_64": "139087a3937799415fd829e5a88162a69a32c23725a44457f9c96b98e4d64a7c",
                "aarch64": "7ddc335bd10fc32d3039ef36248a5d0c4865db2437c8aad20a2428a6cf41df09",
            },
            "linux": {
                "x86_64": "8f754fdd5af783fe9020978c64e414cb45f3ad0a6f44d045219bbf2210ca3cb9",
                "aarch64": "f406136010e6a1cdce3fb6573506f00d23858af49dd20a46723c3fa5257b7796",
                "powerpc64le": "3f1d0d5bb13213348dc65e373f8c412fc0a12ee55abc1c864f7e0300932fc687",
            },
        },
        "1.60.0": {
            "darwin": {
                "x86_64": "0b10dc45cddc4d2355e38cac86d71a504327cb41d41d702d4050b9847ad4258c",
                "aarch64": "b532672c278c25683ca63d78e82bae829eea1a32308e844954fb66cfe34ad222",
            },
            "linux": {
                "x86_64": "b8a4c3959367d053825e31f90a5eb86418eb0d80cacda52bfa80b078e18150d5",
                "aarch64": "99c419c2f35d4324446481c39402c7baecd7a8baed7edca9f8d6bbd33c05550c",
                "powerpc64le": "80125e90285b214c2b1f56ab86a09c8509aa17aec9d7127960a86a7008e8f7de",
            },
        },
    }

    # Normalize architectures returned by platform to those used by the
    # Rust project.
    rust_targets = {
        "aarch64": "aarch64",
        "amd64": "x86_64",
        "arm64": "aarch64",
        "powerpc64le": "powerpc64le",
        "ppc64le": "powerpc64le",
        "x86_64": "x86_64",
    }

    # Convert operating system names into the format used for Rust
    # download server.
    rust_os = {"darwin": "apple-darwin", "linux": "unknown-linux-gnu"}

    # Determine system os and architecture/target.
    os = platform.system().lower()
    target = rust_targets.get(platform.machine().lower(), platform.machine().lower())

    # Pre-release versions of the bootstrap compiler.
    # Note: These versions are unchecksumed since they will change
    # periodically as new versions are released.
    version("beta")
    version("nightly")

    # Stable releases of the bootstrap compiler.
    # Construct releases for current system configuration.
    for release in rust_releases:
        if os in rust_releases[release] and target in rust_releases[release][os]:
            version(release, sha256=rust_releases[release][os][target])

    def url_for_version(self, version):
        # Allow maintainers to checksum multiple architectures via
        # `spack checksum rust-bootstrap@1.70.0-darwin-aarch64`.
        match = re.search(r"(\S+)-(\S+)-(\S+)", str(version))
        if match:
            version = match.group(1)
            os = self.rust_os[match.group(2)]
            target = self.rust_targets[match.group(3)]
        else:
            os = self.rust_os[self.os]
            target = self.target

        url = "https://static.rust-lang.org/dist/rust-{0}-{1}-{2}.tar.gz"
        return url.format(version, target, os)

    def install(self, spec, prefix):
        install_script = Executable("./install.sh")
        install_script(f"--prefix={prefix}")
