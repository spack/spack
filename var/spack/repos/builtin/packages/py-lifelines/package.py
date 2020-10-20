# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyLifelines(PythonPackage):
    """Survival analysis was originally developed and applied heavily
    by the actuarial and medical community. Its purpose was to answer
    *why do events occur now versus later* under uncertainty (where
    *events* might refer to deaths, disease remission, etc.). This is
    great for researchers who are interested in measuring lifetimes:
    they can answer questions like *what factors might influence
    deaths?*
    But outside of medicine and actuarial science, there are many
    other interesting and exciting applications of survival
    analysis. For example:

    - SaaS providers are interested in measuring subscriber lifetimes,
      or time to some first action
    - inventory stock out is a censoring event for true "demand" of a good.
    - sociologists are interested in measuring political parties'
      lifetimes, or relationships, or marriages
    - A/B tests to determine how long it takes different groups to
      perform an action.
    *lifelines* is a pure Python implementation of the best parts of
      survival analysis."""

    homepage = "https://github.com/CamDavidsonPilon/lifelines"
    url      = "https://pypi.io/packages/source/l/lifelines/lifelines-0.9.4.tar.gz"

    version('0.9.4', sha256='0f19a8b18ace80c231de60487b2b1a3de3eb418445c6a6d0d72c1110d860f676')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.14:', type=('build', 'run'))
    depends_on('py-scipy@1.2.0:', type=('build', 'run'))
    depends_on('py-pandas@0.23.0:', type=('build', 'run'))
    depends_on('py-matplotlib@3.0:', type=('build', 'run'))
    depends_on('py-autograd@1.3:', type=('build', 'run'))
    depends_on('py-autograd-gamma@0.3:', type=('build', 'run'))
    depends_on('py-patsy@0.5.0:', type=('build', 'run'))
