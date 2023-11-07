# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections

import spack.detection
import spack.spec


def test_detection_update_config(mutable_config):
    # mock detected package
    detected_packages = collections.defaultdict(list)
    detected_packages["cmake"] = [
        spack.detection.common.DetectedPackage(
            spec=spack.spec.Spec("cmake@3.27.5"), prefix="/usr/bin"
        )
    ]

    # update config for new package
    spack.detection.common.update_configuration(detected_packages)
    # Check entries in 'packages.yaml'
    packages_yaml = spack.config.get("packages")
    assert "cmake" in packages_yaml
    assert "externals" in packages_yaml["cmake"]
    externals = packages_yaml["cmake"]["externals"]
    assert len(externals) == 1
    external_gcc = externals[0]
    assert external_gcc["spec"] == "cmake@3.27.5"
    assert external_gcc["prefix"] == "/usr/bin"
