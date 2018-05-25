##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class RMlrmbo(RPackage):
    """Flexible and comprehensive R toolbox for model-based optimization
       ('MBO'), also known as Bayesian optimization. It is designed for both
       single- and multi-objective optimization with mixed continuous,
       categorical and conditional parameters. The machine learning toolbox
       'mlr' provide dozens of regression learners to model the performance of
       the target algorithm with respect to the parameter settings. It provides
       many different infill criteria to guide the search process. Additional
       features include multi-point batch proposal, parallel execution as well
       as visualization and sophisticated logging mechanisms, which is
       especially useful for teaching and understanding of algorithm behavior.
       'mlrMBO' is implemented in a modular fashion, such that single
       components can be easily replaced or adapted by the user for specific
       use cases."""

    homepage = "https://github.com/mlr-org/mlrMBO/"
    url      = "https://cran.r-project.org/src/contrib/mlrMBO_1.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mlrMBO"

    version('1.1.1', '9a35b41ceb8754111af294dee0ae76e0')
    version('1.1.0', '9e27ff8498225d24863b8da758d2918e')

    depends_on('r-mlr@2.10:', type=('build', 'run'))
    depends_on('r-paramhelpers@1.10:', type=('build', 'run'))
    depends_on('r-smoof@1.5.1:', type=('build', 'run'))
    depends_on('r-backports@1.1.0:', type=('build', 'run'))
    depends_on('r-bbmisc@1.11:', type=('build', 'run'))
    depends_on('r-checkmate@1.8.2:', type=('build', 'run'))
    depends_on('r-data-table', type=('build', 'run'))
    depends_on('r-lhs', type=('build', 'run'))
    depends_on('r-parallelmap@1.3:', type=('build', 'run'))
