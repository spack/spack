# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyCmyt(PythonPackage):
    """Matplotlib colormaps from the yt project !"""
    homepage = "https://yt-project.org"
    url      = "https://github.com/yt-project/cmyt/archive/v1.0.4.tar.gz"
    git      = "https://github.com/yt-project/cmyt.git"

    maintainers = ['qobilidop', 'charmoniumq']

    version("develop", branch="main")

    version("1.0.4", "c833ed24eadca8c788e59ce27119d26b2e7d4c6af83293e69385412629294b2a")
    version("1.0.3", "7d071f86cd9e53ab4f2af9f1b6539d632f52c0d453caf93a80376105ac351556")
    version("1.0.2", "4cf2e5f06031141e03ab9301a66c99be024a1a8c35ed99d1a88a24baf754234e")
    version("1.0.1", "c20ec811c0cd71ffb3482e0d269bd22e0f088a3187dd615c59edf348cbefded1")
    version("1.0.0", "64751ecd5916efe817beb92d0b5b34b0dc134c8ee0dab3f212cb089b6b78bbd4")

    depends_on("py-colorspacious@1.1.2:")
    depends_on("py-matplotlib@2.1.0:")
    depends_on("py-more-itertools@8.4.0:")
    depends_on("py-numpy@1.13.3:")
    depends_on("py-typing-extensions@3.10.0.2:", when="^python@:3.8")
    # python_version < "3.8"
