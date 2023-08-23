# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFfmpegPython(PythonPackage):
    """Python bindings for FFmpeg - with complex filtering support"""

    homepage = "https://github.com/kkroening/ffmpeg-python"
    pypi = "ffmpeg-python/ffmpeg-python-0.2.0.tar.gz"

    version("0.2.0", sha256="65225db34627c578ef0e11c8b1eb528bb35e024752f6f10b78c011f6f64c4127")

    depends_on("ffmpeg", type="run")
