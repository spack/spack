# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RManipulatewidget(RPackage):
    """Like package 'manipulate' does for static graphics, this package helps
       to easily add controls like sliders, pickers, checkboxes, etc. that can
       be used to modify the input data or the parameters of an interactive
       chart created with package 'htmlwidgets'."""

    homepage = "https://github.com/rte-antares-rpackage/manipulateWidget"
    url      = "https://cloud.r-project.org/src/contrib/manipulateWidget_0.10.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/manipulateWidget/"

    version('0.10.0', sha256='3d61a3d0cedf5c8a850a3e62ed6af38c600dc3f25b44c4ff07a5093bf9ca4ffd')

    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-codetools', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-miniui', type=('build', 'run'))
    depends_on('r-shiny@1.0.3:', type=('build', 'run'))
    depends_on('r-webshot', type=('build', 'run'))
