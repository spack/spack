# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNum2words(PythonPackage):
    """Modules to convert numbers to words. Easily extensible."""

    homepage = "https://github.com/savoirfairelinux/num2words"
    pypi = "num2words/num2words-0.5.10.tar.gz"

    license("LGPL-2.1-or-later")

    version(
        "0.5.12",
        sha256="9eeef488658226ab36818c06d7aeb956d19b530fb62030596b6802fb4659f30e",
        url="https://pypi.org/packages/eb/09/b14d798bc02411b1e5a9896d680f8f417cadc53232bbf7ae9d30263dcf45/num2words-0.5.12-py3-none-any.whl",
    )
    version(
        "0.5.10",
        sha256="0b6e5f53f11d3005787e206d9c03382f459ef048a43c544e3db3b1e05a961548",
        url="https://pypi.org/packages/eb/a2/ea800689730732e27711c41beed4b2a129b34974435bdc450377ec407738/num2words-0.5.10-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-docopt@0.6.2:", when="@0.5.8:")
