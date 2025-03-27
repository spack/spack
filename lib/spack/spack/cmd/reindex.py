# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

from llnl.util import tty

import spack.database
import spack.store

description = "rebuild Spack's package database"
section = "admin"
level = "long"


def reindex(parser, args):
    current_index = spack.store.STORE.db._index_path
    if os.path.isfile(current_index):
        backup = f"{current_index}.bkp"
        shutil.copy(current_index, backup)
        tty.msg(f"Created a back-up copy of the DB at {backup}")

    spack.store.STORE.reindex()
    tty.msg(f"The DB at {current_index} has been reindex to v{spack.database._DB_VERSION}")
