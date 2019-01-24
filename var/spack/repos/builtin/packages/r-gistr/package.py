# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RGistr(RPackage):
    """Work with 'GitHub' 'gists' from 'R'. This package allows the user to
    create new 'gists', update 'gists' with new files, rename files, delete
    files, get and delete 'gists', star and 'un-star' 'gists', fork 'gists',
    open a 'gist' in your default browser, get embed code for a 'gist', list
    'gist' 'commits', and get rate limit information when 'authenticated'. Some
    requests require authentication and some do not."""

    homepage = "https://github.com/ropensci/gistr"
    url      = "https://cran.r-project.org/src/contrib/gistr_0.3.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/gistr"

    version('0.3.6', '49d548cb3eca0e66711aece37757a2c0')

    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-rmarkdown', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
