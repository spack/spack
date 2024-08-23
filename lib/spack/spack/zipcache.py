# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import zipfile
from typing import Dict, Set, Tuple

zipfilecache: Dict[str, Tuple[zipfile.ZipFile, Set[str]]] = {}


def get(path: str):
    if path not in zipfilecache:
        file = zipfile.ZipFile(path)
        names = set(file.namelist())
        zipfilecache[path] = (file, names)
        return file, names
    return zipfilecache[path]
