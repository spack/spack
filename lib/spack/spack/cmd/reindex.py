# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

import spack.database
import spack.store
from spack.util import tty

description = "rebuild Spack's package database"
section = "admin"
level = "long"


def reindex(parser, args):
    store = spack.store.STORE
    current_index = store.db._index_path
    needs_backup = os.path.isfile(current_index)

    if needs_backup:
        backup = f"{current_index}.bkp"
        shutil.copy(current_index, backup)
        tty.msg("Created a backup copy of the DB at", backup)

    old_db_path = os.path.join(store.root, spack.database._DB_DIRNAME)
    new_db_path = os.path.join(store.unpadded_root, spack.database._DB_DIRNAME)
    migrating = (
        store.root != store.unpadded_root
        and os.path.exists(old_db_path)
        and not os.path.exists(new_db_path)
    )

    if migrating:
        old_db_temp = old_db_path + ".old"
        tty.msg(f"Migrating database from {old_db_path} to {new_db_path}")
        shutil.move(old_db_path, old_db_temp)

        try:
            from spack.store import Store

            store = Store(
                store.root,
                unpadded_root=store.unpadded_root,
                projections=store.projections,
                hash_length=store.hash_length,
                upstreams=store.upstreams,
                lock_cfg=store.lock_cfg,
            )
            spack.store.STORE = store

            store.reindex()

            shutil.rmtree(old_db_temp)
            tty.msg(f"Removed old database at {old_db_path}")
        except Exception:
            if os.path.exists(old_db_temp):
                shutil.move(old_db_temp, old_db_path)
            raise
    else:
        store.reindex()

    final_index = store.db._index_path
    extra = ["If you need to restore, replace it with the backup."] if needs_backup else []
    tty.msg(f"The DB at {final_index} has been reindexed to v{spack.database._DB_VERSION}", *extra)
