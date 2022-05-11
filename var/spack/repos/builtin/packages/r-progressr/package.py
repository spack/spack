# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RProgressr(RPackage):
    """An Inclusive, Unifying API for Progress Updates.

    A minimal, unifying API for scripts and packages to report progress updates
    from anywhere including when using parallel processing. The package is
    designed such that the developer can to focus on what progress should be
    reported on without having to worry about how to present it. The end user
    has full control of how, where, and when to render these progress updates,
    e.g. in the terminal using utils::txtProgressBar() or
    progress::progress_bar(), in a graphical user interface using
    utils::winProgressBar(), tcltk::tkProgressBar() or shiny::withProgress(),
    via the speakers using beep::beepr(), or on a file system via the size of a
    file. Anyone can add additional, customized, progression handlers. The
    'progressr' package uses R's condition framework for signaling progress
    updated. Because of this, progress can be reported from almost anywhere in
    R, e.g. from classical for and while loops, from map-reduce API:s like the
    lapply() family of functions, 'purrr', 'plyr', and 'foreach'. It will also
    work with parallel processing via the 'future' framework, e.g.
    future.apply::future_lapply(), furrr::future_map(), and 'foreach' with
    'doFuture'. The package is compatible with Shiny applications."""

    cran = "progressr"

    version('0.10.0', sha256='4c95dc11c50c792440fa17f4538d59f1f3012bf6ef462a5a141609f87319badc')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
