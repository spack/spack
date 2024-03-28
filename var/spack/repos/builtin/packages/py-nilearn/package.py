# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNilearn(PythonPackage):
    """Statistical learning for neuroimaging in Python."""

    homepage = "https://nilearn.github.io/"
    pypi = "nilearn/nilearn-0.7.1.tar.gz"
    git = "https://github.com/nilearn/nilearn"

    maintainers("ChristopherChristofi")

    license("BSD")

    version(
        "0.10.3",
        sha256="353bc3c4a73b20ade1d6a35287236c9cccd4f293f9aed75c4fc37110c02ebbb5",
        url="https://pypi.org/packages/b8/4a/27f961d8f1ebc630c0b1759a914f61b23d9e3ecdc279f3897b7eb4d6e689/nilearn-0.10.3-py3-none-any.whl",
    )
    version(
        "0.10.1",
        sha256="4528dc8c04465c0ad0d98168fc4460086ad4ea07dde789a44116d7f124b4b23d",
        url="https://pypi.org/packages/cc/cd/e83c3ec620bd0f994dbc63b9ea96c42798049f9d254fe1f9f57996741972/nilearn-0.10.1-py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="a78df43e0d9dcea18ac3bc2e56e0683c7bfd98cd2dd17e1e134f3003ce464868",
        url="https://pypi.org/packages/2c/39/ff1a661c569f01dee8a9c8a1a5887655dbaf28d14dd28e62b0d03b47baf8/nilearn-0.10.0-py3-none-any.whl",
    )
    version(
        "0.9.2",
        sha256="71b9d9a948ffb3fdb70fe7ff671fdaade436168c91f99d8b8fefa78e2ee2ee6d",
        url="https://pypi.org/packages/75/a4/2ebfe8ce00f0bab8d4c850c370c94b8f281de207b1bac5a74db76baaefe4/nilearn-0.9.2-py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="3cb16270e53f5dd50ab2979e3e98ad4fc48485284e33b42eb376efba21734546",
        url="https://pypi.org/packages/45/fe/a25e7413b1d8d0db9729b40cd6537dd08427480b8faf2ed2095dc290b43c/nilearn-0.9.0-py3-none-any.whl",
    )
    version(
        "0.8.1",
        sha256="15ffbd509d017aea8642c303920e77968f1f7a79646d2019c9c7f839dc32beb0",
        url="https://pypi.org/packages/06/99/37fce7e258cc663923cc68b08e23ed1b72391f489dfc80e4bbed32b6f44f/nilearn-0.8.1-py3-none-any.whl",
    )
    version(
        "0.8.0",
        sha256="938635c5bda145f07384ebf704aa3f4312d99b0147eebc572646c60db15088dc",
        url="https://pypi.org/packages/c7/03/54010b2bbbf0e784ee11ca0d25bd644dba05e618d876f7fb8fdeb8eafaa0/nilearn-0.8.0-py3-none-any.whl",
    )
    version(
        "0.7.1",
        sha256="9d2681c7e828f6e1a8715470416c2f3bc752f06fcd1308b0ed0b7bb33fd32c3d",
        url="https://pypi.org/packages/4a/bd/2ad86e2c00ecfe33b86f9f1f6d81de8e11724e822cdf1f5b2d0c21b787f1/nilearn-0.7.1-py3-none-any.whl",
    )
    version(
        "0.6.2",
        sha256="3872b34b860524f579cfe94e48bf37d92d3e36253bb642cde48ef122b261d9c9",
        url="https://pypi.org/packages/b9/c2/f5f1bdd37a3da28b3b34305e4ba27cce468db6073998d62a38abd0e281da/nilearn-0.6.2-py3-none-any.whl",
    )
    version(
        "0.4.2",
        sha256="1fb094dfa85ae4cd02523bd9c19a4f4cf26a5d3a85f94fe2673af358e946ef8a",
        url="https://pypi.org/packages/f5/b8/ecf17d4ce0aee488ea4c1dc483cd191811f79c644010255258623988bd5b/nilearn-0.4.2-py2.py3-none-any.whl",
    )

    variant("plotting", default=False)

    with default_args(type="run"):
        depends_on("py-joblib@1:", when="@0.10:")
        depends_on("py-joblib@0.15:", when="@0.9.1:0.9")
        depends_on("py-joblib@0.12:", when="@0.7:0.9.0")
        depends_on("py-joblib@0.11:", when="@0.6.0:0.6")
        depends_on("py-kaleido@0.1.0.post:0.1", when="@0.10.3:+plotting platform=windows")
        depends_on("py-kaleido", when="@0.10.3:+plotting platform=linux")
        depends_on("py-kaleido", when="@0.10.3:+plotting platform=freebsd")
        depends_on("py-kaleido", when="@0.10.3:+plotting platform=darwin")
        depends_on("py-kaleido", when="@0.10.3:+plotting platform=cray")
        depends_on("py-lxml", when="@0.9.1:")
        depends_on("py-matplotlib@3.3.0:", when="@0.10:+plotting")
        depends_on("py-matplotlib@3.0.0:", when="@0.9.1:0.9+plotting")
        depends_on("py-nibabel@4.0.0:", when="@0.10.3:")
        depends_on("py-nibabel@3.2:", when="@0.10:0.10.2")
        depends_on("py-nibabel@3.0.0:", when="@0.9.1:0.9")
        depends_on("py-nibabel@2.5:", when="@0.8:0.9.0")
        depends_on("py-nibabel@2.0.2:", when="@0.5.0-beta0:0.7")
        depends_on("py-numpy@1.19.0:", when="@0.10:")
        depends_on("py-numpy@1.18.0:", when="@0.9.1:0.9")
        depends_on("py-numpy@1.16.0:", when="@0.8:0.9.0")
        depends_on("py-numpy@1.11.0:", when="@0.6.0:0.7")
        depends_on("py-packaging", when="@0.10.1:")
        depends_on("py-pandas@1.1.5:", when="@0.10:")
        depends_on("py-pandas@1.0.0:", when="@0.9.1:0.9")
        depends_on("py-pandas@0.24.0:", when="@0.8:0.9.0")
        depends_on("py-pandas@0.18:", when="@0.7")
        depends_on("py-plotly", when="@0.10.3:+plotting")
        depends_on("py-requests@2.25:", when="@0.10:")
        depends_on("py-requests@2:", when="@0.7:0.9")
        depends_on("py-scikit-learn@1.0:", when="@0.10:")
        depends_on("py-scikit-learn@0.22:", when="@0.9.1:0.9")
        depends_on("py-scikit-learn@0.21.0:", when="@0.8:0.9.0")
        depends_on("py-scikit-learn@0.19.0:", when="@0.6.0:0.7")
        depends_on("py-scipy@1.8.0:", when="@0.10.3:")
        depends_on("py-scipy@1.6.0:", when="@0.10:0.10.2")
        depends_on("py-scipy@1.5.0:", when="@0.9.1:0.9")
        depends_on("py-scipy@1.2.0:", when="@0.8:0.9.0")
        depends_on("py-scipy@0.19:", when="@0.6.0:0.7")
        depends_on("py-sklearn", when="@0.6.0:0.6")

    # sklearn.linear_model.base was deprecated in py-scikit.learn@0.24
    # older py-nilearn versions use import sklearn.external.joblib which was
    # deprecated in py-scikit-learn@0.23:

    # older py-nilearn versions use matplotlib.cm.revcmap which was deprecated
    # in py-matplotlib@3.4:

    @property
    def skip_modules(self):
        modules = []

        if self.spec.satisfies("~plotting"):
            modules.append("nilearn.plotting")
            if self.spec.satisfies("@0.7:"):
                modules.append("nilearn.reporting")

        return modules
