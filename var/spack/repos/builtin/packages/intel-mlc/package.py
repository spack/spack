# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob
import os

from spack.package import *


class IntelMlc(Package):
    """Intel® Memory Latency Checker (Intel® MLC) is a tool used to measure
    memory latencies and b/w, and how they change with increasing load on the
    system. It also provides several options for more fine-grained
    investigation where b/w and latencies from a specific set of cores to
    caches or memory can be measured as well."""

    homepage = "https://www.intel.com/content/www/us/en/developer/articles/tool/intelr-memory-latency-checker.html"

    version(
        "3.11b",
        url="https://downloadmirror.intel.com/834254/mlc_v3.11b.tgz",
        sha256="5d5abd27d145af59d564c9c53938301a08205f075b9bd41f2f92b4c8efeb2824",
        preferred=True,
    )

    version(
        "3.11a",
        url="https://downloadmirror.intel.com/822971/mlc_v3.11a.tgz",
        sha256="e5fe60c370962a22028e3da4d6e093fde232f92f06aa217e0eac602533d94ef1",
    )

    version(
        "3.11",
        url="https://downloadmirror.intel.com/793041/mlc_v3.11.tgz",
        sha256="e34d246a52a1d2d4461dc156e073b81fa142d30fde172ca412eb77ad73376cf5",
    )

    version(
        "3.10",
        url="https://downloadmirror.intel.com/763324/mlc_v3.10.tgz",
        sha256="39bdc467d134ed43561e622efe664d62cdee147bf87bf3090f2a56f86313d789",
    )

    version(
        "3.9a",
        url="https://downloadmirror.intel.com/736634/mlc_v3.9a.tgz",
        sha256="1036b9579eaa08f431802bb879d7588960eb93bbe4612d238ac9c6d34e0bfa34",
    )

    license_url = "https://www.intel.com/content/www/us/en/download/736633/intel-memory-latency-checker-intel-mlc.html"

    variant(
        "license-agreed",
        default=False,
        sticky=True,
        description="Confirm acceptance of the EULA presented after "
        f"clicking download at ({license_url})",
    )

    conflicts(
        "~license-agreed",
        msg=(
            f"Installation of intel-mlc requires accptance of the EULA found at {license_url}. "
            f"Set the +license-agreed variant to confirm acceptance of the agreement."
        ),
    )

    @run_before("install")
    def license_reminder(self):
        if self.spec.satisfies("+license-agreed"):
            tty.msg(
                "Reminder: by setting +license-agreed you are confirming you agree to the terms "
                "of the {0} EULA (found at {1})".format(self.spec.name, self.license_url),
                "After installation, the EULA text will be placed "
                "in the package's share directory",
            )
        else:
            # Conflict means we should never get here...
            msg = (
                "Installation of {0} requires acceptance of the EULA (found at {1}). Set the "
                "+license-agreed variant to confirm acceptance of the EULA"
            ).format(self.spec.name, self.license_url)
            raise InstallError(msg)

    def install(self, spec, prefix):
        mkdirp(prefix.share)
        mkdirp(prefix.bin)

        file_list = glob.glob(os.path.join(self.stage.source_path, "*"))

        for file_path in file_list:
            if os.path.isfile(file_path):
                file_name = os.path.basename(file_path)
                install(file_path, os.path.join(prefix.share, file_name))

        if self.spec.satisfies("platform=windows"):
            install_tree(os.path.join(self.stage.source_path, "Windows"), prefix.bin)
        else:
            install_tree(os.path.join(self.stage.source_path, "Linux"), prefix.bin)
